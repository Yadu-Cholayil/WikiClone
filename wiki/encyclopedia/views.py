from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import redirect, render

import markdown2 as md
import random

import re
from . import util
from .forms import AddEntryForm

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    file = util.get_entry(title = title)
    if file is not None:
        files = md.markdown(file)
        return render(request, "encyclopedia/entry.html", {'title': title, 'file': files})

def addentry(request):
    forms = AddEntryForm()
    titles = util.list_entries()
    if request.method == "POST":
        forms = AddEntryForm(request.POST)
        if forms.is_valid():
            if forms.cleaned_data['title'] in titles:
                return HttpResponseBadRequest("Filename already exists")
            util.save_entry(forms.cleaned_data['title'], forms.cleaned_data['content'])
            return redirect(index)
    return render(request, "encyclopedia/addentry.html", {'forms': forms})

def RandomPage(request):
    title = random.choice(util.list_entries())
    return redirect('entry', title=title)

def SearchPage(request):
    search = request.GET.get('q')
    search = search.upper()
    titles =  [title.upper() for title in util.list_entries()]
    if search not in titles:
        titles = " ".join(titles)
        if search is not None:
            title = re.search("\w+" + search + "\w+", titles)
            if title is None:
                title = re.search("\w+" + search, titles)
            if title is None:
                title = re.search(search + "\w+", titles)
            try:
                return render (request, 'encyclopedia/search.html', {'search': title.group()})
            except:
                return HttpResponseNotFound("File not found")
    return redirect('entry', title=search)


def EditPage(request, title):
    file = util.get_entry(title = title)
    file = {"title": title, "content": file}
    forms = AddEntryForm(initial=file)
    if request.method == 'POST':
        forms = AddEntryForm(request.POST)
        if forms.is_valid():
            util.save_entry(forms.cleaned_data['title'], forms.cleaned_data['content'])
            return redirect(index)
    return render(request, 'encyclopedia/edit.html', {'forms': forms})