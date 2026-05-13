from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('notes/', views.notes, name='notes'),
    path('notes/delete/<int:note_id>/', views.del_note, name='del_note'),
    path('notes/find/', views.find_note, name='find_note'),
    path('notes/delete_csrf/<int:note_id>/', views.del_note_csrf, name='del_csrf'),
]
