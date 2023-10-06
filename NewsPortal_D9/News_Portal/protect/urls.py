from django.urls import path
from .views import IndexView
import news
from news.views import NewsList, NewsDetail, Search, NewsEdit, NewsDelete, ArticleCreate, ArticleEdit, ArticleDelete,\
    CategoryListView, subscribe, CategoryList

from django.views.decorators.cache import cache_page

app_name = 'news'

urlpatterns = [

    path('', IndexView.as_view()),

    path('', news.views.Start_Padge, name='Start'),  # URL-шаблон Стартовой страницы

    path('search/', Search.as_view(), name='search'),  # URL-шаблон Поисковой страницы

    path('news/', NewsList.as_view(), name='news_list'),  # URL-шаблон для списка новостей

    path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),  # URL-шаблон для списка новостей

    path('article/', news.views.article_list, name='article_list'),  # URL-шаблон для списка статей

    path('articles/<int:post_id>/', news.views.article_detail, name='article_detail'),  # URL-шаблон для статьи

    path('news/create/', news.views.NewsCreate.as_view(), name='news_create'),  # URL-шаблон для создания новостей

    path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),  # URL-шаблон для редактирования новостей

    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),  # URL-шаблон для удаления новостей

    path('articles/create/', news.views.ArticleCreate.as_view(), name='articles_create'),  # URL-шаблон для создания статьи

    path('articles/<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),  # URL-шаблон для редактирования статьи

    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),  # URL-шаблон для удаления статьи

    path('news/category/', CategoryList.as_view(), name='categories'),

    path('news/category/<int:pk>/', CategoryListView.as_view(), name='category_list'),

    path('news/category/<int:pk>/subscribe/', subscribe, name='subscribe'),
]