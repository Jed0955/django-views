# -*- coding: utf-8 -*-
# PROJECT : django-views
# TIME    : 17-5-28 下午5:00
# AUTHOR  : youngershen <younger.x.shen@gmail.com>
from django.http import Http404
from django.conf import settings
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from .mixins import \
    ContextMixin, \
    RedirectResponseMixin, \
    JsonResponseMixin, \
    FlashNoteMixin, \
    PermissionMixin, \
    HookMixin, \
    APIContextMixin, \
    GetJson, \
    PostJson, \
    GetTemplate, \
    PostRedirect


class Generic(
        GetTemplate,
        PostRedirect,
        HookMixin,
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
        if self.use_get_hook:
            response = self.get_hook(request, context, *args, **kwargs)
            if self.get_hook_force_return:
                return response

        context.update(self.get_context_data(request, *args, **kwargs))

        if self.get_template:
            return self.render_to_response(context)

        elif self.get_redirect:
            self.add_note_dict(request, context)
            return self.redirect(request, *args, **kwargs)

        elif self.get_json:
            return self.response_json(context, **kwargs)

    def post(self, request, *args, **kwargs):
        context = {}
        if self.use_post_hook:
            response = self.post_hook(request, context, *args, **kwargs)
            if self.post_hook_force_return:
                return response

        context.update(self.post_context_data(request, *args, **kwargs))
        if self.post_json:
            return self.response_json(context, **kwargs)

        elif self.post_redirect:
            self.add_note(request, context)
            return self.redirect(request, *args, **kwargs)
        else:
            return Http404


class APIGeneric(GetJson, PostJson, APIContextMixin, PermissionMixin, Generic):
    use_get_hook = True
    use_post_hook = True
    use_put_hook = True
    use_delete_hook = True


class PermissionGeneric(PermissionMixin, Generic):
    use_get_hook = True
    use_post_hook = True

    def get_hook(self, request, context, *args, **kwargs):
        ret = self.has_permission(request)
        context.update({'permission': ret})

    def post_hook(self, request, context, *args, **kwargs):
        ret = self.has_permission(request)
        context.update({'permission': ret})
