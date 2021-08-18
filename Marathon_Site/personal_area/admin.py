import csv
import logging
import os
from pathlib import Path

from django.contrib import admin
from django.core.files import File
from django.forms import TextInput, Textarea
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from .models import *


# Register your models here.


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    model = Users
    actions = ['import_csv']
    search_fields = ['username', 'first_name', 'last_name']
    list_filter = ['sex', 'marathon__name']
    list_display = ['tg_id', 'username', 'first_name', 'last_name', 'marathon']
    fields = ['username', ('first_name', 'last_name'), 'sex', 'scopes', 'marathon', ('complete_task', 'get_photo',
                                                                                     'get_measurement', 'get_bzu')]
    readonly_fields = ['complete_task', 'get_photo', 'get_measurement', 'get_bzu', 'marathon', 'sex', 'username']
    list_display_links = ['tg_id', 'marathon']

    def import_csv(self, request, queryset):
        try:
            file_path = f"{Path(__file__).resolve().parent.parent}/media/csv_files"
            if not os.path.isdir(file_path):
                os.mkdir(file_path)
            with open(f'{file_path}/file_csv.csv', 'w', encoding='utf-8') as csv_file:
                data = [['tg_id', 'tg_nickname', 'Имя', 'Фамилия', 'Возраст', 'Пол', 'Кол-во баллов', 'Грудь ДО',
                         'Талия ДО', 'Бедра ДО', 'Вес ДО', 'Грудь ПОСЛЕ', 'Талия ПОСЛЕ', 'Бедра ПОСЛЕ', 'Вес ПОСЛЕ']]
                for user in queryset:
                    writer = csv.writer(csv_file, delimiter=';')
                    if not user.measurement:
                        continue
                    data.append([user.tg_id, user.username, user.first_name, user.last_name, user.age, user.sex,
                                 user.scopes, user.measurement.waist_before, user.measurement.breast_before,
                                 user.measurement.femur_before, user.measurement.weight_before,
                                 user.measurement.waist_after, user.measurement.breast_after,
                                 user.measurement.femur_after, user.measurement.weight_after])
                for row in data:
                    writer.writerow(row)
            f = open(f'{file_path}/file_csv.csv', 'r', encoding='utf-8')
            my_file = File(f)
            response = HttpResponse(my_file)
            response['Content-Disposition'] = 'attachment; filename=' + 'file_csv.csv'
            return response
        except Exception as exc:
            logging.error(exc)

    def complete_task(self, request):
        complete_task = TasksUsers.objects.filter(users_id=request.id)
        text_url = ''
        for task in complete_task:
            text_url += f'<li><b><a href="/admin/personal_area/tasks/{task.id}/change/" target="_blank">' \
                        f'{task.tasks.name}</a></b></li>\n'
        url = f"""
                <ul>
                    {text_url}
                </ul>
                """
        return mark_safe(url)

    def get_photo(self, request):
        url = f'<b><a href="/admin/personal_area/photo/{request.photos.id}/change/" target="_blank">Тык сюды</a></b>'
        return mark_safe(url)

    def get_measurement(self, request):
        url = f'<b><a href="/admin/personal_area/measurement/{request.measurement.id}/change/" target="_blank">' \
              f'Тык сюды</a></b>'
        return mark_safe(url)

    def get_bzu(self, request):
        url = f'<b><a href="/admin/personal_area/bzuusers/{request.bzu.id}/change/" target="_blank">' \
              f'Тык сюды</a></b>'
        return mark_safe(url)

    get_measurement.short_description = 'Замеры пользователя'
    get_photo.short_description = 'Фотографии пользователя'
    complete_task.short_description = 'Выполненные задания'
    import_csv.short_description = 'Выгрузить в CSV'
    get_bzu.short_description = 'Показатели БЖУ пользователя'


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    fields = ['user_change', 'front_before', 'sideways_before', 'back_before', 'front_after',
              'sideways_after', 'back_after']
    readonly_fields = ['user_change', 'front_before', 'sideways_before', 'back_before', 'front_after',
                       'sideways_after', 'back_after']
    list_display = ['user_display']

    def user_display(self, request):
        for user in request.users_set.all():
            url = f'<b><a href="/admin/personal_area/photo/{user.photos.id}/change/" target="_blank">' \
                  f'{user.first_name} {user.last_name} - {user.marathon.name}</a></b>'
            return mark_safe(url)

    def user_change(self, request):
        for user in request.users_set.all():
            url = f'<b><a href="/admin/personal_area/users/{user.id}/change/" target="_blank">{user.first_name} ' \
                  f'{user.last_name} - {user.marathon.name}</a></b>'
            return mark_safe(url)

    user_display.short_description = 'Пользователь:'
    user_change.short_description = 'Пользователь:'

    def front_before(self, obj):
        url = f'<a href="{obj.photo_front_before.url}" target="_blank"><img src="{obj.photo_front_before.url}" ' \
              f'style="max-height:200px;"></a>'
        return mark_safe(url)

    front_before.short_description = 'Фото спереди до:'

    def sideways_before(self, obj):
        url = f'<a href="{obj.photo_sideways_before.url}" target="_blank"><img src="{obj.photo_sideways_before.url}"' \
              f'style="max-height: 200px;"></a> '
        return mark_safe(url)

    sideways_before.short_description = 'Фото сбоку до:'

    def back_before(self, obj):
        url = f'<a href="{obj.photo_back_before.url}" target="_blank"><img src="{obj.photo_back_before.url}"' \
              f'style="max-height:200px;"></a> '
        return mark_safe(url)

    back_before.short_description = 'Фото сзади до:'

    def front_after(self, obj):
        url = f'<a href="{obj.photo_front_after.url}" target="_blank"><img src="{obj.photo_front_after.url}"' \
              f'style="max-height:200px;"></a> '
        return mark_safe(url)

    front_after.short_description = 'Фото спереди после:'

    def sideways_after(self, obj):
        url = f'<a href="{obj.photo_sideways_after.url}" target="_blank"><img src="{obj.photo_sideways_after.url}"' \
              f'style="max-height:200px;"></a> '
        return mark_safe(url)

    sideways_after.short_description = 'Фото сбоку после:'

    def back_after(self, obj):
        url = f'<a href="{obj.photo_back_after.url}" target="_blank"><img src="{obj.photo_back_after.url}"' \
              f' style="max-height:200px;"></a> '
        return mark_safe(url)

    back_after.short_description = 'Фото сзади после:'


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    fields = ['user_change', 'waist_before', 'breast_before', 'femur_before', 'weight_before',
              'waist_after', 'breast_after', 'femur_after', 'weight_after']
    readonly_fields = ['user_change', 'waist_before', 'breast_before', 'femur_before', 'weight_before',
                       'waist_after', 'breast_after', 'femur_after', 'weight_after']
    list_display = ['user_display']

    def user_display(self, request):
        for user in request.users_set.all():
            url = f'<b><a href="/admin/personal_area/measurement/{user.measurement.id}/change/" target="_blank">' \
                  f'{user.first_name} {user.last_name} - {user.marathon.name}</a></b>'
            return mark_safe(url)

    def user_change(self, request):
        for user in request.users_set.all():
            url = f'<b><a href="/admin/personal_area/users/{user.id}/change/" target="_blank">{user.first_name} ' \
                  f'{user.last_name} - {user.marathon.name}</a></b>'
            return mark_safe(url)

    user_display.short_description = mark_safe('<b>Пользователь</b>')
    user_change.short_description = mark_safe('<b>Пользователь</b>')


