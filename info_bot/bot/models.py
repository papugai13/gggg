from django.db import models
from django import utils


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название категории",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="sub_category"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название подкатегории"
    )
    text = models.TextField(
        null=True,
        blank=True
    )
    file = models.FileField(
        verbose_name="Ваш файл",
        upload_to="files/%Y/%m/%d/",
        null=True,
        blank=True
    )
    image = models.ImageField(
        verbose_name='Фото',
        upload_to='img/%Y/%m/%d/',
        null=True,
        blank=True
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
        verbose_name='Родительская категория'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок отображения"
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ['order']


class User(models.Model):
    tg_id = models.CharField(
        primary_key=True,
        max_length=100,
        verbose_name='Телеграмм id'
    )
    user_name = models.CharField(
        max_length=100,
        verbose_name="Имя"
    )
    number = models.CharField(
        max_length=100,
        verbose_name="Номер телефона"
    )
    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"



class OrganisationCategory(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название категории'
    )
    def __str__(self) -> str:
        return self.name
    class Meta:
        verbose_name = "Категории организации"
        verbose_name_plural = "Категории организаций"



class Organisation(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название организации"
    )
    description = models.CharField(
        max_length=500,
        verbose_name="Описание"
    )
    category = models.ForeignKey(
        OrganisationCategory,
        on_delete=models.CASCADE,
        related_name="Organisation"
    )
    def __str__(self) -> str:
        return self.name
    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Оргагизации"




