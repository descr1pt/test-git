from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Author(models.Model):
    rating = models.IntegerField(default = 1)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name = 'Имя')

    def update_rating(self):
        rating_of_post_by_author = Post.objects.filter(author=self).aggregate(Sum('rating'))['rating__sum'] * 3
        rating_of_comments_by_author = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum']
        rating_of_comments_under_post_of_author = Comment.objects.filter(post__author__user=self.user).aggregate(Sum('rating'))['rating__sum']

        self.rating = rating_of_post_by_author + rating_of_comments_by_author + rating_of_comments_under_post_of_author
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length = 255, unique = True)


class Post(models.Model):
    news = 'NE'
    article = 'AR'

    POST_TYPES = [
        (news, 'Новость'),
        (article, 'Статья'),
    ]
    time_in = models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения')
    title = models.CharField(max_length = 255, default = 'Some Title', verbose_name='Заголовок')
    text = models.CharField(max_length = 2048, default = 'Some Text', verbose_name='Контент')
    rating = models.IntegerField(default = 0)
    news_or_post = models.CharField(max_length=2, choices=POST_TYPES, default=article, verbose_name='Вид поста')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    categories = models.ManyToManyField(Category, through='PostCategory')

    def preview(self):
        a = self.text
        new_a = a[:124]
        return new_a + '...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.title}: {self.author.user.username}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.CharField(max_length = 255, default = 'Some Comm', verbose_name='Комментарий')
    time_in = models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения')
    rating = models.IntegerField(default = 0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
