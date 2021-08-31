import csv
import logging
import os
import subprocess
from pathlib import Path

from django.contrib import admin
from django.contrib.admin import AdminSite
from django.core.checks import messages
from django.core.files import File
from django.forms import TextInput, Textarea
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, path
from django.utils.safestring import mark_safe

from .models import *


# Register your models here.


class UsersAdmin(admin.ModelAdmin):
    model = Users
    actions = ['import_csv']
    search_fields = ['username', 'first_name', 'last_name']
    list_filter = ['sex', 'marathon__name']
    list_display = ['tg_id', 'username', 'first_name', 'last_name', 'marathon']
    fields = ['username', ('first_name', 'last_name'), 'sex', 'scopes', 'marathon', ('get_photo', 'get_measurement',
                                                                                     'get_bzu')]
    readonly_fields = ['get_photo', 'get_measurement', 'get_bzu', 'marathon', 'sex', 'username']
    list_display_links = ['tg_id', 'marathon']
    list_per_page = 50
    list_max_show_all = 200

    def import_csv(self, request, queryset):
        try:
            file_path = f"{Path(__file__).resolve().parent.parent}/media/csv_files"
            if not os.path.isdir(file_path):
                os.mkdir(file_path)
            data = [
                ['tg_id', 'tg_nickname', 'Имя', 'Фамилия', 'Возраст', 'Вес', 'Рост', 'Цель', 'ККАЛ', 'Пол',
                 'Кол-во баллов', 'Грудь ДО', 'Талия ДО', 'Бедра ДО', 'Вес ДО', 'Грудь ПОСЛЕ', 'Талия ПОСЛЕ',
                 'Бедра ПОСЛЕ', 'Вес ПОСЛЕ', 'Белки', 'Жиры', 'Углеводы']
            ]
            with open(f'{file_path}/file_csv.csv', 'w', encoding='utf-8') as csv_file:
                for user in queryset:
                    writer = csv.writer(csv_file, delimiter=';')
                    purpose = 'Похудение' if user.purpose == '-' else 'Поддержание веса' if user.purpose == '=' else \
                        'Набор массы' if user.purpose == '+' else ""
                    data.append(
                        [user.tg_id, user.username, user.first_name, user.last_name, user.age, user.weight, user.height,
                         purpose, user.kcal, user.sex,
                         user.scopes, user.measurement.waist_before if user.measurement else '-',
                         user.measurement.breast_before if user.measurement else '-',
                         user.measurement.femur_before if user.measurement else '-',
                         user.measurement.weight_before if user.measurement else '-',
                         user.measurement.waist_after if user.measurement else '-',
                         user.measurement.breast_after if user.measurement else '-',
                         user.measurement.femur_after if user.measurement else '-',
                         user.measurement.weight_after if user.measurement else '-',
                         user.bzu.proteins if user.bzu else '-',
                         user.bzu.fats if user.bzu else '-',
                         user.bzu.carbohydrates if user.bzu else '-',
                         ]
                    )
                for row in data:
                    writer.writerow(row)
            f = open(f'{file_path}/file_csv.csv', 'r', encoding='utf-8')
            my_file = File(f)
            response = HttpResponse(my_file)
            response['Content-Disposition'] = 'attachment; filename=' + 'file_csv.csv'
            return response
        except Exception as exc:
            logging.error(exc)

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

    def delete_queryset(self, request, queryset):
        for user in queryset:
            users_delete(user)
            user.delete()

    get_measurement.short_description = 'Замеры пользователя'
    get_photo.short_description = 'Фотографии пользователя'
    import_csv.short_description = 'Выгрузить в CSV'
    get_bzu.short_description = 'Показатели БЖУ пользователя'


class PhotoAdmin(admin.ModelAdmin):
    fields = ['user_change', 'front_before', 'sideways_before', 'back_before', 'front_after',
              'sideways_after', 'back_after']
    readonly_fields = ['user_change', 'front_before', 'sideways_before', 'back_before', 'front_after',
                       'sideways_after', 'back_after']
    list_display = ['user_display']
    list_filter = ['users__marathon__name']

    def user_display(self, request):
        user = request.users
        url = f'<b><a href="/admin/personal_area/photo/{user.photos.id}/change/">' \
              f'{user.first_name} {user.last_name} - {user.marathon.name}</a></b>'
        return mark_safe(url)

    def user_change(self, request):
        user = request.users
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


