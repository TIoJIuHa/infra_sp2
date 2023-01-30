from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Category(models.Model):
    """Категории (типы) произведений"""

    name = models.CharField(max_length=60)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.name} {self.slug}"


class Genre(models.Model):
    """Жанры произведений"""

    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.name} {self.slug}"


class Title(models.Model):
    """Произведения, к которым пишут отзывы"""

    """(определённый фильм, книга или песенка)."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre, through="GenreTitle")
    name = models.CharField(max_length=30)
    year = models.IntegerField()
    description = models.TextField(max_length=250, blank=True)


class GenreTitle(models.Model):
    """Вспомогательный класс для модели Title"""

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.genre}"


class Review(models.Model):
    """Отзывы к произведениям"""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )
    text = models.TextField("Текст отзыва")
    score = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1, f"Минимальная оценка {1}"),
            MaxValueValidator(10, f"Максимальная оценка {10}"),
        ],
    )
    pub_date = models.DateTimeField("Дата", auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_review"
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Комментарии к отзывам"""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField("Текст комментария")
    pub_date = models.DateTimeField("Дата", auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text
