from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F, Q
from django.views.generic import ListView
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from .models import Post, Category, SitePage, HomePage
from datetime import date


def _duolingo_streak() -> int:
    """Calculate Duolingo streak from a fixed start date."""
    start = date(2025, 8, 14)  # 322 days by July 1, 2026
    return (date.today() - start).days + 1


def home(request):
    """首页 - 个人名片"""
    homepage = HomePage.objects.first()
    return render(request, 'blog/home.html', {
        'homepage': homepage,
        'duolingo_streak': _duolingo_streak(),
    })


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        lang = self.request.LANGUAGE_CODE
        qs = Post.objects.filter(status="published", language=lang).order_by("-created_at")
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['current_category'] = get_object_or_404(Category, slug=category_slug)
        return context


def post_detail(request, slug):
    try:
        post = get_object_or_404(Post, slug=slug, status='published')
    except Exception:
        post = get_object_or_404(Post, slug=slug)

    # 浏览量 +1
    Post.objects.filter(pk=post.pk).update(views=F('views') + 1)
    post.refresh_from_db()

    lang = request.LANGUAGE_CODE

    # 上一页 / 下一页（按发布时间排序，同语言已发布文章）
    published_posts = Post.objects.filter(status='published', language=lang).order_by('-created_at')
    post_list = list(published_posts.values_list('slug', flat=True))
    try:
        current_index = post_list.index(post.slug)
    except ValueError:
        current_index = -1
    prev_post = published_posts[current_index + 1] if current_index < len(post_list) - 1 else None
    next_post = published_posts[current_index - 1] if current_index > 0 else None

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.content_type = ContentType.objects.get_for_model(Post)
            comment.object_id = post.pk
            if comment.author_name:
                comment.user = None
            elif request.user.is_authenticated:
                comment.user = request.user
            comment.is_active = True
            comment.save()
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'form': form,
        'prev_post': prev_post,
        'next_post': next_post,
    })


def about(request):
    page = get_object_or_404(SitePage, slug='about')
    return render(request, 'blog/about.html', {
        'page': page,
    })


class SearchListView(ListView):
    """搜索视图"""
    model = Post
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', '').strip()
        lang = self.request.LANGUAGE_CODE
        if q:
            return Post.objects.filter(
                status='published',
                language=lang
            ).filter(
                Q(title__icontains=q) | Q(content__icontains=q)
            ).order_by('-created_at')
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '').strip()
        return context


def resume(request):
    """简历页面"""
    return render(request, 'blog/resume.html')


def portfolio(request):
    """我的作品页面"""
    return render(request, 'blog/portfolio.html')

