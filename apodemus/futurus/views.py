from django.shortcuts import render, get_object_or_404
from futurus.models import Organization, Project, Person
from django.conf import settings

def index(request):
    return render(request, 'futurus/index.html', {'zone': settings.ZONE})

def find_organizations(request):
    organizations = Organization.objects.all()
    return render(request, 'futurus/find_organizations.html', {'zone': settings.ZONE, 'organizations': organizations})

def find_projects(request):
    projects = Project.objects.all()
    return render(request, 'futurus/find_projects.html', {'projects': projects})

def find_people(request):
    people = Person.objects.all()
    return render(request, 'futurus/find_people.html', {'people': people})

def organization(request, slug):
    organization = get_object_or_404(Organization, slug=slug)
    return render(request, 'futurus/organization.html', {'zone': settings.ZONE, 'organization': organization})

def project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'futurus/project.html', {'zone': settings.ZONE, 'project': project})

def person(request, slug):
    person = get_object_or_404(Person, slug=slug)
    #organizations = person.organization_set.all
    return render(request, 'futurus/person.html', {'zone': settings.ZONE, 'person': person})
