from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

STR_TEXT_LEN = 15


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок',
    )
    slug = models.SlugField(
        max_length=200, unique=True,
        verbose_name='Идентификатор',
    )
    description = models.TextField(verbose_name='Описание',)

    class Meta:
        verbose_name_plural = 'Сообщества'
        verbose_name = 'Сообщество'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст поста',
        help_text='Введите текст поста',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User, verbose_name='Автор',
        on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Сообщество',
        help_text='Сообщество, к которому будет относиться пост',
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='posts/', null=True, blank=True)

    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'
        default_related_name = 'posts'

    def __str__(self):
        return self.text[:self.STR_TEXT_LEN]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост'
    )
    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Напишите ваши мысли, по поводу поста (будьте вежливы)',
    )
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        default_related_name = 'comments'

    def __str__(self):
        return self.text[:self.STR_TEXT_LEN]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follower'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='following'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'], name='unique_user_author',
            ),
        ]
        verbose_name_plural = 'Подписки'
        verbose_name = 'Подписка'

    def __str__(self):
        return f'{self.user} подписался на публикации {self.following}'
