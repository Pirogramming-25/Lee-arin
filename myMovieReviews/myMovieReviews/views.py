from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie


# Create your views here.
def reviews_list(request):
    reviews = Movie.objects.all().order_by('-release_date')
    return render(request, 'myMovieReviews/reviews_list.html', {'reviews': reviews})

def reviews_detail(request, pk):
    review = get_object_or_404(Movie, pk=pk)
    return render(request, 'myMovieReviews/reviews_detail.html', {'review': review})

def reviews_create(request):
    if request.method == 'POST':    # 폼 제출 -> 저장
        title = request.POST.get('title')
        director = request.POST.get('director')
        actors = request.POST.get('actors')
        genre = request.POST.get('genre')
        release_date = request.POST.get('release_date')
        rating = request.POST.get('rating')
        runningtime = request.POST.get('runningtime')
        review_text = request.POST.get('review_text')

        movie = Movie(
            title=title,
            director=director,
            actors=actors,
            genre=genre,
            release_date=release_date,
            rating=rating,
            runningtime=runningtime,
            review_text=review_text
        )
        movie.save() # 옵젝을 db에 저장하는 함수
        return redirect('reviews-list') # redirect는 url로 이동 (cf. render는 html로 이동)
    else:   #  빈 폼
        return render(request, 'myMovieReviews/reviews_create.html')
    
def reviews_edit(request, pk):
    review = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        review.title = request.POST.get('title')
        review.director = request.POST.get('director')
        review.actors = request.POST.get('actors')
        review.genre = request.POST.get('genre')
        review.release_date = request.POST.get('release_date')
        review.rating = request.POST.get('rating')
        review.runningtime = request.POST.get('runningtime')
        review.review_text = request.POST.get('review_text')

        review.save()
        return redirect('reviews-detail', pk=review.pk)
    else:
        return render(request, 'myMovieReviews/reviews_edit.html', {'review': review})

def reviews_delete(request, pk):
    review = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('reviews-list')
    else:
        return render(request, 'myMovieReviews/reviews_delete.html', {'review': review})