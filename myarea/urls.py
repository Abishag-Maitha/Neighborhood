from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('',views.index,name = 'index'),
    path('register/',views.register, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='auth/logout.html'), name='logout'),
    path('hoods/', views.all_hoods, name='hoods'),
    path('createhood/', views.createhood, name='createhood'),
    path('single_hood/<int:hood_id>', views.single_hood, name='single_hood'),
    path('<hood_id>/new-post', views.create_post, name='post'),
    path('join_hood/<id>', views.join_hood, name='join_hood'),
    path('leave_hood/<id>', views.leave_hood, name='leave_hood'),
    path('profile/<id>', views.profile, name='profile'),
    path('profile/<id>/edit/', views.updateprofile, name='updateprofile'),
    path('search/', views.search_business, name='search'),
    
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)