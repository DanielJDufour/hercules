from django.contrib import admin
from futurus.models import Donation, Donor, Facebook, Link, LinkedIn, Location, Membership, Organization, Person, Privacy, Project, Step, Task, Twitter, Video, Wiki

class OrganizationAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

class ProjectAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('title',)}

class PersonAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

admin.site.register(Donation)
admin.site.register(Donor)
admin.site.register(Facebook)
admin.site.register(Link)
admin.site.register(LinkedIn)
admin.site.register(Location)
admin.site.register(Membership)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Privacy)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Step)
admin.site.register(Task)
admin.site.register(Twitter)
admin.site.register(Video)
admin.site.register(Wiki)
