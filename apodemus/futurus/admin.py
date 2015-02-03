from django.contrib import admin
from futurus import models

class OrganizationAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

class ProjectAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('title',)}

class PersonAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

admin.site.register(models.Donation)
admin.site.register(models.Donor)
admin.site.register(models.Facebook)
admin.site.register(models.Link)
admin.site.register(models.LinkedIn)
admin.site.register(models.Location)
admin.site.register(models.Membership)
admin.site.register(models.Organization, OrganizationAdmin)
admin.site.register(models.PageView)
admin.site.register(models.Person, PersonAdmin)
admin.site.register(models.Picture)
admin.site.register(models.Preferences)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Step)
admin.site.register(models.Task)
admin.site.register(models.Text)
admin.site.register(models.Twitter)
admin.site.register(models.Video)
admin.site.register(models.Wiki)
