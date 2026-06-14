from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.user_list, name='user_list'),
    path('<int:pk>/', views.user_detail, name='user_detail'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-profile/', views.profile_edit, name='profile_edit'),
    path('change-password/', views.password_change, name='password_change'),
    # AJAX маршруты для JS-скрипта Практикума
    path('skills/', views.skills_autocomplete, name='skills_autocomplete'),
    path('<int:user_id>/skills/add/', views.add_skill, name='add_skill'),
    path('<int:user_id>/skills/<int:skill_id>/remove/', views.remove_skill, name='remove_skill'),
]