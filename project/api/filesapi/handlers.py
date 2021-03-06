from app.files.forms import FileForm, FileTagForm
from app.files.models import File, FileTag
from app.files.views import handle_file_tags
from piston.handler import BaseHandler
from app.contacts.models import Contact
from app.stock.models import Product
from core import Core
from piston.utils import rc

class FileHandler(BaseHandler):
    model = File
    fields = ('id', 'name', 'date_created', 'date_edited', 'tags', ('editor', ('id', 'first_name', 'last_name')), 'get_file',
                  ('revisions', (
                  'id', 'name','tags', ('editor', ('id', 'first_name', 'last_name')), 'date_created', 'date_edited',
                  'get_file'))) 

    def read(self, request, id=None):
        all = Core.current_user().get_permitted_objects("VIEW", File).filter(trashed=False, )
        if id:
            try:
                return all.get(id=id)
            except File.DoesNotExist:
                return rc.NOT_FOUND

        return all

    def create(self, request, id=None):

        clone = None

        if id:
            instance = File.objects.get(id=id)
            clone = instance.clone()

        else:
            instance = File()

        form = FileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            file = form.save(commit=False)

            file.tags = []
            file.tags.add(*handle_file_tags(request.POST['tags']))

            file.save()

            if id:
                clone.save()

            return file

        else:
            return form.errors


class FileTagHandler(BaseHandler):
    model = FileTag
    fields = ('id', 'name')

    def read(self, request, id=None):
        all = Core.current_user().get_permitted_objects("VIEW", FileTag).filter(trashed=False, )
        if id:
            try:
                return all.get(id=id)
            except FileTag.DoesNotExist:
                return rc.NOT_FOUND

        return all

    def create(self, request, id=None):
        clone = None

        if id:
            instance = FileTag.objects.get(id=id)
        else:
            instance = FileTag()

        form = FileTagForm(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return obj
        else:
            return form.errors