"""Public blog views."""
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import BlogPost, BlogTag, BlogCategory, BlogPageSettings, BlogAuthor


def _blog_queryset():
    return BlogPost.objects.filter(status='published').select_related('category', 'author').prefetch_related('tags')


@require_GET
def blog_search_suggest(request):
    """AJAX: return search suggestions (title, slug, thumbnail, category, author)."""
    q = request.GET.get('q', '').strip()
    if len(q) < 2:
        return JsonResponse({'results': []})
    limit = int(request.GET.get('limit', 8))
    posts = _blog_queryset().filter(
        Q(title__icontains=q) | Q(excerpt__icontains=q) | Q(long_excerpt__icontains=q)
    )[:limit]
    results = []
    for p in posts:
        thumb = p.featured_image.url if p.featured_image else None
        results.append({
            'title': p.title,
            'slug': p.slug,
            'url': request.build_absolute_uri(p.get_absolute_url()),
            'thumbnail': request.build_absolute_uri(thumb) if thumb else None,
            'category': p.category.name if p.category else None,
            'author': p.get_author_display(),
        })
    return JsonResponse({'results': results})


@require_GET
def blog_api(request):
    """AJAX: return filtered posts as JSON for dynamic loading."""
    tag_slugs = request.GET.getlist('tags[]') or request.GET.getlist('tag')
    author_id = request.GET.get('author', '')
    search_q = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))
    per_page = min(int(request.GET.get('per_page', 9)), 24)

    qs = _blog_queryset()
    if tag_slugs:
        qs = qs.filter(tags__slug__in=tag_slugs).distinct()
    if author_id and author_id.isdigit():
        qs = qs.filter(author_id=int(author_id))
    if search_q:
        qs = qs.filter(
            Q(title__icontains=search_q) |
            Q(excerpt__icontains=search_q) |
            Q(long_excerpt__icontains=search_q)
        )

    settings = BlogPageSettings.get()
    order = '-date' if settings.default_sort == 'latest' else 'date'
    qs = qs.order_by(order).distinct()
    paginator = Paginator(qs, per_page)
    pager = paginator.get_page(page)

    posts_data = []
    for p in pager:
        thumb = p.featured_image.url if p.featured_image else None
        posts_data.append({
            'id': p.pk,
            'title': p.title,
            'slug': p.slug,
            'url': request.build_absolute_uri(p.get_absolute_url()),
            'excerpt': p.excerpt[:120] + '...' if len(p.excerpt) > 120 else p.excerpt,
            'date': p.date.strftime('%b %d, %Y'),
            'category': p.category.name if p.category else None,
            'author': p.get_author_display(),
            'thumbnail': request.build_absolute_uri(thumb) if thumb else None,
        })

    return JsonResponse({
        'posts': posts_data,
        'page': page,
        'has_next': pager.has_next(),
        'total_pages': paginator.num_pages,
    })


def blog_list(request):
    """Blog listing page with card grid, search, filters, and optional featured layout."""
    tag_slug = request.GET.get('tag')
    category_slug = request.GET.get('category')
    search_q = request.GET.get('q', '').strip()

    qs = BlogPost.objects.filter(status='published').select_related('category', 'author').prefetch_related('tags')

    if tag_slug:
        qs = qs.filter(tags__slug=tag_slug)
    if category_slug:
        qs = qs.filter(category__slug=category_slug)
    if search_q:
        qs = qs.filter(
            Q(title__icontains=search_q) |
            Q(excerpt__icontains=search_q) |
            Q(long_excerpt__icontains=search_q)
        )

    settings = BlogPageSettings.get()
    order = '-date' if settings.default_sort == 'latest' else 'date'
    qs = qs.order_by(order).distinct()

    featured = None
    if settings.enable_featured_layout:
        for p in qs:
            if p.featured:
                featured = p
                break
        if featured is None and qs.exists():
            featured = qs.first()

    if featured:
        qs = qs.exclude(pk=featured.pk)

    paginator = Paginator(qs, settings.posts_per_page)
    page = request.GET.get('page', 1)
    posts = paginator.get_page(page)
    popular_tags = BlogTag.objects.filter(is_popular=True).order_by('order', 'name')
    if popular_tags.exists():
        tags = popular_tags
    else:
        # Fallback: order tags by how many posts use them (reverse M2M name is "blogpost")
        tags = BlogTag.objects.annotate(
            _cnt=Count('blogpost')
        ).order_by('-_cnt', 'order', 'name')[:20]
    authors = BlogAuthor.objects.filter(
        blogpost__status='published'
    ).distinct().order_by('name')

    return render(request, 'blog/list.html', {
        'featured': featured,
        'posts': posts,
        'tags': tags,
        'active_tag': tag_slug,
        'active_tags': tag_slug.split(',') if tag_slug else [],
        'active_category': category_slug,
        'active_author': request.GET.get('author', ''),
        'search_q': search_q,
        'blog_settings': settings,
        'authors': authors,
    })


def blog_detail(request, slug):
    """Blog detail page with rich content sections."""
    post = get_object_or_404(
        BlogPost.objects.filter(status='published').select_related('category', 'author').prefetch_related('tags', 'content_blocks'),
        slug=slug
    )

    # Related: same category or shared tags
    related = BlogPost.objects.filter(status='published').exclude(pk=post.pk)
    if post.category:
        related = related.filter(category=post.category)
    if post.tags.exists():
        tag_ids = list(post.tags.values_list('pk', flat=True))
        related = related.filter(tags__pk__in=tag_ids)
    related = related.distinct()[:3]
    embed_url = request.build_absolute_uri(post.get_absolute_url())
    settings = BlogPageSettings.get()

    return render(request, 'blog/detail.html', {
        'post': post,
        'related': related,
        'embed_url': embed_url,
        'blog_settings': settings,
    })
