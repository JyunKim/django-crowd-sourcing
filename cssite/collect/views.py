from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.views import generic, View
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Account, Task, Participation, ParsedFile, MappingInfo
from .forms import LoginForm, GradeForm
from datetime import date


# 홈
def index(request):
    return render(request, 'collect/index.html')


# 회원가입
def signup(request):
    context = {}
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
                return redirect(reverse('collect:allocated-parsedfiles'))
        else:
            context.update({'error':"비밀번호가 일치하지 않습니다."})
    return render(request, 'collect/signup.html', context)


# 로그인
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if user.account.role == '제출자':
                return redirect(reverse('collect:tasks'))
            elif user.account.role == '평가자':
                return redirect(reverse('collect:allocated-parsedfiles'))
        return HttpResponse('로그인 실패. 다시 시도 해보세요.')
    else:
        form = LoginForm()
        return render(request, 'collect/login.html', {'form': form})


# 로그아웃
def logout(request):
    auth.logout(request)
    return redirect(reverse('collect:index'))


# 회원 정보 수정
def update(request, pk):
    if request.method == "POST":
        user = request.user
        if request.POST["password1"] == request.POST["password2"]:
            user.set_password(request.POST["password1"])
            user.save()
            account = user.account
            account.name=request.POST["name"]
            account.contact = request.POST["contact"]
            account.birth = request.POST["birth"]
            account.gender = request.POST["gender"]
            account.address = request.POST["address"]
            account.save()
            auth.login(request, user)
            if account.role == '제출자':
                return redirect(reverse('collect:tasks'))
            elif account.role == '평가자':
                return redirect(reverse('collect:allocated-parsedfiles'))
    return render(request, 'collect/update.html')

# 회원 탈퇴
def delete(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    return redirect(reverse('collect:index'))


# 태스크 목록
class TaskList(generic.ListView):
    model = Task
    context_object_name = 'task_list'
    template_name = 'collect/task.html'


# 태스크 상세 정보
class TaskDetail(generic.DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'collect/task_detail.html'


# 태스크 참여
def create_participation(request, pk):
    user = request.user
    task = get_object_or_404(Task, pk=pk)
    participation = Participation(account=user.account, task=task)
    participation.save()
    return redirect(reverse('collect:participations'))


# 참여 중인 태스크 목록
class ParticipationList(View):
    def get(self, request):
        user = request.user
        participations = user.account.participations.all()
        return render(request, 'collect/participation.html', {'participations': participations})


# 태스크 참여 취소
def delete_participation(request, pk):
    participation = get_object_or_404(Participation, pk=pk)
    participation.delete()
    return redirect(reverse('collect:participations'))


# 제출한 파일 목록
class ParsedfileList(View):
    def get(self, request, pk):
        user = request.user
        task = get_object_or_404(Task, pk=pk)
        parsedfile_list = user.account.parsed_submits.filter(task=task)
        total_tuple = sum(parsedfile.total_tuple for parsedfile in parsedfile_list)
        context = {
            'task': task,
            'parsedfile_list': parsedfile_list,
            'total_tuple': total_tuple
        }
        return render(request, 'collect/submitted_parsedfile.html', context)


# 평가된 파일 목록
class GradedfileList(View):
    def get(self, request):
        user = request.user
        parsedfiles = user.account.parsed_grades.filter(grading_score__isnull=False)
        return render(request, 'collect/graded_parsedfile.html', {'parsedfiles': parsedfiles})


# 할당된 파일 목록
class AllocatedfileList(View):
    def get(self, request):
        user = request.user
        parsedfiles = user.account.parsed_grades.filter(grading_score__isnull=True)
        now = date.today()
        context = {
            'parsedfiles': parsedfiles,
            'now': now
        }
        return render(request, 'collect/allocated_parsedfile.html', context)


# 파일 평가
def grade_parsedfile(request, pk):
    if request.method == "POST":
        form = GradeForm(request.POST)
        parsedfile = get_object_or_404(ParsedFile, pk=pk)
        if form.is_valid():
            parsedfile.grading_score = form.cleaned_data['grading_score']
            parsedfile.pass_state = form.cleaned_data['pass_state']
            parsedfile.save()
            return redirect(reverse('collect:graded-parsedfiles'))
        context = {
            'form': form,
            'parsedfile': parsedfile
        }
        context.update({'error':'0 ~ 10 사이의 숫자를 입력해주세요.'})
        return render(request, 'collect/grade.html', context)
    else:
        form = GradeForm()
        parsedfile = get_object_or_404(ParsedFile, pk=pk)
        context = {
            'form': form,
            'parsedfile': parsedfile
        }
        return render(request, 'collect/grade.html', context)
