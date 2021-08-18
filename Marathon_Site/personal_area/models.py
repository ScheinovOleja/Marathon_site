import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Manager

from personal_area.validators import validate_date, validate_price


class MyManager(Manager):

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class CategoryTasks(models.Model):
    category = models.CharField(max_length=50, verbose_name='Категория задания')

    class Meta:
        db_table = 'category_tasks'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return f'{self.category}'


class CategoryTasksMarathon(models.Model):
    category = models.OneToOneField(CategoryTasks, models.DO_NOTHING)
    marathon = models.ForeignKey('Marathon', models.DO_NOTHING)

    class Meta:
        db_table = 'categorytasks_marathon'
        unique_together = (('category', 'marathon'),)

    def __str__(self):
        return f'{self.category} {self.marathon}'


class Tasks(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название задания')
    category = models.ForeignKey(CategoryTasks, models.DO_NOTHING, verbose_name='Категория задания')
    description = models.TextField(max_length=1000, verbose_name='Описание задания')
    count_scopes = models.IntegerField(verbose_name='Количество очков за задание')
    image = models.ImageField(blank=True, upload_to='photo_tasks/', null=True, verbose_name='Фотография задания')
    date_start = models.DateTimeField(auto_created=datetime.datetime.now(), null=False,
                                      verbose_name='Дата открытия задания')
    date_stop = models.DateTimeField(auto_created=datetime.datetime.now(), null=False,
                                     verbose_name='Дата закрытия задания')

    class Meta:
        db_table = 'tasks'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return f'{self.id} - {self.name}'


class Marathon(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название марафона')
    description = models.TextField(verbose_name='Описание марафона')
    date_start = models.DateField(verbose_name='Дата начала марафона', )
    date_end = models.DateField(validators=[validate_date], verbose_name='Дата окончания марафона')
    send_measurements_before = models.BooleanField(default=False, verbose_name='Отправка замеров ДО')
    send_measurements_after = models.BooleanField(default=False, verbose_name='Отправка замеров ПОСЛЕ')
    close = models.BooleanField(default=False, verbose_name='Закрыт ли марафон')
    price = models.IntegerField(default=0, validators=[validate_price], verbose_name="Стоимость марафона")

    class Meta:
        db_table = 'marathon'
        verbose_name_plural = 'Марафон'

    def __str__(self):
        return f'{self.name}'


class Measurement(models.Model):
    waist_after = models.FloatField(blank=True, null=True, verbose_name='Отправка замеров груди ДО')
    breast_after = models.FloatField(blank=True, null=True, verbose_name='Отправка замеров груди ДО')
    femur_after = models.FloatField(blank=True, null=True, verbose_name='Отправка замеров груди ДО')
    weight_after = models.FloatField(blank=True, null=True, verbose_name='Отправка замеров груди ДО')
    waist_before = models.FloatField(blank=True, null=True, verbose_name='Отправка замеров груди ПОСЛЕ')
    breast_before = models.FloatField(blank=True, null=True, verbose_name='Отправка замеров талии ПОСЛЕ')
    femur_before = models.FloatField(blank=True, null=True, verbose_name='Отправка замеров бедер ПОСЛЕ')
    weight_before = models.FloatField(blank=True, null=True, verbose_name='Отправка замеров веса ПОСЛЕ')

    class Meta:
        db_table = 'measurement'
        verbose_name_plural = 'Замеры пользователей'


class Photo(models.Model):
    photo_front_before = models.ImageField(upload_to="users_photo/", blank=True, null=True,
                                           verbose_name='Отправка фото спереди ДО')
    photo_sideways_before = models.ImageField(upload_to="users_photo/", blank=True, null=True,
                                              verbose_name='Отправка фото сбоку ДО')
    photo_back_before = models.ImageField(upload_to="users_photo/", blank=True, null=True,
                                          verbose_name='Отправка фото сзади ДО')
    photo_front_after = models.ImageField(upload_to="users_photo/", blank=True, null=True,
                                          verbose_name='Отправка фото спереди ПОСЛЕ')
    photo_sideways_after = models.ImageField(upload_to="users_photo/", blank=True, null=True,
                                             verbose_name='Отправка фото сбоку ПОСЛЕ')
    photo_back_after = models.ImageField(upload_to="users_photo/", blank=True, null=True,
                                         verbose_name='Отправка фото сзади ПОСЛЕ')

    class Meta:
        db_table = 'photo'
        verbose_name_plural = 'Фотографии пользователей'


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название приза')
    description = models.TextField(verbose_name="Описание приза")
    image = models.ImageField(blank=True, upload_to='photo_products/', null=True, verbose_name='Фото приза')
    marathon = models.ForeignKey(Marathon, models.DO_NOTHING, verbose_name='Марафон, в котором этот товар')

    class Meta:
        db_table = 'product'
        verbose_name_plural = 'Призы(бывшие товары)'

    def __str__(self):
        return f'{self.id} - {self.name}'


class ProductUsers(models.Model):
    product = models.OneToOneField(Product, models.DO_NOTHING)
    users = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        db_table = 'product_users'
        unique_together = (('product', 'users'),)


class TasksUsers(models.Model):
    tasks = models.OneToOneField(Tasks, models.DO_NOTHING)
    users = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        db_table = 'tasks_users'
        unique_together = (('tasks', 'users'),)


class BZUUsers(models.Model):
    proteins = models.IntegerField()
    fats = models.IntegerField()
    carbohydrates = models.IntegerField()

    class Meta:
        db_table = 'bzu_users'
        verbose_name_plural = 'БЖУ пользователей'


class Codes(models.Model):
    code = models.CharField(max_length=20, verbose_name='Код для халявных баллов')
    scopes = models.IntegerField(verbose_name='Количество халявных очков')
    marathon = models.ForeignKey(Marathon, models.DO_NOTHING, verbose_name='Марафон, в котором находится код')

    class Meta:
        db_table = 'codes'
        verbose_name_plural = 'Коды'

    def __str__(self):
        return f'{self.code} - {self.scopes}'


class CodesUsers(models.Model):
    codes = models.OneToOneField(Codes, models.DO_NOTHING)
    users = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        db_table = 'codes_users'
        unique_together = (('codes', 'users'),)


class Users(models.Model):
    objects = MyManager()

    GENDERS = [
        ("m", "M"),
        ("w", "W")
    ]

    tg_id = models.IntegerField(verbose_name='Telegram id пользователя')
    username = models.CharField(max_length=100, blank=True, null=True, verbose_name='Telegram id пользователя')
    first_name = models.CharField(max_length=50, verbose_name='Имя пользователя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия пользователя')
    scopes = models.IntegerField(verbose_name='Количество очков пользователя')
    sex = models.CharField(max_length=1, blank=True, null=True, verbose_name='Пол пользователя', choices=GENDERS)
    age = models.IntegerField(default=0, null=True)
    weight = models.IntegerField(default=0, null=True)
    height = models.IntegerField(default=0, null=True)
    purpose = models.CharField(default='', max_length=1, null=True)
    kcal = models.IntegerField(default=0, null=True)
    is_enter_invite_code = models.BooleanField(blank=True, null=True, verbose_name='Ввел ли пригласительный код?')
    marathon = models.ForeignKey(Marathon, models.DO_NOTHING, verbose_name='Марафон пользователя')
    measurement = models.ForeignKey(Measurement, models.DO_NOTHING, blank=True, null=True)
    photos = models.ForeignKey(Photo, models.DO_NOTHING, blank=True, null=True)
    bzu = models.ForeignKey(BZUUsers, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'users'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.tg_id} - {self.last_name} {self.first_name}'


class PhotoStates(models.Model):
    class Meta:
        db_table = 'photo_states'
        verbose_name_plural = 'Примеры фотографий'
        verbose_name = 'Категория фотографии'

    CATEGORIES = [
        ("front", "Спереди"),
        ("sideways", "Сбоку"),
        ("back", "Сзади"),
    ]

    category_photo = models.CharField(max_length=50, verbose_name='На какую фотографию выдавать эту?',
                                      choices=CATEGORIES)
    photo = models.ImageField(upload_to='photo_states/', blank=True, null=True, verbose_name='Отправка фото сбоку ДО')

    def __str__(self):
        return f'{self.category_photo}'


class KcalCategoryReadyMadeMenu(models.Model):
    kcal_category = models.CharField(max_length=50, verbose_name='Количество калорий на готовое меню')

    class Meta:
        db_table = 'kcal_category_ready_made'
        verbose_name_plural = 'Категории готовых меню'

    def __str__(self):
        return f'{self.kcal_category}'


class KcalCategoryReadyMadeMenuMarathon(models.Model):
    category = models.OneToOneField(KcalCategoryReadyMadeMenu, models.DO_NOTHING,
                                    verbose_name='Категория готового меню')
    marathon = models.ForeignKey('Marathon', models.DO_NOTHING, verbose_name='Марафон, в котором эта категория')

    class Meta:
        db_table = 'kcalcategoryreadymademenu_marathon'
        verbose_name = ' Категории готовых меню'
        unique_together = (('category', 'marathon'),)

    def __str__(self):
        return f'{self.category} - {self.marathon}'


class DayReadyMadeMenu(models.Model):
    day = models.CharField(max_length=50, verbose_name='День готового меню')
    kcal_category = models.ForeignKey('KcalCategoryReadyMadeMenu', models.DO_NOTHING,
                                      verbose_name='ККАЛ готового меню')

    class Meta:
        db_table = 'day_ready_made'
        verbose_name_plural = 'Дни готовых меню'

    def __str__(self):
        return f'{self.day} - {self.kcal_category} - {self.kcal_category.kcalcategoryreadymademenumarathon.marathon.name}'


class TimeDayReadyMadeMenu(models.Model):
    time_day = models.CharField(max_length=50, verbose_name='Время дня')
    day = models.ForeignKey(DayReadyMadeMenu, models.DO_NOTHING, verbose_name='День')

    class Meta:
        db_table = 'time_day_ready_made'
        verbose_name_plural = '  Готовые меню'

    def __str__(self):
        return f'{self.time_day} - {self.day}'


class ReadyMadeMenu(models.Model):
    name_menu = models.CharField(max_length=50, verbose_name='Название меню')
    description = models.TextField(verbose_name='Описание меню')
    time_day = models.ForeignKey('TimeDayReadyMadeMenu', models.DO_NOTHING, verbose_name='Время дня меню')
    photo = models.ImageField(upload_to='photo_ready_made/', blank=True, null=True, verbose_name='Фотография блюда:')

    class Meta:
        db_table = 'ready_made'
        verbose_name_plural = 'Готовые меню'
        verbose_name = 'Готовые меню'

    def __str__(self):
        return f'{self.name_menu}'


class CategoryTrainingMenu(models.Model):
    category = models.CharField(max_length=200, default='', null=False, verbose_name='Категория для обучения')

    class Meta:
        db_table = 'category_training'
        verbose_name_plural = 'Обучение составления меню'

    def __str__(self):
        return f'{self.category}'


class CategoryTrainingMenuMarathon(models.Model):
    category = models.OneToOneField(CategoryTrainingMenu, models.DO_NOTHING, verbose_name='Категория меню для обучения')
    marathon = models.ForeignKey('Marathon', models.DO_NOTHING, verbose_name='Марафон, в котором эта категория')

    class Meta:
        verbose_name = 'Категории в составлении меню'
        db_table = 'categorytrainingmenu_marathon'
        unique_together = (('category', 'marathon'),)

    def __str__(self):
        return f'{self.category} - {self.marathon}'


class TrainingInfo(models.Model):
    name = models.CharField(max_length=100, default='', null=False, verbose_name='Название рецепта обучения')
    description = models.TextField(max_length=5000, default='', null=False, verbose_name='Описание обучения')
    category = models.ForeignKey(CategoryTrainingMenu, models.DO_NOTHING, verbose_name='Категория обучающего меню')
    photo = models.ImageField(upload_to='photo_training_menu/', blank=True, null=True, verbose_name='Фотография блюда:')

    class Meta:
        db_table = 'training_info'
        verbose_name_plural = 'Обучение составления меню'

    def __str__(self):
        return f'{self.name}'
