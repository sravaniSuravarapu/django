from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from authapp.forms import PostForm
from .models import Post

# Create your views here.
def index(request):
    return render(request,'index.html')
def home(request):
    return render(request,'home.html')
def signin(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        myuser = authenticate(username=uname,password=pass1)
        if myuser is not None:
            login(request,myuser)
            messages.warning(request,'successfully logged in')
            return redirect('/')
        else:
            messages.warning(request,'invalid credentials')
            return redirect('../signin/')
    return render(request,'login.html')
def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        confirmpassword = request.POST.get('pass2')
        if password != confirmpassword:
            messages.warning(request,'password doesnt match')
            return redirect('../signup/')
        try:
            if User.objects.get(username=uname):
                messages.warning(request,'user already exists')
                return redirect('../signup/')
        except:
            pass
        try:
            if User.objects.get(username=uname):
                messages.warning(request,'email is already in use')
                return redirect('../signup/')
        except:
            pass
        myuser = User.objects.create_user(uname,email,password)
        myuser.save()
        messages.success(request,'successfully registered')
        return redirect('../signup/')
    return render(request,'signup.html')
def handlelogout(request):
    logout(request)
    messages.success(request,'successfully logged out')
    return redirect('../signin/')
def nav(request):
    return render(request,'nav.html')
def dashboard(request):
    posts = Post.objects.all()
    return render(request,'dashboard.html',{'posts':posts})

# def updatepost(request):
#     return render(request,'updateposts.html')

# Update/Edit Post
def update_post(request, id):
  if request.user.is_authenticated:
    if request.method == 'POST':
      pi = Post.objects.get(pk=id)
      form = PostForm(request.POST, instance=pi)
      if form.is_valid():
        form.save()
        messages.success(request,'successfully updated')
    else:
      pi = Post.objects.get(pk=id)
      form = PostForm(instance=pi)
    return render(request, 'updateposts.html', {'form':form})
  else:
    return HttpResponseRedirect('/login/')

# Delete Post
def delete_post(request, id):
  if request.user.is_authenticated:
    if request.method == 'POST':
      pi = Post.objects.get(pk=id)
      pi.delete()
      messages.success(request,'successfully deleted the post')
      return HttpResponseRedirect('/posts/')
  else:
    return HttpResponseRedirect('/dashboard/')
def posts(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_username()
        return render(request,'posts.html',{'posts':posts, 'full_name':full_name})
    else:
        return HttpResponseRedirect('/login/')


def add_post(request):
 if request.user.is_authenticated:
  if request.method == 'POST':
   form = PostForm(request.POST)
   if form.is_valid():
    title = form.cleaned_data['title']
    desc = form.cleaned_data['desc']
    pst = Post(title=title, desc=desc)
    pst.save()
    messages.success(request,'successfully added the post')
    form = PostForm()
  else:
   form = PostForm()
  return render(request, 'addposts.html', {'form':form})
 else:
  return HttpResponseRedirect('../signin/')
    


