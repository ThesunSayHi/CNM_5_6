from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from .forms import UserSignupForm, UserLoginForm, ProfileForm, PostForm
from .models import *
from django.contrib.auth import authenticate, login as loginUser,logout
from django.contrib import messages
from django.views import View
# Create your views here.
def home(request):
    if request.user.is_anonymous:
        return render(request, "base.html")
    return Post_Room(request)

def about(request):
    return render(request, "about.html")


def services(request):
    return render(request, "services.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get("fullname")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        data = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
        }
        message = '''
        New message: {}

        Form: {}
        '''.format(data['message'], data['email'])
        send_mail(data['subject'], message, '',['quoctoan040501@gmail.com'])
    return render(request, "contact.html", {})

def teams(request):
    return render(request, "teams.html")

def login(request):
    if request.method == 'GET':
        form = UserLoginForm()
        context = {
            "form": form
        }
        return render(request, 'login.html', context=context)
    else:
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                loginUser(request, user)
                return redirect('home')
        else:
            context = {
                "form": form
            }
            return render(request, 'login.html', context=context)
        
def signup(request):
    form = UserSignupForm()
    context = {
            "form": form
    }
    if request.method == 'GET':
        return render(request, 'signup.html', context=context)
    else:
        print(request.POST)
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
            # if user is not None:
            #     return redirect('login')
        else:
            messages.warning(request,'Đăng ký không thành công !')
        return render(request, 'signup.html', context=context)
    
def Post_Room(request):
    posts = Posts.objects.all()
    sorted_posts = sorted(posts, key=lambda x: (0 if x.post_type == 'Pro' else (1 if x.post_type == 'VIP' else 2)))
    context = {'post': sorted_posts}
    return render(request, 'post.html', context)

def post_detail_view(request, pk):
    post = Posts.objects.get(pk=pk)

    context = {
        'post': post,
    }
    return render(request, 'post_detail.html', context)

def user_logout(request):
    logout(request)
    return home(request)


def use_directory_paths(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.id, filename)
    return "user_{0}/{1}".format(instance.id, filename)
class ProfileViews(View):
    def get(self, request):
        form = ProfileForm()
        return render(request, 'profile.html', {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            gender = form.cleaned_data['gender']
            facebook = form.cleaned_data['facebook']
            image = form.cleaned_data['image']

            if hasattr(image, 'name'):
                image_name = image.name
            else:
                image_name = image

            image_path = use_directory_paths(user, image_name)
            reg = Profile(user=user, full_name=full_name, email=email, phone=phone, gender=gender, facebook=facebook, image=image_path)
            reg.save()
            messages.success(request, 'Lưu Thành Công')
            return redirect('information')
        else:
            messages.warning(request, "Lỗi !!!!")
            return render(request, 'profile.html', {'form': form})
def information(request):
    profiles =  Profile.objects.filter(user=request.user)
    return render(request,'information.html', locals())

class updateInfor(View):
    def get(self, request, pk):
        add = Profile.objects.get(pk=pk)
        form = ProfileForm(instance=add)
        return render(request,'updateinfor.html', locals())
    def post(selff,request,pk):
        form =  ProfileForm(request.POST)
        if form.is_valid():
            add = Profile.objects.get(pk=pk)
            add.full_name = form.cleaned_data['full_name']
            add.email = form.cleaned_data['email']
            add.phone = form.cleaned_data['phone']
            add.gender = form.cleaned_data['gender']
            add.facebook = form.cleaned_data['facebook']
            add.image = form.cleaned_data['image']
            add.save()
            messages.success(request,'Lưu Thành Công')
        else:
            messages.warning(request,"Lỗi !!!!")
        return redirect('information')


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.posted_by = request.user
            try:
                post.save()
                print("Post saved successfully")
                return redirect('room')
            except Exception as e:
                print("Error saving post:", e)
        else:
            print("Form is invalid")
    else:
        form = PostForm()
    return render(request, 'addroom.html', {'form': form})