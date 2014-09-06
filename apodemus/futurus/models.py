from django.db import models
#from django.contrib.gis.db import models as geomodels

class Organization(models.Model):
    bricked = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to="futurus/static/futurus/images/", blank=True, null=True)
    notable_members = models.ManyToManyField('Person')
    entry_created = models.DateTimeField()
    organization_created = models.DateTimeField(null=True, blank=True)
    links = models.ManyToManyField('Link')
    projects = models.ManyToManyField('Project')
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Person(models.Model):
    biography = models.OneToOneField('Biography')

class Membership(models.Model):
    organization = models.ForeignKey(Organization)
    person = models.ForeignKey(Person)
    position = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)

class Biography(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    hometown = models.ManyToManyField('Location')

    def __str__(self):
        return self.name + "'s Biography"
    class Meta:
        ordering = ['name']

class Location(models.Model):
    name = models.CharField(max_length=200)
#    coords = geomodels.PointField()
#    polygon = geomodels.PolygonField()

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
    
class Privacy(models.Model):
    hidden = models.BooleanField(default=True)

class Donor(models.Model):
    donated = models.DecimalField(max_digits=100, default=0.00,decimal_places=2)

class Donation(models.Model):
    donor = models.ForeignKey(Donor)
    amount = models.DecimalField(max_digits=100, default=0.00,decimal_places=2)
    recipient = models.ManyToManyField('Organization')

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']
    
class Link(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=200, null=True, blank=True)

class YouTubeVideo(models.Model):
    url = models.URLField(null=True, blank=True)

class FacebookPage(models.Model):
    url = models.URLField(null=True, blank=True)

class Twitter(models.Model):
    handle = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(default = "", null=True, blank=True)
