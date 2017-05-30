# -*- coding: utf-8 -*-
# PROJECT : haval
# TIME    : 17-5-30 下午4:11
# AUTHOR  : youngershen <younger.x.shen@gmail.com>
from django.utils.translation import ugettext as _


class NoteExistsException(Exception):
    message = _('name {NAME} exists in the note buffer')
    name = None

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.message.format(NAME=self.name)
