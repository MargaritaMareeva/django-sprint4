from django.shortcuts import get_object_or_404, render
from .constants import POSTS_ON_MAIN

from .models import Category, Post


def index(request):
    post_list = Post.objects.published().with_related()[:POSTS_ON_MAIN]
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.published().with_related(),
        pk=post_id,
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = category.posts.published().with_related()
    return render(
        request,
        'blog/category.html',
        {'category': category, 'post_list': post_list}
    )
