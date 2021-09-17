import asyncio
import time
from threading import Thread

from django.shortcuts import render
from django.views import View

# Create your views here.
from personal_area.forms import UploadFileForm
from personal_area.mailing import mailing


class SendMessageToTG(View):
    form = UploadFileForm()

    def post(self, request, *args, **kwargs):
        start_time = time.time()
        # asyncio.(mailing(request))
        # print('test')
        Thread(target=mailing, kwargs={'request': request}).start()
        # loop = asyncio.new_event_loop()
        # loop.run_until_complete(mailing(request))
        # loop.close()
        print("--- %s seconds ---" % (time.time() - start_time))
        return render(request, 'personal_area/base.html', {'context': {'sent': False, 'form': self.form}})

    def get(self, request):
        return render(request, 'personal_area/base.html', {'context': {'sent': False, 'form': self.form}})

