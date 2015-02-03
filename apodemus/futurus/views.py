from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, get_object_or_404, render_to_response
from django.conf import settings
from futurus.forms import ChangeLanguageForm, CreateOrgForm, CreatePersonForm, EditOrgForm, EditPersonForm, FacebookForm, LinkedInForm, UserForm, PersonForm, WikiForm
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from futurus import forms, models
from futurus.models import Donation, Facebook, LinkedIn, Membership, Organization, PageView, Person, Project, Task, Twitter, Wiki
import datetime, json, requests, sys

def about(request):
    language = get_language(request)
    return render(request, 'futurus/about.html', {'language': language, 'texts_header': get_texts("header", language), 'texts': get_texts("about", language)})

def advise(request):

    language = get_language(request)

    if request.method == 'POST':
        print "data", request.POST
        form = forms.AdviseForm(data=request.POST)

        if form.is_valid():
            print "form is valid"
            print "cleaned_data is", form.cleaned_data            
            for text_id in form.cleaned_data:
                print "changing text of",text_id," to ", form.cleaned_data[text_id]
                textObj = models.Text.objects.get(id=text_id)
                textObj.text=form.cleaned_data[text_id]
                textObj.save()
        else:
            print "NOT valid is form because:"
            print form.errors

    qsOfTexts = models.Text.objects.filter(language=language).exclude(description="")
    templates = qsOfTexts.values_list('template', flat=True).distinct()
    print "templates are", templates
    dictOfTexts = {}
    listOfTexts = []

    for template in templates:
        print "for template", template
        url = "http://localhost:8000/translate"
        #get url for the template; don't store in db
        if template != "":
            textsForTemplate = qsOfTexts.filter(template=template)
            print "     textsForTemplate is", textsForTemplate
            dictOfTexts[template] = []
            for text in textsForTemplate:
                dictOfTexts[template].append({'id': text.id, 'description': text.description, 'text': text.text}) 

    print "dictOfTexts is", listOfTexts


    return render(request, 'futurus/advise.html', {'language': language, 'texts': dictOfTexts, 'texts_header': get_texts("header", language)})

@login_required
def account(request):
    language = get_language(request)
    user = request.user
    return render(request, 'futurus/account.html', {'language': language, 'user': user, 'texts_header': get_texts("header", language)})

def browse_organizations(request):
    language = get_language(request)
    organizations = Organization.objects.all().exclude(name="").exclude(logo="")
    return render(request, 'futurus/browse_organizations.html', {'language': language, 'organizations': organizations, 'texts_header': get_texts("header", language)})

def browse_people(request):
    language = get_language(request)
    people = Person.objects.all().exclude(name="").exclude(user=None).exclude(pic="")

    listOfDonorIds = Donation.objects.all().values_list('donor_id', flat=True)
    donors = []
    newUsers = []
    activeUsers = []
    for person in people:

        # check to see if should add to donor list
        try:
            if person.user.donor.id in listOfDonorIds:
                donors.append(person)
        except Exception as e:
            print e


        # check to see if should to joined recently list
        try:
            if person.user.date_joined:
               newUsers.append(person) 
        except Exception as e:
            print e


        # check to see if active users
        try:
            if person.user.last_login:
                activeUsers.append(person)
        except: pass

    return render(request, 'futurus/browse_people.html', {'language': language, 'people': people, 'donors': donors, 'newUsers': newUsers, 'activeUsers': activeUsers, 'texts_header': get_texts("header", language)})

def browse_projects(request):
    language = get_language(request)
    projects = Project.objects.all().exclude(title="")
    return render(request, 'futurus/browse_projects.html', {'language': language, 'projects': projects, 'texts_header': get_texts("header", language)})

