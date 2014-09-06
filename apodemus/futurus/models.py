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

class Membership(models.Model):
    organization = models.ForeignKey(Organization)
    person = models.ForeignKey(Person)
    position = models.CharField(null=True, blank=True)
    description = models.CharField(null=True, blank=True)

class Biography(models.Model)
    name = models.CharField(null=True, blank=True)
    hometown = models.ManyToManyField(Location)

class Location(models.Model):
    name = models.CharField()
    coords = geomodels.PointField()
    polygon = geomodels.PolygonField()
    
def Privacy(models.Model):
    hidden = models.BooleanField(default=True)

def Donor(models.Model):
    donated = models.DecimalField(default=0.00,decimal_places=2)
    donations = models.ManyToOneField(Donation)

def Donation(models.Model):
    donor = ForeignKey(Donor)
    amount = models.DecimalField(default=0.00,decimal_places=2)
    recipient = models.ManyToManyField(Organization)

def Project(models.Model):
    title = models.CharField()
    description = models.CharField(null=True, blank=True)
    
def Link(models.Model):
    url = URLField()
    title = Model.Charfield(null=True, blank=True)

def YouTubeVideo(models.Model)
    url = Models.URLField(null=True, blank=True)

def FacebookPage(models.Model):
    url = Models.URLField(null=True, blank=True)

def Twitter(models.Model):
    handle = Models.CharField(null=True, Blank=True)
    url = Models.URLField(default = "", null=True, blank=True)
