from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre


User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username',
                              read_only=True,
                              default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')  # без review
        required_fields = ('text',)


class ReviewSerializer(serializers.ModelSerializer):

    author = SlugRelatedField(slug_field='username',
                              read_only=True,
                              default=serializers.CurrentUserDefault())

    def validate(self, data):
        request = self.context.get("request")
        if request.method != 'POST':
            return data
        title_id = int(self.context['view'].kwargs.get('title_id'))
        author = request.user
        if Review.objects.filter(title=title_id, author=author).exists():
            raise serializers.ValidationError(
                'Нельзя создавать больше 1 отзыва на произведение'
            )
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        required_fields = ('text', 'score')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        required_fields = ('name', 'slug')
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        required_fields = ('name', 'slug')
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class TitleGenreSerializer(serializers.ModelSerializer):
    title = SlugRelatedField(slug_field='title',
                             queryset=Review.objects.all())
    genre = SlugRelatedField(slug_field='slug',
                             queryset=Genre.objects.all())
    validators = [UniqueTogetherValidator(queryset=TitleGenre.objects.all(),
                                          fields=('title', 'genre'))]


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(default=0, read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer(many=False)

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score')).get('score__avg')
        return rating

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(many=True, slug_field='slug',
                             queryset=Genre.objects.all())
    category = SlugRelatedField(many=False, slug_field='slug',
                                queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category')
        required_fields = ('name', 'year', 'genre', 'category')

    def to_representation(self, instance):
        response = super().to_representation(instance)  # доразобраться
        response['category'] = CategorySerializer(instance.category).data
        for entry in instance.genre.all():
            genre = GenreSerializer(entry).data
            response['genre'].append(genre)
        return response
