from django.urls import path
from . import views


app_name = "collect"
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/<int:pk>/', views.update, name='update'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('tasks/', views.TaskList.as_view(), name='tasks'),
    path('tasks/<int:pk>/', views.TaskDetail.as_view(), name='task-detail'),
    path('participations/', views.ParticipationList.as_view(), name='participations'),
    path('tasks/<int:pk>/create/', views.create_participation, name='create-participation'),
    path('participations/<int:pk>/delete/', views.delete_participation, name='delete-participation'),
    path('tasks/<int:pk>/parsedfiles/', views.ParsedfileList.as_view(), name='submitted-parsedfiles'),
    path('graded-parsedfiles/', views.GradedfileList.as_view(), name='graded-parsedfiles'),
    path('allocated-parsedfiles/', views.AllocatedfileList.as_view(), name='allocated-parsedfiles'),
    path('allocated-parsedfiles/<int:pk>/', views.grade_parsedfile, name='grade-parsedfile'),
]
