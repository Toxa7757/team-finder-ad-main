from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.col_urls if hasattr(admin.site, 'col_urls') else admin.site.urls),
    path('users/', include('users.urls')),
    path('projects/', include('projects.urls')),
    # Редирект с корня на список проектов, как требует ТЗ
    path('', lambda request: redirect('/projects/list/', permanent=False)),
]