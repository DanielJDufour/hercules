from django.contrib import admin
from futurus.models import Organization, Membership, Biography, Location, Privacy, Donor, Donation, Project, Link, YouTubeVideo, FacebookPage, Twitter

class OrganizationAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Membership)
admin.site.register(Biography)
admin.site.register(Location)
admin.site.register(Privacy)
admin.site.register(Donor)
admin.site.register(Donation)
admin.site.register(Project)
admin.site.register(Link)
admin.site.register(YouTubeVideo)
admin.site.register(FacebookPage)
admin.site.register(Twitter)
