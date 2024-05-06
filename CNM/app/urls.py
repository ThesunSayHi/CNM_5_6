from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('teams/', views.teams, name='teams'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('room/', views.Post_Room, name='room'),
    path('post/<int:pk>/', views.post_detail_view, name='post_detail'),
    path('dangxuat/', views.user_logout, name='user_logout'),
    path('profile/', views.ProfileViews.as_view(), name='profile'),
    path('information/', views.information, name='information'),
    path('updateinfor/<int:pk>', views.updateInfor.as_view(), name='updateinfor'),
    

    path('addroom/', views.create_post, name='addroom'),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)