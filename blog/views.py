from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from django.urls import reverse

from blog.models import Post, Comment
from marketing.models import Signup
from blog.forms import CommentForm


def get_category_count():
    queryset = Post.objects.values('category__title').annotate(Count('category__title'))
    return queryset

def index(request):
    queryset = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[:3]
    
    if request.method == "POST":
        email = request.POST['email']
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'posts': queryset,
        'latest': latest,
    }
    return render(request, 'index.html', context)

def blog(request):
    category_count = get_category_count()
    article_list = Post.objects.all()
    latest = Post.objects.order_by('-timestamp')[:3]
    paginator = Paginator(article_list, 2)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'article_list': paginated_queryset,
        'page_request_var': page_request_var,
        'latest': latest,
        'category_count': category_count,
    }
    return render(request, 'blog.html', context)

def serach(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset,
    }

    return render(request, 'search_result.html', context)


def post(request, id):
    post = Post.objects.get(id=id)
    category_count = get_category_count()
    latest = Post.objects.order_by('-timestamp')[:3]
    
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse('post_detail', kwargs={
                'id': post.id
            }))
    context = {
        'post': post,
        'latest': latest,
        'category_count': category_count,
        'form': form,
    }
    return render(request, 'post.html', context)

