from django.shortcuts import render,redirect

# Create your views here.
from .models import Profile,Followers
from django.contrib.auth.models import User
from posts.models import Post,Comment,Like
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

@login_required(login_url='account_login')
def my_profile(request):
    profile = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(author=profile)
    
    context = {'profile':profile,'posts':posts}
    
    return render(request, 'profiles/my_profile.html',context)

@login_required(login_url='account_login')
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
    context = {'form':form}
    return render(request, 'profiles/edit_profile.html',context)
    

@login_required(login_url='account_login')
def get_profiles(request,pk):
    profile = Profile.objects.get(pk=pk)
    posts = Post.objects.filter(author=profile)
    context = {'profile':profile,'posts':posts}
    return render(request, 'profiles/get_profiles.html',context)

@login_required(login_url='account_login')
def get_all_profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles':profiles}
    return render(request, 'profiles/get_all_profiles.html',context)

@login_required(login_url='account_login')
def search(request):
    if request.method == 'POST':
        query = request.POST.get("search")
        profiles = Profile.objects.filter(user__username__icontains=query).exclude(user=request.user)
        context = {'profiles':profiles}
        return render(request, 'profiles/search.html',context)
    return render(request, 'profiles/search.html')

@login_required(login_url='account_login')
def add_follow(request,pk):
    profile = Profile.objects.get(pk=pk)
    prof = Profile.objects.get(user=request.user)
    if request.user not in profile.followers.all():
        profile.followers.add(request.user)
    else:
        profile.followers.remove(request.user)
    
    follow,created = Followers.objects.get_or_create(sender=prof,receiver=profile)
    
    if created:
        follow.save()
    else:
        follow.delete()
    return redirect('get_profiles',pk=pk)


def all_user_followers(request):
    profile = Profile.objects.get(user=request.user)
    followers = Followers.objects.filter(receiver=profile)
    context = {'followers':followers}
    return render(request, 'profiles/all_user_followers.html',context)

def user_followers(request,pk):
    profile = Profile.objects.get(pk=pk)
    followers = Followers.objects.filter(receiver=profile)
    context = {'followers':followers}
    return render(request, 'profiles/user_followers.html',context)