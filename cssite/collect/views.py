from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.views import generic, View
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Account, Task, Participation, ParsedFile, MappingInfo
from .forms import LoginForm


def index(request):
    return render(request, 'collect/index.html')


def signup(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password1"])
            account = Account(
                user=user,
                name=request.POST["name"],
                contact = request.POST["contact"],
                birth = request.POST["birth"],
                gender = request.POST["gender"],
                address = request.POST["address"],
                role = request.POST["role"])
            account.save()
            auth.login(request, user)
            if account.role == '제출자':
                return redirect(reverse('collect:tasks'))
            elif account.role == '평가자':
                return redirect(reverse('collect:index'))
    return render(request, 'collect/signup.html')


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
                return redirect(reverse('collect:index'))
        else:
            return HttpResponse('로그인 실패. 다시 시도 해보세요.')
    else:
        form = LoginForm()
        return render(request, 'collect/login.html', {'form': form})


def logout(request):
    auth.logout(request)
    return redirect(reverse('collect:index'))


class TaskList(generic.ListView):
    model = Task
    context_object_name = 'task_list'
    template_name = 'collect/task.html'


class TaskDetail(generic.DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'collect/task_detail.html'


def create_participation(request, pk):
    user = request.user
    task = get_object_or_404(Task, pk=pk)
    participation = Participation(account=user.account, task=task)
    participation.save()
    return redirect(reverse('collect:participations'))


class ParticipationList(View):
    def get(self, request):
        user = request.user
        participations = user.account.participations.all()
        return render(request, 'collect/participation.html', {'participations': participations})


def delete_participation(request, pk):
    participation = get_object_or_404(Participation, pk=pk)
    participation.delete()
    return redirect(reverse('collect:participations'))


class ParsedfileList(View):
    def get(self, request, pk):
        user = request.user
        task = get_object_or_404(Task, pk=pk)
        parsedfile_list = []

        for parsedfile in user.account.parsed_submits.all():
            if parsedfile in task.parsedfiles.all():
                parsedfile_list.append(parsedfile)
        
        context = {
            'task': task,
            'parsedfile_list': parsedfile_list
        }
        return render(request, 'collect/parsedfile.html', context)
