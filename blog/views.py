from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Post, Category, Comment, Profile
from .forms import UserSignupForm, UserUpdateForm, ProfileUpdateForm, PostForm, CommentForm


# Post List View (Homepage)
class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = Post.objects.filter(status='published')
        query = self.request.GET.get('q')
        category_slug = self.request.GET.get('category')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(author__username__icontains=query)
            )
        
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Remove featured post from general listing on page 1 of home to avoid duplication
        featured_post = Post.objects.filter(status='published').first()
        if featured_post and not self.request.GET.get('page') and not query and not category_slug:
            queryset = queryset.exclude(id=featured_post.id)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        context['search_query'] = self.request.GET.get('q', '')
        # Get featured post (the latest published post)
        published_posts = Post.objects.filter(status='published')
        context['featured_post'] = published_posts.first() if published_posts.exists() else None
        return context


# Post Detail View
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        # Check if current user liked the post
        context['user_has_liked'] = False
        if self.request.user.is_authenticated:
            context['user_has_liked'] = self.object.likes.filter(id=self.request.user.id).exists()
        return context


# Post Create View
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully!")
        return super().form_valid(form)


# Post Update View
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully!")
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# Post Delete View
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Post deleted successfully!")
        return super().delete(request, *args, **kwargs)


# Category Post List View
class CategoryPostsView(ListView):
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(category=self.category, status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        return context


# AJAX Like Post View
class LikePostView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
            
        return JsonResponse({
            'liked': liked,
            'total_likes': post.total_likes
        })


# AJAX Comment Submission View
class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()

            avatar_url = '/static/images/default-avatar.png'
            if request.user.profile.avatar:
                avatar_url = request.user.profile.avatar.url

            return JsonResponse({
                'status': 'success',
                'comment_id': comment.id,
                'username': comment.user.username,
                'avatar_url': avatar_url,
                'content': comment.content,
                'created_on': comment.created_on.strftime('%b %d, %Y, %I:%M %p')
            })
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


# Signup View
class SignupView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = UserSignupForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to the Blog, {user.username}! Your account has been created.")
            return redirect('home')
        return render(request, 'registration/signup.html', {'form': form})


# Profile View (details + editing user profile)
@login_required
def profile_view(request, username=None):
    if username is None:
        user = request.user
    else:
        user = get_object_or_404(User, username=username)

    posts = Post.objects.filter(author=user)
    # If viewing someone else's profile, show only published posts
    if user != request.user:
        posts = posts.filter(status='published')

    if request.method == 'POST' and user == request.user:
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.profile)

    context = {
        'profile_user': user,
        'posts': posts,
        'u_form': u_form,
        'p_form': p_form,
        'is_own_profile': (user == request.user)
    }
    return render(request, 'blog/profile.html', context)
