from django.contrib import admin
from futurus import Organization

class OrganizationAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

admin.site.register(Organization, OrganizationAdmin)
