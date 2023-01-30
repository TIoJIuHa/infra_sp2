import datetime as dt

from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")
        lookup_field = "slug"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")
        lookup_field = "slug"


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(default=0)

    class Meta:
        fields = '__all__'
        model = Title
        read_only_fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )


class TitlePostSerialzier(TitleSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    rating = serializers.IntegerField(required=False)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        model = Title

    def validate_date(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                "Год не может быть больше текущего"
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ("title",)

    def validate(self, data):
        if self.context["request"].method == "POST":
            if Review.objects.filter(
                author=self.context["request"].user,
                title=self.context["view"].kwargs.get("title_id"),
            ).exists():
                raise serializers.ValidationError(
                    "Нельзя оставить отзыв на одно произведение дважды"
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        fields = "__all__"
        model = Comment
        read_only_fields = ("review",)
