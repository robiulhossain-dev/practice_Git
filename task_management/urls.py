from django.contrib import admin
from django.urls import path, include
from tasks.views import manager_dashboard
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('manager-dashboard/', manager_dashboard),
    path('tasks/', include("tasks.urls"))
]+ debug_toolbar_urls()