@login_required
def create_organization(request):
    language = get_language(request)
    #checks to see if a user has created a profile (i.e. person object)
    # if they haven't, they gotta do that first
    if request.user.person:

        language = get_language(request)
        texts = get_texts("create_organization", language)

        if request.method == 'POST':
            print "request.POST:\n", request.POST
            form = CreateOrgForm(data=request.POST)
            if form.is_valid():
                print "form is valid!"
                print "form.cleaned_data is ", form.cleaned_data
                abbreviation = form.cleaned_data['abbreviation']
                name = form.cleaned_data['name']
                mission = form.cleaned_data['mission']
                organization_created = form.cleaned_data['organization_created']
                website = form.cleaned_data['website']
                
                org = Organization.objects.create(bricked=False, hidden=False, name=name, abbreviation=abbreviation, slug=slugify(name), mission=mission, organization_created=organization_created, website=website)

                if 'logo' in request.FILES:
                    org.logo = request.FILES['logo']
               
                
                print "org is", org

                print type(form.cleaned_data['owners'])
 
                for owner in form.cleaned_data['owners']:
                    org.owners.add(owner)

                for member in form.cleaned_data['members']:
                    Membership.objects.create(organization=org, person=request.user.person).save()

                print "org is", org
              


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
                user = request.user
                person = user.person
                people = Person.objects.exclude(user__isnull=True).exclude(id=person.id)
                return render(request, 'futurus/create_organization.html', {'language': language, 'person': person, 'people': people, 'user': user, 'form': form, 'texts': texts, 'texts_header': get_texts("header", language)})
        else:
            user = request.user
            print "user is ", user
            person = user.person
            print "person is ", person
            people = Person.objects.exclude(user__isnull=True).exclude(id=person.id)
            print "people is", people
            return render(request, 'futurus/create_organization.html', {'language': language, 'person': person, 'people': people, 'user': user, 'texts': texts, 'texts_header': get_texts("header", language)})

def change_language(request):
    print "starting change_language"
    if request.method == 'POST':
        print "request.method == 'POST'"
        form = ChangeLanguageForm(data=request.POST)
        if form.is_valid():
            print "form.cleaned_data is", form.cleaned_data
            newLanguage = form.cleaned_data['language']
            if request.user.is_authenticated():
                preferences = models.Preferences.objects.get_or_create(user = request.user)[0]
                preferences.language = newLanguage
                preferences.save()
            else:
                request.session['language'] = newLanguage 

    ## reload page here, so page in new language pops up
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def create_person(request):
    print "checking to see if user has created a person (i.e. profile)"
    language = get_language(request)
    if Person.objects.filter(user=request.user):
        return HttpResponseRedirect("/people/"+request.user.person.slug+"/edit")
    else:
        if request.method == 'POST':
            form = CreatePersonForm(data=request.POST)
            if form.is_valid():
                print "form.cleaned_data is", form.cleaned_data
                name = form.cleaned_data['name']
                story = form.cleaned_data['story']
                hometown = form.cleaned_data['hometown']
                slug = slugify(name)

                person = Person.objects.create(name=name, story=story, hometown=hometown, slug=slug)

                person.user = request.user

                if form.cleaned_data['pic_choice'] == "FromComputer":
                    if 'pic' in request.FILES:
                        person.pic = request.FILES['pic']
                elif form.cleaned_data['pic_choice'] == 'FromInternet':
                    try:
                       person.pic = requests.get(form.cleaned_data['pic']) 
                    except Exception as e:
                        print e
                person.save()

                facebook_url = form.cleaned_data['facebook']
                if facebook_url:
                    facebook = Facebook(url=facebook_url)
                    facebook.save()
                    person.facebook = facebook

                linkedin_url = form.cleaned_data['linkedin']
                if linkedin_url:
                    linkedin = LinkedIn(url=linkedin_url)
                    linkedin.save()
                    person.linkedin = linkedin

                twitter_handle = form.cleaned_data['twitter']
                if twitter_handle:
                    print "person didn't have a twitter, so we're creating one"
                    twitter = Twitter(handle=twitter_handle)
                    twitter.save()
                    person.twitter = twitter

                person.save()
                person.update()
                return HttpResponseRedirect("/people/"+person.slug)
            else:
                print form.errors
                people = Person.objects.all()
                orgs = Organization.objects.all()
                return render(request, 'futurus/create_person.html', {'language': language, 'people': people, 'orgs': orgs, 'form': form})

        else:
            people = Person.objects.all()
            orgs = Organization.objects.all()
            return render(request, 'futurus/create_person.html', {'language': language, 'people': people, 'orgs': orgs, 'texts_header': get_texts("header", language)})



