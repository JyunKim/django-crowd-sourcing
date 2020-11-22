from django.urls import path
from . import views


app_name = "collect"
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('tasks/', views.TaskList.as_view(), name='tasks'),
    path('tasks/<int:pk>/', views.TaskDetail.as_view(), name='task-detail'),
    path('participations/', views.ParticipationList.as_view(), name='participations'),
    path('tasks/<int:pk>/create/', views.create_participation, name='create-participation'),
    path('participations/<int:pk>/delete/', views.delete_participation, name='delete-participation'),
]
