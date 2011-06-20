# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import *

class FileForm(ModelForm):
    class Meta:
        model = File
        fields = ('name', 'file','tags')


class FileTagForm(ModelForm):
    class Meta:
        model = FileTag
        fields = ('name',)