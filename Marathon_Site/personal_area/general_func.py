import os

from Marathon_Site.settings import MEDIA_ROOT


def users_delete(user):
    for codes_user in user.codesusers_set.all():
        codes_user.delete()
    for product_user in user.productusers_set.all():
        product_user.delete()
    for task_user in user.tasksusers_set.all():
        task_user.delete()
    try:
        user.measurement.delete()
    except (AttributeError, AssertionError):
        pass
    try:
        user.photos.delete()
        command = f'rm -r {MEDIA_ROOT}/users_photo/{user.tg_id}/{user.marathon_id}/'
        os.system(command)
    except (AttributeError, AssertionError):
        pass
    try:
        user.bzu.delete()
    except (AttributeError, AssertionError):
        pass


def marathon_delete(marathon):
    for category_task_marathon in marathon.categorytasksmarathon_set.all():
        for task in category_task_marathon.category.tasks_set.all():
            if task.image.name != '':
                command = f'rm -r {MEDIA_ROOT}/{task.image.name}'
                os.system(command)
            task.delete()
        category_task_marathon.category.delete()
        category_task_marathon.delete()
    for category_training_menu in marathon.categorytrainingmenumarathon_set.all():
        for menu in category_training_menu.category.traininginfo_set.all():
            if menu.photo.name != '':
                command = f'rm -r {MEDIA_ROOT}/{menu.photo.name}'
                os.system(command)
            menu.delete()
        category_training_menu.category.delete()
        category_training_menu.delete()
    for kcal_category in marathon.kcalcategoryreadymademenumarathon_set.all():
        for day in kcal_category.category.dayreadymademenu_set.all():
            for time in day.timedayreadymademenu_set.all():
                for ready_made in time.readymademenu_set.all():
                    if ready_made.photo.name != '':
                        command = f'rm -r {MEDIA_ROOT}/{ready_made.photo.name}'
                        os.system(command)
                    ready_made.delete()
                time.delete()
            day.delete()
        kcal_category.category.delete()
        kcal_category.delete()
    for product in marathon.product_set.all():
        for product_users in product.productusers_set.all():
            product_users.delete()
        if product.image.name != '':
            command = f'rm -r {MEDIA_ROOT}/{product.image.name}'
            os.system(command)
        product.delete()
    for invite in marathon.invitecode_set.all():
        invite.delete()
    for user in marathon.users_set.all():
        users_delete(user)
        user.delete()


def task_delete(category):
    for task in category.tasks_set.all():
        try:
            command = f'rm -r {MEDIA_ROOT}/{task.image}'
            os.system(command)
        except (AttributeError, AssertionError):
            pass
        task.delete()


def product_delete(product):
    try:
        command = f'rm -r {MEDIA_ROOT}/{product.image}'
        os.system(command)
    except (AttributeError, AssertionError):
        pass
    product.delete()


def kcal_category_delete(kcal_category):
    for day_menu in kcal_category.dayreadymademenu_set.all():
        for time_day in day_menu.timedayreadymademenu_set.all():
            for menu in time_day.readymademenu_set.all():
                try:
                    command = f'rm -r {MEDIA_ROOT}/media/{menu.photo}'
                    os.system(command)
                except (AttributeError, AssertionError):
                    pass
                menu.delete()
            time_day.delete()
        day_menu.delete()
    kcal_category.delete()


def ready_made_delete(ready_made):
    ready_made.delete()
