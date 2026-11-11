from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from blog.service import paginate_queryset

from .forms import ProfileEditForm, RegistrationForm

User = get_user_model()


def register(request):
    """Регистрация. После успеха — редирект на главную."""
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('blog:index')
    return render(
        request,
        'registration/registration_form.html',
        {'form': form},
    )


def profile(request, username):
    """Публичный профиль.

    Владелец видит все свои посты (включая неопубликованные,
    отложенные и из снятых категорий), остальные — только опубликованные.
    """
    profile_user = get_object_or_404(User, username=username)
    if request.user == profile_user:
        post_queryset = profile_user.posts.with_related()
    else:
        post_queryset = profile_user.posts.published()
    page_obj = paginate_queryset(request, post_queryset)
    return render(
        request,
        'blog/profile.html',
        {'profile': profile_user, 'page_obj': page_obj},
    )


@login_required
def edit_profile(request):
    """Редактирование собственного профиля. Шаблон — blog/user.html."""
    user = request.user
    form = ProfileEditForm(request.POST or None, instance=user)
    if form.is_valid():
        user = form.save()
        return redirect('blog:profile', username=user.username)
    return render(request, 'blog/user.html', {'form': form})
