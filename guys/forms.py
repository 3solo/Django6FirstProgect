from django import forms
from guys.models import FloodMessages, News, Category, Topic, TopicMessages


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Файл')


class FloodForm(forms.ModelForm):
    class Meta:
        model = FloodMessages
        fields =['message']
        widgets ={'message':forms.TextInput(attrs={'placeholder':'Введите сообщение..'})}


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'photo']
        labels = {
            'title': 'Название',
            'content': 'Информация',
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description']
        labels = {
            'name': 'Название',
            'slug': 'URL',
            'description': 'Описание',
        }


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title']


class TopicMessagesForm(forms.ModelForm):
    class Meta:
        model = TopicMessages
        fields = ['content']
        widgets = {'content': forms.TextInput(attrs={'placeholder':'Введите сообщение..'})}


