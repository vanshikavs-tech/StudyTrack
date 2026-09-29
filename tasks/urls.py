from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_task_view, name='add_task'),
    path('<int:id>/complete/', views.complete_task_view, name='complete_task'),
    path('<int:id>/delete/', views.delete_task_view, name='delete_task'),
]
