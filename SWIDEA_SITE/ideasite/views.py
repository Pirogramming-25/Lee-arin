from django.shortcuts import render, get_object_or_404, redirect
from .models import Idea, Devtool, IdeaStar
from django.http import JsonResponse
from .forms import IdeaRegisterForm

# main page
def idea_list(request):
    sort = request.GET.get('sort', '-registered_at') 
    sort_options = {
        'newest': '-registered_at',   
        'oldest': 'registered_at',    
        'name': 'title',             
    }
    order = sort_options.get(sort, '-registered_at')   
    ideas = Idea.objects.all().order_by(order) 
    return render(request, "ideasite/main.html", {
        "ideas": ideas,
        "sort": sort,          # 지금 어떤 정렬인지 템플릿에 넘김
    })

def idea_star(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)

    if not request.session.session_key:   # 세션 키가 없으면 만들기
        request.session.create()
    session_key = request.session.session_key

    star, created = IdeaStar.objects.get_or_create(
        session_key=session_key,
        idea=idea,
    )
    if not created:          # 이미 있었으면 → 취소
        star.delete()
        liked = False
    else:                    # 새로 만들었으면 → 별 켜짐
        liked = True

    return JsonResponse({'liked': liked, 'count': idea.idea_stars.count()})

def idea_list(request):
    sort = request.GET.get('sort', 'newest')
    sort_options = {
        'newest': '-registered_at',
        'oldest': 'registered_at',
        'name': 'title',
    }
    order = sort_options.get(sort, '-registered_at')
    ideas = Idea.objects.all().order_by(order)

    session_key = request.session.session_key
    starred_ideas = list(
        IdeaStar.objects.filter(session_key=session_key)
        .values_list('idea_id', flat=True)
    )   # 이 브라우저가 별 누른 아이디어 id 목록

    return render(request, "ideasite/main.html", {
        "ideas": ideas,
        "sort": sort,
        "starred_ideas": starred_ideas,
    })


def idea_interest(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    action = request.POST.get('action')

    if action == 'up':
        idea.interest += 1
    elif action == 'down' and idea.interest > 0:
        idea.interest -= 1

    idea.save()
    return JsonResponse({'interest': idea.interest})   # 바뀐 값을 JSON으로 응답


# register page
def idea_register(request):
    if request.method == "POST":
        form = IdeaRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save()
            return redirect("ideasite:detail", idea_id=idea.id)
    else:
        form = IdeaRegisterForm()
    return render(request, "ideasite/register.html", {"form": form})
    

# detail page
def idea_detail(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    return render(request, "ideasite/detail.html", {"idea": idea})

def idea_delete(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    idea.delete()
    return redirect("ideasite:list")    


# edit page
def idea_edit(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    if request.method == "POST":
        form = IdeaRegisterForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            form.save()
            return redirect("ideasite:detail", idea_id=idea.id)
    else:
        form = IdeaRegisterForm(instance=idea)
    return render(request, "ideasite/edit.html", {"form": form})    

# devtool page
def devtool_list(request):
    sort = request.GET.get('sort', 'dev_name')
    devtools = Devtool.objects.all().order_by(sort)
    return render(request, "devtool/main.html", {"devtools": devtools})

# devtool register page
def devtool_register(request):
    if request.method == "POST":
        dev_name = request.POST.get("dev_name")
        dev_kind = request.POST.get("dev_kind")
        dev_content = request.POST.get("dev_content")

        devtool = Devtool(
            dev_name=dev_name,
            dev_kind=dev_kind,
            dev_content=dev_content
        )
        devtool.save()
        return redirect("ideasite:devtool_detail", devtool_id=devtool.id)
    else:
        return render(request, "devtool/register.html")
    
# devtool detail page
def devtool_detail(request, devtool_id):
    devtool = get_object_or_404(Devtool, id=devtool_id)
    return render(request, "devtool/detail.html", {"devtool": devtool})

def devtool_delete(request, devtool_id):
    devtool = get_object_or_404(Devtool, id=devtool_id)
    devtool.delete()
    return redirect("ideasite:devtool_list")    

# devtool edit page
def devtool_edit(request, devtool_id):
    devtool = get_object_or_404(Devtool, id=devtool_id)
    if request.method == "POST":
        devtool.dev_name = request.POST.get("dev_name")
        devtool.dev_kind = request.POST.get("dev_kind")
        devtool.dev_content = request.POST.get("dev_content")
        devtool.save()
        return redirect("ideasite:devtool_detail", devtool_id=devtool.id)
    else:
        return render(request, "devtool/edit.html", {"devtool": devtool})