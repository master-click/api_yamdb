from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import IntegrityError, models

User = get_user_model() # поменять!


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField(validators=[
        MaxValueValidator(datetime.now().year)])
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="titles", blank=True, null=True)
    genre = models.ManyToManyField(
        Genre, through='TitleGenre')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}, жанр - {self.genre}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["title", "genre"],
                                    name='unique_genre')
        ]

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

    def unique_review(self):
        if Review.objects.filter(title=self.title, author=self.author).exists():
            raise IntegrityError(
                'нельзя создавать два отзывы на одно произведения')

    def save(self, *args, **kwargs):  # надо ли?
        if Review.objects.filter(pk=self.pk).exists():
            return super().save(*args, **kwargs)
        self.unique_review()
        return super().save(*args, **kwargs)


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
        ordering = ['pub_date']
