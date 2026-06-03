from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F
from django.views.generic import ListView
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from .models import Post, Category
from .models import SitePage
import markdown


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        qs = Post.objects.all().order_by("-created_at").filter(status="published")
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

    # 生成 Markdown 和目录 TOC
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.tables',
            'markdown.extensions.toc',
            'markdown.extensions.sane_lists',
        ],
        extension_configs={
            'markdown.extensions.codehilite': {
                'guess_lang': False,
                'linenums': False,
                'css_class': 'codehilite',
            },
            'markdown.extensions.toc': {
                'permalink': False,
            }
        }
    )

    post_html = md.convert(post.content)
    post_toc = md.toc

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
        'post_html': post_html,
        'post_toc': post_toc,
        'form': form,
    })


def about(request):
    page = get_object_or_404(SitePage, slug='about')

    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.tables',
            'markdown.extensions.toc',
            'markdown.extensions.sane_lists',
        ],
        extension_configs={
            'markdown.extensions.codehilite': {
                'guess_lang': False,
                'linenums': False,
                'css_class': 'codehilite',
            },
            'markdown.extensions.toc': {
                'permalink': False,
            }
        }
    )

    page_html = md.convert(page.content or "")
    page_toc = md.toc

    return render(request, 'blog/about.html', {
        'page': page,
        'page_html': page_html,
        'page_toc': page_toc,
    })
