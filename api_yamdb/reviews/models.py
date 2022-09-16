from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)
    # реализовать ^[-a-zA-Z0-9_]+$


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(validators=[
        MaxValueValidator(datetime.now().year)])
    description = models.TextField()
    genre = models.ManyToManyField(Genre,
                                   related_name='titles',
                                   through='TitleGenre')
    # through здесь необязательно?
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='titles')


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(validators=[
        MaxValueValidator(10), MinValueValidator(1)])
    # можно default=10, но не нужно  валидация!
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):   # на всякий случай
        return self.text

    class Meta:
        constraints = [models.UniqueConstraint(fields=["author", "title"],
                       name='unique_review')]
        # только один отзыв на title на одно произведение
        ordering = ['-pub_date']
    # required - text, score


class Comment(models.Model):
    text = models.TextField()
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='follower',)
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name='following',)

    def __str__(self):
        return f'{self.title} {self.genre}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["title", "genre"],
                                    name='unique_genre')
        ]
