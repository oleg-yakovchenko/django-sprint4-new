from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .constants import POSTS_BY_PAGE
from .forms import CommentForm, PostForm
from .models import Category, Comment, Post


def index(request):
    post_queryset = Post.objects.published()
    page_obj = Paginator(post_queryset, POSTS_BY_PAGE).get_page(
        request.GET.get('page')
    )
    return render(
        request,
        'blog/index.html',
        {'page_obj': page_obj, 'post_list': page_obj.object_list},
    )


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    post_queryset = category.posts.published()
    page_obj = Paginator(post_queryset, POSTS_BY_PAGE).get_page(
        request.GET.get('page')
    )
    return render(
        request,
        'blog/category.html',
        {
            'category': category,
            'page_obj': page_obj,
            'post_list': page_obj.object_list,
        },
    )


def post_detail(request, post_id):
    """Автор видит свой отложенный/снятый пост, остальные — 404."""
    post = get_object_or_404(
        Post.objects.visible_for(request.user),
        id=post_id,
    )
    return render(
        request,
        'blog/detail.html',
        {
            'post': post,
            'form': CommentForm(),
            'comments': post.comments.all(),
        },
    )


@login_required
def create_post(request):
    form = PostForm(data=request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    form = PostForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=post,
    )
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', username=request.user.username)
    return render(
        request,
        'blog/create.html',
        {'form': PostForm(instance=post)},
    )


@login_required
def add_comment(request, post_id):
    """Создание комментария. Автор — из request.user, пост — из URL."""
    post = get_object_or_404(
        Post.objects.visible_for(request.user),
        id=post_id,
    )
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(
        request,
        'blog/detail.html',
        {
            'post': post,
            'form': form,
            'comments': post.comments.all(),
        },
    )


@login_required
def edit_comment(request, post_id, comment_id):
    """Редактирование. Комментарий должен принадлежать посту из URL."""
    comment = get_object_or_404(
        Comment,
        id=comment_id,
        post_id=post_id,
    )
    if comment.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    form = CommentForm(data=request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(
        request,
        'blog/comment.html',
        {'form': form, 'comment': comment},
    )


@login_required
def delete_comment(request, post_id, comment_id):
    """GET — подтверждение, POST — удаление."""
    comment = get_object_or_404(
        Comment,
        id=comment_id,
        post_id=post_id,
    )
    if comment.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)
    return render(
        request,
        'blog/comment.html',
        {'comment': comment},
    )
