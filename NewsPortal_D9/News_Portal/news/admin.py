from django.contrib import admin

from .models import Author, Category, Post, Comment, PostCategory
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('title', 'author', 'creationDate', 'rating',)
    list_filter = ('rating', 'creationDate', 'title')
    search_fields = ('title',)


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Post, ProductAdmin)
admin.site.register(Comment)