class MeasurementAdmin(admin.ModelAdmin):
    fields = ['user_change', 'breast_before', 'waist_before', 'femur_before', 'weight_before',
              'breast_after', 'waist_after', 'femur_after', 'weight_after']
    readonly_fields = ['user_change', 'breast_before', 'waist_before', 'femur_before', 'weight_before',
                       'breast_after', 'waist_after', 'femur_after', 'weight_after']
    list_display = ['user_display']
    list_filter = ['users__marathon__name']

    def user_display(self, request):
        user = request.users
        url = f'<b><a href="/admin/personal_area/measurement/{user.measurement.id}/change/">' \
              f'{user.first_name} {user.last_name} - {user.marathon.name}</a></b>'
        return mark_safe(url)

    def user_change(self, request):
        user = request.users
        url = f'<b><a href="/admin/personal_area/users/{user.id}/change/" target="_blank">{user.first_name} ' \
              f'{user.last_name} - {user.marathon.name}</a></b>'
        return mark_safe(url)

    user_display.short_description = mark_safe('<b>Пользователь</b>')
    user_change.short_description = mark_safe('<b>Пользователь</b>')


class MarathonAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'date_start', 'date_end', 'send_measurements_before', 'send_measurements_after',
              'close', 'price', 'count_users']
    list_display = ['name', 'date_start', 'date_end', 'send_measurements_before', 'send_measurements_after', 'close',
                    'count_users']
    list_editable = ['date_start', 'date_end', 'send_measurements_before', 'send_measurements_after', 'close',
                     'count_users']

    def delete_queryset(self, request, queryset):
        for marathon in queryset:
            marathon_delete(marathon)
            marathon.delete()


class TaskInline(admin.StackedInline):
    model = Tasks
    fields = ['name', 'category', 'description', 'count_scopes', 'unique_code', ('image', 'preview'), ('date_start', 'date_stop')]
    readonly_fields = ['preview']
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


class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryTasksInline, TaskInline]
    list_display = ['category', 'get_marathon']
    list_filter = ['categorytasksmarathon__marathon__name']

    def get_marathon(self, obj):
        return obj.categorytasksmarathon.marathon.name

    get_marathon.short_description = 'Марафон'


class PhotoStatesAdmin(admin.ModelAdmin):
    fields = ['category_photo', 'photo', 'get_photo']
    readonly_fields = ['get_photo']

    def get_photo(self, obj):
        url = f'<a href="{obj.photo.url}" target="_blank"><img src="{obj.photo.url}"' \
              f'style="max-height:200px;"></a> '
        return mark_safe(url)

    get_photo.short_description = 'Превью'


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


class BZUAdmin(admin.ModelAdmin):
    list_display = ['user_display', 'proteins', 'fats', 'carbohydrates']
    fields = ['user_change', 'proteins', 'fats', 'carbohydrates']
    readonly_fields = ['user_change']
    list_filter = ['users__marathon__name']

    def user_display(self, request):
        url = f'<b><a href="/admin/personal_area/bzuusers/{request.users.bzu.id}/change/">' \
              f'{request.users.first_name} {request.users.last_name} - {request.users.marathon.name}</a></b>'
        return mark_safe(url)

    def user_change(self, request):
        url = f'<b><a href="/admin/personal_area/users/{request.users.id}/change/" target="_blank">' \
              f'{request.users.first_name} {request.users.last_name} - {request.users.marathon.name}</a></b>'
        return mark_safe(url)

    user_display.short_description = 'Пользователь'
    user_change.short_description = 'Пользователь:'


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


class KcalCategoryAdmin(admin.ModelAdmin):
    list_display = ['kcal_category', 'get_marathon']
    list_filter = ['kcalcategoryreadymademenumarathon__marathon__name']
    inlines = [KcalCategoryInLine, DayReadyMadeInline]

    def get_marathon(self, obj):
        return obj.kcalcategoryreadymademenumarathon.marathon.name

    get_marathon.short_description = 'Марафон'


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


