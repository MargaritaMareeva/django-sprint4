from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from .constants import POSTS_ON_PAGE
from .forms import UserEditForm
from .models import Category, Post

User = get_user_model()


class PaginatedListView(ListView):
    paginate_by = POSTS_ON_PAGE


class PostListView(PaginatedListView):
    model = Post
    template_name = 'blog/index.html'
    queryset = Post.objects.published().with_related()


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_queryset(self):
        return Post.objects.published().with_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        return context


class CategoryPostListView(PaginatedListView):
    model = Post
    template_name = 'blog/category.html'

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return self.category.posts.published().with_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ProfileListView(PaginatedListView):
    model = Post
    template_name = 'blog/profile.html'

    def get_queryset(self):
        self.profile_user = get_object_or_404(
            User,
            username=self.kwargs['username']
        )
        return Post.objects.filter(
            author=self.profile_user
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile_user
        return context


@login_required
def edit_profile(request):
    form = UserEditForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/user.html', {'form': form})
