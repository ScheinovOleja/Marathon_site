import json

from django import forms

from .models import Marathon

TYPES_FILE = (
    ('image', 'Изображение'),
    ('video-common', 'Обычное видео'),
    ('video-round', 'Круговое видео'),
    ('file', 'Файл'),
)


class UploadFileForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(), label='Ваше сообщение', required=False)
    file = forms.FileField(label='Ваш файл', required=False, widget=forms.FileInput)
    type_file = forms.ChoiceField(widget=forms.RadioSelect(), choices=TYPES_FILE, label='Тип файла', required=False)
    marathon = forms.ModelChoiceField(Marathon.objects.all(),
                                      label='В какой марафон разослать(--- если разослать всем):', required=False,)

