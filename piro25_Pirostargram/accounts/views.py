from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import SignupForm, ProfileForm
from .models import User


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("posts:feed")
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html", {"form": form})


class MyLoginView(LoginView):
    template_name = "accounts/login.html"


@login_required
def search(request):
    query = request.GET.get("q", "").strip()
    users = User.objects.none()
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | Q(name__icontains=query)
        ).exclude(pk=request.user.pk)
    return render(request, "accounts/search.html", {"users": users, "query": query})


@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = profile_user.posts.all().order_by("-created_at")
    context = {
        "profile_user": profile_user,
        "posts": posts,
        "is_following": request.user.followings.filter(pk=profile_user.pk).exists(),
    }
    return render(request, "accounts/profile.html", context)


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile", request.user.username)
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/profile_edit.html", {"form": form})


@require_POST
@login_required
def follow(request, username):
    target = get_object_or_404(User, username=username)
    if target == request.user:
        return JsonResponse({"error": "self follow"}, status=400)
    if request.user.followings.filter(pk=target.pk).exists():
        request.user.followings.remove(target)
        is_following = False
    else:
        request.user.followings.add(target)
        is_following = True
    return JsonResponse({
        "is_following": is_following,
        "follower_count": target.followers.count(),
    })
