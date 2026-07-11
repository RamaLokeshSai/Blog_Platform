from django.urls import path
from . import views

urlpatterns = [
    # Homepage & listings
    path('', views.HomeView.as_view(), name='home'),
    path('category/<slug:slug>/', views.CategoryPostsView.as_view(), name='category_posts'),
    
    # Post CRUD
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # AJAX Interactivity
    path('like/', views.LikePostView.as_view(), name='like_post'),
    path('post/<int:post_id>/comment/', views.AddCommentView.as_view(), name='add_comment'),
    
    # Accounts & Profile
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
]
