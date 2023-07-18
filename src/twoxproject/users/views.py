from django.db.models import Count
from django.shortcuts import get_object_or_404, render,redirect    
from django.urls import path,reverse
from django.contrib.auth.forms import UserCreationForm
from . forms import UserRegisterForm, StepForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from .models import Step, UserProfile
from django.http import Http404
from django.contrib.auth.models import User
#autocomplete title ---
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q
#---



# Create your views here.
def login_view(request, *args, **kwargs):
    return render(request,'users/login.html')
# def dashboard_view(request, *args, **kwargs):
#     return render(request,'users/dashboard.html')
def register_view(request, *args, **kwargs):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Hi {username}, your account was created succesfully.\n Please log in.")
            return redirect('users:login')
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form':form})
@login_required
def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    latest_step_list = get_latest_steps()
    top_step_list = get_top_steps()
    user_steps = get_user_steps(request.user)
    user_profile = user_profile



    context = {
        "latest_step_list" : latest_step_list,
        "top_step_list": top_step_list,
        "user_steps": user_steps,
        "user_profile": user_profile,



    }
    return render(request,'users/profile.html', context)

def get_latest_steps():
    return Step.objects.order_by("-pub_date")[:5]
def get_all_steps():
    return Step.objects.order_by("-pub_date")
def get_top_steps():
    return Step.objects.annotate(total_upvotes=Count('upvotes')).order_by('-total_upvotes')[:5]


def step_list_recent(request):
    latest_step_list = get_latest_steps()
    context = {
        "latest_step_list": latest_step_list,

    }
    return render(request,"users/recent-steps.html",context )
def step_list_recent_all(request):
    latest_step_list_all = get_all_steps()
    context = {
        "latest_step_list_all": latest_step_list_all,

    }
    return render(request,"users/recent-steps-all.html",context )
def top_steps(request):
    top_step_list = get_top_steps()

    context = {
        "top_step_list": top_step_list,
    }
    return render(request, 'users/top-steps.html', context)


def detail(request, step_id):
    step = get_object_or_404(Step, pk = step_id)
    total_upvotes =step.total_upvotes()
    upvoted = False
    #if user id upvotes means that exists
    if step.upvotes.filter(id=request.user.id).exists():
        upvoted = True
    context ={
        "step":step,
        "total_upvotes": total_upvotes,
        "upvoted": upvoted,
        "step_user": step.user,  # Update the variable name to "step_user"
        }
    return render(request, "users/detail.html", context)

def results(request, step_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % step_id)

def vote(request, step_id):
    return HttpResponse("You're voting on question %s." % step_id)   
def add_method(request):
        return render(request,"users/add-method.html" )


def todo(request):
        return render(request,"users/todo.html" )

#create a step form
def create_step(request):
    if request.method == 'POST':
        form = StepForm(request.POST)
        if form.is_valid():
            step = form.save(commit=False)
            step.user = request.user  # Set the current user as the creator
            step.save()

            # Update the user's total_unit_number in UserProfile
            unit_number = form.cleaned_data['unit_number']
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.total_unit_number += unit_number
            user_profile.save()

            return redirect('/profile/')  # Redirect to the list of steps
    else:
        form = StepForm()
    
    return render(request, 'users/create-step.html', {'form': form})

#upvote a post
    #request contains the user ID
def UpvoteView(request, pk):
    #we are looking at a step id
    step = get_object_or_404(Step, id = request.POST.get('step_id'))
    #we set the Upvoted to False
    Upvoted = False
    #we check if the user Upvoted a step
    if step.upvotes.filter(id=request.user.id).exists():
        #if upvoted we can remove it
        step.upvotes.remove(request.user)
        #if removed then no longer exists
        upvoted = False
    else:
        #adds an upvote for whatever user upvotes
        step.upvotes.add(request.user)  
        upvoted = True
    return HttpResponseRedirect(reverse('users:detail', args=[str(pk)]))
#get the steps of a user
def get_user_steps(user):
    return Step.objects.filter(user=user).order_by("-pub_date")
#display the user steps on a page
def user_steps(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_steps = get_user_steps(user)
    user_profile = UserProfile.objects.get(user=request.user)


    context = {
        'user': user,
        'user_steps': user_steps,
        "user_profile": user_profile,

    }
    return render(request, 'users/user-steps.html', context)
@require_GET
def step_title_autocomplete(request):
    term = request.GET.get('term', '')

    # Query the Step model for similar step titles
    similar_steps = Step.objects.filter(Q(step_title__icontains=term))

    # Extract the step titles and return them as a JSON response
    titles = [step.step_title for step in similar_steps]
    return JsonResponse(titles, safe=False)
