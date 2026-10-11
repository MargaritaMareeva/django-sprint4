from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .constants import POSTS_ON_MAIN
from .forms import UserEditForm
from .models import Category, Post

User = get_user_model()


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


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(
        author=profile_user
    ).order_by('-pub_date')
    paginator = Paginator(post_list, POSTS_ON_MAIN)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'profile': profile_user,
        'page_obj': page_obj,
    }
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    form = UserEditForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/user.html', {'form': form})
