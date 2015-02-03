from datetime import datetime
from django.conf import settings
from django.db import models
#from django.contrib.gis.db import models as geomodels
from django.db.models.signals import m2m_changed, post_save
from django.contrib.auth.models import User
import os, re, requests
from bs4 import BeautifulSoup
#from futurus.views import __name__

class Donation(models.Model):
    donor = models.ForeignKey('Donor', null=True, blank=True)
    step = models.ForeignKey('Step', null=True, blank=True)
    amount = models.DecimalField(max_digits=100, default=0.00,decimal_places=2)

    datetime = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "donation of " + str(self.amount) + " from " + self.donor.user.email + " to " + self.step.name
    class Meta:
        ordering = ['datetime']

class Donor(models.Model):
    user = models.OneToOneField(User, unique=True, null=True)
    donated = models.DecimalField(max_digits=100, default=0.00,decimal_places=2)
    def __str__(self):
        try:
            return self.user.person.name + " (" + self.user.email + ")"
        except:
            return self.user.email


class Facebook(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    def update(self):
        if self.url == "":
            self.title = ""
        else:
            try:
                self.title = BeautifulSoup(requests.get(self.url).content).title.string.split(" -")[0].strip().split(" |")[0].strip() 
            except Exception as e:
                print e
            self.save()
    def __str__(self):
        if self.title:
            return self.title
        elif self.url:
            return self.url
        else:
            return "[unknown Facebook objects]"
    class Meta:
        ordering = ['title']  

class Link(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']

class LinkedIn(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    def __str__(self):
        if self.title:
            return self.title
        elif self.url:
            return self.url
        else:
            return "unnamed linkedin obj"
    class Meta:
        ordering = ['title']  

class Location(models.Model):
    name = models.CharField(max_length=200)
#    coords = geomodels.PointField()
#    polygon = geomodels.PolygonField()

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
 

class Membership(models.Model):
    organization = models.ForeignKey('Organization')
    person = models.ForeignKey('Person')
    position = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)


class Organization(models.Model):
    abbreviation = models.CharField(max_length=200, blank=True, null=True)
    abbreviation_ar = models.CharField(max_length=200, blank=True, null=True)
    bricked = models.NullBooleanField(default=False, null=True, blank=True)
    entry_created = models.DateTimeField(auto_now_add=True)
    facebook = models.OneToOneField('Facebook', blank=True, null=True)
    hidden = models.NullBooleanField(default=True, null=True, blank=True)
    linkedin = models.OneToOneField('LinkedIn', null=True, blank=True) 
    links = models.ManyToManyField('Link', blank=True)
    logo = models.ImageField(upload_to="images/logos", blank=True, null=True)
    members = models.ManyToManyField('Person', through='Membership')
    mission = models.TextField(null=True, blank=True)
    mission_ar = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    name_ar = models.CharField(max_length=200, null=True, blank=True)
    organization_created = models.DateField(null=True, blank=True)
    owners = models.ManyToManyField(User, blank=True, null=True)
    partners = models.ManyToManyField('Organization', blank=True)
    projects = models.ManyToManyField('Project', blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    #islamic year.... maybe add a method to the DateField that returns year month day of Islamic Calendar
    #tasks = models.ManyToManyField('Task', blank=True)
    twitter = models.OneToOneField('Twitter', null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    wiki = models.OneToOneField('Wiki', blank=True, null=True)


    def update(self):
        self.facebook.update()
        self.wiki.update()
    def __str__(self):
        if self.name:
            return self.name
        else:
            return "Un-named Org"
    class Meta:
        ordering = ['name']

class PageView(models.Model):
    user = models.ForeignKey(User, unique=False, blank=True, null=True)
    session = models.CharField(max_length=200, null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    page = models.CharField(max_length=200, null=True, blank=True)

class Person(models.Model):
    user = models.OneToOneField(User, blank=True, null=True)
    notable = models.NullBooleanField(blank=True, null=True, default=False)
    name = models.CharField(max_length=200)
    name_ar = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(unique=True)
    pic = models.ImageField(upload_to="images/biopics", blank=True, null=True)
    story = models.TextField(null=True, blank=True)
    story_ar = models.TextField(null=True, blank=True)
    hometown = models.CharField(max_length=200, null=True, blank=True)
    hometown_ar = models.CharField(max_length=200, null=True, blank=True)
    facebook = models.OneToOneField('Facebook', blank=True, null=True)
    linkedin = models.OneToOneField('LinkedIn', null=True, blank=True)
    twitter = models.OneToOneField('Twitter', null=True, blank=True)
    wiki = models.OneToOneField('Wiki', blank=True, null=True)
#    wiki_ar = models.OneToOneField('Wiki', blank=True, null=True)

    #tasks = models.ManyToManyField('Task', blank=True)

    def update(self):
        if self.facebook:
            self.facebook.update()
        if self.wiki:        
            self.wiki.update()
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Picture(models.Model):
    pic = models.ImageField(upload_to="images/pictures", blank=True, null=True)
    caption = models.CharField(max_length=200, null=True, blank=True)
    date_captured = models.DateTimeField(null=True, blank=True)

class Preferences(models.Model):
    CHOICES = [("en","English"), ("ar","Arabic"),("ku","Kurdish")]
    language = models.CharField(max_length=2, choices=CHOICES, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    def __str__(self):
        return self.user.username
    class Meta:
        ordering = ['user']

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    steps = models.ManyToManyField('Step', blank=True)
    money_requested = models.DecimalField(max_digits=100, default=0.00,decimal_places=2)
    money_donated = models.DecimalField(max_digits=100, default=0.00,decimal_places=2)
    percent_funded = models.DecimalField(max_digits=100, default=0.00, decimal_places=2)

    def __str__(self):
        return self.title
    def calc_money(self):
        self.money_requested = sum([step.money_requested for step in self.steps.all()])
        self.money_donated = sum([step.money_donated for step in self.steps.all()])
        self.percent_funded = (self.money_donated * 100)/self.money_requested if self.money_requested > 0 else 0
        self.save()
    class Meta:
        ordering = ['title']

class Step(models.Model):
    name = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    money_requested = models.DecimalField(max_digits=100, default=0.00,decimal_places=2)
    money_donated = models.DecimalField(max_digits=100, default=0.00,decimal_places=2)
    order = models.IntegerField(null=True, blank=True)
    percent_funded = models.DecimalField(max_digits=100, default=0.00, decimal_places=2)
    pictures = models.ManyToManyField('Picture', blank=True)
    def __str__(self):
        return self.name
    def calc_money(self):
        self.percent_funded = (self.money_donated * 100)/self.money_requested if self.money_requested > 0 else 0
        self.save()
    class Meta:
        ordering = ['order']

class Task(models.Model):
    user = models.ForeignKey(User, unique=False, blank=True, null=True)
   # short_name = models.CharField(max_length=200, null=True, blank=True, default="person:facebook")
    name = models.CharField(max_length=200, null=True, blank=True)
    #description = models.CharField(max_length=200, null=True, blank=True)
    completed = models.NullBooleanField(null=True, blank=True)
    #completed_at = models.DateTimeField(null=True, blank=True)
    url = models.URLField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.name

class Text(models.Model):
    CHOICES_LANGUAGE = (('en',"English"),('ar',"Arabic"))
    language = models.CharField(choices=CHOICES_LANGUAGE, max_length=200)

    name = models.CharField(max_length=200, unique=False)
    text = models.TextField()

    #CHOICES_VIEW = views
    template = models.CharField(max_length=200)

    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return " ["+self.template + ":" + self.language + "] " + self.name

class TeamMember(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to="images", null=True, blank=True, default=settings.STATIC_URL+"skyshaker/img/user/default.jpg")
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Twitter(models.Model):
    handle = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    def __str__(self):
        if self.handle:
            return "@" + self.handle
        elif self.url:
            return self.url
        else:
            return "[unhandled twitter object]"
    class Meta:
        ordering = ['handle']  

class Video(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    embed = models.TextField(default="",null=True,blank=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']

class Wiki(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    def update(self):
        if self.url == "":
            self.title = ""
        else:
            self.title = re.search('(?<=wiki\/)\w+', self.url).group(0)
            self.save()
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']

def updatePartners(sender, instance, **kwargs):
    print "updating partners"    
    #instance.save()
    #instance.partners.remove()
    #instance.updatePartners(instance)
    #instance.save()

def updateVideoEmbed(sender, instance, **kwargs):
    instance_url = str(instance.url)
    if 'youtube' in instance_url:
        idOfYoutubeVideo = re.search('(?<=v=)\w+', instance_url).group(0)
        instance.embed = '<iframe width="100%" height="315" src="//www.youtube.com/embed/' + idOfYoutubeVideo + '" frameborder="0" allowfullscreen></iframe>'
    elif 'vimeo' in instance.url:
        idOfVimeoVideo = re.search('(?<=com/)\w+', instance_url).group(0)
        instance.embed = '<iframe src="//player.vimeo.com/video/' + idOfVimeoVideo + '" width="500" height="281" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>'
    post_save.disconnect(updateVideoEmbed, sender=Video)
    instance.save()
    post_save.connect(updateVideoEmbed, sender=Video)


m2m_changed.connect(updatePartners, sender=Organization.projects.through)
post_save.connect(updateVideoEmbed, sender=Video)
