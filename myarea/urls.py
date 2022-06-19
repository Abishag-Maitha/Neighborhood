from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns=[
    url('',views.index,name = 'index'),
    url('newpost', views.new_post, name='newpost'),
    url('hoods', views.all_hoods, name='hoods'),
    url('business/',views.create_business,name = 'business'),
    url('profile/<id>', views.profile, name='profile'),
    url('createHood/', views.createHood, name='createHood'),
    url('updateprofile', views.updateprofile, name='updateprofile'),
    url('join/', views.join, name='joinHood'),
    url('search/', views.search, name='search'),
]

urlpatterns = [
    path('',views.index, name = 'home'),
    path('register/',views.register, name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='log_user'),
    path('search/', views.searchproject, name='search'),
    path('newproject/',views.addProject,name = 'project'),
    path('profile/<id>',views.profile,name = 'profile'),
    path('editprofile/',views.editprofile,name = 'editprofile'), 
    path('logout/', auth_views.LogoutView.as_view(template_name='auth/logout.html'), name='logout'),
    path('api/profile',views.ProfileList.as_view(), name='apiprofiles'),
    path('api/projects',views.ProjectList.as_view(), name='apiprojects'),
    path('projects/<int:id>',views.projects,name = 'projects'),
    path(r'ratings/', include('star_ratings.urls', namespace='ratings')),
    path('rate/<id>/',views.rate,name = 'rate')
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)