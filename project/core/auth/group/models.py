# -*- coding: utf-8 -*-
from inspect import isclass
from django.contrib.contenttypes.models import ContentType
from django.db import models
from core import Core
from core.auth.company.models import Company
from core.auth.permission.models import Permission, Role, Action
from core.managers import PersistentManager
from core.utils import get_class, get_content_type_for_model

class Group(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey("group.Group", related_name="children", null=True)
    members = models.ManyToManyField("user.User", related_name="groups", null=True, blank=True)
    company = models.ForeignKey(Company, related_name="groups", null=True)
    deleted = models.BooleanField()

    objects = PersistentManager()
    all_objects = models.Manager()

    def __unicode__(self):
        return self.name

    def add_member(self, user):
        self.members.add(user)
        self.save()

        user.invalidate_permission_tree()
        
    def remove_member(self, user):
        self.members.remove(user)
        self.save()

        user.invalidate_permission_tree()

    def get_parents(self):
        groups = []
        if self.parent:
            groups.append(self.parent)
            groups.extend(self.parent.get_parents())
        return groups

    def invalidate_permission_tree_for_members(self):
        for user in self.members.all():
            user.invalidate_permission_tree()

    def grant_role(self, role, object):
        
        object_id = 0
        if not isclass(object):
            object_id = object.id

        content_type = get_content_type_for_model(object)

        act = Role.get_by_name(role)

        perm = Permission(
            role=act,
            group=self,
            content_type=content_type,
            object_id=object_id
        )

        perm.save()

        self.invalidate_permission_tree_for_members()

    def save_without_permissions(self):
        super(Group, self).save()

    def save(self, *args, **kwargs):
        action = "EDIT"
        if not self.id:
            action = "ADD"

        super(Group, self).save()

        if action == "ADD":
            Core.current_user().grant_role("Owner", self)
            admin_group = Core.current_user().get_company_admingroup()
            allemployeesgroup = Core.current_user().get_company_allemployeesgroup()

            if admin_group:
                admin_group.grant_role("Admin", self)

            if allemployeesgroup:
                allemployeesgroup.grant_role("Member", self)


    def get_permissions(self):
        return Permission.objects.filter(group = self)

    def grant_permissions (self, actions, object, **kwargs):
        from_date = None
        to_date = None
        negative = False

        #Set time limits, if set in func-call
        if 'from_date' in kwargs:
            from_date = kwargs['from_date']
        if 'to_date' in kwargs:
            to_date = kwargs['to_date']

        #Set negative to negative value in kwargs
        if 'negative' in kwargs:
            negative = True

        #Make it possible to set permissions for classes
        object_id = 0
        if not isclass(object):
            object_id = object.id

        #Get info about the object
        content_type = get_content_type_for_model(object)

        perm = Permission(
            group=self,
            content_type=content_type,
            object_id=object_id,
            from_date=from_date,
            to_date=to_date,
            negative=negative,
            )
        perm.save()

        for p in Action.get_list_by_names(actions):
            perm.actions.add(p)

        perm.save()

        self.invalidate_permission_tree_for_members()

    def has_permission_to (self, action_str, object, id=None, any=False):
        if isinstance(object, str):
            raise Exception(
                'Argument 2 in user.has_permission_to was a string; The proper syntax is has_permission_to(action, object)!')

        content_type = get_content_type_for_model(object)

        object_id = 0
        if not isclass(object):
            object_id = object.id

        action = Action.get_by_name(action_str)
        allAction = Action.get_by_name('ALL')

        #Checks if the group is permitted
        perms = Permission.objects.filter(content_type=content_type,
                                          object_id=object_id,
                                          group=self,
                                          negative=False,
                                          )

        for perm in perms:
            if action in perm.get_valid_actions():
                return True

            if allAction in perm.get_valid_actions():
                return True

        if self.parent:
            return self.parent.has_permission_to(action, object, id=id, any=any)

        return False