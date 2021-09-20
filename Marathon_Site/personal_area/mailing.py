import asyncio
import os
import re
from datetime import datetime

import requests
from Marathon_Site.settings import MEDIA_ROOT
from aiogram import Bot, types
from aiogram.types import ChatActions
from aiogram.utils.exceptions import BotBlocked, CantTalkWithBots
from asgiref.sync import sync_to_async

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


def mailing(request):
    loop = asyncio.new_event_loop()
    bot_cfg = loop.run_until_complete(get_cfg())
    # bot_cfg = await get_cfg()
    start_time = datetime.now()
    bot = Bot(token=bot_cfg.bot_token, parse_mode=types.ParseMode.HTML)
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    message = request.POST['message']
    text = f'{message}\n\n\nНажмите /start, чтобы выйти в главное меню!'
    if request.FILES:
        path = MEDIA_ROOT + '/tmp/'
        if not os.path.isdir(path):
            os.mkdir(path)
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
        all_users = loop.run_until_complete(get_all_users())
        # all_users = await get_all_users()
    else:
        all_users = loop.run_until_complete(get_users_from_marathon(request.POST['marathon']))
        # all_users = await get_users_from_marathon(request.POST['marathon'])
    for user in all_users:
        try:
            if check:
                if request.POST['type_file'] == 'image':
                    # await bot.send_chat_action(user.tg_id, ChatActions.UPLOAD_PHOTO)
                    loop.run_until_complete(bot.send_chat_action(user.tg_id, ChatActions.UPLOAD_PHOTO))
                    if file_id:
                        loop.run_until_complete(bot.send_photo(user.tg_id, file_id, caption=text))
                        # await bot.send_photo(user.tg_id, file_id, caption=text)
                    else:
                        with open(f'{path}{file_from_form.name}', 'rb') as file:
                            # msg = await bot.send_photo(user.tg_id, file, caption=text)
                            msg = loop.run_until_complete(bot.send_photo(user.tg_id, file, caption=text))
                            file_id = msg.photo[-1].file_id
                elif request.POST['type_file'] == 'video-common':
                    loop.run_until_complete(bot.send_chat_action(user.tg_id, ChatActions.RECORD_VIDEO))
                    # await bot.send_chat_action(user.tg_id, ChatActions.RECORD_VIDEO)
                    if file_id:
                        loop.run_until_complete(bot.send_video(user.tg_id, file_id, caption=text))
                        # await bot.send_video(user.tg_id, file_id, caption=text)
                    else:
                        with open(f'{path}{file_from_form.name}', 'rb') as file:
                            # msg = await bot.send_video(user.tg_id, file, caption=text)
                            msg = loop.run_until_complete(bot.send_video(user.tg_id, file, caption=text))
                            file_id = msg.video.file_id
                elif request.POST['type_file'] == 'video-round':
                    loop.run_until_complete(bot.send_chat_action(user.tg_id, ChatActions.RECORD_VIDEO_NOTE))
                    # await bot.send_chat_action(user.tg_id, ChatActions.RECORD_VIDEO_NOTE)
                    if file_id:
                        loop.run_until_complete(bot.send_video_note(user.tg_id, file_id, duration=5))
                        # await bot.send_video_note(user.tg_id, file_id, duration=5)
                    else:
                        with open(f'{path}{file_from_form.name}', 'rb') as file:
                            msg = loop.run_until_complete(bot.send_video_note(user.tg_id, file, duration=5))
                            # msg = await bot.send_video_note(user.tg_id, file, duration=5)
                            file_id = msg.video_note.file_id
                elif request.POST['type_file'] == 'file':
                    loop.run_until_complete(bot.send_chat_action(user.tg_id, ChatActions.UPLOAD_DOCUMENT))
                    # await bot.send_chat_action(user.tg_id, ChatActions.UPLOAD_DOCUMENT)
                    if file_id:
                        loop.run_until_complete(bot.send_document(user.tg_id, file_id, caption=text))
                        # await bot.send_document(user.tg_id, file_id, caption=text)
                    else:
                        with open(f'{path}{file_from_form.name}', 'rb') as file:
                            msg = loop.run_until_complete(bot.send_document(user.tg_id, file, caption=text))
                            # msg = await bot.send_document(user.tg_id, file, caption=text)
                            file_id = msg.document.file_id
            else:
                loop.run_until_complete(bot.send_message(user.tg_id, text))
                # await bot.send_message(user.tg_id, text)
            i += 1
        except (BotBlocked, CantTalkWithBots):
            user.delete()
        except Exception as exc:
            print(exc)
    if path:
        os.system(f'rm {path}{file_from_form.name}')
    # await bot.send_message(bot_cfg.admin_id, f'Сообщения пришли {i} людям.\nВремя, ушедшее на рассылку - '
    #                                          f'{datetime.now() - start_time}')
    loop.close()
    token = bot_cfg.bot_token
    url = "https://api.telegram.org/bot"
    channel_id = bot_cfg.admin_id
    url += token
    method = url + "/sendMessage"
    text = f'Сообщения пришли {i} людям.\nВремя, ушедшее на рассылку - {datetime.now() - start_time}'
    requests.post(method, data={
        "chat_id": channel_id,
        "text": text
    })
