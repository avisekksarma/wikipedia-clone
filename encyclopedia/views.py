from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown
from django.contrib import messages
import random

from . import util

markdowner = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# topics and entries mean same thing
def topics(request, title):
    title_for_url = title
    try:
        x = markdowner.convert(util.get_entry(f'{title}'))

        if '<h1>' in str(x):    # this is for not making  big titles get repeated due to heading of content
            title = None
        return render(request, 'encyclopedia/topics.html', {
            'title': title,
            'title_for_url': title_for_url,
            'description': x
        })
    except TypeError:  # exception for the case when None is return by get_entry for not existing title
        return render(request, 'encyclopedia/topics.html', {
            'title': None,
            'title_for_url': None,
            'description': None
        })


def searchresults(request):
    try:
        q = request.GET['q']
        entries = util.list_entries()
        print(entries)
        matched_results = []
        if q in entries:
            return HttpResponseRedirect(reverse('topics', kwargs={'title': q}))
        else:
            for entry in entries:
                if q in entry:
                    matched_results.append(entry)

        return render(request, 'encyclopedia/searchresults.html', {
            'entries': matched_results
        })
    except Exception:   # catching the error for get request on /search only
        return HttpResponseRedirect(reverse('index'))


def createpage(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        if title in util.list_entries():
            messages.info(request, f'There is already a title with name {title}')
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('topics', kwargs={'title': title}))
    return render(request, 'encyclopedia/createpage.html')


def edit(request, title):
    if request.method == "POST":
        print("title => ", title)
        print("content => ", request.POST['content'])
        util.save_entry(title, request.POST['content'])
        return HttpResponseRedirect(reverse('topics', kwargs={'title': title}))
    content = util.get_entry(f'{title}')
    return render(request, 'encyclopedia/edit.html', {'title': title,
                                                      'content': content
                                                      })


def randompage(request):
    random_title = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse('topics', kwargs={'title': random_title}))
