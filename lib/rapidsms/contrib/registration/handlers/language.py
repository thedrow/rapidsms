#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
import os

from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler
from rapidsms.models import Contact
from rapidsms.conf import settings

class LanguageHandler(KeywordHandler):
    """
    Allow remote users to set their preferred language, by updating the
    ``language`` field of the Contact associated with their connection.
    """

    keyword = "language|lang"

    def help(self):
        self.respond(self.templates('language_help'))

    def handle(self, text):
        if self.msg.connection.contact is None:
            return self.respond_error(self.templates('language_unregistered'))

        t = text.lower()
        for code, name in settings.LANGUAGES:
            if t != code.lower() and t != name.lower():
                continue

            self.msg.connection.contact.language = code
            self.msg.connection.contact.save()

            return self.respond(self.templates('language_success'),
                language=name)

        return self.respond_error(self.templates('language_unsupported'),
            language=text)
