from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .models import User, Skill
from .forms import ProfileEditForm, RegistrationForm, LoginForm, PasswordChangeForm

# 1. Список пользователей с фильтрацией по навыкам
def user_list(request):
    users_queryset = User.objects.all().order_by('-id')
    active_skill = request.GET.get('skill')
    
    if active_skill:
        users_queryset = users_queryset.filter(skills__name=active_skill)
        
    all_skills = Skill.objects.all().order_by('name')
    
    # Пагинация по 12 пользователей
    paginator = Paginator(users_queryset, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        "participants": page_obj,  # Имя переменной должно совпадать с шаблоном Практикума
        "all_skills": all_skills,
        "active_skill": active_skill,
    }
    return render(request, 'users/participants.html', context)

# 2. Страница отдельного пользователя
def user_detail(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    return render(request, 'users/user-details.html', {"user": user_obj})

# 3. AJAX: Автодополнение навыков (GET)
def skills_autocomplete(request):
    query = request.GET.get('q', '').strip()
    if query:
        skills = Skill.objects.filter(name__istartswith=query).order_by('name')[:10]
        data = [{"id": skill.id, "name": skill.name} for skill in skills]
    else:
        data = []
    return JsonResponse(data, safe=False)

# 4. AJAX: Добавление навыка (POST)
@login_required
@require_POST
def add_skill(request, user_id):
    import json
    if request.user.id != int(user_id):
        return JsonResponse({"error": "Permission denied"}, status=403)
        
    user = get_object_or_404(User, pk=user_id)
    
    try:
        data = json.loads(request.body)
        skill_id = data.get('skill_id')
        name = data.get('name')
    except json.JSONDecodeError:
        skill_id = request.POST.get('skill_id')
        name = request.POST.get('name')
    
    created, added = False, False
    skill = None

    if skill_id:
        skill = get_object_or_404(Skill, pk=skill_id)
    elif name:
        skill, created = Skill.objects.get_or_create(name=name.strip())

    if skill and skill not in user.skills.all():
        user.skills.add(skill)
        added = True

    return JsonResponse({
        "skill_id": skill.id if skill else None,
        "created": created,
        "added": added
    })

# 5. AJAX: Удаление навыка (POST)
@login_required
@require_POST
def remove_skill(request, user_id, skill_id):
    if request.user.id != int(user_id):
        return JsonResponse({"error": "Permission denied"}, status=403)
        
    user = get_object_or_404(User, pk=user_id)
    skill = get_object_or_404(Skill, pk=skill_id)
    
    if skill in user.skills.all():
        user.skills.remove(skill)
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error", "message": "Skill not found in profile"}, status=400)

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/projects/list/')
            else:
                form.add_error(None, 'Неверный имейл или пароль')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/projects/list/')

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_detail', pk=request.user.pk)
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            if not request.user.check_password(form.cleaned_data['old_password']):
                form.add_error('old_password', 'Неверный старый пароль')
            else:
                request.user.set_password(form.cleaned_data['new_password1'])
                request.user.save()
                update_session_auth_hash(request, request.user)
                return redirect('user_detail', pk=request.user.pk)
    else:
        form = PasswordChangeForm()
    return render(request, 'users/change_password.html', {'form': form})