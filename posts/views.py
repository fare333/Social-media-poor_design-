from django.shortcuts import render,redirect

from .models import *
from profiles.models import Profile

from .forms import PostForm,CommentForm

# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required(login_url='account_login')
def get_all_posts(request):
    posts = Post.objects.all()
    
    profile = Profile.objects.get(user=request.user)
    
    p_form = PostForm()
    if "submit_p_form" in request.POST:
        p_form = PostForm(request.POST)
        if p_form.is_valid():
            insta = p_form.save(commit=False)
            insta.author = profile
            insta.save()
            p_form = PostForm()
            
            
    c_form = CommentForm()
    if "submit_c_form" in request.POST:
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.author = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentForm()
    
    context = {
        "posts":posts,
        "c_form":c_form,
        "p_form":p_form
        }
    return render(request, 'posts/all_posts.html',context)


@login_required(login_url='account_login')
def delete_post(request,pk):
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('get_all_posts')
    return render(request, 'posts/delete_post.html')

@login_required(login_url='account_login')
def update_post(request,pk):
    post = Post.objects.get(pk=pk)
    
    form = PostForm(instance=post)
    
    if request.user == post.author.user:
        if request.method == "POST":
            form = PostForm(request.POST,instance=post)
            if form.is_valid():
                form.save()
                return redirect('get_all_posts')
            
    context = {'form':form}
    return render(request, 'posts/update_post.html',context)

@login_required(login_url='account_login')
def delete_comment(request,pk):
    comment = Comment.objects.get(pk=pk)
    if request.user == comment.author.user:
        if request.method == "POST":
            comment.delete()
            return redirect('get_all_posts')
    return render(request, 'posts/delete_comment.html')

@login_required(login_url='account_login')
def post_detail(request,pk):
    post = Post.objects.get(pk=pk)
    
    profile = Profile.objects.get(user=request.user)
    
    c_form = CommentForm()
    if "submit_c_form" in request.POST:
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.author = profile
            instance.post = post
            instance.save()
            c_form = CommentForm()
            
    context = {
        "post":post,
        "c_form":c_form,
        }
    return render(request, 'posts/post_detail.html',context)

@login_required(login_url='account_login')
def add_like(request):
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=request.user)
        
        if profile in post.liked.all():
            post.liked.remove(profile)
        else:
            post.liked.add(profile)
        
        like,created = Like.objects.get_or_create(post=post,author=profile)
        
        if not created:
            if like.value== "Like":
                like.value = "Unlike"
            else:
                like.value = "Like"
        else:
            like.value="Like"
            like.save()
            
    return redirect("get_all_posts")