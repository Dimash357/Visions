from django.urls import path, re_path
from django_app import views

app_name = 'django_app'
urlpatterns = [
    path('', views.home_view, name=''),
    path('home_main/', views.home_main, name='home_main'),


    path('register/', views.register, name='register'),
    path('login/', views.login_, name='login'),
    path('logout/', views.logout_f, name='logout'),


    path('homework/', views.homework, name='homework'),
    # path('visions/', views.visions, name='visions'),
    path('upload_task/<int:task_id>/', views.upload_task, name='upload_task'),

    path('profile/', views.profile_create, name='profile'),
    path('profile_update/', views.profileupdate, name='profile_update'),


    path('todo/create/', views.todo_create, name='todo_create'),
    path('todo/<int:todo_id>/', views.todo_read, name='todo_read'),
    path('todo/list/', views.todo_read_list, name='todo_read_list'),
    path('todo/<int:todo_id>/update/', views.todo_update, name='todo_update'),
    re_path(r'^todo/(?P<todo_id>\d+)/delete/$', views.todo_delete, name='todo_delete'),

]