from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre

from rest_framework import serializers

from reviews.models import Title, Genre, Category

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User
from .validators import validate_username, validate_email




class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username',
                              read_only=True,
                              default=serializers.CurrentUserDefault())
    review = serializers.PrimaryKeyRelatedField(
        read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')  # без review
        required_fields = ('text',)


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.PrimaryKeyRelatedField(
        read_only=True)
    author = SlugRelatedField(slug_field='username',
                              read_only=True,
                              default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')  # без title
        validators = [
            UniqueTogetherValidator(queryset=Review.objects.all(),
                                    fields=('author', 'title')),
        ]
        # проверить как работает валидация
        required_fields = ('text', 'score')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
        required_fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'
        required_fields = ('name', 'slug')


class TitleGenreSerializer(serializers.ModelSerializer):
    title = SlugRelatedField(slug_field='title',
                             queryset=Review.objects.all())
    genre = SlugRelatedField(slug_field='slug',
                             queryset=Genre.objects.all())   # список - many=True
    validators = [UniqueTogetherValidator(queryset=TitleGenre.objects.all(),
                                          fields=('title', 'genre'))]
                                          
                                    
class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    def get_rating(self, title):
        rating = title.reviews.aggregate(Avg('score')).get('score__avg')
        return rating

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        required_fields = ('name', 'year', 'genre', 'category')    


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор получения токена"""
    confirmation_code = serializers.CharField(allow_blank=False)
    username = serializers.CharField(max_length=64, allow_blank=False)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        confirmation_code = default_token_generator.make_token(user)
        if str(confirmation_code) != data['confirmation_code']:
            raise ValidationError('Неверный код подтверждения!')
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей"""
    email = serializers.EmailField(max_length=64, allow_blank=False,
                                   validators=[validate_email])
    username = serializers.CharField(max_length=64, allow_blank=False,
                                     validators=[validate_username])

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'bio', 'role')


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор процедуры регистрации"""
    email = serializers.EmailField(max_length=64, allow_blank=False,
                                   validators=[validate_email])
    username = serializers.CharField(max_length=64, allow_blank=False,
                                     validators=[validate_username])

    class Meta:
        model = User
        fields = ('email', 'username')
