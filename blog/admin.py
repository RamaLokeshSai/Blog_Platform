from django.contrib import admin
from .models import Post, Category, Comment, Profile

# Post Admin Customization
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on', 'author')
    list_filter = ('status', 'created_on', 'category')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'created_on'
    ordering = ('-created_on',)


# Category Admin Customization
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


# Comment Admin Customization
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('content', 'user__username', 'post__title')


# Profile Admin Customization
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'website')
    search_fields = ('user__username', 'bio')
