import json

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from accounts.models import User
from stories.models import Story
from .forms import PostForm
from .models import Post, Comment


@login_required
def feed(request):
    following_ids = list(request.user.followings.values_list("pk", flat=True))
    following_ids.append(request.user.pk)

    posts = (
        Post.objects.filter(author__pk__in=following_ids)
        .select_related("author")
        .prefetch_related("likes", "comments__author")
    )

    query = request.GET.get("q", "").strip()
    if query:
        posts = posts.filter(content__icontains=query)

    sort = request.GET.get("sort", "recent")
    if sort == "likes":
        posts = posts.annotate(num_likes=Count("likes")).order_by("-num_likes", "-created_at")
    else:
        posts = posts.order_by("-created_at")

    stories = (
        Story.objects.filter(author__pk__in=following_ids)
        .select_related("author")
        .order_by("-created_at")
    )
    suggested_users = User.objects.exclude(pk__in=following_ids)[:4]

    context = {
        "posts": posts,
        "stories": stories,
        "suggested_users": suggested_users,
        "query": query,
        "sort": sort,
    }
    return render(request, "posts/feed.html", context)


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("posts:feed")
    else:
        form = PostForm()
    return render(request, "posts/post_form.html", {"form": form})


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("posts:feed")
    else:
        form = PostForm(instance=post)
    return render(request, "posts/post_form.html", {"form": form, "post": post})


@require_POST
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    post.delete()
    return redirect("posts:feed")


@require_POST
@login_required
def like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(pk=request.user.pk).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({"liked": liked, "like_count": post.like_count})


@require_POST
@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    data = json.loads(request.body)
    content = data.get("content", "").strip()
    if not content:
        return JsonResponse({"error": "empty"}, status=400)
    comment = Comment.objects.create(post=post, author=request.user, content=content)
    return JsonResponse({
        "id": comment.pk,
        "author": comment.author.username,
        "content": comment.content,
    })


@require_POST
@login_required
def comment_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    data = json.loads(request.body)
    content = data.get("content", "").strip()
    if not content:
        return JsonResponse({"error": "empty"}, status=400)
    comment.content = content
    comment.save()
    return JsonResponse({"id": comment.pk, "content": comment.content})


@require_POST
@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    comment.delete()
    return JsonResponse({"deleted": True})
