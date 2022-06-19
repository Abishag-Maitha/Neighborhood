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
    path('newpost/', views.new_post, name='newpost'),
    path('hoods/', views.all_hoods, name='hoods'),
    path('business/',views.create_business,name = 'business'),
    path('profile/<id>', views.profile, name='profile'),
    path('createHood/', views.createHood, name='createHood'),
    path('updateprofile/', views.updateprofile, name='updateprofile'),
    path('join/', views.join, name='joinHood'),
    path('search/', views.search_hood, name='search'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)