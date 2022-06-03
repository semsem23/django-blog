from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm, CommentForm
from .models import User, Post, Comment, Author, Category, Like

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'username', 'is_admin', 'is_active', 'date_joined', 'last_login',)
    list_filter = ('is_admin',)
    fieldsets = ((None, {'fields': ('email', 'password','date_joined', 'last_login',)}),
     ('Personal info', {'fields': ('username',)}),
     ('Permissions', {'fields': ('is_admin',)}),)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publishedDate'
    ordering       = ('-publishedDate',)
    list_display = ('title', 'publishedDate', 'category', 'author',  ) 
    
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content',  'post', 'createdDate', 'active',)
    list_filter = ('createdDate',)
    search_fields = ('content',)
    actions = ['active']
    


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    

admin.site.register(Comment, CommentAdmin) 
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Like)
admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)