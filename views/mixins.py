# -*- coding: utf-8 -*-
# PROJECT : django-views
# TIME    : 17-5-28 下午5:00
# AUTHOR  : youngershen <younger.x.shen@gmail.com>
import logging
from django.shortcuts import reverse
from django.urls.exceptions import NoReverseMatch
from django.http import \
    HttpResponsePermanentRedirect, \
    HttpResponseRedirect, \
    HttpResponseGone, \
    JsonResponse

logger = logging.getLogger(__name__)


class ContextMixin:
    def post_context_data(self, request, *args, **kwargs):
        pass

    def get_context_data(self, request, *args, **kwargs):
        pass


class RedirectResponseMixin:
    """
      A view that provides a redirect on any GET or POST request.
    """
    permanent = False
    url = None
    pattern_name = None
    query_string = False

    def get_redirect_url(self, request, *args, **kwargs):
        """
        Return the URL redirect to. Keyword arguments from the
        URL pattern match generating the redirect request
        are provided as kwargs to this method.
        """
        if self.url:
            url = self.url.format(kwargs)
        elif self.pattern_name:
            try:
                url = reverse(self.pattern_name, args=args, kwargs=kwargs)
            except NoReverseMatch:
                return None
        else:
            return None

        args = request.META.get('QUERY_STRING', '')
        if args and self.query_string:
            url = "{URL}?{PARAMS}".format(URL=url, PARAMS=args)
        return url

    def redirect(self, request, *args, **kwargs):
        url = self.get_redirect_url(*args, **kwargs)
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


class PermissionMixin:
    pass


class PaginationMixin:
    pass


class FilterMixin:
    pass


class JsonResponseMixin:
    json_safe = False

    def response_json(self, context, **kwargs):
        return JsonResponse(context, safe=self.json_safe, **kwargs)
