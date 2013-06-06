#! coding: utf-8
from django.db import models
from datetime import datetime

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from utils.models import Generic, Country, Language

class Database(Generic):

    class Meta:
        verbose_name = _("database")
        verbose_name_plural = _("databases")

    name = models.CharField(_("name"), max_length=255)
    avaiable_in_vhl = models.BooleanField(_("database avaiable in VHL?"), default=True)

    def __unicode__(self):
        return unicode(self.name)

class PublicationType(Generic):

    class Meta:
        verbose_name = _("publication type")
        verbose_name_plural = _("publication types")

    name = models.CharField(_("name"), max_length=255)

    def __unicode__(self):
        return unicode(self.name)

class Condition(Generic):

    class Meta:
        verbose_name = _("condition")
        verbose_name_plural = _("conditions")

    name = models.CharField(_("name"), max_length=255)

    def __unicode__(self):
        return unicode(self.name)

class Request(Generic):
    """
    Model principal ref as requisições que um solicitante faz
    Obs:
    - responsável é o creator do generic
    """

    class Meta:
        verbose_name = _("request")
        verbose_name_plural = _("requests")

    owner = models.ForeignKey(User, null=True, blank=True)

    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"))
    deadlines = models.TextField(_("deadlines"))

    main_subject = models.TextField(_("main search subject"))
    # secundary_object é RequestSecundarySubject, para fazer campo repetitivo

    databases = models.ManyToManyField(Database, verbose_name=_("databases"), through="RequestDatabase")

    year = models.CharField(_("publication year"), max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name=_("country of publication"), blank=True, null=True, related_name="+")
    country_as_subject = models.ForeignKey(Country, verbose_name=_("country as subject"), blank=True, null=True)
    text_language = models.ForeignKey(Language, verbose_name=_("text language"), blank=True, null=True)
    publication_types = models.ManyToManyField(PublicationType, verbose_name=_("publication types"), through="RequestPublicationType", blank=True, null=True)
    conditions = models.ManyToManyField(Condition, verbose_name=_("publication types"), through="RequestCondition", blank=True, null=True)

    def __unicode__(self):
        return unicode(self.title)

class RequestDatabase(Generic):
    """
    Tabela de Ligação N:N de requests e databases
    """

    class Meta:
        verbose_name = _("database in request")
        verbose_name_plural = _("databases in request")

    request = models.ForeignKey("Request", verbose_name=_("request"))
    database = models.ForeignKey("Database", verbose_name=_("database"))

class RequestCondition(Generic):
    """
    Tabela de Ligação N:N de requests e conditions
    """

    class Meta:
        verbose_name = _("database in request")
        verbose_name_plural = _("databases in request")

    request = models.ForeignKey("Request", verbose_name=_("request"))
    condition = models.ForeignKey("Condition", verbose_name=_("condition"))

class RequestPublicationType(Generic):
    """
    Tabela de Ligação N:N de requests e publication types
    """

    class Meta:
        verbose_name = _("publication type in request")
        verbose_name_plural = _("publication types in request")

    request = models.ForeignKey("Request", verbose_name=_("request"))
    publication_type = models.ForeignKey("PublicationType", verbose_name=_("publication type"))

class RequestSecundarySubject(Generic):
    """
    Model responsável por 1:N dos assuntos secundários da pesquisa
    """

    class Meta:
        verbose_name = _("secundary object")
        verbose_name_plural = _("secundary objects")

    request = models.ForeignKey(Request)
    subject = models.TextField(_("secondary search subject"), null=True, blank=True)

    def __unicode__(self):
        return unicode(self.subject)

class RequestComment(Generic):
    """
    Model responsável por 1:N dos comentários de uma solicitação
    """

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

    request = models.ForeignKey(Request)
    comment = models.TextField(_("comment"))

    def __unicode__(self):
        return unicode(self.comment)

class RequestSearchQuery(Generic):
    """
    """

    class Meta:
        verbose_name = _("search query")
        verbose_name_plural = _("search queries")

    request = models.ForeignKey(Request)
    search_query = models.CharField(_("search query"), max_length=255)
    is_approved_by_user = models.BooleanField(_("is approved by user?"))
    likes = models.IntegerField(_("likes"), default=0)

    def __unicode__(self):
        return unicode(self.search_query)
