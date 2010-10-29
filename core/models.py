from django.db import models
from django.contrib.contenttypes.models import ContentType
from managers import PersistentManager
from core.middleware import *
from datetime import datetime

"""
The Company class.
All users belong to a company, therefore all objects belongs to a company, like projects, orders...
A user can only see objects within the same company.
 * An exception to this, if the user is a guest in another companys project.
"""
class Company(models.Model):
    name = models.CharField(max_length=80)

    def __unicode__(self):
        return self.name


"""
Class for logs, saves user in action and reference to object logged
"""
class Log(models.Model):
    date         = models.DateTimeField()
    creator      = models.ForeignKey(User, related_name="logs")
    content_type = models.ForeignKey(ContentType, null=True)
    object_id    = models.PositiveIntegerField(null=True)
    message      = models.TextField()
    company      = models.ForeignKey(Company, related_name="logs", null=True)

    def __unicode__(self):
        s = "%s endret: %s: %s " % ((self.creator), self.content_type, self.message)
        return s.decode("utf-8")


    def save(self, *args, **kwargs):

        self.date = datetime.now()
        self.company = get_current_company()
        print kwargs
        if 'user' in kwargs:
            self.creator = kwargs['user']
        else:
            self.creator = get_current_user()

        super(Log, self).save()


"""
The "all mighty" model, all other models inherit from this one. 
Contains all the useful fields like who created and edited the object, and when it was done.
It also automatically saves the information about the user interaction with the object.
"""

class PersistentModel(models.Model):
    deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=datetime.now())
    date_edited = models.DateTimeField(default=datetime.now())

    creator = models.ForeignKey(User, blank=True, null=True, default=None, related_name="%(class)s_created")
    editor = models.ForeignKey(User, blank=True, null=True, default=None, related_name="%(class)s_edited")
    company = models.ForeignKey(Company, blank=True, null=True, default=None, related_name="%(class)s_edited")

    objects = PersistentManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def save(self, **kwargs):

        if not self.id:
            self.creator = get_current_user()
            self.company = get_current_user().get_profile().company

        #self.editor = get_current_user()
        self.date_edited = datetime.now()
        super(PersistentModel, self).save()

        if 'nolog' not in kwargs:
            #Save log entry , if not chosen not to do so
            Log(message = "%s endret %s" % (get_current_user(), self),
                object_id = self.id,
                content_type = ContentType.objects.get_for_model(self.__class__)
            ).save()


    def delete(self, **kwargs):
        self.deleted = True
        super(PersistentModel, self).save()


    """
    whoHasPermissionTo
    returns a list of users who are permitted perform actions on the object
    """

    def whoHasPermissionTo(self, perm):
        try:
            content_type = ContentType.objects.get_for_model(self)
            id = self.id
            users = []

            for u in ObjectPermission.objects.filter(content_type=content_type, negative=False, object_id=id,
                                                     **{'can_%s' % perm: True}):
                if u.user and u.user not in users:
                    users.append(u.user)
                if u.membership:
                    for user in u.membership.users.all():
                        if user and user not in users:
                            users.append(user)
            return users
        except:
            return []

"""
Memberships, user can be members of memberships, which can have permissions for instance
"""
class Membership(PersistentModel):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User, related_name="memberships")

    def __unicode__(self):
        return self.name


"""
ROLES
"""
class Role(models.Model):
    name = models.CharField(max_length=200)
    permission = models.CharField(max_length=50, default="")
    user = models.ForeignKey(User, blank=True, null=True, related_name="roles")
    membership = models.ForeignKey(Membership, blank=True, null=True, related_name='roles')

    content_type = models.ForeignKey(ContentType)

    def __unicode__(self):
        return unicode(self.content_type)


"""
Adding object permissins to object, using a content_type for binding with all kinds of objects
"""
class ObjectPermission(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, related_name="permissions")
    membership = models.ForeignKey(Membership, blank=True, null=True, related_name='permissions')

    deleted = models.BooleanField()

    #General permissions
    can_view = models.BooleanField()
    can_change = models.BooleanField()
    can_delete = models.BooleanField()

    negative = models.BooleanField()

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    def __unicode__(self):
        return unicode(self.get_object())

    def get_object(self):
        return self.content_type.get_object_for_this_type(id=self.object_id)

from django.db.models.signals import post_save

"""
Userprofiles, for adding additional informartion about the user
"""
class UserProfile(models.Model):
# This is the only required field
    user = models.ForeignKey(User, unique=True)
    company = models.ForeignKey(Company, blank=True, null=True, related_name="%(app_label)s_%(class)s_users")

    def __unicode__(self):
        return "Profile for: %s" % self.user


"""
Keeping users and their userprofile in sync, when creating a user, a userprofile is createad as well.
"""

def create_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        up = UserProfile(user=user)
        try:
            up.company = get_current_user().get_profile()
        except:
            up.save()

post_save.connect(create_profile, sender=User)

"""
Adding some initial data to the model when run syncdb
"""

from app.timetracking.models import *

def initial_data ():
    comp = Company(name="Focus AS")
    comp.save()

    a, created = User.objects.get_or_create(username="superadmin",
                                            first_name="SuperAdmin",
                                            last_name="",
                                            is_superuser=True,
                                            is_staff=True,
                                            is_active=True)
    a.set_password("superpassord")
    a.save()

    u, created = User.objects.get_or_create(username="bjarte",
                                            first_name="Bjarte",
                                            last_name="Hatlenes",
                                            is_active=True)
    u.set_password("superpassord")
    u.save()
    u.get_profile().company = comp
    u.get_profile().save()