@login_required
def create_project(request):
    language = get_language(request)
    #checks to see if a user has created a profile (i.e. person object)
    # if they haven't, they gotta do that first
    if request.user.person:
        if request.method == 'POST':
            form = CreateProjectForm(data=request.POST)
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
            orgs = Organization.objects.all()
            return render(request, 'futurus/create_project.html', {'language': language, 'person': person, 'people': people, 'orgs': orgs, 'texts_header': get_texts("header", language)})


def get_language(request):
    if request.user.is_authenticated():
        preferences = models.Preferences.objects.get(user=request.user)
        if preferences.language is None:
            if "language" in request.session:
                preferences.language = request.session['language']
            else:
                preferences.language = "en"
            preferences.save()
        return preferences.language
    else:
        if "language" in request.session:
            return request.session['language']
        else:
            request.session['language'] = "en"
            return request.session['language']
       
    return request.session['language']

def get_texts(nameOfTemplate, language):
    # unfortunately, there's no way in python to get method name you're in
    texts_qs = models.Text.objects.filter(template=nameOfTemplate, language=language)
    texts = {}
    for text in texts_qs:
        texts[str(text.name)] = text.text.encode("utf-8")
    #print "texts are ", texts
    return texts

def index(request):
    #print "requ is", request
    #print "self is", dir(sys.modules[__name__])
    user = request.user
    language = get_language(request)
    numberOfUsers = User.objects.count()
    numberOfOrganizations = Organization.objects.count()
    numberOfDonations = Donation.objects.count()
    numberOfCompleteTasks = 0
    numberOfIncompleteTasks = 0
    if user.is_authenticated():
        calculateTasks(user)
        tasks = Task.objects.filter(user=user)
        numberOfCompleteTasks = len(tasks.filter(completed=True))
        numberOfIncompleteTasks = len(tasks.filter(completed=False))

    texts = get_texts("index", language)
    texts_header = get_texts("header", language)

    return render(request, 'futurus/index.html', {'numberOfUsers': numberOfUsers, 'numberOfIncompleteTasks': numberOfIncompleteTasks, 'numberOfCompleteTasks': numberOfCompleteTasks, 'numberOfOrganizations': numberOfOrganizations, 'numberOfDonations': numberOfDonations, 'language': language, 'texts': texts, 'texts_header': texts_header, 'texts_header': get_texts("header", language)})


@login_required
def edit_organization(request, slug): 
    language = get_language(request)
    #checks to see if a user has created a profile (i.e. person object)
    # if they haven't, they gotta do that first
    organization = Organization.objects.get(slug=slug)
    print "organization is ", organization
    user = request.user
    print "user is", user
    if request.user.person:
        if request.method == 'POST':
            print "request.POST:\n", request.POST
            form = EditOrgForm(data=request.POST)
            if form.is_valid():
                print "form is valid!"
                print "form.cleaned_data is ", form.cleaned_data
                organization.abbreviation = form.cleaned_data['abbreviation']
                organization.name = form.cleaned_data['name']
                organization.mission = form.cleaned_data['mission']
                organization.organization_created = form.cleaned_data['organization_created']
                organization.website = form.cleaned_data['website']
                

                if 'logo' in request.FILES:
                    organization.logo = request.FILES['logo']
               
                
                print type(form.cleaned_data['owners'])
 
                owners_ids_old = [int(owner.id) for owner in organization.owners.all()]
                print "owners old are", owners_ids_old
                owners_ids_new = [int(owner)for owner in form.cleaned_data['owners']]
                print "owners new are", owners_ids_new
                owners_to_remove = list(set(owners_ids_new) -set(owners_ids_old))
                for owner_id in owners_ids_new:
                    if owner_id not in owners_ids_old:
                        organization.owners.add(owner_id)
                for owner_id in owners_to_remove:
                    organization.owners.remove(owner)
                print "owners updated"

                for member in form.cleaned_data['members']:
                    Membership.objects.get_or_create(organization=organization, person=request.user.person)[0]

                print "org is", organization
              


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
                else:
                    try: organization.twitter.delete()
                    except: pass
                 
                #links = form.cleaned_data['links']
                #if links:
                #    pass

                wiki_url = form.cleaned_data['wiki']
                if wiki_url:
                    pass
                organization.save()
                #organization.update()
                return HttpResponseRedirect("/orgs/"+organization.slug)
            else:
                print form.errors
                person = user.person
                people = Person.objects.exclude(user__isnull=True).exclude(id=person.id)
                return render(request, 'futurus/edit_organization.html', {'language': language, 'person': person, 'people': people, 'user': user, 'form': form, 'organization': organization, 'texts_header': get_texts("header", language)})
        else:
            person = user.person
            print "person is ", person
            people = Person.objects.exclude(user__isnull=True).exclude(id=person.id)
            print "people is", people
            return render(request, 'futurus/edit_organization.html', {'language': language, 'person': person, 'people': people, 'user': user, 'organization': organization, 'texts_header': get_texts("header", language)})

