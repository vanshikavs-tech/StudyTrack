from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.http import HttpResponse
from tasks import views as task_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', lambda request: HttpResponse(status=204)),
    path('', RedirectView.as_view(url='/dashboard/', permanent=False), name='root_redirect'),
    path('login/', task_views.login_view, name='login'),
    path('logout/', task_views.logout_view, name='logout'),
    path('dashboard/', task_views.dashboard_view, name='dashboard'),
    path('tasks/', include('tasks.urls')),
]

