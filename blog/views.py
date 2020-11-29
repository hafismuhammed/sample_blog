from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from django.urls import reverse
from django.contrib import messages
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView 

from blog.models import Post, Comment, Author, PostView
from marketing.models import Signup
from blog.forms import PostForm, CommentForm


def get_author(user):
    qur = Author.objects.filter(user=user)
    if qur.exists():
        return qur[0]
    return None

def get_category_count():
    queryset = Post.objects.values('category__title').annotate(Count('category__title'))
    return queryset

# corresponding cbv of fbv 'index'
class IndexView(View):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.filter(featured=True)
        latest = Post.objects.order_by('-timestamp')[:3]
        context = {
            'posts': queryset,
            'latest': latest,
        }
        return render(request, 'index.html', context)

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
        messages.info(request, 'successfully subscribe')
        return redirect('home')


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

# corresponding cbv of fbv 'post_list'
class PostListView(ListView):
    model = Post
    template_name = 'blog.html'
    context_object_name = 'article_list'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        latest = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['page_request_var'] = 'page'
        context['latest'] = latest
        context['category_count'] = category_count
        return context


def post_list(request):
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
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
        'latest': latest,
        'category_count': category_count,
    }
    return render(request, 'blog.html', context)

# corresponding cbv of fbv 'serach'
class SerachView(View):
    def get(self, request, *args, **kwargs):
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

# corresponding cbv of fbv 'post_detail'
class PostDetailView(DetailView):
    form = CommentForm()
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(user=self.request.user, post=obj)
        return obj

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        latest = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['latest'] = latest
        context['category_count'] = category_count
        context['form'] = self.form
        return context
    
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse('post_detail', kwargs={
                'pk': post.pk
            }))

def post_detail(request, id):
    post = Post.objects.get(id=id)
    category_count = get_category_count()
    latest = Post.objects.order_by('-timestamp')[:3]
    
    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)

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

# corresponding cbv of fbv 'post_create'
class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect(reverse('post_detail', kwargs={
            'pk': form.instance.pk
        }))


def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post_detail', kwargs={
                'id': form.instance.id
            }))

    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'post_create.html', context)

# corresponding cbv of fbv 'post_update'
class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect(reverse('post_detail', kwargs={
                'pk': form.instance.pk
            }))



def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post_detail', kwargs={
                'id': form.instance.id
            }))

    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'post_create.html', context)

# corresponding cbv of fbv 'post_delete'
class PostDeleteView(DeleteView):
    model = Post
    success_url = '/blog'
    template_name = 'post_confirm_delete.html'

def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse('blog'))