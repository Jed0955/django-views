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

from .exceptions import NoteExistsException

logger = logging.getLogger(__name__)


class ContextMixin:
    def post_context_data(self, request, *args, **kwargs):
        pass

    def get_context_data(self, request, *args, **kwargs):
        pass


class GetResponseTemplateMixin:
    get_to_template = True
    get_to_json = False
    get_to_redirect = False


class GetResponseJsonMixin:
    get_to_template = False
    get_to_json = True
    get_to_redirect = False


class GetResponseDirectMixin:
    get_to_template = False
    get_to_json = False
    get_to_redirect = True


class PostResponseTemplateMixin:
    post_to_template = True
    post_to_json = False
    post_to_redirect = False


class PostResponseJsonMixin:
    post_to_template = False
    post_to_json = True
    post_to_redirect = False


class PostResponseDirectMixin:
    post_to_template = False
    post_to_json = False
    post_to_redirect = True


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


class PaginationMixin:
    allow_empty_first_page = False
    pagination_class = Paginator
    page_size = 10

    def get_page_obj(self, query_set, page=1):
        pager = self.pagination_class(query_set, self.page_size, allow_empty_first_page=self.allow_empty_first_page)
        page_obj = pager.page(page)
        return page_obj

    def get_page(self, query_set):
        pager = self.pagination_class(query_set, self.page_size, allow_empty_first_page=self.allow_empty_first_page)
        return pager


class JsonResponseMixin:
    json_safe = False

    def response_json(self, context, **kwargs):
        return JsonResponse(context, safe=self.json_safe, **kwargs)


# it must return as
# { status: False, message: 'need user to login'}
# { status: True, message: 'ok'}

class PermissionMixin:
    def get_permission(self, request):
        pass

    def post_permission(self, request):
        pass

    def put_permission(self, request):
        pass

    def delete_permission(self, request):
        pass
