from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, F
from django.db.models.functions import TruncDay
from .models import Link, Click
from .utils import encode
from .forms import UserProfileForm
import json
import qrcode
import io
import base64

def landing(request):
    recent_links = []
    if request.user.is_authenticated:
        recent_links = Link.objects.filter(owner=request.user)[:5]
    else:
        recent_ids = request.session.get('recent_link_ids', [])
        # Preserve order of IDs
        links_dict = {l.id: l for l in Link.objects.filter(id__in=recent_ids)}
        recent_links = [links_dict[link_id] for link_id in recent_ids if link_id in links_dict]
        
    return render(request, 'core/landing.html', {'recent_links': recent_links})

def shorten_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        custom_code = request.POST.get('custom_code', '').strip()
        
        if not original_url:
            return HttpResponse("URL is required", status=400)
        
        # Check if user is logged in
        owner = request.user if request.user.is_authenticated else None
        
        # Custom Alias Logic
        if custom_code:
            if not owner:
                context = {'error': 'Sign up to use custom aliases!', 'original_url': original_url}
                if request.htmx:
                    return render(request, 'core/partials/error_message.html', context)
                return render(request, 'core/landing.html', {**context, 'recent_links': get_recent_links(request)})

            if not custom_code.isalnum() and '-' not in custom_code and '_' not in custom_code:
                 context = {'error': 'Alias can only contain letters, numbers, dashes, and underscores.', 'original_url': original_url}
                 if request.htmx:
                    return render(request, 'core/partials/error_message.html', context)
                 return render(request, 'core/landing.html', {**context, 'recent_links': get_recent_links(request)})
            
            if Link.objects.filter(short_code=custom_code).exists():
                 context = {'error': 'That alias is already taken. Try another one.', 'original_url': original_url}
                 if request.htmx:
                    return render(request, 'core/partials/error_message.html', context)
                 return render(request, 'core/landing.html', {**context, 'recent_links': get_recent_links(request)})
        
        # Create Link
        try:
            link = Link.objects.create(original_url=original_url, owner=owner, short_code=custom_code if custom_code else None)
        except Exception as e:
             # Fallback for race conditions
             context = {'error': 'Something went wrong. Please try again.', 'original_url': original_url}
             if request.htmx:
                return render(request, 'core/partials/error_message.html', context)
             return render(request, 'core/landing.html', {**context, 'recent_links': get_recent_links(request)})

        # Session persistence for anonymous users
        if not owner:
            recent_ids = request.session.get('recent_link_ids', [])
            recent_ids.insert(0, link.id)
            request.session['recent_link_ids'] = recent_ids[:5]
            request.session.modified = True
        
        # If it's an HTMX request, we can return a snippet
        if request.htmx:
            return render(request, 'core/partials/short_link_result.html', {'link': link})
            
        return redirect('dashboard' if owner else 'landing')
    return redirect('landing')

def get_recent_links(request):
    # Helper to re-fetch context if we need to render the page with an error
    recent_links = []
    if request.user.is_authenticated:
        recent_links = Link.objects.filter(owner=request.user)[:5]
    else:
        recent_ids = request.session.get('recent_link_ids', [])
        links_dict = {l.id: l for l in Link.objects.filter(id__in=recent_ids)}
        recent_links = [links_dict[link_id] for link_id in recent_ids if link_id in links_dict]
    return recent_links

def redirect_url(request, short_code):
    # 1. Check Redis (Cache Hit)
    cached_url = cache.get(f"url_{short_code}")
    
    link = None
    if not cached_url:
        # Cache Miss: Lookup in DB
        link = get_object_or_404(Link, short_code=short_code)
        cached_url = link.original_url
        cache.set(f"url_{short_code}", cached_url, timeout=3600*24)
    else:
        # We still need link object for DB updates if we want to be exact,
        # but for performance, we often just do a late write or async.
        # Here we'll get it to record the Click model.
        link = get_object_or_404(Link, short_code=short_code)

    # 2. Record Analytics (Click Model)
    Click.objects.create(
        link=link,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT'),
        referer=request.META.get('HTTP_REFERER')
    )

    # 3. Update Link aggregate count
    Link.objects.filter(id=link.id).update(clicks_count=F('clicks_count') + 1)
    
    response = HttpResponseRedirect(cached_url, status=302)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@login_required
def link_analysis(request, short_code):
    link = get_object_or_404(Link, short_code=short_code, owner=request.user)
    
    # Aggregate clicks by day for the last 7 days
    seven_days_ago = timezone.now() - timezone.timedelta(days=7)
    clicks_data = Click.objects.filter(link=link, timestamp__gte=seven_days_ago) \
        .annotate(day=TruncDay('timestamp')) \
        .values('day') \
        .annotate(count=Count('id')) \
        .order_by('day')

    # Format for Chart.js
    labels = []
    values = []
    for entry in clicks_data:
        labels.append(entry['day'].strftime('%b %d'))
        values.append(entry['count'])

    context = {
        'link': link,
        'chart_labels': json.dumps(labels),
        'chart_values': json.dumps(values),
        'total_clicks': link.clicks_count,
    }
    return render(request, 'core/analysis.html', context)

@login_required
def generate_qr(request, short_code):
    link = get_object_or_404(Link, short_code=short_code, owner=request.user)
    full_url = f"{request.scheme}://{request.get_host()}/{link.short_code}"
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(full_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    if request.htmx:
        return render(request, 'core/partials/qr_code_modal.html', {
            'qr_image': img_str,
            'link': link,
            'full_url': full_url
        })
    
    # Fallback for direct download or similar
    response = HttpResponse(buffer.getvalue(), content_type="image/png")
    response['Content-Disposition'] = f'attachment; filename="qr_{short_code}.png"'
    return response

@login_required
def dashboard(request):
    links = Link.objects.filter(owner=request.user)
    # Pre-format dates to avoid template filter issues
    for link in links:
        link.formatted_date = link.created_at.strftime("%b %d, %Y")
    return render(request, 'core/dashboard.html', {'links': links})

@login_required
def profile(request):
    links_count = Link.objects.filter(owner=request.user).count()
    context = {
        'links_count': links_count,
        'member_since': request.user.date_joined,
        'user_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.email,
        'initials': (request.user.first_name[:1] + request.user.last_name[:1]).upper() if request.user.first_name and request.user.last_name else request.user.email[:1].upper()
    }
    return render(request, 'core/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'core/edit_profile.html', {'form': form})
