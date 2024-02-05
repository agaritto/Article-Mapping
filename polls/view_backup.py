#django
from django.shortcuts import render, redirect
from django.http import JsonResponse
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
        if 'crossref_temp' in request.session:
            del request.session['crossref_temp']
        if 'sec_temp' in request.session:
            del request.session['sec_temp']
        if 'out_temp' in request.session:
            del request.session['out_temp']


        doi_id = request.POST['request']
    # input_doi = {"doi_temp": doi_id}
    # doi_id = request.POST['request']                    # 입력받은 DOI (ex doi.org/xxxxx/xxxxx)
    doi_id = doi_id.replace("\n", "")
    doi_id = doi_id.replace("\r", "")
    doi_id = doi_id.replace(" ", "")
    doi_temp = doi_id                                   # DOI 임시저장 - database가 doi로 되어 있어서
    print(doi_id)
    doi_id = "https://doi.org/" + doi_id                   # iframe 위한 https:// 붙이기
    print(doi_id)
    # database에서 데이터 가져오기

    reference_list = CitationLocation.objects.all()     # citation 데이터 가져오기
    paper_list = Paper.objects.all()                    # 논문 데이터 가져오기
    # outline_list = Outline.objects.all()
    data = crawler(doi_id)
    outline_data, ref_data, body_data, doi_data = data_parsing(data)

    #intext_crawler -> body data
    section_data = intext_crawler(body_data)

    #reference_list = bib_id_list, reference_prop_list = bib_prop_list
    reference_list, reference_prop_list = reference_crawl(ref_data)
    ref_data_list, main_article = crossref_crawl(doi_data)
    # create_article_node_reference(ref_data_list)
    # create_article_node_main(main_article)

    request.session['doi_temp'] = doi_id
    request.session['crossref_temp'] = ref_data_list
    request.session['sec_temp'] = section_data
    request.session['out_temp'] = outline_data
    return render(request, 'base.html', {
        "doi_temp" : doi_id,
        "out_temp": outline_data, #out_temp = outline_data(아웃라인)
        "sec_temp": section_data,
        "ref_temp_list" : reference_list, #ref_temp_list = reference_list(reference bbib리스트 제공)
        "ref_temp_prop" : reference_prop_list,
        "crossref_temp" : ref_data_list
    })

def relation(request):
    if request.method == "POST":
        # reference_data = request.POST.get("relation")
        print(request)
        if 'doi_temp' in request.session:
            main_doi = request.session['doi_temp']

        if 'crossref_temp' in request.session:
            crossref_data = request.session['crossref_temp']

        if 'sec_temp' in request.session:
            intext_citation_list = request.session['sec_temp']

        if 'out_temp' in request.session:
            og_outline = request.session['out_temp']


        for i in og_outline:
            x = request.POST[i]
            # print(x)
        changed_outline = request.POST
        # print(og_outline)
        # print(changed_outline)

        intext_citation = intext_citation_list
        reference_article = crossref_data
        main_article = main_doi[16:]




        create_article_relationship(main_article, reference_article, intext_citation, changed_outline)
    # create_article_node_reference(reference_data)
    return render(request, 'relation.html',
                  {"doi_temp" : main_doi,  "sec_temp": intext_citation,  "crossref_temp" : reference_article, "main_doi" : main_article, "changed_ol":changed_outline}
                  )

def test(request):

    return render(request, 'science_crawling.html', )

def test2(request):
    if request.method == 'POST':
        inputdata = request.POST['request']
        print(inputdata)
    paper_list = Paper.objects.all()
    citatoin_link = CitationLocation.objects.filter(citing_paper_doi=inputdata)
    outline_list = CitationLocation.objects.filter(citing_paper_doi=inputdata).distinct().values_list("outline")
    print(len(citatoin_link))
    print(outline_list)
    for i in outline_list:
        print(i[0])
    return render(request, 'science_crawling.html', {"paper_list": paper_list, "input_DOI": inputdata, "citation_list": citatoin_link, "outline":outline_list})

def test3(request):

    return render(request, 'test.html', )

def test4(request):
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
        if 'crossref_temp' in request.session:
            del request.session['crossref_temp']
        if 'sec_temp' in request.session:
            del request.session['sec_temp']
        if 'out_temp' in request.session:
            del request.session['out_temp']


        doi_id = request.POST['request']
    # input_doi = {"doi_temp": doi_id}
    doi_id = request.POST['request']                    # 입력받은 DOI (ex doi.org/xxxxx/xxxxx)
    doi_temp = doi_id                                   # DOI 임시저장 - database가 doi로 되어 있어서
    doi_id = "https://" + str(doi_id)  # iframe 위한 https:// 붙이기

    # database에서 데이터 가져오기

    reference_list = CitationLocation.objects.filter(citing_paper_doi=doi_temp)     # citation 데이터 가져오기
    paper_list = Paper.objects.filter()  # 논문 데이터 가져오기
    data = crawler(doi_id)
    outline_data, ref_data, body_data, doi_data = data_parsing(data)

    #intext_crawler -> body data
    section_data = intext_crawler(body_data)

    #reference_list = bib_id_list, reference_prop_list = bib_prop_list
    ref_data_list, main_article = crossref_crawl(doi_data)
    create_article_node_reference(ref_data_list)
    create_article_node_main(main_article)


    request.session['doi_temp'] = doi_id
    request.session['crossref_temp'] = ref_data_list
    request.session['sec_temp'] = section_data
    request.session['out_temp'] = outline_data
    return render(request, 'test.html', {
        "doi_temp" : doi_id,
        "out_temp": outline_data, #out_temp = outline_data(아웃라인)
        "sec_temp": section_data,
        "crossref_temp" : ref_data_list
    })

def test5(request):

    return render(request, 'science_crawling.html', )

def create_node(request):



    return render(request, 'science_crawling.html', )


def create_relation(request):
    return render(request, 'science_crawling.html', )