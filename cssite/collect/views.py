from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.views import generic, View
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Account, Task, Participation, ParsedFile, MappingInfo
from .forms import LoginForm


class TaskList(generic.ListView):
    model = Task
    context_object_name = 'task_list'
    template_name = 'collect/task.html'


class TaskDetail(generic.DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'collect/task_detail.html'


class ParticipationList(View):
    def get(self, request):
        user = request.user
        participations = user.account.participations.all()
        context = {
            'participations': participations,
            'user': user
        }
        return render(request, 'collect/participation.html', context)


def delete_participation(request, pk):
    participation = Participation.objects.get(pk=pk)
    participation.delete()
    return redirect(reverse('collect:participations'))


def signup(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password1"])
            nickname = request.POST["nickname"]
            profile = Profile(user=user, nickname=nickname)
            profile.save()
            auth.login(request,user)
            return redirect(reverse('collect:index'))
    return render(request, 'account/signup.html')


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username = username, password = password)
        if user is not None:
            auth.login(request, user)
            if user.account.role == '제출자':
                return redirect(reverse('collect:tasks'))
            elif user.account.role == '평가자':
                return redirect(reverse(''))
        else:
            return HttpResponse('로그인 실패. 다시 시도 해보세요.')
    else:
        form = LoginForm()
        return render(request, 'collect/login.html', {'form': form})


def logout(request):
    auth.logout(request)
    return redirect(reverse('collect:index'))
