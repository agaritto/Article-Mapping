#django
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password
# from django.contrib.auth.models import User
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
    paper_list.append(paper_temp[0]['doi'])
    paper_list.append(paper_temp[0]['article_title'])
    paper_list.append(paper_temp[0]['journal_title'])
    paper_list.append(paper_temp[0]['author'])
    paper_list.append(paper_temp[0]['year'])
    paper_list.append(paper_temp[0]['volume'])
    paper_list.append(paper_temp[0]['issue'])
    # reference
    reference_list = CitationLocation.objects.filter(citing_paper_doi=doi_temp).values("cited_paper_doi").distinct()
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
    # outline
    outline_list = Outline.objects.filter(paper_doi=doi_temp).values()
    outline_link = []
    for i in outline_list:
        outline_link.append(i['original_outline'])
    # intext
    intext_list = CitationLocation.objects.filter(citing_paper_doi=doi_temp).order_by('outline').values()
    intext_citation = []
    for i in intext_list:
        temp = []
        temp.append(i['citing_paper_doi'])
        temp.append(i['cited_paper_doi'])
        temp.append(i['outline'])
        temp.append(i['count'])
        intext_citation.append(temp)

    doi_id = "https://doi.org/" + str(doi_id)  # iframe 위한 https:// 붙이기



    request.session['doi_temp'] = doi_temp
    request.session['paper_list'] = paper_list
    request.session['reference_list'] = reference_link
    request.session['outline_list'] = outline_link
    request.session['intext_citation'] = intext_citation
    request.session['doi_id'] = doi_id
    # request.session['user_id'] = user_id


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

    changed_outline_temp = []
    for i in outline_list:
        x = request.POST[i]
        changed_outline_temp.append(x)
    changed_outline = request.POST
    # print(og_outline)
    # print(changed_outline)
    outline = Outline.objects.filter(paper_doi=doi_temp).values()
    temp = 0
    for i in outline:
        outline = Outline.objects.get(id=i['id'])
        outline.changed_outline = changed_outline_temp[temp]
        outline.save()
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
        member = auth.models.User.objects.get(username=username)
        print(member)
        if user is not None:
            auth.login(request, user)
            request.session['user'] = member.username
            print(request.session['user'])
            return redirect('/')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def test(request):

    return render(request, 'science_crawling.html', )

def neo4jwork(request):
    print(request)
    login_session = request.session.get('login_session')
    print(login_session)

    if request.session['user'] == "admin":
        print("login_id: ")
        print(request.session['user'])
        return render(request, 'test.html')
    else:
        return redirect('/')

def neo4j_nodeinput(request):
    article = Paper.objects.values()
    # article = Paper.objects.filter(doi="10.1016/j.joi.2022.101332").values()
    # print(article[0]['doi'])
    i = 0
    print("-------------------------------------------------------------------------------------")
    for paper in article:
        doi = article[i]['doi']
        title = article[i]['article_title']
        journal = article[i]['journal_title']
        author = article[i]['author']
        year = article[i]['year']
        volume = article[i]['volume']
        issue = article[i]['issue']
        print(doi, title, journal, author, year, volume, issue)
        create_article_node(paper)
        print(i)
        i +=1
        print("-------------------------------------------------------------------------------------")

    return render(request, 'test.html', {'article': article})


def neo4j_relationinput(request):
    citing_article = Paper.objects.filter(doi=i).values()[0]['doi']
    cited_temp = CitationLocation.objects.filter(citing_paper_doi=i).values()
    for j in cited_temp:
        cited_article = j['cited_paper_doi']
        temp = j['outline']
        # changed_temp =
        changed_outline = Outline.objects.filter(paper_doi=i, original_outline=temp).values()[0]['changed_outline']
        citation_counts = j['count']
        print(
            'citing article : {} | cited article : {} | outline : {} | count : {}'.format(citing_article, cited_article,
                                                                                          temp, citation_counts))
        print("---------------------------------------------")
        print('citing article : {} | cited article : {} | changed outline : {} | count : {}'.format(citing_article,
                                                                                                    cited_article,
                                                                                                    changed_outline,
                                                                                                    citation_counts))
        print('==============================================')
    # create_relationship(citing_article, cited_article, changed_outline, citation_counts)
    return render(request, 'test.html')


def relationcreatedb(request):
    if request.method == "POST":
        article_list = CitationLocation.objects.all().order_by('-citing_paper_doi').values('citing_paper_doi').distinct()
        for article in article_list:
            # print("========================================================================")
            # print("article : {}".format(article))
            doi = article['citing_paper_doi']
            # print("DOI : {}".format(doi))
            citing_article = Paper.objects.filter(doi=doi).values()[0]['doi']
            # print(citing_article)
            cited_temp = CitationLocation.objects.filter(citing_paper_doi=doi).values()

            for j in cited_temp:
                cited_article = j['cited_paper_doi']
                temp = j['outline']
                # changed_temp =
                changed_outline = Outline.objects.filter(paper_doi=doi, original_outline=temp).values()[0][
                    'changed_outline']
                if changed_outline == '':
                    break
                citation_counts = j['count']
                print('citing article : {} | cited article : {} | outline : {} | count : {}'.format(citing_article,
                                                                                                    cited_article, temp,
                                                                                                    citation_counts))

                id = '{}/{}/{}'.format(citing_article[19:], cited_article, changed_outline)
                print("---------------------------------------------")
                print('citing article : {} | cited article : {} | changed outline : {} | count : {} | id : {}'.format(citing_article, cited_article, changed_outline, citation_counts, id))
                print(id)
                print('==============================================')
                # obj, created = CreateRelation.objects.get_or_create()
                try:
                    if CreateRelation.objects.filter(id=id).exists():
                        print('already exists')
                        data = CreateRelation.objects.filter(id=id).values()
                        edit_ver = CreateRelation.objects.get(id=id)
                        edit_ver.citation_counts = str(int(edit_ver.citation_counts) + int(citation_counts))
                        edit_ver.save()
                        check_change = CreateRelation.objects.filter(id=id).values()
                        print("********************************************************************************")
                        print("original : {}".format(data))
                        print("edit ver : {}".format(check_change))
                        print("********************************************************************************")
                        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    else:
                        print('creating')
                        ex = CreateRelation(id=id,
                                            citing_article=citing_article,
                                            cited_article=cited_article,
                                            changed_outline=changed_outline,
                                            citation_counts=citation_counts,
                                            )
                        ex.save()
                        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                except Exception as e:
                    break
                    print("--------------------")
                    print(e)
                    print("--------------------")
                    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    break
            if changed_outline == '':
                break
    comment = "Data inserted to create =_relation table"
    print("Finished")



    return render(request, 'test.html', {comment: 'comment'})