@login_required
def edit_person(request, slug):
    language = get_language(request)
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
                print "form.cleaned_data is", form.cleaned_data
                person.name = form.cleaned_data['name']
                person.name_ar = form.cleaned_data['name_ar']
                person.story = form.cleaned_data['story']
                person.story_ar = form.cleaned_data['story_ar']
                person.hometown = form.cleaned_data['hometown']
                person.hometown_ar = form.cleaned_data['hometown_ar']
                person.save()
                if 'pic' in request.FILES:
                    person.pic = request.FILES['pic']
                person.save()

                facebook_url = form.cleaned_data['facebook']
                if person.facebook:
                    if facebook_url:
                        person.facebook.url = facebook_url
                    else:
                        person.facebook.delete()
                else:
                    if facebook_url:
                        facebook = Facebook(url=facebook_url)
                        facebook.save()
                        person.facebook = facebook
                person.save()

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
        return render(request, 'futurus/edit_person.html', {'language': language, 'person': person, 'form': form, 'texts_header': get_texts("header", language)})
    else: #this isn't the current user's profile
        return HttpResponseRedirect("/people/"+slug)

def find_organizations(request):
    language = get_language(request)
    organizations = Organization.objects.all()
    return render(request, 'futurus/find_organizations.html', {'language': language, 'organizations': organizations, 'texts_header': get_texts("header", language)})

def find_projects(request):
    language = get_language(request)
    projects = Project.objects.all()
    return render(request, 'futurus/find_projects.html', {'language': language, 'texts_header': get_texts("header", language)})

def find_people(request):
    language = get_language(request)
    people = Person.objects.all()
    return render(request, 'futurus/find_people.html', {'language': language, 'people': people, 'texts_header': get_texts("header", language)})

@login_required
def memberships(request, slug):
    language = get_language(request)
    texts = get_texts("memberships", language)

    person = get_object_or_404(Person, slug=slug)
    memberships = Membership.objects.filter(person=person)
    print "memberships are ", memberships
    return render(request, 'futurus/memberships.html', {'memberships': memberships, 'language': language, 'texts': texts, 'texts_header': get_texts("header", language)})


def organization(request, slug):
    language = get_language(request)
    organization = get_object_or_404(Organization, slug=slug)
    user = request.user
    request.session.session_key
    PageView.objects.create(user=user, page=request.path, session=request.session.session_key)
    pageViews = PageView.objects.filter(page=request.path)
    numberOfTotalPageViews = len(pageViews)
    numberOfUniquePageViewers = len(pageViews.values_list('user', flat=True).distinct())
    print numberOfUniquePageViewers
    return render(request, 'futurus/organization.html', {'language': language, 'organization': organization, 'user': user, 'numberOfTotalPageViews': numberOfTotalPageViews, 'numberOfUniquePageViewers': numberOfUniquePageViewers, 'texts_header': get_texts("header", language)})

def json_organizations(request):
   # data = {}
   # data['orgs'] = [{'name': org.name, 'mission': org.mission for org in Organization.objects.all()]
    data = [{'name': org.name, 'mission': org.mission} for org in Organization.objects.all()]
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')

def project(request, slug):
    language = get_language(request)
    project = get_object_or_404(Project, slug=slug)
    project.calc_money()
    steps = project.steps.all()
    print "steps are", steps
    print "update percent_funded for each step"
    for step in steps:
        step.calc_money()

    donations = Donation.objects.filter(step__in=steps)
    print "donations are ", donations
    donors = list(set([donation.donor for donation in donations]))
    print "donors are", donors
    return render(request, 'futurus/project.html', {'language': language, 'project': project, 'donors': donors, 'texts_header': get_texts("header", language)})