class TimeDayReadyMadeMenuAdmin(admin.ModelAdmin):
    inlines = [ReadyMadeMenuInline]
    fields = ['time_day', 'day', 'get_marathon']
    readonly_fields = ['get_marathon']
    list_display = ['time_day', 'day', 'get_marathon']
    list_filter = ['day__kcal_category__kcalcategoryreadymademenumarathon__marathon__name']

    def get_marathon(self, obj):
        return obj.day.kcal_category.kcalcategoryreadymademenumarathon.marathon.name

    get_marathon.short_description = 'Марафон'


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


class CategoryTrainingMenuAdmin(admin.ModelAdmin):
    list_display = ['category', 'get_marathon']
    inlines = [CategoryTrainingMenuInline, TrainingInfoInline]
    list_filter = ['categorytrainingmenumarathon__marathon__name']

    def get_marathon(self, obj):
        return obj.categorytrainingmenumarathon.marathon.name

    get_marathon.short_description = 'Марафон'


class InviteCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'marathon', 'date_delete']
    list_filter = ['marathon']


class ButtonsTextAdmin(admin.ModelAdmin):
    save_on_top = True

    def add_view(self, request, form_url='', extra_context=None):
        if self.model.objects.count() >= 1:
            self.message_user(request, 'Нельзя добавить больше одной записи!',
                              messages.ERROR)
            return HttpResponseRedirect(reverse(f'admin:{self.model._meta.app_label}_buttonstext_changelist'))
        return super().add_view(request, form_url, extra_context)


class BotConfigAdmin(admin.ModelAdmin):
    list_display = ['name_bot', 'start_bot']

    def add_view(self, request, form_url='', extra_context=None):
        if self.model.objects.count() >= 1:
            self.message_user(request, 'Нельзя добавить больше одной записи!',
                              messages.ERROR)
            return HttpResponseRedirect(reverse(f'admin:{self.model._meta.app_label}_botconfig_changelist'))
        return super().add_view(request, form_url, extra_context)

    def start_bot(self, request):
        return mark_safe(
            f'<a class="button" href="{reverse("admin:start")}">Запустить</a>'
            f'<a class="button" href="{reverse("admin:stop")}">Остановить</a>'
            f'<a class="button" href="{reverse("admin:restart")}">Перезапустить</a>')

        # Добавляем к существующим ссылкам в админке, ссылки на кнопки для их обработки

    def get_urls(self):
        urls = super().get_urls()
        shard_urls = [path('#', self.admin_site.admin_view(self.start), name="start"),
                      path('#', self.admin_site.admin_view(self.stop), name="stop"),
                      path('#', self.admin_site.admin_view(self.restart), name="restart")
                      ]

        # Список отображаемых столбцов
        return shard_urls + urls

        # Обработка событий кнопок

    def start(self, request):
        start_bot = subprocess.run(["sh", "start.sh"])
        return HttpResponseRedirect(reverse(f'admin:personal_area_botconfig_changelist'))

    def stop(self, request):
        stop_bot = subprocess.run(["sh", "stop.sh"])
        return HttpResponseRedirect(reverse(f'admin:personal_area_botconfig_changelist'))

    def restart(self, request):
        restart_bot = subprocess.run(["sh", "restart.sh"])
        return HttpResponseRedirect(reverse(f'admin:personal_area_botconfig_changelist'))

    start_bot.short_description = 'Управление'


class AllUsersAdmin(admin.ModelAdmin):
    list_display = ['tg_id']


class MyAdminSite(AdminSite):

    def get_app_list(self, request):
        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        return app_list


admin.site = MyAdminSite()
admin.site.register(Marathon, MarathonAdmin)
admin.site.register(Users, UsersAdmin)
admin.site.register(BZUUsers, BZUAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(CategoryTasks, CategoryAdmin)
admin.site.register(KcalCategoryReadyMadeMenu, KcalCategoryAdmin)
admin.site.register(TimeDayReadyMadeMenu, TimeDayReadyMadeMenuAdmin)
admin.site.register(CategoryTrainingMenu, CategoryTrainingMenuAdmin)
admin.site.register(Product, ProductsAdmin)
admin.site.register(Codes, CodesAdmin)
admin.site.register(InviteCode, InviteCodeAdmin)
admin.site.register(ButtonsText, ButtonsTextAdmin)
admin.site.register(BotConfig, BotConfigAdmin)
admin.site.register(AllUsers, AllUsersAdmin)
