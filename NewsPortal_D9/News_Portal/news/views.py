from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required

from .filters import PostFilter
from .forms import NewsForm, ArticleForm
from .models import Post, Category, PostCategory

from django.http import HttpResponse
from django.views import View
from .tasks import send_notifications

"""
get_object_or_404 - используется для получения объекта из базы данных по заданным условиям. 
Если объект не найден, то функция вызывает исключение `Http404`, и возвращает страницу с ошибкой 404.
"""


# ====== Стартовая страница ============================================================================================
def Start_Padge(request):
    posts = Post.objects.filter(type='NW').order_by('-creationDate')[:4]
    return render(request, 'flatpages/Start.html', {'posts': posts})


# ====== Новости =======================================================================================================
class NewsList(ListView):
    paginate_by = 4
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset().filter(type='NW')
        return queryset.order_by('-creationDate')


class NewsDetail(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'post'


class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Post
    form_class = NewsForm
    template_name = 'news_create.html'
    success_url = '/'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NW'
        post.author = self.request.user.author
        post.save()
        send_notifications.delay(post.pk)
        return super().form_valid(form)


class NewsEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = NewsForm
    template_name = 'news_edit.html'
    success_url = '/'
    permission_required = ('news.change_post',)


class NewsDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = '/'
    permission_required = ('news.delete_post',)


class CategoryList(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categories'
#
#
# class CategoryDetail(DetailView):
#     model = Category
#     template_name = 'category_detail.html'
#     context_object_name = 'category'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         category_object = self.object.id
#         context['post'] = Post.objects.filter(postCategory=category_object)
#         return context


# ====== Статьи ========================================================================================================
def article_list(request):
    article = Post.objects.filter(type='AR').order_by('-creationDate')  # Фильтруем только статьи
    # и сортируем по убыванию даты
    paginator = Paginator(article, 1)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, 'news/article_list.html', {'articles': articles})


def article_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'news/article_detail.html', {'post': post})


class ArticleCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Post
    form_class = ArticleForm
    template_name = 'article_create.html'
    success_url = '/'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AR'
        post.author = self.request.user.author
        post.save()
        return super().form_valid(form)


class ArticleEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = ArticleForm
    template_name = 'article_edit.html'
    success_url = '/'
    permission_required = ('news.change_post',
                           'news.add_post')


class ArticleDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = '/'
    permission_required = ('news.delete_post',)


# ====== Поиск =========================================================================================================
class Search(ListView):
    model = Post
    template_name = 'flatpages/search.html'
    context_object_name = 'search'
    filterset_class = PostFilter
    paginate_by = 7

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['categories'] = Category.objects.all()  # Получение всех категорий
        return context


# def subscribe_to_category(request, pk):
#     category = get_object_or_404(Category, pk=pk)
#     if request.user.is_authenticated:
#         category.subscribers.add(request.user)
#     return redirect('posts_of_categories_list', pk=pk)
#
#
# def send_news_notification(user_email, category, news):
#     subject = f"Новая статья в категории {category}"
#     html_message = render_to_string('email/notification.html',
#                                     {'category': category, 'news': news})
#     plain_message = strip_tags(html_message)
#     send_mail(subject, plain_message, 'your_email@example.com',
#               [user_email], html_message=html_message)


class CategoryListView(NewsList):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.category).order_by('-creationDate')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку'
    return render(request, 'subscribe.html', {'category': category, 'message': message})
