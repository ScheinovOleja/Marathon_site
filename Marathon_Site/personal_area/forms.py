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
                                      label='В какой марафон разослать(--- если разослать всем):', required=False, )


class EditButtonsForm(forms.Form):
    json_file = open('marathon_bot/settings/buttons.json', 'r')
    test = json.load(json_file)
    jsonfield = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 60, 'class': 'json-editor'}),
                                label='Ваше сообщение')

    def clean_jsonfield(self):
        jdata = self.cleaned_data['jsonfield']
        try:
            json_data = json.loads(jdata)  # loads string as json
            # validate json_data
        except:
            raise forms.ValidationError("Invalid data in jsonfield")
        # if json data not valid:
        # raise forms.ValidationError("Invalid data in jsonfield")
        return jdata
    # json_file = open('marathon_bot/settings/buttons.json', 'r')
    # test = json.load(json_file)
    # text_buttons = forms.JSONField(initial=test)
#
# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm):
#         model = Users
#         fields = ('username', 'email', 'sex')
#
#
# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = Users
#         fields = ('username', 'email', 'sex')
#
#     # email = forms.EmailField()
#     sex = forms.CharField()
