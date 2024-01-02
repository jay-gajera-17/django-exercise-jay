from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Choice,Question
from django.shortcuts import get_object_or_404, render , redirect
from django.urls import reverse
from django.views import generic
from .models import CustomUser,Vote
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from mysite.settings import EMAIL_HOST_USER
from django.conf import settings

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

@login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    user = request.user
    question = get_object_or_404(Question, pk=question_id)
    # selected_choice = question.choice_set.get(pk=request.POST["choice"])
    if Vote.objects.filter(user=user, question=question).exists():
        return HttpResponse("You have already voted for this question.")

    selected_choice = question.choice_set.get(pk=request.POST["choice"])

    if user.votes_count >= 3:
        send_mail(
            'Thanks for Voting',
            'Thanks for voting. You have voted on more than three questions.',
            'jay.g@auberginesolutions.com',
            [user.email],
            fail_silently=True,
        )
        return HttpResponse("Thanks for voting. You have voted on more than three questions.")

    else:
        
        selected_choice.votes+=1
        selected_choice.save()
        Vote.objects.create(user=user, question=question, choice=selected_choice)
        user.votes_count+=1
        user.save()
        
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

login_required(login_url='login')
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    login_required(login_url='login')
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]

login_required(login_url='login')
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

login_required(login_url='login')
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"



def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        first_name = request.POST.get('first_name')
        profile_picture = request.FILES.get('profile_picture')

        if pass1!=pass2:
            return HttpResponse("not same")
        else:
             my_user = CustomUser.objects.create_user(
                username=uname,
                email=email,
                password=pass1,
                first_name=first_name,
            )
             my_user.profile_picture = profile_picture
             my_user.save()
             return redirect('login')


    return render(request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('pass')
        user=authenticate(request,username=username,password=password)
        print(username,password)
        if user is not None:
            login(request,user)
            return redirect('/polls')
        else:
            return HttpResponse("incorrect login")
    return render(request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')