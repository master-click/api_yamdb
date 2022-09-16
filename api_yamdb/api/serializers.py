from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre


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


class TitleSerializer(serializers.ModelSerializer):
    # еще пагинация здесь!
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(read_only=True, many=True)  # проверки должны быть
    category = CategorySerializer(read_only=True, many=False)  # не так,
    # валидации должны быть

    def get_rating(self, title):
        rating = title.reviews.aggregate(Avg('score')).get('score__avg')
        # генерится словарь и мы берем его элемент
        # для списка может лучше annotate сделать - экономия запросов?
        return rating

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        required_fields = ('name', 'year', 'genre', 'category')


class TitleGenreSerializer(serializers.ModelSerializer):
    title = SlugRelatedField(slug_field='title',
                             queryset=Review.objects.all())
    genre = SlugRelatedField(slug_field='slug',
                             queryset=Genre.objects.all())
    validators = [UniqueTogetherValidator(queryset=TitleGenre.objects.all(),
                                          fields=('title', 'genre'))]
