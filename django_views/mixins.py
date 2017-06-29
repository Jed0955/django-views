# -*- coding: utf-8 -*-
# PROJECT : django-views
# TIME    : 17-5-28 下午5:00
# AUTHOR  : youngershen <younger.x.shen@gmail.com>
import logging
from django.core.paginator import Paginator
from django.shortcuts import reverse
from django.urls.exceptions import NoReverseMatch
from django.http import \
    HttpResponsePermanentRedirect, \
    HttpResponseRedirect, \
    HttpResponseGone, \
    JsonResponse
from django.contrib.auth.models import Permission, Group

from .exceptions import NoteExistsException

logger = logging.getLogger(__name__)


class ContextMixin:
    def post_context_data(self, request, *args, **kwargs):
        pass

    def get_context_data(self, request, *args, **kwargs):
        pass


class APIContextMixin(ContextMixin):
    def put_context_data(self, request, *args, **kwargs):
        pass

    def delete_context_data(self, request, *args, **kwargs):
        pass


class RedirectResponseMixin:
    """
      A view that provides a redirect on any GET or POST request.
    """
    permanent = False
    url = None
    pattern_name = None
    query_string = False
    query_string_redirect = False
    redirect_query_name = 'redirect-to'

    def get_redirect_url(self, request, *args, **kwargs):
        """
        Return the URL redirect to. Keyword arguments from the
        URL pattern match generating the redirect request
        are provided as kwargs to this method.
        """
        url = None

        if self.url:
            url = self.url.format(kwargs)
        elif self.pattern_name:
            try:
                url = reverse(self.pattern_name, args=args, kwargs=kwargs)
            except NoReverseMatch:
                pass
        elif self.query_string_redirect:
            url = request.GET.get(self.redirect_query_name)
        else:
            url = request.get_full_path()

        args = request.META.get('QUERY_STRING', '')
        if args and self.query_string:
            url = "{URL}?{PARAMS}".format(URL=url, PARAMS=args)

        return url

    def redirect(self, request, *args, **kwargs):
        url = self.get_redirect_url(request, *args, **kwargs)
        if url:
            if self.permanent:
                return HttpResponsePermanentRedirect(url)
            else:
                return HttpResponseRedirect(url)
        else:
            logger.warning(
                'Gone: %s', request.path,
                extra={'status_code': 410, 'request': request}
            )
            return HttpResponseGone()


class FlashNoteMixin:
    note_key_name = 'note'
    safe = True

    def add_note_dict(self, request, data):
        try:
            note = request.session[self.note_key_name]
        except KeyError:
            note = {}

        note.update(data)
        request.session[self.note_key_name] = note

    def add_note(self, request, name, value, safe=None):
        if not safe:
            safe = self.safe

        try:
            note = request.session[self.note_key_name]
        except KeyError:
            note = {}

        if safe and name and name in note:
            raise NoteExistsException(name)

        note.update({name: value})
        request.session[self.note_key_name] = note

    def get_note(self, request):
        try:
            note = request.session[self.note_key_name]
        except KeyError:
            note = {}
        else:
            del request.session[self.note_key_name]

        return note


class PermissionMixin:
    # group name
    group = []
    # extra func name
    extra = []
    # code name
    user = []
    # redirect when permission check failed
    permission_redirect_url = None

    messages = {
        'user':
            {
            },
        'group':
            {
            },
        'extra':
            {
            }
    }

    def has_permission(self, request):
        status = False
        warnings = \
            {
                'user': {},
                'group': {},
                'extra': {}
            }

        # if we want more permission info with the current user
        # the user must login first
        if self.user_login_permission(request):
            user = request.user
            for perm in self.user:
                try:
                    user.user_permissions.get(codename=perm)
                except Permission.DoesNotExist:
                    status = False
                    warnings['user'].update({perm: self.messages['user'].get(perm, '')})

            for perm in self.group:
                try:
                    user.groups.get(name=perm)
                except Group.DoesNotExist:
                    status = False
                    warnings['group'].update({perm: self.messages['group'].get(perm, '')})

            for perm in self.extra:
                func = getattr(self, perm + '_permission', None)
                if func and callable(func):
                    status = func(request)
                    if not status:
                        message = self.messages['extra'].get(perm, '')
                        warnings.update({'extra': {perm: messages}})
        else:
            message = self.messages['user'].get('login', '')
            warnings.update({'user': {'login': message}})
            status = False

        return {'status': status, 'messages': warnings}

    @staticmethod
    def user_login_permission(request):
        if request.user.is_authenticated():
            return True
        else:
            return False


class HookMixin:
    use_get_hook = True
    use_post_hook = True
    use_put_hook = True
    use_delete_hook = True

    get_hook_force_return = False
    post_hook_force_return = False
    put_hook_force_return = False
    delete_hook_force_return = False

    def get_hook(self, request, context, *args, **kwargs):
        pass

    def post_hook(self, request, context, *args, **kwargs):
        pass

    def put_hook(self, request, context, *args, **kwargs):
        pass

    def delete_hook(self, request, context, *args, **kwargs):
        pass


class PaginationMixin:
    allow_empty_first_page = False
    pagination_class = Paginator
    per_page = 10

    def get_page(self, query_set, page=1):
        pager = self.pagination_class(query_set, self.per_page, allow_empty_first_page=self.allow_empty_first_page)

        page_obj = pager.page(page)
        return page_obj


class FilterMixin:
    pass


class JsonResponseMixin:
    json_safe = False

    def response_json(self, context, **kwargs):
        return JsonResponse(context, safe=self.json_safe, **kwargs)


class GetRedirect:
    get_json = False
    get_redirect = True
    get_template = False


class GetJson:
    get_json = True
    get_redirect = False
    get_template = False


class GetTemplate:
    get_tempalte = True
    get_json = False
    get_redirect = False


class PostJson:
    post_json = True
    post_redirect = False


class PostRedirect:
    post_json = False
    post_redirect = True
