from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home-page'),
    path('register/', views.register, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('delete-task/<int:id>/', views.DeleteTask, name='delete'),
    path('update/<int:id>/', views.Update, name='update'),
    path('edit/<int:id>/', views.Edit, name='edit'),
    path('finished-todos/', views.Finished, name='finished'),
    path('pending-todos/', views.Pending, name='pending'),
    path('task-by-speech/', views.speech, name='task-by-speech'),




]