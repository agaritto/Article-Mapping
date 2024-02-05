#django
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from .models import *
from .crawler import *
from neomodel import *
from .neo4j_import import *
# from django.urls import reverse, reverse_lazy
# from django.views.generic import (
#     ListView,
#     CreateView,
#     UpdateView,
#     DeleteView,
# )
# from django.http import HttpResponseRedirect
import json

#csrf
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator





@method_decorator(csrf_exempt)
def index(request):
    return render(request, 'base.html')

def doi(request):
    """
    :param request: doi 입력 - doi.org/xxxxx
    :return:
    "doi_temp" : doi_id,                                 #doi_id
    "out_temp": outline_data,                            #out_temp = outline_data(아웃라인)
    "sec_temp": section_data,                            #sec_temp -> intext citation
    "ref_temp_list" : reference_list,                    #ref_temp_list = reference_list(reference bbib리스트 제공)
    "ref_temp_prop" : reference_prop_list,               #
    "crossref_temp" : ref_data_list                      #
    """
    if request.method == 'POST':
        print(request)
        if 'doi_temp' in request.session:
            del request.session['doi_temp']
        if 'doi_id' in request.session:
            del request.session['doi_id']
        if 'paper_list' in request.session:
            del request.session['paper_list']
        if 'reference_list' in request.session:
            del request.session['reference_list']
        if 'outline_list' in request.session:
            del request.session['outline_list']
        if 'intext_citation' in request.session:
            del request.session['intext_citation']


        doi_id = request.POST['request']  # 입력받은 DOI (ex doi.org/xxxxx/xxxxx)

    doi_temp = doi_id.replace("\n", "")
    doi_temp = doi_temp.replace("\r", "")
    doi_temp = doi_temp.replace(" ", "")
                                      # DOI 임시저장 - database가 doi로 되어 있어서

    # main
    paper_temp = Paper.objects.filter(doi=doi_temp).values()
    paper_list = []
    print(paper_temp)
    paper_list.append(paper_temp[0]['doi'])
    paper_list.append(paper_temp[0]['article_title'])
    paper_list.append(paper_temp[0]['journal_title'])
    paper_list.append(paper_temp[0]['author'])
    paper_list.append(paper_temp[0]['year'])
    paper_list.append(paper_temp[0]['volume'])
    paper_list.append(paper_temp[0]['issue'])
    print("paper_list : ")
    print(paper_list)
    print("===============================================================================")
    # reference
    reference_list = CitationLocation.objects.filter(citing_paper_doi=doi_temp).values("cited_paper_doi").distinct()
    print(reference_list[0]['cited_paper_doi'])
    reference_link = []
    for i in reference_list:
        temp = []
        temp2 = Paper.objects.filter(doi__exact=i['cited_paper_doi']).values()
        temp.append(temp2[0]['doi'])
        temp.append(temp2[0]['article_title'])
        temp.append(temp2[0]['journal_title'])
        temp.append(temp2[0]['author'])
        temp.append(temp2[0]['year'])
        temp.append(temp2[0]['volume'])
        temp.append(temp2[0]['issue'])
        reference_link.append(temp)
    print("reference_link : ")
    print(reference_link)
    print("===============================================================================")
    # outline
    outline_list = Outline.objects.filter(paper_doi=doi_temp).values()
    outline_link = []
    for i in outline_list:
        outline_link.append(i['original_outline'])
    print("outline_link : ")
    print(outline_link)
    print("===============================================================================")
    # intext
    intext_list = CitationLocation.objects.filter(citing_paper_doi=doi_temp).order_by('outline').values()
    print(intext_list)
    intext_citation = []
    for i in intext_list:
        temp = []
        temp.append(i['citing_paper_doi'])
        temp.append(i['cited_paper_doi'])
        temp.append(i['outline'])
        temp.append(i['count'])
        intext_citation.append(temp)
    print("intext_citation : ")
    print(intext_citation)
    print("===============================================================================")

    doi_id = "https://doi.org/" + str(doi_id)  # iframe 위한 https:// 붙이기



    request.session['doi_temp'] = doi_temp
    request.session['paper_list'] = paper_list
    request.session['reference_list'] = reference_link
    request.session['outline_list'] = outline_link
    request.session['intext_citation'] = intext_citation
    request.session['doi_id'] = doi_id

    print("===========================================================")
    print(doi_id)
    print("===========================================================")
    print(paper_list)
    print("===========================================================")
    print(reference_link)
    print("===========================================================")
    print(outline_link)
    print("===========================================================")
    print(intext_citation)
    print("===========================================================")


    print("===========================================================")
    print("DOI ID: ")
    print(request.session['doi_temp'])
    print("===========================================================")
    print("PAPER LIST: ")
    print(request.session['paper_list'])
    print("===========================================================")
    print("REFERENCE LINK: ")
    print(request.session['reference_list'])
    print("===========================================================")
    print("OUTLINE LINK: ")
    print(request.session['outline_list'])
    print("===========================================================")
    print("INTEXT CITATION: ")
    print(request.session['intext_citation'])
    print("===========================================================")



    return render(request, 'base.html', {
        "doi_temp" : doi_id,
        "paper_list": paper_list, #out_temp = outline_data(아웃라인)
        "reference_list": reference_link,
        "outline_list" : outline_link,
        "intext_citation" : intext_citation
    })

