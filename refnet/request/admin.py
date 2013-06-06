from django.contrib import admin
from models import *
from utils.admin import GenericAdmin, GenericAdminStackedInline

class DatabaseAdmin(GenericAdmin):
    model = Database
    list_display = ('__unicode__', 'avaiable_in_vhl')
    list_filter = ('avaiable_in_vhl', )

class RequestConditionAdminStacked(GenericAdminStackedInline):
    model = RequestCondition
    extra = 0

class RequestPublicationTypeAdminStacked(GenericAdminStackedInline):
    model = RequestPublicationType
    extra = 0

class RequestSecundarySubjectAdminStacked(GenericAdminStackedInline):
    model = RequestSecundarySubject
    extra = 0

class RequestCommentAdminStacked(GenericAdminStackedInline):
    model = RequestComment
    extra = 0

class RequestSearchQueryAdminStacked(GenericAdminStackedInline):
    model = RequestSearchQuery
    extra = 0

class RequestAdmin(GenericAdmin):
    model = Request
    inlines = (RequestSecundarySubjectAdminStacked, RequestConditionAdminStacked, 
        RequestPublicationTypeAdminStacked, RequestSearchQueryAdminStacked, RequestCommentAdminStacked)

    fieldsets = (
        (None, {'fields': ('title', 'description', 'deadlines')}),
        ("Referencist", {'fields': ('owner', )}),
        ("Search Subject", {'fields': ('main_subject', )}),
        ("General Search Filters", {'fields': ('year', 'country', 'country_as_subject', 'text_language', )}),
    )

admin.site.register(PublicationType, GenericAdmin)
admin.site.register(Condition, GenericAdmin)

admin.site.register(Database, DatabaseAdmin)
admin.site.register(Request, RequestAdmin)