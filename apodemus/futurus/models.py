from django.db import models
#from django.contrib.gis.db import models as geomodels
from django.db.models.signals import m2m_changed
from django.contrib.auth.models import User

class Organization(models.Model):
    bricked = models.BooleanField(default=False)
    hidden = models.BooleanField(default=True)
    name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to="images/logos", blank=True, null=True)
    entry_created = models.DateTimeField(auto_now_add=True)
    organization_created = models.DateField(null=True, blank=True)
#    members = models.ManyToManyField('Person', blank=True, null=True)
    links = models.ManyToManyField('Link', blank=True)
    projects = models.ManyToManyField('Project', blank=True)
    partners = models.ManyToManyField('Organization', blank=True)
    twitter = models.OneToOneField('Twitter', null=True, blank=True)
    facebook = models.OneToOneField('Facebook', null=True, blank=True)    

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Person(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    pic = models.ImageField(upload_to="images/biopics", blank=True, null=True)
    story = models.TextField(null=True, blank=True)
    hometown = models.ManyToManyField('Location', blank=True)
    twitter = models.OneToOneField('Twitter', null=True, blank=True)
    facebook = models.OneToOneField('Facebook', null=True, blank=True)
    def __str__(self):
        return self.name

class Donor(models.Model):
    user = models.ForeignKey(User, unique=True, null=True)
    donated = models.DecimalField(max_digits=100, default=0.00,decimal_places=2)

class Membership(models.Model):
    organization = models.ForeignKey(Organization)
    person = models.ForeignKey(Person)
    position = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)

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

class Donation(models.Model):
    donor = models.ForeignKey(Donor)
    amount = models.DecimalField(max_digits=100, default=0.00,decimal_places=2)
    recipient = models.ManyToManyField('Organization')

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    steps = models.ManyToManyField('Step', blank=True)

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']

class Step(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.title
    
class Link(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=200, null=True, blank=True)

class YouTubeVideo(models.Model):
    url = models.URLField(null=True, blank=True)

class Facebook(models.Model):
    url = models.URLField(null=True, blank=True)

class Twitter(models.Model):
    handle = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(default = "", null=True, blank=True)

def updatePartners(sender, instance, **kwargs):
    print "updating partners"    
    #instance.save()
    #instance.partners.remove()
    #instance.updatePartners(instance)
    #instance.save()

m2m_changed.connect(updatePartners, sender=Organization.projects.through)
