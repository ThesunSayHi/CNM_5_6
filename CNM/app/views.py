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

def payment(request):
    return render(request, "payment.html")

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
        return render(request, 'signup.html', context=context)
    
def Post_Room(request):
    posts = Posts.objects.all()
    sorted_posts = sorted(posts, key=lambda x: (0 if x.post_type == 'Pro' else (1 if x.post_type == 'VIP' else 2)))
    context = {'post': sorted_posts}
    return render(request, 'post.html', context)

def post_detail_view(request, pk):
    post = get_object_or_404(Posts, pk=pk)
    
    try:
        profile = Profile.objects.get(user=post.posted_by)
    except Profile.DoesNotExist:
        profile = None
    
    context = {
        'post': post,
        'profile': profile,
    }
    return render(request, 'post_detail.html', context)

def user_logout(request):
    logout(request)
    return home(request)


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
            image = None
            if 'image' in request.FILES:
                image = form.cleaned_data['image']
            reg = Profile(user=user, full_name=full_name, email=email, phone=phone, gender=gender, facebook=facebook, image=image)
            reg.save()
            return redirect('information')
        else:
            return render(request, 'profile.html', {'form': form})
def information(request):
    profiles =  Profile.objects.filter(user=request.user)
    return render(request,'information.html', locals())

class updateInfor(View):
    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        form = ProfileForm(instance=profile)
        return render(request, 'updateinfor.html', {'form': form})

    def post(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            if form.cleaned_data['full_name'] != '':
                profile.full_name = form.cleaned_data['full_name']
            if form.cleaned_data['email'] != '':
                profile.email = form.cleaned_data['email']
            if form.cleaned_data['phone'] != '':
                profile.phone = form.cleaned_data['phone']
            if form.cleaned_data['gender'] != '':
                profile.gender = form.cleaned_data['gender']
            if form.cleaned_data['facebook'] != '':
                profile.facebook = form.cleaned_data['facebook']
            if form.cleaned_data.get('image'):
                profile.image = form.cleaned_data['image']
            profile.save()
        return redirect('information')


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.posted_by = request.user
            user = request.user
            post_type = form.cleaned_data.get('post_type')
            profile = Profile.objects.filter(user=user)
            if not profile:
                return redirect('profile')
            if not profile.full_name or not profile.email or not profile.phone:
                return redirect('profile')
            if post_type == Posts.NORMAL and user.wallet.total_balance< 5000:
                return redirect('payment')
            elif post_type == Posts.VIP and user.wallet.total_balance < 7000:
                return redirect('payment')
            elif post_type == Posts.PRO and user.wallet.total_balance < 10000:
                return redirect('payment')
            try:
                wallet = user.wallet
                if post_type == Posts.NORMAL:
                    wallet.total_balance -= 5000
                    wallet.total_expenses += 5000
                elif post_type == Posts.VIP:
                    wallet.total_balance -= 7000
                    wallet.total_expenses += 7000
                elif post_type == Posts.PRO:
                    wallet.total_balance -= 10000
                    wallet.total_expenses += 10000
                wallet.save()
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

from django.db.models import Q
from django.http import JsonResponse
def search_posts(request):
    query = request.GET.get('q')
    if query:
        posts = Posts.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(address__icontains=query) |
            Q(post_type__icontains=query)
        )
    else:
        posts = Posts.objects.all()

    data = [
        {
            'pk': post.pk,
            'title': post.title,
            'description': post.description,
            'address': post.address,
            'price': float(post.price),
            'image_url': post.ImageURL,
        }
        for post in posts
    ]
    return JsonResponse(data, safe=False)


def wallet_view(request):
    user_wallet = Wallet.objects.get(user=request.user)
    return render(request, 'wallet.html', {'wallet': user_wallet})


def YourPost(request):
    user_posts = Posts.objects.filter(posted_by=request.user)
    sorted_posts = sorted(user_posts, key=lambda x: (0 if x.post_type == 'Pro' else (1 if x.post_type == 'VIP' else 2)))
    context = {'posts': sorted_posts}
    return render(request, 'yourpost.html', context)