def person(request, slug):
    language = get_language(request)
    request.session.language = 'en'
    person = get_object_or_404(Person, slug=slug)
    return render(request, 'futurus/person.html', {'language': language, 'person': person, 'language': request.session.language, 'texts_header': get_texts("header", language)})


def register(request):
    language = get_language(request)
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
            email = user_form.cleaned_data['email']
            print "email is ", email
            print User.objects.filter(email=email).count()
            print User.objects.filter(username=email).count()

            if User.objects.filter(email=email).count() > 0 or User.objects.filter(username=email).count() > 0:

                print "already used email"
                print type(user_form.errors)
                user_form.add_error('email', "That email is already being used.")
            else:

                # Save the user's form data to the database.
                print "will now try to save user_form"
                user = user_form.save(commit=False)

                print " Now we hash the password with the set_password method."
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
            {'form': user_form, 'language': language, 'registered': registered, 'texts_header': get_texts("header", language)},
            context)

def translate(request):

    language = get_language(request)

    if request.method == 'POST':
        print "data", request.POST
        form = forms.TranslationForm(data=request.POST)

        if form.is_valid():
            print "form is valid"
            print "cleaned_data is", form.cleaned_data            
            for text_id in form.cleaned_data:
                print "changing text of",text_id," to ", form.cleaned_data[text_id]
                textObj = models.Text.objects.get(id=text_id)
                textObj.text=form.cleaned_data[text_id]
                textObj.save()
        else:
            print "NOT valid is form because:"
            print form.errors

    qsOfTexts = models.Text.objects.all()
    templates = qsOfTexts.values_list('template', flat=True).distinct()
    print "templates are", templates
    languages = qsOfTexts.values_list('language', flat=True).distinct()
    dictOfTexts = {}
    listOfTexts = []

    for template in templates:
        url = "http://localhost:8000/translate"
        #get url for the template; don't store in db
        if template != "":
            names = qsOfTexts.filter(template=template).values_list('name', flat=True).distinct()
            for name in names:
                print "for name ", name
                name_en_obj = qsOfTexts.get_or_create(template=template, name=name, language='en')[0]
                name_ar_obj = qsOfTexts.get_or_create(template=template, name=name, language='ar')[0]

                listOfTexts.append({'template:name': template+":"+name, 'en': {'id': name_en_obj.id, 'text': name_en_obj.text}, 'ar': {'id': name_ar_obj.id, 'text':name_ar_obj.text}})
 
    print "listOfTExts is", listOfTexts


    #return something like this: 
    # [{"name": [{"en": "...", "ar": "..."}]}]
    return render(request, 'futurus/translate.html', {'language': language, 'texts': listOfTexts, 'names': names, 'texts_header': get_texts("header", language)})

def transactions(request):
    language = get_language(request)
    donations = Donation.objects.filter(donor=request.user.donor)
    print "donations are ", donations
    return render(request, 'futurus/transactions.html', {'language': language, 'donations': donations, 'texts_header': get_texts("header", language)})


def user_login(request):
    language = get_language(request)
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
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        else:
            return render_to_response('futurus/login.html', {'language': language, 'texts_header': get_texts("header", language)}, context)


# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

def tasks(request):
    language = get_language(request)
    user = request.user
    calculateTasks(user)
    tasks = Task.objects.filter(user=user)
    print "tasks are ", tasks
    tasks_incomplete = tasks.filter(completed=False)
    print "tasks_incomplete is", tasks_incomplete
    tasks_completed = tasks.filter(completed=True)
    print "tasks_completed is", tasks_completed
    return render(request, 'futurus/tasks.html', {'language': language, 'tasks_incomplete': tasks_incomplete, 'tasks_completed': tasks_completed, 'texts_header': get_texts("header", language)})


