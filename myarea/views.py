from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from myarea.models import Post,Profile,Neighbourhood,Business,Join
from django.http import HttpResponse
from .models import Post,Profile,Neighbourhood,Business,Join
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
        if form.is_valid():
            username=form.cleaned_data.get('username')
            user=form.save()
           
        return redirect('login')
    else:
        form= RegistrationForm()
    params={
        'form':form
    }
    return render(request, 'auth/signup.html', params)


def profile(request,id):
    prof = Profile.objects.get(id = id)
    return render(request,'profile.html',{"profile":prof})


@login_required(login_url='login')  
def updateprofile(request,id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        form = profileForm(request.POST or None,request.FILES or None, instance=user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.id)
    else:
        form = profileForm()
        return render(request, 'updateprofile.html',{"form":form })

@login_required(login_url='login')  
def create_post(request, hood_id):
    hood = Neighbourhood.objects.get(id=hood_id)
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.hood = hood
            post.user = request.user
            post.save()
            return redirect('single_hood', hood.id)
    else:
        form = NewPostForm()
    return render(request, 'new_post.html', {'form': form})

@login_required(login_url='login')  
def createhood(request):
    if request.method == 'POST':
        form = CreateHoodForm(request.POST, request.FILES)
        if form.is_valid():
            hood = form.save(commit = False)
            hood.user = request.user
            hood.save()
       
        return redirect('hoods')
    else:
        form = CreateHoodForm()
        return render(request,'new_hood.html',{"form":form})


# def search_hood(request):

#     if request.GET['hoods']:
#         search_term = request.GET.get("hoods")
#         hoods = Neighbourhood.search_hood(search_term)
#         message = f"{search_term}"

#         return render(request,'search.html',locals())

#     else:
#         message = "You Haven't searched for any item"
#         return render(request,'search.html',locals())

  
@login_required(login_url='login')  
def all_hoods(request):
    all_hoods = Neighbourhood.objects.all()
    all_hoods = all_hoods[::-1]
    params = {
        'hoods': all_hoods,
    }
    return render(request, 'all_hoods.html', params)

def single_hood(request, hood_id):
    hood = Neighbourhood.objects.get(id=hood_id)
    business = Business.objects.filter(hood=hood)
    posts = Post.objects.filter(hood=hood)
    posts = posts[::-1]
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            b_form = form.save(commit=False)
            b_form.neighbourhood = hood
            b_form.user = request.user.profile
            b_form.save()
            return redirect('single_hood', hood.id)
    else:
        form = BusinessForm()
    params = {
        'hood': hood,
        'business': business,
        'form': form,
        'posts': posts
    }
    return render(request, 'hood.html', params)

# def create_business(request):
#     current_user = request.user
#     print(Profile.objects.all())
#     owner = Profile.get_by_id(current_user)
#     if request.method == 'POST':
#         form = BusinessForm(request.POST,request.FILES)
#         if form.is_valid():
#             new_biz=form.save(commit=False)
#             new_biz.user = current_user
#             new_biz.save()
#             return redirect(index)
#     else:
#         form = BusinessForm()
#     return render(request,"businessform.html",locals())


@login_required(login_url='login')  
def join_hood(request, id):
    neighbourhood = get_object_or_404(Neighbourhood, id=id)
    request.user.profile.neighbourhood = neighbourhood
    request.user.profile.save()
    return redirect('hoods')

def leave_hood(request, id):
    hood = get_object_or_404(Neighbourhood, id=id)
    request.user.profile.neighbourhood = None
    request.user.profile.save()
    return redirect('hoods')

def search_business(request):
    if request.method == 'GET':
        name = request.GET.get("title")
        results = Business.objects.filter(name__icontains=name).all()
        print(results)
        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'search.html', params)
    else:
        message = "You haven't searched for any business in the category"
    return render(request, "results.html")