from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Story, StoryImage


@login_required
def story_create(request):
    if request.method == "POST":
        images = request.FILES.getlist("images")
        if images:
            story = Story.objects.create(author=request.user)
            for i, image in enumerate(images):
                StoryImage.objects.create(story=story, image=image, order=i)
            return redirect("posts:feed")
    return render(request, "stories/story_form.html")


@login_required
def story_detail(request, pk):
    story = get_object_or_404(Story, pk=pk)
    return render(request, "stories/story_detail.html", {"story": story})
