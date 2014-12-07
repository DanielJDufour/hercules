from django.shortcuts import render, get_object_or_404, render_to_response
from django.conf import settings
from futurus.forms import CreateOrgForm, EditPersonForm, FacebookForm, LinkedInForm, UserForm, PersonForm, WikiForm
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from futurus.models import Facebook, LinkedIn, Membership, Organization, Person, Project, Twitter, Wiki


def create_organization(request):
    #checks to see if a user has created a profile (i.e. person object)
    # if they haven't, they gotta do that first
    if request.user.person:
        if request.method == 'POST':
            form = CreateOrgForm(data=request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                abbreviation = form.cleaned_data['abbreviation']
                mission = form.cleaned_data['mission']
                organization_created = form.cleaned_data['organization_created']
                
                org = Organization.objects.create(bricked=False, hidden=False, name=name, abbreviation=abbreviation, slug=slugify(name), mission=mission, organization_created=organization_created)

                if 'logo' in request.FILES:
                    org.logo = request.FILES['logo']
                
                owners = form.cleaned_data['owners']
                print 1/0
                if owners:
                    pass    

                members = form.cleaned_data['members']

                facebook_url = form.cleaned_data['facebook']
                if facebook_url:
                    facebook = Facebook(url=facebook_url)
                    facebook.save()
                    organization.facebook = facebook

                linkedin_url = form.cleaned_data['linkedin']
                if linkedin_url:
                    linkedin = LinkedIn(url=linkedin_url)
                    linkedin.save()
                    organization.linkedin = linkedin

                twitter_handle = form.cleaned_data['twitter']
                if twitter_handle:
                    print "person didn't have a twitter, so we're creating one"
                    twitter = Twitter(handle=twitter_handle)
                    twitter.save()
                    organization.twitter = twitter
                
                links = form.cleaned_data['links']
                if links:
                    pass

                wiki_url = form.cleaned_data['wiki']
                if wiki_url:
                    pass
                organization.save()
                organization.update()
                return HttpResponseRedirect("/organizations/"+organization.slug)
            else:
                print form.errors
        else:
            person = request.user.person
            people = Person.objects.all()
            return render(request, 'futurus/create_organization.html', {'zone': settings.ZONE, 'person': person, 'people': people})

def index(request):
    numberOfUsers = User.objects.count()
    return render(request, 'futurus/index.html', {'zone': settings.ZONE, 'numberOfUsers': numberOfUsers})

@login_required
def edit_person(request, slug):
    person = get_object_or_404(Person, slug=slug)
    print "person is ", person
    
    if request.user == person.user:
        context = RequestContext(request)
    
        if request.method == "POST":
            print "request.method == 'POST'"
            print "request.POST is ", request.POST
            print "request.POST is", request.POST
            form = EditPersonForm(data=request.POST)
            if form.is_valid():
                person.name = form.cleaned_data['name']
                person.story = form.cleaned_data['story']
                person.hometown = form.cleaned_data['hometown']
                if 'pic' in request.FILES:
                    person.pic = request.FILES['pic']

                facebook_url = form.cleaned_data['facebook']
                if person.facebook:
                    person.facebook.url = facebook_url
                elif facebook_url:
                    facebook = Facebook(url=facebook_url)
                    facebook.save()
                    person.facebook = facebook

                linkedin_url = form.cleaned_data['linkedin']
                if person.linkedin:
                    person.linkedin.url = linkedin_url
                elif linkedin_url:
                    linkedin = LinkedIn(url=linkedin_url)
                    linkedin.save()
                    person.linkedin = linkedin

                twitter_handle = form.cleaned_data['twitter']
                if person.twitter:
                    print "person already had a twitter, so we're going to update the handle"
                    person.twitter.handle = twitter_handle
                elif twitter_handle:
                    print "person didn't have a twitter, so we're creating one"
                    twitter = Twitter(handle=twitter_handle)
                    twitter.save()
                    person.twitter = twitter
                
                person.save()
                person.update()
                return HttpResponseRedirect("/people/"+slug)
            else:
                print form.errors
        else:
            form = EditPersonForm()
        return render(request, 'futurus/edit_person.html', {'zone': settings.ZONE, 'person': person, 'form': form})
    else: #this isn't the current user's profile
        return HttpResponseRedirect("/people/"+slug)

def find_organizations(request):
    organizations = Organization.objects.all()
    return render(request, 'futurus/find_organizations.html', {'zone': settings.ZONE, 'organizations': organizations})

def find_projects(request):
    projects = Project.objects.all()
    return render(request, 'futurus/find_projects.html', {'projects': projects})

def find_people(request):
    people = Person.objects.all()
    return render(request, 'futurus/find_people.html', {'people': people})

def memberships(request, slug):
    person = get_object_or_404(Person, slug=slug)
    memberships = Membership.objects.filter(person=person)
    print "memberships are ", memberships
    return render(request, 'futurus/memberships.html', {'zone': settings.ZONE, 'memberships': memberships})


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


def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.username = user.email
            user.save()

            # Update our variable to tell the template registration was successful.
            registered = True

            # Now auto-login after registering
            # See: http://stackoverflow.com/questions/2787650/manually-logging-in-a-user-without-password
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render_to_response(
            'futurus/register.html',
            {'user_form': user_form, 'registered': registered},
            context)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        email = request.POST['email']
        password = request.POST['password']

        # Wrote custom login with email, not username
        try:
            user = User.objects.get(email=email)
        except:
            # no user by that email found
            print "There is no user by that email."
            return render_to_response('futurus/login.html', {}, context)
        if user and user.check_password(password) and user.is_active:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('futurus/login.html', {}, context)


# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

def tasks(request):

    # if facebook task doesn't exist create it
    if not request.user.person.tasks.filter(short_name="person:facebook").exists():
        "print Facebook tasks does not exist yet, so create it"
        request.user.person.tasks.create(short_name="person:facebook", name="Add Facebook to Your Profile", description="Adding your Facebook account will help people understand who you are.", completed="False")

    if request.user.person.facebook_url:
        print "user has added Facebook to their profile"
        request.user.person.tasks.filter(short_name="person:facebook").update(completed=True)
    else:
        print "user has not yet added Facebook to their profile"
        request.user.person.tasks.filter(short_name="person:facebook").update(completed=False)

    tasksFromPerson = request.user.person.tasks.all()
    print "tasksFromPerson is ", tasksFromPerson
    #print get_object_or_404(Person, slug=slug)
    #if request.user == person.user:

    #tasksFromOrg = Organizations.objects.filter(
    tasks = tasksFromPerson
    print "tasks are ", tasks
    tasks_incomplete = tasks.filter(completed=False)
    print "tasks_incomplete is", tasks_incomplete
    tasks_completed = tasks.filter(completed=True)
    print "tasks_completed is", tasks_completed
    return render(request, 'futurus/tasks.html', {'zone': settings.ZONE, 'tasks_incomplete': tasks_incomplete, 'tasks_completed': tasks_completed})
