from django.urls import path
from tasks.views import home, manager_dashboard, user_dashboard, test, create_task, view_task

urlpatterns = [
    # path('home/', home),
    path('manager-dashboard/', manager_dashboard),
    path('user-dashboard/', user_dashboard),
    path('test/', test),
    path('create-task/', create_task),
    path('view-task/', view_task),

]