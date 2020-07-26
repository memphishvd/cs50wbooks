from django.shortcuts import render
import re
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import random
import markdown2

# Form For Adding New Entry
class AddForm(forms.Form):
    EntryTitle = forms.CharField(label="Entry Title" , required=True)
    EntryContent = forms.CharField(widget=forms.Textarea, label="Content", required=True)

# Form For Editing Entry
class EditForm(forms.Form):
    title = forms.CharField(widget=forms.HiddenInput(), required=False)
    EntryContent = forms.CharField(widget=forms.Textarea, label="Content")    

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# View For Specific Entry Page
def entrypage(request, title):
# Convert Entry Contents To Html From Markdown using markdown2
    getentry = util.get_entry(title)
    if getentry is None:
            return render(request, "encyclopedia/entrypage.html", {
            "alert": "No Entry Found With The Title: ",
            "title": title
        })
    else:

        contents = markdown2.markdown(getentry)
        if contents:
                return render(request, "encyclopedia/entrypage.html", {
                    "contents": contents,
                    "title": title
                })
        else:
                    return render(request, "encyclopedia/entrypage.html", {
                    "alert": "Unknown Error Encountered While Retrieving Contents Of:",
                    "title": title
                })

# View For Searching An Entry
def searchentry(request):
# Get the search parameter from the search form this will be the intended title of the entry the user is searching for
    searchparameter = request.GET.get('searchparameter')
# Get all the existing entries
    entries = util.list_entries()
# Create an empty list to store entries in lower case
    entrieslowercase = []
# Convert search parameter to lower case
    searchparameterlowercase = searchparameter.lower()
# Loop through and convert entries to lower case
    for entry in entries:
        entrieslowercase.append(entry.lower())
# Check if searched entry title h an exact match in the entries data we have gathered
    if searchparameterlowercase in entrieslowercase:
        getentry = util.get_entry(searchparameter)
        contents = markdown2.markdown(getentry)
        return render(request, "encyclopedia/entrypage.html", {
            "contents": contents,
            "title": searchparameter
        })
# If no exact match found, look for partial matches using regular expressions and store in a list-
    elif not searchparameterlowercase in entrieslowercase:
        matcher = re.compile(".*({}).*".format(searchparameterlowercase))
        result=list(filter(matcher.match, entrieslowercase))
# If no partial match found either then return error page with an error message
        if result==[]:
            return render(request, "encyclopedia/partialentries.html", {
            "alert": "No Entry Found With The Title",
            "title": searchparameter
            })
# If partial match(s) found return all partial matches
        return render(request, "encyclopedia/partialentries.html", {
            "contents": result,
            "title": searchparameter
        })
# View to add new entry
def addentry(request):
# If request method is GET load a blank form to add new entry details
    if request.method=="GET":
        return render(request, "encyclopedia/addentry.html", {
                "form": AddForm()
        })
# If request method is POST add new entry and redirect to new entry page
    elif request.method=="POST":
        form = AddForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["EntryTitle"]
            content = form.cleaned_data["EntryContent"]
# This has been set because the same util.save_entry function in util.py has a dual role, it is being used to add a new entry and to edit an existing one. the util.save_entry will not save an entry if an entry with that title already exists.
            edit = "no"
# Fate variable stores the title of the newly stored entry. If the entry was saved successfully fate will not be empty otherwise it will be empty or None.
            fate = util.save_entry(title,content,edit)
# If fate is not empty/None then redirect to the entrypage function passing the title of the entry as args so the entrypage function can search and retrieve the entry content relating to that title.
            if fate:
                url = reverse('encyclopedia:entrypage', args={fate})
                return HttpResponseRedirect(url)
# If fate is empty/none this means an entry with the specified title already exists, redirect user to the add entry page with an error message.
        #elif fate=="fail":
        return render(request, "encyclopedia/addentry.html", {
        "form": form,
        "alert" : "An Entry With This Title Already Exists, Please Choose Another Title"
    })



   # View to edit entry
def editentry(request, title):
# If the request method is GET render the edit form populated with matching entry contents
    if request.method=="GET":
# Use the title and get matching content
        contents = util.get_entry(title)
        
# If a matching entry is found, render the edit form setting the initial values for title and content fields
        if contents:
            return render(request, "encyclopedia/edit.html", {
                "form": EditForm(initial={'EntryContent': contents,
                                          'title' : title
                                        }),
                "title": title
                                            })
# If no matching entry found send the user to the error page with an error message                

        else:
            return render(request, "encyclopedia/error.html", {
                "alert": "No Entry Found For",
                "title": title
            })

# If request method is post process the form data
    elif request.method=="POST":
        form = EditForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["EntryContent"]
# This is to manage the dual role of util.save_entry function (to save or edit an entry), it serves as an argument for an IF statement in util.py
            edit="yes"
# Using fate variable as a simple of way of checking everything went ok, it saves the title of the entry
            fate= util.save_entry(title,content,edit)
# Redirect to the newly edited entry page passing fate which is the title as an argument so the entrypage function can retrieve relevant data
            if fate:
                url = reverse('encyclopedia:entrypage', args={fate})
                return HttpResponseRedirect(url)

# Send user back to the edit page with an error message 
            return render(request, "encyclopedia/edit.html", {
            "form": form,
            "alert" : "Unable to Edit Entry"
    })





# View to access a random entry page
def randompage(request):
# Get all entries
    allentries = util.list_entries()
# Pick a random entry
    randomentry = random.choice(allentries)
# Pass the picked random entry as an argument to the entrypage functionn and set it as the url variable
    url = reverse('encyclopedia:entrypage', args={randomentry})
# Redirect user to the random entry url
    return HttpResponseRedirect(url)