@admin.register(Marathon)
class MarathonAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'date_start', 'date_end', 'send_measurements_before', 'send_measurements_after',
              'close', 'price']
    list_display = ['name', 'date_start', 'date_end', 'send_measurements_before', 'send_measurements_after', 'close']
    list_editable = ['date_start', 'date_end', 'send_measurements_before', 'send_measurements_after', 'close']

    def delete_queryset(self, request, queryset):
        for marathon in queryset:
            for category_task_marathon in marathon.categorytasksmarathon_set.all():
                CategoryTasks.objects.get(id=category_task_marathon.id).delete()
                category_task_marathon.delete()
            for category_training_menu in marathon.categorytrainingmenumarathon_set.all():
                CategoryTrainingMenu.objects.get(id=category_training_menu.id).delete()
                category_training_menu.delete()
            for kcal_category in marathon.kcalcategoryreadymademenumarathon_set.all():
                KcalCategoryReadyMadeMenu.objects.get(id=kcal_category.id).delete()
                kcal_category.delete()
            for product in marathon.product_set.all():
                product.delete()
            for task in marathon.tasks_set.all():
                task.delete()
            for user in marathon.users_set.all():
                for codes_user in user.codesusers_set.all():
                    codes_user.delete()
                for product_user in user.productusers_set.all():
                    product_user.delete()
                for task_user in user.tasksusers_set.all():
                    task_user.delete()
                try:
                    Photo.objects.get(id=user.photos_id).delete()
                except Exception as exc:
                    logging.error(exc)
                try:
                    Measurement.objects.get(id=user.measurement_id).delete()
                except Exception as exc:
                    logging.error(exc)
                user.delete()
                file_path = f"{Path(__file__).resolve().parent.parent}/media/user_photos/{user.tg_id}/"
                command = f'rm -r {file_path}/{user.tg_id}'
                os.system(command)
            marathon.delete()


