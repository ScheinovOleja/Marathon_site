from django.db import models


class CategoryTasks(models.Model):
    category = models.CharField(max_length=50, verbose_name='Категории заданий')

    class Meta:
        db_table = 'category_tasks'


class CategoryTasksMarathon(models.Model):
    category = models.OneToOneField(CategoryTasks, models.DO_NOTHING)
    marathon = models.ForeignKey('Marathon', models.DO_NOTHING)

    class Meta:
        db_table = 'categorytasks_marathon'
        unique_together = (('category', 'marathon'),)


class Marathon(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название марафона')
    description = models.TextField(verbose_name='Описание марафона')
    date_start = models.DateField(verbose_name='Дата начала марафона')
    date_end = models.DateField(verbose_name='Дата окончания марафона')
    send_measurements_before = models.BooleanField(default=False, verbose_name='Отправка замеров ДО')
    send_measurements_after = models.BooleanField(default=False, verbose_name='Отправка замеров ПОСЛЕ')
    close = models.BooleanField(default=False, verbose_name='Закрыт ли марафон')
    price = models.IntegerField(default=0, verbose_name="Стоимость марафона")

    class Meta:
        db_table = 'marathon'


class Measurement(models.Model):
    waist_before = models.FloatField(blank=True, null=True, verbose_name='Отправка замеров груди ДО')
    breast_before = models.FloatField(blank=True, null=True, verbose_name='Отправка замеров талии ДО')
    femur_before = models.FloatField(blank=True, null=True, verbose_name='Отправка замеров бедер ДО')
    weight_before = models.FloatField(blank=True, null=True, verbose_name='Отправка замеров веса ДО')
    waist_after = models.FloatField(blank=True, null=True, verbose_name='Отправка замеров груди ПОСЛЕ')
    breast_after = models.FloatField(blank=True, null=True, verbose_name='Отправка замеров груди ПОСЛЕ')
    femur_after = models.FloatField(blank=True, null=True, verbose_name='Отправка замеров груди ПОСЛЕ')
    weight_after = models.FloatField(blank=True, null=True, verbose_name='Отправка замеров груди ПОСЛЕ')

    class Meta:
        db_table = 'measurement'


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


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название товара')
    description = models.TextField(verbose_name="Описание товара")
    image = models.ImageField(blank=True, upload_to='photo_products/', null=True)
    price = models.IntegerField(verbose_name='Цена товара')
    unique_code = models.TextField(unique=True, verbose_name='Код товара')
    marathon = models.ForeignKey(Marathon, models.DO_NOTHING, verbose_name='Марафон, в котором этот товар')

    class Meta:
        db_table = 'product'


class ProductUsers(models.Model):
    product = models.OneToOneField(Product, models.DO_NOTHING)
    users = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        db_table = 'product_users'
        unique_together = (('product', 'users'),)


class Tasks(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название Задания')
    category = models.ForeignKey(CategoryTasks, models.DO_NOTHING)
    description = models.TextField(verbose_name='Описание задания')
    count_scopes = models.IntegerField(verbose_name='Количество очков за задание')
    url = models.URLField(blank=True, null=True, verbose_name='Ссылка на материалы задания')
    image = models.ImageField(blank=True, upload_to='photo_tasks/', null=True, verbose_name='Фотография задания')
    unique_key = models.TextField()
    marathon = models.ForeignKey(Marathon, models.DO_NOTHING, verbose_name='Марафон, в котором это задание')

    class Meta:
        db_table = 'tasks'


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


class Codes(models.Model):
    code = models.CharField(max_length=20, verbose_name='Код для халявных баллов')
    scopes = models.IntegerField(verbose_name='Количество халявных очков')

    class Meta:
        db_table = 'codes'


class CodesUsers(models.Model):
    codes = models.OneToOneField(Codes, models.DO_NOTHING)
    users = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        db_table = 'codes_users'
        unique_together = (('codes', 'users'),)


class Users(models.Model):
    tg_id = models.IntegerField(verbose_name='Telegram id пользователя')
    username = models.CharField(max_length=100, blank=True, null=True, verbose_name='Telegram id пользователя')
    first_name = models.CharField(max_length=50, verbose_name='Имя пользователя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия пользователя')
    scopes = models.IntegerField(verbose_name='Количество очков пользователя')
    sex = models.CharField(max_length=1, blank=True, null=True, verbose_name='Пол пользователя')
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


class PhotoStates(models.Model):
    class Meta:
        db_table = 'photo_states'

    category_photo = models.CharField(max_length=50, verbose_name='На какую фотографию выдавать эту?'
                                                                  '(спереди, сбоку, сзади)')
    photo = models.ImageField(upload_to='photo_states/', blank=True, null=True, verbose_name='Отправка фото сбоку ДО')


class DayReadyMadeMenu(models.Model):
    day = models.CharField(max_length=50, verbose_name='День меню')
    kcal_category = models.ForeignKey('KcalCategoryReadyMadeMenu', models.DO_NOTHING)

    class Meta:
        db_table = 'day_ready_made'


class KcalCategoryReadyMadeMenu(models.Model):
    kcal_category = models.TextField()

    class Meta:
        db_table = 'kcal_category_ready_made'


class KcalCategoryReadyMadeMenuMarathon(models.Model):
    category = models.OneToOneField(KcalCategoryReadyMadeMenu, models.DO_NOTHING)
    marathon = models.ForeignKey('Marathon', models.DO_NOTHING)

    class Meta:
        db_table = 'kcalcategoryreadymademenu_marathon'
        unique_together = (('category', 'marathon'),)


class ReadyMadeMenu(models.Model):
    name_menu = models.TextField()
    description = models.TextField()
    time_day = models.ForeignKey('TimeDayReadyMadeMenu', models.DO_NOTHING)
    photo = models.ImageField(upload_to='photo_ready_made/', blank=True, null=True, verbose_name='Фотография блюда:')

    class Meta:
        db_table = 'ready_made'


class TimeDayReadyMadeMenu(models.Model):
    time_day = models.TextField()
    day = models.ForeignKey(DayReadyMadeMenu, models.DO_NOTHING)

    class Meta:
        db_table = 'time_day_ready_made'


class CategoryTrainingMenu(models.Model):
    category = models.CharField(max_length=200, default='', null=False, verbose_name='Категория для обучения')

    class Meta:
        db_table = 'category_training'


class CategoryTrainingMenuMarathon(models.Model):
    category = models.OneToOneField(CategoryTrainingMenu, models.DO_NOTHING)
    marathon = models.ForeignKey('Marathon', models.DO_NOTHING)

    class Meta:
        db_table = 'categorytrainingmenu_marathon'
        unique_together = (('category', 'marathon'),)


class TrainingInfo(models.Model):
    name = models.CharField(max_length=100, default='', null=False, verbose_name='Название рецепта обучения')
    description = models.TextField(max_length=5000, default='', null=False, verbose_name='Описание обучения')
    category = models.ForeignKey(CategoryTrainingMenu, models.DO_NOTHING)
    photo = models.ImageField(upload_to='photo_training_menu/', blank=True, null=True, verbose_name='Фотография блюда:')

    class Meta:
        db_table = 'training_info'
