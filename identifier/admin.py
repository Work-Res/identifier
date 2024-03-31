from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from base_module.constants import DEFAULT_BASE_FIELDS

from .admin_site import identifier_admin
from .models import IdentifierModel

audit_fields = ('user_created', 'user_modified',
                'created', 'modified', 'hostname_created', 'hostname_modified')

audit_fieldset_tuple = (
    'Audit', {
        'classes': ('collapse',),
        'fields': audit_fields})

@admin.register(IdentifierModel, site=identifier_admin)
class IdentifierModelAdmin(admin.ModelAdmin):

    fieldsets = (
        [None, {
            'fields': (
                'identifier',
                'address_code',
                'name',
                'dob',
                'model',
                'sequence_number',
                'identifier_type',
                'linked_identifier',
                'identifier_prefix')}],
        audit_fieldset_tuple,
    )

    list_display = (
        'identifier', 'identifier_type', 'address_code', 'dob',
        'linked_identifier', 'created',
        'user_created', 'hostname_created')
    list_filter = ('identifier_type', 'name', 'address_code',
                   'created', 'user_created')
    search_fields = ('identifier', 'linked_identifier')

    def get_readonly_fields(self, request, obj=None):
        return (
            'identifier',
            'address_code',
            'name',
            'dob',
            'model',
            'sequence_number',
            'identifier_type',
            'linked_identifier',
            'identifier_prefix') + tuple(DEFAULT_BASE_FIELDS)