class TaskInline(admin.TabularInline):
    model = Tasks
    fields = ['name', 'category', 'description', 'count_scopes', ('image', 'preview'), ('date_start', 'date_stop')]
    readonly_fields = ['preview']
    # list_display = ['name', 'category', 'count_scopes', 'date_start', 'date_stop']
    # list_filter = ['category']
    # list_editable = ['count_scopes']
    # list_display_links = ['name']
    # search_fields = ['name', ]
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'cols': 40})},
    }
    extra = 0

    def preview(self, obj):
        url = f'<a href="{obj.image.url}" target="_blank"><img src="{obj.image.url}" style="max-height: 50px;"></a>'
        return mark_safe(url)

    preview.short_description = 'Превью'


class CategoryTasksInline(admin.StackedInline):
    model = CategoryTasksMarathon


@admin.register(CategoryTasks)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryTasksInline, TaskInline]
    list_display = ['category', 'get_marathon']
    list_filter = ['categorytasksmarathon__marathon__name']

    def get_marathon(self, obj):
        return obj.categorytasksmarathon.marathon.name

    get_marathon.short_description = 'Марафон'


@admin.register(PhotoStates)
class PhotoStatesAdmin(admin.ModelAdmin):
    fields = ['category_photo', 'photo', 'get_photo']
    readonly_fields = ['get_photo']

    def get_photo(self, obj):
        url = f'<a href="{obj.photo.url}" target="_blank"><img src="{obj.photo.url}"' \
              f'style="max-height:200px;"></a> '
        return mark_safe(url)

    get_photo.short_description = 'Превью'


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    fields = ['name', 'description', ('image', 'get_photo'), 'marathon']
    readonly_fields = ['get_photo']
    list_filter = ['marathon']
    list_display = ['name', 'marathon']

    def get_photo(self, obj):
        url = f'<a href="{obj.image.url}" target="_blank"><img src="{obj.image.url}"' \
              f'style="max-height:100px;"></a> '
        return mark_safe(url)

    get_photo.short_description = 'Превью'


@admin.register(BZUUsers)
class BZUAdmin(admin.ModelAdmin):
    pass


@admin.register(Codes)
class CodesAdmin(admin.ModelAdmin):
    list_display = ['code', 'scopes', 'marathon']
    list_display_links = ['marathon']
    list_editable = ['code', 'scopes']


class KcalCategoryInLine(admin.StackedInline):
    model = KcalCategoryReadyMadeMenuMarathon
    verbose_name = 'Категория - марафон'


class DayReadyMadeInline(admin.TabularInline):
    model = DayReadyMadeMenu
    extra = 0


class TimeDayReadyMadeMenuInline(admin.TabularInline):
    model = TimeDayReadyMadeMenu
    extra = 0


@admin.register(KcalCategoryReadyMadeMenu)
class KcalCategoryAdmin(admin.ModelAdmin):
    list_display = ['kcal_category', ]
    inlines = [KcalCategoryInLine, DayReadyMadeInline]


class ReadyMadeMenuInline(admin.StackedInline):
    model = ReadyMadeMenu
    extra = 0
    fields = ['name_menu', 'description', 'time_day', 'photo', 'get_photo']
    readonly_fields = ['get_photo']

    def get_photo(self, obj):
        url = f'<a href="{obj.photo.url}" target="_blank"><img src="{obj.photo.url}" ' \
              f'style="max-height:200px;"></a>'
        return mark_safe(url)

    get_photo.short_description = 'Превью'


@admin.register(TimeDayReadyMadeMenu)
class TimeDayReadyMadeMenuAdmin(admin.ModelAdmin):
    inlines = [ReadyMadeMenuInline]
    list_display = ['time_day', 'day']


class CategoryTrainingMenuInline(admin.StackedInline):
    model = CategoryTrainingMenuMarathon


class TrainingInfoInline(admin.StackedInline):
    model = TrainingInfo
    extra = 0
    fields = ['name', 'description', 'category', 'photo', 'get_photo']
    readonly_fields = ['get_photo']

    def get_photo(self, obj):
        url = f'<a href="{obj.photo.url}" target="_blank"><img src="{obj.photo.url}" ' \
              f'style="max-height:200px;"></a>'
        return mark_safe(url)

    get_photo.short_description = 'Превью'


@admin.register(CategoryTrainingMenu)
class CategoryTrainingMenuAdmin(admin.ModelAdmin):
    list_display = ['category']
    inlines = [CategoryTrainingMenuInline, TrainingInfoInline]
