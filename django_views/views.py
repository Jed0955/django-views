# -*- coding: utf-8 -*-
# PROJECT : django-views
# TIME    : 17-5-28 下午5:00
# AUTHOR  : youngershen <younger.x.shen@gmail.com>
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from .mixins import \
    ContextMixin, \
    RedirectResponseMixin, \
    JsonResponseMixin, \
    FlashNoteMixin, \
    APIContextMixin, \
    GetResponseTemplateMixin, \
    PostResponseDirectMixin, \
    GetResponseJsonMixin, \
    PostResponseJsonMixin, \
    PermissionMixin


class Generic(
        PermissionMixin,
        GetResponseTemplateMixin,
        PostResponseDirectMixin,
        FlashNoteMixin,
        JsonResponseMixin,
        RedirectResponseMixin,
        ContextMixin,
        TemplateResponseMixin,
        View):

    template_name = None
    json_safe = False
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        context = {}

        permission = self.get_permission(request)

        if permission.get('status', False):
            context.update(self.get_context_data(request, *args, **kwargs))
        else:
            context.update(permission)

        if self.get_to_template:
            return self.render_to_response(context)

        if self.get_to_redirect:
            self.add_note_dict(request, context)
            return self.redirect(request, *args, **kwargs)

        if self.get_to_json:
            return self.response_json(context, **kwargs)

    def post(self, request, *args, **kwargs):
        context = {}

        permission = self.post_permission(request)

        if permission.get('status', False):
            context.update(self.post_context_data(request, *args, **kwargs))
        else:
            context.update(permission)

        if self.post_to_json:
            return self.response_json(context, **kwargs)

        if self.post_to_redirect:
            self.add_note_dict(request, context)
            return self.redirect(request, *args, **kwargs)

        if self.post_to_template:
            return self.render_to_response(context)


class APIGeneric(GetResponseJsonMixin, PostResponseJsonMixin, APIContextMixin, Generic):

    def put(self, request, *args, **kwargs):
        context = {}

        permission = self.put_permission(request)

        if permission.get('status', False):
            context.update(self.put_context_data(request, *args, **kwargs))
        else:
            context.update(permission)

        return self.response_json(context)

    def delete(self, request, *args, **kwargs):
        context = {}

        permission = self.delete_permission(request)

        if permission.get('status', False):
            context.update(self.delete_context_data(request, *args, **kwargs))
        else:
            context.update(permission)

        return self.response_json(context)
