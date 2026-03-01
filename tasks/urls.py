from django.urls import path
from tasks.views import show_task,specific_task

urlpatterns = [
    path('show-task/', show_task),
    path('show-task/<int:id>/', specific_task)
]