def calculateTasks(user):
    print "starting calculateTasks"

    try:
        person = user.person
    except:
        person = None

    if person is None:
        print "You gotta create a profile"
        
        # check if incomplete create person task exists
        Task.objects.get_or_create(user=user, completed=False, name="Create Your Public Profile")[0]
        #remove old profile
        try: Task.objects.get(user, completed=True, name="Create Your Public Profile").delete()
        except: pass

    else: #person exists
        try: Task.objects.get(user=user, completed=False, name="Create Your Public Profile").delete()
        except: pass
        Task.objects.get_or_create(user=user, completed=True, name="Create Your Public Profile", url="http://localhost:8000/" + "people/" + user.person.slug)


        # Add in code to check different elements of person's profile, such as linkedin, picture, etc... also add in functionality so hide tasks, so people don't see them agin

    try:
        donor = user.donor
    except:
        donor = None

    if donor is None or donor.donated == 0:
        print "give your first donation"
        Task.objects.get_or_create(user=user, completed=False, name="Give Your First Donation")[0]
        try: Task.objects.get(user=user, completed=True, name="Give Your First Donation").delete()
        except: pass
    else: #user has donated
        try: Task.objects.get(user=user, completed=False, name="Give Your First Donation").delete()
        except: pass
        Task.objects.get_or_create(user=user, completed=True, name="Give Your First Donation")

    for organization in user.organization_set.all(): 
        print "org is ", organization.name
        url_org = "http://localhost:8000/orgs/" + organization.slug
        print "url_org is", url_org
        try: facebook = organization.facebook
        except: facebook = None
        if facebook is None or facebook.url is None:
            print "    facebook doesn't exist :("
            Task.objects.get_or_create(user=user, completed=False, name="Add Facebook to " + organization.name, url=url_org)
            try: Task.objects.get(user=user, completed=True, name="Add Facebook to " + organization.name, url=url_org).delete()
            except: pass
        else:
            print "    facebook exists! yay!"
            try: Task.objects.get(user=user, completed=False, name="Add Facebook to " + organization.name, url=url_org).delete()
            except: pass
            Task.objects.get_or_create(user=user, completed=True, name="Add Facebook to " + organization.name, url=url_org)

        try: linkedin  = organization.linkedin
        except: linkedin = None
        if linkedin is None or linkedin.url is None:
            Task.objects.get_or_create(user=user, completed=False, name="Add LinkedIn to " + organization.name, url=url_org)
            try: Task.objects.get_or_create(user=user, completed=True, name="Add LinkedIn to " + organization.name, url=url_org)
            except: pass
        else:
            try: Task.objects.get(user=user, completed=False, name="Add LinkedIn to " + organization.name).delete()
            except: pass
            Task.objects.get_or_create(user=user, completed=True, name="Add Linkedin to " + organization.name)

        if organization.logo is None or organization.logo == "":
            Task.objects.get_or_create(user=user, completed=False, name="Add Logo to " + organization.name, url=url_org)
            try: Task.objects.get_or_create(user=user, completed=True, name="Add Logo to " + organization.name, url=url_org)
            except: pass
        else:
            try: Task.objects.get(user=user, completed=False, name="Add Logo to " + organization.name, url=url_org).delete()
            except: pass
            Task.objects.get_or_create(user=user, completed=True, name="Add Logo to " + organization.name, url=url_org)

        if organization.mission is None or organization.mission == "":
            Task.objects.get_or_create(user=user, completed=False, name="Add Mission to " + organization.name, url=url_org)
            try: Task.objects.get_or_create(user=user, completed=True, name="Add Mission to " + organization.name, url=url_org)
            except: pass
        else:
            try: Task.objects.get(user=user, completed=False, name="Add Mission to " + organization.name, url=url_org).delete()
            except: pass
            Task.objects.get_or_create(user=user, completed=True, name="Add Mission to " + organization.name, url=url_org)

        try: twitter = organization.twitter
        except: twitter = None
        if twitter is None or twitter.url is None:
            Task.objects.get_or_create(user=user, completed=False, name="Add Twitter to " + organization.name, url=url_org)
            try: Task.objects.get_or_create(user=user, completed=True, name="Add Twitter to " + organization.name, url=url_org)
            except: pass
        else:
            try: Task.objects.get(user=user, completed=False, name="Add Twitter to " + organization.name, url=url_org).delete()
            except: pass
            Task.objects.get_or_create(user=user, completed=True, name="Add Twitter to " + organization.name, url=url_org)
    print "finishing calculateTasks"
