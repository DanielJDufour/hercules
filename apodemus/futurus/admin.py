from django.contrib import admin
from futurus.models import Organization, Membership, Location, Privacy, Donor, Donation, Project, Link, YouTubeVideo, Facebook, Twitter, Person, Step

class OrganizationAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

class ProjectAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('title',)}

class PersonAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Person, PersonAdmin)
#admin.site.register(Organization)
#admin.site.register(Project)
admin.site.register(Step)
admin.site.register(Membership)
admin.site.register(Location)
admin.site.register(Privacy)
admin.site.register(Donor)
admin.site.register(Donation)
admin.site.register(Link)
admin.site.register(YouTubeVideo)
admin.site.register(Facebook)
admin.site.register(Twitter)
