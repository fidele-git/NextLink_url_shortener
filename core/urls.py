from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('shorten/', views.shorten_url, name='shorten'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('analytics/<str:short_code>/', views.link_analysis, name='link_analysis'),
    path('qr/<str:short_code>/', views.generate_qr, name='generate_qr'),
    path('<str:short_code>', views.redirect_url, name='redirect'),
]
