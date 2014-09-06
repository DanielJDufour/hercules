from django.contrib import admin
from futurus import models

class OrganizationAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Organization, OrganizationAdmin)
