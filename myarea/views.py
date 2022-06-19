from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from myarea.models import Post,Profile,Neighbourhood,Business,Join
from django.http import HttpResponse
from .models import Post,Profile,Neighbourhood,Business,Join
from django.contrib import messages
from . forms import NewPostForm,CreateHoodForm,BusinessForm, RegistrationForm, profileForm
from django.contrib.auth.models import User


def index(request):
    hoods = Neighbourhood.objects.all()
    business = Business.objects.all()
    posts = Post.objects.all()
    print(posts)
    return render(request, 'index.html',locals())

def register(request):
    if request.method=="POST":
        form=RegistrationForm(request.POST)
        procForm=profileForm(request.POST, request.FILES)
        if form.is_valid() and procForm.is_valid():
            username=form.cleaned_data.get('username')
            user=form.save()
            profile=procForm.save(commit=False)
            profile.user=user
            profile.save()

        return redirect('login')
    else:
        form= RegistrationForm()
        prof=profileForm()
    params={
        'form':form,
        'profForm': prof
    }
    return render(request, 'auth/register.html', params)


@login_required(login_url='login')  
def profile(request,user_id=None):
    if user_id == None:
        user_id=request.user.id
    current_user = User.objects.get(id = user_id)
    user = current_user
    images = Post.objects.filter(user=current_user)
    profile = Profile.objects.all()
    return render(request, 'profile.html', locals())


@login_required(login_url='login')  
def updateprofile(request):
	if request.method == 'POST':
		form = profileForm(request.POST,request.FILES, instance=request.user.profile)
		if form.is_valid():
			form.save()
			return redirect('profile')

	else:
			form = profileForm()
	return render(request, 'updateprofile.html',{"form":form })


@login_required(login_url='login')  
def new_post(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
            return redirect('hoods')
    else:
        form = NewPostForm()
    return render(request, 'new_post.html', {"form":form})

@login_required(login_url='login')  
def createHood(request):
    if request.method == 'POST':
        form = CreateHoodForm(request.POST)
        if form.is_valid():
            hood = form.save(commit = False)
            hood.user = request.user
            hood.save()
       
        return redirect('index')
    else:
        form = CreateHoodForm()
        return render(request,'new_hood.html',{"form":form})

def search(request):

    if request.GET['hoods']:
        search_term = request.GET.get("hoods")
        hoods = Neighbourhood.search_hood(search_term)
        message = f"{search_term}"

        return render(request,'search.html',locals())

    else:
        message = "You Haven't searched for any item"
        return render(request,'search.html',locals())


  
@login_required(login_url='login')  
def all_hoods(request):

    if request.user.is_authenticated:
        if Join.objects.filter(user_id=request.user).exists():
            hood = Neighbourhood.objects.get(pk=request.user.join.hood_id.id)
            businesses = Business.objects.filter(hood=request.user.join.hood_id.id)
            posts = Post.objects.filter(hood=request.user.join.hood_id.id)
            print(posts)
            return render(request, "hood.html", locals())
        else:
            neighbourhoods = Neighbourhood.objects.all()
            return render(request, 'hood.html', locals())
    else:
        neighbourhoods = Neighbourhood.objects.all()

        return render(request, 'hood.html', locals())

def create_business(request):
    current_user = request.user
    print(Profile.objects.all())
    owner = Profile.get_by_id(current_user)
    if request.method == 'POST':
        form = BusinessForm(request.POST,request.FILES)
        if form.is_valid():
            new_biz=form.save(commit=False)
            new_biz.user = current_user
            new_biz.save()
            return redirect(index)
    else:
        form = BusinessForm()
    return render(request,"businessform.html",locals())


@login_required(login_url='login')  
def join(request, hoodId):
    neighbourhood = Neighbourhood.objects.get(pk=hoodId)
    if Join.objects.filter(user_id=request.user).exists():

        Join.objects.filter(user_id=request.user).update(hood_id=neighbourhood)
    else:

        Join(user_id=request.user, hood_id=neighbourhood).save()

    messages.success(request, 'Success! You have succesfully joined this Neighbourhood ')
    return redirect('hoods')
