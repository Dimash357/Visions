import os

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django_app import models
from .forms import ProfileUpdateForm
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.utils import timezone
from .models import profile


# def logging(controller_func):
#     def wrapper(*args, **kwargs):
#         print(args, kwargs)
#         request: WSGIRequest = args[0]
#         print(request.META)
#
#         models.Logging.objects.create(
#             user=request.user,
#             method=request.method,
#             status=0,
#             url="",
#             description="init"
#         )
#         try:
#             response: HttpResponse = controller_func(*args, **kwargs)
#             if settings.DEBUG_LOG:
#                 models.Logging.objects.create(
#                     user=request.user,
#                     method=request.method,
#                     status=200,
#                     url="",
#                     description="Response: " + str(response.content)
#                 )
#             return response
#         except Exception as error:
#             models.Logging.objects.create(
#                 user=request.user,
#                 method=request.method,
#                 status=500,
#                 url="",
#                 description="Error: " + str(error)
#             )
#             context = {"detail": str(error)}
#             if str(error).find("query does not exist"):
#                 context["extra"] = "Такого объекта не существует"
#             return render(request, "components/error.html", context=context)
#
#     return wrapper


class CustomPaginator:
    @staticmethod
    def paginate(object_list: any, per_page=5, page_number=1):
        paginator_instance = Paginator(object_list=object_list, per_page=per_page)
        try:
            page = paginator_instance.page(number=page_number)
        except PageNotAnInteger:
            page = paginator_instance.page(number=1)
        except EmptyPage:
            page = paginator_instance.page(number=paginator_instance.num_pages)
        return page


class HomeView(View):  # TODO контроллер класс
    template_name = 'django_app/home.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {}
        return render(request, 'django_app/home.html', context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        context = {}
        return render(request, 'django_app/home.html', context=context)

# @logging
def home_view(request: HttpRequest) -> HttpResponse:  # TODO контроллер функция
    context = {}
    return render(request, 'django_app/home.html', context=context)


def home_main(request):
    users = profile.objects.all().order_by('-points')  # Получаем всех пользователей
    notifications = [
        "Вы получили 200 поинтов за регистрацию"
    ]  # Массив уведомлений
    return render(request, 'django_app/home_main.html', {'users': users, 'notifications': notifications})

from .models import Task

def homework(request):
    tasks = Task.objects.all()
    return render(request, 'django_app/homework.html', {'tasks': tasks})


def upload_task(request, task_id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id)
            uploaded_file = request.FILES['attachment']

            # Логика обработки прикрепленного файла (например, сохранение в файловую систему)
            task_dir = os.path.join('C:/Users/Lenova/Documents/visions/static/media/tasks', str(task_id))

            # Создаём директорию, если она не существует
            os.makedirs(task_dir, exist_ok=True)

            file_path = os.path.join(task_dir, uploaded_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Отмечаем задание выполненным
            task.is_completed = True
            task.save()

            return redirect('django_app:homework')  # Перенаправляем обратно на страницу заданий
        except Task.DoesNotExist:
            return redirect('django_app:homework')


def visions(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, 'django_app/home.html', context=context)

# @logging
def profile_create(request):
    return render(request, 'django_app/profile.html')

# @logging
from django.contrib.auth.decorators import login_required

@login_required
def profileupdate(request):
    user_profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('django_app:profile')  # Укажите URL для перенаправления
    else:
        form = ProfileUpdateForm(instance=user_profile)
    return render(request, 'django_app/profileupdate.html', {'form': form})


# @logging
def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)

        return redirect(reverse('django_app:home', args=()))
    return render(request, 'django_app/register.html', context={})

# @logging
def login_(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, email=email, password=password)
        if user:
            login(request, user)
            return redirect(reverse('django_app:home_main', args=()))
        else:
            raise Exception("Логин или пароль не верны!")
    return render(request, 'django_app/login.html')

# @logging
def logout_f(request):
    logout(request)
    return redirect(reverse('django_app:login', args=()))

# @logging


def todo_create(request):
    if request.method == 'POST':
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        models.Todo.objects.create(
            author=User.objects.get(id=1),
            title=title,
            description=description,
            is_completed=False,
        )
        return redirect(reverse('django_app:todo_read_list', args=()))
    context = {
    }
    return render(request, 'django_app/todo_create.html', context)


def todo_read(request, todo_id=None):
    todo = models.Todo.objects.get(id=todo_id)
    context = {
        "todo": todo
    }
    return render(request, 'django_app/todo_detail.html', context)


def todo_read_list(request):

    is_detail_view = request.GET.get("is_detail_view", True)
    if is_detail_view == "False":
        is_detail_view = False
    elif is_detail_view == "True":
        is_detail_view = True
    todo_list = models.Todo.objects.all()

    def paginate(objects, num_page):
        paginator = Paginator(objects, num_page)
        pages = request.GET.get('page')
        try:
            local_page = paginator.page(pages)
        except PageNotAnInteger:
            local_page = paginator.page(1)
        except EmptyPage:
            local_page = paginator.page(paginator.num_pages)
        return local_page

    page = paginate(objects=todo_list, num_page=3)
    context = {
        "page": page,
        "is_detail_view": is_detail_view
    }
    return render(request, 'django_app/todo_list.html', context)


def todo_update(request, todo_id=None):
    if request.method == 'POST':
        todo = models.Todo.objects.get(id=todo_id)
        is_completed = request.POST.get("is_completed", "")
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        if is_completed:
            if is_completed == "False":
                todo.is_completed = False
            elif is_completed == "True":
                todo.is_completed = True
        if title and title != todo.title:
            todo.title = title
        if description and description != todo.description:
            todo.description = description
        todo.updated = timezone.now()
        todo.save()
        return redirect(reverse('django_app:todo_read_list', args=()))
    todo = models.Todo.objects.get(id=todo_id)
    context = {
        "todo": todo
    }
    return render(request, 'django_app/todo_change.html', context)


def todo_delete(request, todo_id=None):
    models.Todo.objects.get(id=todo_id).delete()
    return redirect(reverse('django_app:todo_read_list', args=()))
