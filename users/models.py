from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from lms.models import Course, Lesson


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Создать и вернуть пользователя с email и паролем."""
        if not email:
            raise ValueError('У пользователя должен быть email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создать и вернуть суперпользователя с email и паролем."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=30, verbose_name="Имя", blank=True, null=True)
    last_name = models.CharField(max_length=30, verbose_name="Фамилия", blank=True, null=True)

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Введите email"
    )
    phone = models.CharField(
        max_length=35, verbose_name="Телефон", help_text="Введите телефон", **NULLABLE
    )
    city = models.CharField(
        max_length=100,
        verbose_name="Город",
        help_text="Введите город проживания",
        **NULLABLE
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        help_text="Загрузите аватар",
        **NULLABLE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    course = models.ForeignKey(
        Course, verbose_name="Курс", on_delete=models.CASCADE, blank=True, null=True
    )
    lesson = models.ForeignKey(
        Lesson,
        verbose_name="Урок",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    total_price = models.FloatField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(max_length=50, verbose_name="Способ оплаты")

    def __str__(self):
        return (
            f"{self.user} - {self.course if self.course else self.lesson} = "
            f"{self.total_price}$"
        )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"