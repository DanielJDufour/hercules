from django.db import models
from django.contrib.gis.db import models as geomodels

class Organization(models.Model):
    bricked = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    name = models.CharField()
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to="futurus/static/futurus/images/", blank=True, null=True)
    notable_members = models.ManyToManyField(Person)
    entry_created = models.DateTimeField()
    organization_created = models.DateTimeField(null=True, blank=True)
    links = models.ManyToManyField(Link)
    projects = models.ManyToManyField(Project)
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Membership(models.Model):
    organization = models.ForeignKey(Organization)
    person = models.ForeignKey(Person)
    position = models.CharField(null=True, blank=True)
    description = models.CharField(null=True, blank=True)

class Biography(models.Model)
    name = models.CharField(null=True, blank=True)
    hometown = models.ManyToManyField(Location)

    def __str__(self):
        return self.name + "'s Biography'
    class Meta:
        ordering = ['name']

class Location(models.Model):
    name = models.CharField()
    coords = geomodels.PointField()
    polygon = geomodels.PolygonField()

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
    
class Privacy(models.Model):
    hidden = models.BooleanField(default=True)

class Donor(models.Model):
    donated = models.DecimalField(default=0.00,decimal_places=2)
    donations = models.ManyToOneField(Donation)

class Donation(models.Model):
    donor = ForeignKey(Donor)
    amount = models.DecimalField(default=0.00,decimal_places=2)
    recipient = models.ManyToManyField(Organization)

class Project(models.Model):
    title = models.CharField()
    description = models.CharField(null=True, blank=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']
    
class Link(models.Model):
    url = URLField()
    title = Model.Charfield(null=True, blank=True)

class YouTubeVideo(models.Model)
    url = Models.URLField(null=True, blank=True)

class FacebookPage(models.Model):
    url = Models.URLField(null=True, blank=True)

class Twitter(models.Model):
    handle = Models.CharField(null=True, Blank=True)
    url = Models.URLField(default = "", null=True, blank=True)
