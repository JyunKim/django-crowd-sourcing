from django.urls import path
from . import views


app_name = "collect"
urlpatterns = [
    path('login/', views.login, name='login'),
    path('tasks/', views.TaskList.as_view(), name='tasks'),
    path('tasks/<int:pk>/', views.TaskDetail.as_view(), name='task-detail'),
    path('participations/', views.ParticipationList.as_view(), name='participations'),
    path('participations/<int:pk>', views.delete_participation, name='delete-participation'),
]
