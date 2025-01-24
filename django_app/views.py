import os
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django_app import models
from .forms import ProfileUpdateForm
from django.utils import timezone
from .models import profile, Notification
from django.shortcuts import redirect
from django.contrib import messages
from .models import Task


import requests
from django.http import JsonResponse
from django.conf import settings

TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/getChatMember"
CHANNEL_ID = "@visionskz"  # Ваш канал

def check_subscription_telegram(request):
    telegram_username = request.GET.get("username")  # Имя пользователя Telegram
    if not telegram_username:
        return JsonResponse({"success": False, "message": "Введите ваш Telegram username."})

    url = TELEGRAM_API_URL.format(token=settings.TELEGRAM_BOT_TOKEN)
    response = requests.get(url, params={"chat_id": CHANNEL_ID, "user_id": telegram_username})
    data = response.json()

    if data.get("ok") and data.get("result", {}).get("status") in ["member", "administrator", "creator"]:
        # Пользователь подписан
        profile_obj = get_object_or_404(profile, user=request.user)
        if not Notification.objects.filter(user=request.user, message="Вы подписались на Telegram и получили 50 очков!").exists():
            profile_obj.points += 100
            profile_obj.save()
            Notification.objects.create(
                user=request.user,
                message="Вы подписались на Telegram и получили 100 очков!"
            )
        return JsonResponse({"success": True, "message": "Вы успешно подписаны на канал! Баллы начислены."})
    else:
        return JsonResponse({"success": False, "message": "Вы не подписаны на канал. Пожалуйста, подпишитесь и попробуйте снова."})


def check_subscription_instagram(request):
    profile_obj = get_object_or_404(profile, user=request.user)

    # Проверяем, начислялись ли уже баллы за Instagram
    if not Notification.objects.filter(user=request.user, message="Вы подписались на Instagram и получили 50 очков!").exists():
        # Здесь должна быть логика проверки подписки через Instagram API
        # Если подписка успешна:
        profile_obj.points += 100
        profile_obj.save()

        Notification.objects.create(
            user=request.user,
            message="Вы подписались на Instagram и получили 100 очков!"
        )
        messages.success(request, "Вы успешно подписались на Instagram! Баллы начислены.")
    else:
        messages.info(request, "Вы уже получили баллы за подписку на Instagram.")

    return redirect('https://www.instagram.com/visions_kz/')  # Ссылка на ваш аккаунт в Instagram



def login_user(request):
    if not request.user.is_staff:  # Только для обычных пользователей
        user = authenticate(request, username='user', password='password')
        if user is not None:
            login(request, user)


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

def home_view(request: HttpRequest) -> HttpResponse:  # TODO контроллер функция
    context = {}
    return render(request, 'django_app/home_main.html', context=context)


def home_main(request):
    users = profile.objects.all().order_by('-points')  # Получаем всех пользователей
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    notifications.update(is_read=True)

    return render(request, 'django_app/home_main.html', {'users': users, 'notifications': notifications})


def homework(request):
    tasks = Task.objects.filter(user=request.user).order_by('is_completed')

    return render(request, 'django_app/homework.html', {'tasks': tasks})


def upload_task(request, task_id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id, user=request.user)
            uploaded_file = request.FILES['attachment']

            task_dir = os.path.join('C:/Users/Lenova/Documents/visions/static/media/tasks', str(task_id))

            os.makedirs(task_dir, exist_ok=True)

            username = request.user.username
            file_name = f"{username}_{uploaded_file.name}"

            file_path = os.path.join(task_dir, file_name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            task.is_completed = True
            task.save()

            profile = request.user.profile
            profile.points += 300
            total_tasks = 6  # Общее количество заданий
            completed_tasks = Task.objects.filter(user=request.user, is_completed=True).count()  # Выполненные задания

            if completed_tasks == total_tasks and total_tasks > 0:  # Все задания выполнены
                profile.is_eligible_for_testing = True
                Notification.objects.create(
                    user=request.user,
                    message="Поздравляем! Вы выполнили все задания и допущены к тестированию!",
                )
                messages.success(request, "Поздравляем! Вы выполнили все задания и допущены к тестированию!")

            profile.save()

            Notification.objects.create(
                user=request.user,
                message=f"Вы выполнили задание '{task.title}' и получили 300 очков!",
            )

            return redirect('django_app:homework')
        except Task.DoesNotExist:
            return redirect('django_app:homework')

def about(request):
    return render(request, 'django_app/about.html')


def profile_create(request):
    return render(request, 'django_app/profile.html')


def profileupdate(request):
    if request.method == 'POST':
        profile = request.user.profile

        pform = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if pform.is_valid():
            pform.save()

            if all([profile.image, profile.city, profile.description]):
                if profile.points == 100:
                    profile.points += 200
                    profile.save()

                    Notification.objects.create(
                        user=request.user,
                        message="Вы заполнили все данные и получили 200 очков!",
                    )

                    messages.success(request, "Вы получили 200 очков за заполнение профиля!")

            return redirect('django_app:profile')
    else:
        profile = request.user.profile
        pform = ProfileUpdateForm(instance=profile)

    return render(request, 'django_app/profileupdate.html', {'pform': pform})


# @logging
def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")

        if User.objects.filter(username=username).exists():
            error_message = "Пользователь с таким логином уже существует."
            return render(request, 'django_app/register.html', {'error_message': error_message})

        if User.objects.filter(email=email).exists():
            error_message = "Пользователь с таким email уже существует."
            return render(request, 'django_app/register.html', {'error_message': error_message})

        try:
            validate_password(password)
        except ValidationError as e:
            error_message = "Вы ввели очень легкий пароль"  # Объединяем все сообщения об ошибках в одну строку
            return render(request, 'django_app/register.html', {'error_message': error_message})

        if username and email and password:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)

            profile = request.user.profile
            profile.points += 100
            profile.save()

            Notification.objects.create(
                user=request.user,
                message=f"Вы зарегистрировались и получили 100 очков!",
            )
            return redirect(reverse('django_app:home_main', args=()))
        else:
            error_message = "Все поля обязательны для заполнения."
            return render(request, 'django_app/register.html', {'error_message': error_message})
    else:
        return render(request, 'django_app/register.html')


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
            error_message = "Логин или пароль не верны!"
            return render(request, 'django_app/login.html', {'error_message': error_message})
    return render(request, 'django_app/login.html')

def logout_f(request):
    logout(request)
    return redirect(reverse('django_app:login', args=()))


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
