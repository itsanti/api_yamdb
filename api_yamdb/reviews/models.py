from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField('Категория', max_length=256)

    slug = models.SlugField(
        unique=True,
        verbose_name='slug'
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=256)

    slug = models.SlugField(
        unique=True,
        verbose_name='slug'
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Произведение', max_length=256)

    year = models.PositiveSmallIntegerField('Дата выхода')

    description = models.TextField(
        'Описание',
        blank=True,
        null=True,
    )

    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField('Текст отзыва')

    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=(MinValueValidator(1), MaxValueValidator(10))
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='one_review_per_title'
            ),
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField('Текст комментария')

    pub_date = models.DateTimeField(
        'Дата добавления комментария', auto_now_add=True,
    )

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='comments',
        verbose_name='Отзыв'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
