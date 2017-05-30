# -*- coding: utf-8 -*-
# PROJECT : django-views
# TIME    : 17-5-28 下午5:00
# AUTHOR  : youngershen <younger.x.shen@gmail.com>
from django.http import Http404
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from .mixins import \
    ContextMixin, \
    RedirectResponseMixin,\
    JsonResponseMixin, \
    FlashNoteMixin


class Generic(FlashNoteMixin, JsonResponseMixin, RedirectResponseMixin, ContextMixin, TemplateResponseMixin, View):

    post_json = False
    post_redirect = True
    get_json = False
    get_redirect = False
    get_template = True
    template_name = None
    json_safe = False
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):

        context = self.get_context_data(request, *args, **kwargs)

        if self.get_template:
            return self.render_to_response(context)

        elif self.get_redirect:
            return self.redirect(request, *args, **kwargs)

        elif self.get_template:
            return self.response_json(context, **kwargs)

    def post(self, request, *args, **kwargs):

        context = self.post_context_data(request, *args, **kwargs)
        if self.post_json:
            return self.response_json(context, **kwargs)

        elif self.post_redirect:
            return self.redirect(request, *args, **kwargs)

        else:
            return Http404

"""

common view

get -> return a template

post -> return a json obj or redirect

"""
