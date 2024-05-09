from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import MyPasswordChangeForm, MySetPasswordForm,MyPasswordResetForm

urlpatterns = [
    path('', views.home),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('payment/', views.payment, name='payment'),
    path('teams/', views.teams, name='teams'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('room/', views.Post_Room, name='room'),
    path('yourpost/', views.YourPost, name='yourpost'),
    path('post/<int:pk>/', views.post_detail_view, name='post_detail'),
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/', views.ProfileViews.as_view(), name='profile'),
    path('information/', views.information, name='information'),
    path('updateinfor/<int:pk>', views.updateInfor.as_view(), name='updateinfor'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='password.html',form_class=MyPasswordChangeForm, success_url = '/passwordchangedone'), name = 'passwordchange'),
    path('passwordchangedone', auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'), name = 'passwordchangedone'),
     path('search/', views.search_posts, name='search'),
    path('addroom/', views.create_post, name='addroom'),
    path('wallet/', views.wallet_view, name='wallet_view'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)