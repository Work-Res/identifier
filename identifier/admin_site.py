from django.contrib.admin.sites import AdminSite


class IdentifierAdminSite(AdminSite):
    site_header = 'Identifier'
    site_title = 'Identifier'
    index_title = 'Identifier'


identifier_admin = IdentifierAdminSite(name='identifier_admin')
