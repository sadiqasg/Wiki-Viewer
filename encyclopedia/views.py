from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect

from . import util
import markdown2
from random import choice

class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        "class":"w-25 mb-3"
    }))
    info = forms.CharField(widget=forms.Textarea(attrs={
        "placeholder":"Enter Entry Info",
        "style":"height: 40vh",
    }))

#index
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#single entry view
def wiki_entry(request, wiki_title):
    entry = util.get_entry(wiki_title)
    if entry:
        return render(request, "encyclopedia/wiki.html", {
            "title": wiki_title,
            "content": markdown2.markdown(entry)
        })
    else:
        return HttpResponseRedirect("/error")

#error view
def error(request):
    return render(request, "encyclopedia/error.html", {
        "title": "Error"
    })

#search view
def search(request):
    query = request.GET['q']

    if query == "" or query is None:
            return HttpResponseRedirect("/")

    entry = util.get_entry(query)

    if entry:
        return render(request, "encyclopedia/wiki.html", {
            "title": query,
            "content": markdown2.markdown(entry)
        })

    elif query and entry is None:
        entries = util.list_entries()
        matched_entry = []
        
        for entry in entries:
            if query.lower() in entry.lower():
                matched_entry.append(entry)

        return render(request, 'encyclopedia/search.html', {
            "title": query,
            "entries": matched_entry,
            "matched_array": len(matched_entry) > 0
        })

#new view
def new(request):
    page_title = "New Entry"
    if request.method=="POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            info = form.cleaned_data["info"]
            if util.get_entry(title):
                return render(request, "encyclopedia/new.html", {
                    "title": page_title,
                    "form": form,
                    "message": "Error! Entry title already exists!"
                })
            else:
                content = f"#{title}\n\n{info}"
                util.save_entry(title=title, content=content)

                return HttpResponseRedirect(f"/wiki/{title}")

    else:
        return render(request, "encyclopedia/new.html",{
            "title": page_title,
            "form": NewEntryForm(),
            "message": ""
        })

# edit view 
def edit(request, title):
    content = util.get_entry(title)
    if request.method=="POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            info = form.cleaned_data["info"]

            util.save_entry(title=title, content=info)

            return HttpResponseRedirect(f"/wiki/{title}")

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": NewEntryForm(initial={'title': title, 'info': content})
    })

#random view
def random(request):
    random_entry = choice(util.list_entries())
    return HttpResponseRedirect(f"/wiki/{random_entry}")