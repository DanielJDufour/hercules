from django.shortcuts import render, get_object_or_404, render_to_response
from futurus.models import Organization, Project, Person
from django.conf import settings
from futurus.forms import UserForm, PersonForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'futurus/index.html', {'zone': settings.ZONE})

@login_required
def edit_person(request, slug):
    person = get_object_or_404(Person, slug=slug)
    if request.user == person.user:
        context = RequestContext(request)
        print "person is ", person
        if request.method == "POST":
            print "request.method == 'POST'"
            form = PersonForm(data=request.POST, instance=person)
            if form.is_valid():
                form.save()
                person.update()
                return HttpResponseRedirect("/people/"+slug)
            else:
                print form.errors
        else:
            form = PersonForm()
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
