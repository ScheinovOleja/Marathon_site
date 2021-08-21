import os
import re
from datetime import datetime

from aiogram import Bot, types
from aiogram.types import ChatActions
from aiogram.utils.exceptions import BotBlocked, CantTalkWithBots
from asgiref.sync import sync_to_async

from Marathon_Site.settings import MEDIA_ROOT

from personal_area.models import AllUsers, Users, BotConfig


@sync_to_async
def get_all_users():
    return AllUsers.objects.all()


@sync_to_async
def get_users_from_marathon(marathon_id):
    return Users.objects.filter(marathon_id=marathon_id)


@sync_to_async
def get_cfg():
    return BotConfig.objects.first()


async def mailing(request):
    bot_cfg = await get_cfg()
    start_time = datetime.now()
    bot = Bot(token=bot_cfg.bot_token, parse_mode=types.ParseMode.HTML)
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    message = request.POST['message']
    text = f'{message}\n\n\nНажмите /start, чтобы выйти в главное меню!'
    if request.FILES:
        path = MEDIA_ROOT + '/tmp/'
        file_from_form = request.FILES['file']
        file_from_form.name = re.sub('\W+', '.', file_from_form.name)
        with open(f'{path}{file_from_form.name}', 'wb') as file_to_tmp:
            file_to_tmp.write(file_from_form.file.read())
        check = True
    else:
        file_from_form = None
        path = None
        check = False
    file_id = None
    i = 0
    if request.POST['marathon'] == '':
        all_users = await get_all_users()
    else:
        all_users = await get_users_from_marathon(request.POST['marathon'])
    for user in all_users:
        try:
            if check:
                if request.POST['type_file'] == 'image':
                    await bot.send_chat_action(user.tg_id, ChatActions.UPLOAD_PHOTO)
                    if file_id:
                        await bot.send_photo(user.tg_id, file_id, caption=text)
                    else:
                        with open(f'{path}{file_from_form.name}', 'rb') as file:
                            msg = await bot.send_photo(user.tg_id, file, caption=text)
                            file_id = msg.photo[-1].file_id
                elif request.POST['type_file'] == 'video-common':
                    await bot.send_chat_action(user.tg_id, ChatActions.RECORD_VIDEO)
                    if file_id:
                        await bot.send_video(user.tg_id, file_id, caption=text)
                    else:
                        with open(f'{path}{file_from_form.name}', 'rb') as file:
                            msg = await bot.send_video(user.tg_id, file, caption=text)
                            file_id = msg.video.file_id
                elif request.POST['type_file'] == 'video-round':
                    await bot.send_chat_action(user.tg_id, ChatActions.RECORD_VIDEO_NOTE)
                    if file_id:
                        await bot.send_video_note(user.tg_id, file_id, duration=5)
                    else:
                        with open(f'{path}{file_from_form.name}', 'rb') as file:
                            msg = await bot.send_video_note(user.tg_id, file, duration=5)
                            file_id = msg.video_note.file_id
                elif request.POST['type_file'] == 'file':
                    await bot.send_chat_action(user.tg_id, ChatActions.UPLOAD_DOCUMENT)
                    if file_id:
                        await bot.send_document(user.tg_id, file_id, caption=text)
                    else:
                        with open(f'{path}{file_from_form.name}', 'rb') as file:
                            msg = await bot.send_document(user.tg_id, file, caption=text)
                            file_id = msg.document.file_id
            else:
                await bot.send_message(user.tg_id, text)
            i += 1
        except (BotBlocked, CantTalkWithBots):
            user.delete()
        except Exception as exc:
            print(exc)
    if path:
        os.system(f'rm {path}{file_from_form.name}')
    try:
        await bot.send_message(438861723, f'Сообщения пришли {i} людям.\nВремя, ушедшее на рассылку - '
                                          f'{datetime.now() - start_time}')
    except Exception:
        await bot.send_message(715845455, f'Сообщения пришли {i} людям.\nВремя, ушедшее на рассылку - '
                                          f'{datetime.now() - start_time}')
