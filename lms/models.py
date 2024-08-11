from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    name_course = models.CharField(
        max_length=150,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="materials/preview ",
        verbose_name="Превью",
        help_text="Загрузить превью",
        **NULLABLE,
    )
    description = models.TextField(verbose_name="Описание", **NULLABLE)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return f"{self.name_course}"


class Lesson(models.Model):
    name_ln = models.CharField(
        max_length=150,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    preview = models.ImageField(
        upload_to="materials/preview ",
        verbose_name="Превью",
        help_text="Загрузить превью",
        **NULLABLE,
    )
    link_video = models.FileField(
        upload_to="materials/video",
        verbose_name="Видео",
        help_text="Добавьте ссылку на видео",
        **NULLABLE,
    )
    name_course = models.ForeignKey(
        Course,
        verbose_name="Курс",
        related_name="Урок",
        on_delete=models.CASCADE,
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

        def __str__(self):
            return f"Урок {self.name_ln} из курса {self.name_course}"