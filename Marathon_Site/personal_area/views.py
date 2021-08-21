import asyncio

from django.shortcuts import render
from django.views import View

# Create your views here.
from personal_area.forms import UploadFileForm
from personal_area.mailing import mailing


class SendMessageToTG(View):
    form = UploadFileForm()

    def post(self, request, *args, **kwargs):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(mailing(request))
        loop.close()
        return render(request, 'personal_area/base.html', {'context': {'sent': False, 'form': self.form}})

    def get(self, request):
        return render(request, 'personal_area/base.html', {'context': {'sent': False, 'form': self.form}})