def relation(request):
    if request.method == "POST":
        # reference_data = request.POST.get("relation")
        print(request)
        if 'doi_temp' in request.session: # 10.1016/j.joi.2022.101332
            doi_temp = request.session['doi_temp'] # 10.1016/j.joi.2022.101332
        if 'doi_id' in request.session:
            doi_id = request.session['doi_id']
        if 'paper_list' in request.session:
            paper_info = request.session['paper_list']
        if 'reference_list' in request.session:
            reference_list = request.session['reference_list']
        if 'outline_list' in request.session:
            outline_list = request.session['outline_list']
        if 'intext_citation' in request.session:
            intext_citation = request.session['intext_citation']

    print("===========================================================")
    print("DOI TEMP: ")
    print(request.session['doi_temp'])
    print("===========================================================")
    print("DOI ID: ")
    print(request.session['doi_id'])
    print("===========================================================")
    print("PAPER LIST: ")
    print(request.session['paper_list'])
    print("===========================================================")
    print("REFERENCE LINK: ")
    print(request.session['reference_list'])
    print("===========================================================")
    print("OUTLINE LINK: ")
    print(request.session['outline_list'])
    print("===========================================================")
    print("INTEXT CITATION: ")
    print(request.session['intext_citation'])
    print("===========================================================")

    changed_outline_temp = []
    for i in outline_list:
        x = request.POST[i]
        print(x)
        changed_outline_temp.append(x)
    print(len(changed_outline_temp))
    changed_outline = request.POST
    # print(og_outline)
    # print(changed_outline)
    outline = Outline.objects.filter(paper_doi=doi_temp).values()
    print(outline)
    print("===========================================================")
    temp = 0
    for i in outline:
        print(i)
        print(changed_outline_temp[temp])
        outline = Outline.objects.get(id=i['id'])
        outline.changed_outline = changed_outline_temp[temp]
        outline.save()
        print(Outline.objects.filter(id=i['id']).values())
        temp += 1

    return render(request, 'relation.html',
                  {"doi_temp" : doi_id,
                   "intext_citation": intext_citation,
                   "reference_list": reference_list,
                   "main_doi" : paper_info,
                   "changed_ol":changed_outline}
                  )

def login(request):
    if request.method == "POST":
        username = request.POST['id']
        password = request.POST['pwd']
        user = auth.authenticate(request, username=username, password=password)
        print(user)
        if username == "admin":
            print("yes")

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
# def logout(request):
#     if request.method == "POST":
#         username = request.POST['id']
#         password = request.POST['pwd']
#         user = auth.authenticate(request, username=username, password=password)
#         print("들어옴")
#         if user is not None:
#             auth.login(request, user)
#             return redirect('/')
#         else:
#             return render(request, '/login/')
#     else:
#         return render(request, '/login/')


def test(request):

    return render(request, 'science_crawling.html', )

def test2(request):
    if request.method == 'POST':
        inputdata = request.POST['request']
        print(inputdata)

    #main
    paper_list = Paper.objects.filter(doi=inputdata).values()

    # reference
    reference_list = CitationLocation.objects.filter(citing_paper_doi=inputdata).values("cited_paper_doi").distinct()
    print(reference_list[0]['cited_paper_doi'])
    temp_list = []
    for i in reference_list:
        temp = []
        temp2 = Paper.objects.filter(doi__exact=i['cited_paper_doi']).values()
        temp.append(temp2[0]['doi'])
        temp.append(temp2[0]['article_title'])
        temp.append(temp2[0]['journal_title'])
        temp.append(temp2[0]['author'])
        temp.append(temp2[0]['year'])
        temp.append(temp2[0]['volume'])
        temp.append(temp2[0]['issue'])
        temp_list.append(temp)
    print(temp_list)
    reference_link = temp_list
    print(len(reference_link))

    #outline
    outline_list = Outline.objects.filter(paper_doi=inputdata).values()
    outline_link = []
    for i in outline_list:
        outline_link.append(i['original_outline'])
    print(outline_link)

    # intext
    intext_list = CitationLocation.objects.filter(citing_paper_doi=inputdata).order_by('outline').values()
    print(intext_list)
    intext_citation = []
    for i in intext_list:
        temp = []
        temp.append(i['citing_paper_doi'])
        temp.append(i['cited_paper_doi'])
        temp.append(i['outline'])
        temp.append(i['count'])
        intext_citation.append(temp)
    print(intext_citation)
    return render(request, 'science_crawling.html', {"paper_list": paper_list, "input_DOI": inputdata, "reference_list": reference_link, "outline":outline_link, "intext_list": intext_citation})

def test3(request):

    return render(request, 'test.html', )


def neo4jwork(request):
    if request.method == "POST":
        username = request.POST['id']
        password = request.POST['pwd']
        user = auth.authenticate(request, username=username, password=password)
        print(user)
        if username == "admin":
            print("yes")
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')