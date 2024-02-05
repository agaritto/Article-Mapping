import json
import logging
import traceback

from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from crossref.restful import Works
from .models import *
from neomodel import *
from neo4j import *
import re
from django.http import JsonResponse

def crawler(url):

    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(1000000)
    sleep(3)
    html = driver.page_source


    soup = BeautifulSoup(html, 'html.parser')

    driver.quit()
    return soup

def data_parsing(fulldata):
    data = fulldata
    """
    refdata
    """
    #ref_data
    ref_data = data.find('dl', {'class': 'references'})
    """
    OUTLINE
    """
    #body_data
    body_data = data.find('div', {'id': 'body'})
    outline_list = []
    outline_data = body_data.find_all("h2")

    """
    DOI
    """
    citing_data = data.find('article', {'role': 'main'})
    doi_pre_data = citing_data.find('div', {'class': 'ArticleIdentifierLinks'})
    #doi_data
    doi_data = doi_pre_data.find('a', {'class': 'doi'})["href"]
    doi_data = doi_data[16:]


    for i in outline_data:
        temp = i.get_text().replace(" ", "")
        outline_list.append(temp)
    # print(outline_list, "\n", doi_data, "\n")

    return outline_list, ref_data, body_data, doi_data



def intext_crawler(bodydata):

    #본문만 뽑기
    sec_divdata = bodydata.select('div > section')


    outline_list = []
    content_link_list = []

    for i in range(len(sec_divdata)):

        temp = sec_divdata[i].find('h2', {'class': 'u-h3 u-margin-l-top u-margin-xs-bottom'}).get_text().replace(" ", '')
        outline_list.append(temp)


    sec_link_list = []
    for i in range(len(sec_divdata)):
        temp = sec_divdata[i].find_all('a', {'class': 'workspace-trigger'})
        temp2 = []
        for j in range(len(temp)):
            contemp_id = temp[j].attrs['name']
            if contemp_id[:4] == "bbib":
                temp2.append(temp[j].attrs['name'][1:])

        temp3 = []
        temp3.append(outline_list[i])
        temp3.append(temp2)
        sec_link_list.append(temp3)

    return(sec_link_list)

def reference_crawl(refdata):

    data_dt = refdata.find_all('dt', {'class': 'label'})
    data_dd = refdata.find_all('dd', {'class': 'reference'})


    bib_id_list = []
    bib_prop_list = []
    for i in range(len(data_dt)):
        id = data_dt[i].find('a').attrs['href']
        bib_id_list.append(id[1:])

    for i in range(len(data_dd)):
        prop = []

        refid = data_dt[i].find('a').attrs['href']
        # refid
        # try:
        #     refid = data_dd[i].find('dt', {'class': 'label'})
        #     refid = refid.find('a').attrs['href']
        #     print(refid)
        # except AttributeError:
        #     refid = ""


        try:
            contribution = data_dd[i].find('div', {'class': 'contribution'}).text
        except AttributeError:
            contribution = ""


        try:
            title = data_dd[i].find('strong', {'class': 'title'}).text
        except AttributeError:
            title = ""


        try:
            host = data_dd[i].find('div', {'class': 'host'}).text
        except AttributeError:
            host = ""


        prop.append(refid[1:])

        try:
            prop.append(contribution[:len(contribution) - len(title)].split(", "))
        except AttributeError:
            prop.append("")
        prop.append(title)

        try:

            prop.append(host)
        except AttributeError:
            prop.append("")


        bib_prop_list.append(prop)


    return(bib_id_list, bib_prop_list)


"""
crossrefapi사용
"""
def crossref_crawl(doidata):
    works = Works()
    crossref_refdata = works.doi(doidata)

    ref_data_list = []
    for i in crossref_refdata['reference']:
        ref_data_list.append(i)

    return(ref_data_list, crossref_refdata)
"""
Node Input
"""

""" Main Article"""
def create_article_node_main(data):
    print("Running")
    try:
        main_node = Article.nodes.get(doi=data['DOI'])
        print(main_node)
        print("Main Node Already Exists")
    except:

        author_temp = []
        for i in data['author']:
            author_temp.append(i['given'] + " " + i['family'])
        try:
            temp = Article(
                doi=data['DOI'],
                title=data['title'][0],
                volume=data['volume'],
                issue=data['issue'],
                author=author_temp,
                year=int(data['published-print']['date-parts'][0][0]),
                journal=data['short-container-title'][0],
                )
            print(temp)
            temp.save()
            print("Main Node was created")
        except:
            print("no")


""" Reference """
def create_article_node_reference(data):
    print("Running")

    for article in data:
        print(article)

        try:
            reference_input_node = Article.nodes.get(doi=article['DOI'])
            print("Reference Node Already Exists")
            print(reference_input_node)
        except:
            try:
                temp = Article(
                    doi = article['DOI'],
                    title = article['article-title'],
                    volume = article['volume'],
                    issue = article['issue'],
                    author = article['author'],
                    year = int(article['year']),
                    journal = article['journal-title'],
                )
                temp.save()

                print("Reference Node was created")
            except Exception as e:
                print(e)
                article['volume'] = ''
                if str(e) == "'volume'":
                    article['volume'] = ''
                    temp = Article(
                        doi=article['DOI'],
                        title=article['article-title'],
                        volume='',
                        issue=article['issue'],
                        author=article['author'],
                        year=int(article['year']),
                        journal=article['journal-title'],
                    )
                    temp.save()
                    print("Reference Node was created")
                elif str(e) == "'issue'":
                    article['issue'] = ''
                    temp = Article(
                        doi=article['DOI'],
                        title=article['article-title'],
                        volume=article['volume'],
                        issue=article['issue'],
                        author=article['author'],
                        year=int(article['year']),
                        journal=article['journal-title'],
                    )
                    temp.save()
                    print("Reference Node was created")


                else:
                    print(e)
                    logging.error(traceback.format_exc())

def create_article_node(data):
    print("Running")

    for article in data:
        print(article)

        try:
            reference_input_node = Article.nodes.get(doi=article['DOI'])
            print("Reference Node Already Exists")
            print(reference_input_node)
        except:
            try:
                temp = Article(
                    doi = article['DOI'],
                    title = article['article-title'],
                    volume = article['volume'],
                    issue = article['issue'],
                    author = article['author'],
                    year = int(article['year']),
                    journal = article['journal-title'],
                )
                temp.save()

                print("Reference Node was created")
            except Exception as e:
                print(e)
                article['volume'] = ''
                if str(e) == "'volume'":
                    article['volume'] = ''
                    temp = Article(
                        doi=article['DOI'],
                        title=article['article-title'],
                        volume='',
                        issue=article['issue'],
                        author=article['author'],
                        year=int(article['year']),
                        journal=article['journal-title'],
                    )
                    temp.save()
                    print("Reference Node was created")
                elif str(e) == "'issue'":
                    article['issue'] = ''
                    temp = Article(
                        doi=article['DOI'],
                        title=article['article-title'],
                        volume=article['volume'],
                        issue=article['issue'],
                        author=article['author'],
                        year=int(article['year']),
                        journal=article['journal-title'],
                    )
                    temp.save()
                    print("Reference Node was created")


                else:
                    print(e)
                    logging.error(traceback.format_exc())


"""Relationship"""


""" Create Relationship"""
def create_article_relationship(citing_article, cited_article, intext_citation, changed_outline):

    main_article = citing_article.replace("\n", "")
    main_article = main_article.replace("\r", "")
    main_article = main_article.replace(" ", "")

    try:
        print(main_article)

        main_article_node = Article.nodes.get(doi=main_article)
        for i in cited_article:

            try:
                print(i["DOI"])
                print(i["key"])
                print(i['key'][26:])
                for j in intext_citation:
                    if i['key'][26:] in j[1]:
                        print(i["DOI"] + " is in " + j[0])
                        print(j[0])
                        print()
                        try:
                            cited_temp = Article.nodes.get(doi=i["DOI"])
                            print(cited_temp)
                            print()
                            citation_counts = j[1].count(i['key'][26:])
                            print(j[0] + " 에서 인용된 횟수: " + str(citation_counts))
                            print()
                            #Introduction
                            if "Introduction" == changed_outline[j[0]]:
                            # Relation이 이미 존재하는지 조사 - 나중에 작성
                            #     cited_temp.nodes.has(Introduction=True)
                            #     print("already relationed in introduction")
                            #
                            # else:

                                if citation_counts > 0:

                                    try:
                                        rel = cited_temp.Introduction.connect(main_article_node, {'counts': citation_counts})

                                        rel.save
                                    except:
                                        print(cited_temp)
                                        print("Not Connected - Introduction")
                                        logging.error(traceback.format_exc())
                                        print()

                            #Data
                            elif "Data" == changed_outline[j[0]]:


                                if citation_counts > 0:
                                    try:
                                        rel = cited_temp.Data.connect(main_article_node,{'counts': citation_counts})

                                        rel.save
                                    except:
                                        print(cited_temp)
                                        print("Not Connected - Data")
                                        logging.error(traceback.format_exc())
                                        print()

                            #Methon
                            elif "Method" == changed_outline[j[0]]:


                                if citation_counts > 0:
                                    try:
                                        rel = cited_temp.Method.connect(main_article_node,{'counts': citation_counts})

                                        rel.save
                                    except:
                                        print(cited_temp)
                                        print("Not Connected - Method")
                                        logging.error(traceback.format_exc())
                                        print()

                            #Result
                            elif "Result" == changed_outline[j[0]]:


                                if citation_counts > 0:
                                    try:
                                        rel = cited_temp.Result.connect(main_article_node,{'counts': citation_counts})

                                        rel.save
                                    except:
                                        print(cited_temp)
                                        print("Not Connected - Result")
                                        logging.error(traceback.format_exc())
                                        print()

                            #Conclusion
                            elif "Conclusion" == changed_outline[j[0]]:


                                if citation_counts > 0:
                                    try:
                                        rel = cited_temp.Conclusion.connect(main_article_node,{'counts': citation_counts})

                                        rel.save
                                    except:
                                        print(cited_temp)
                                        print("Not Connected - Conclusion")
                                        logging.error(traceback.format_exc())
                                        print()

                            #Discussion
                            elif "Discussion" == changed_outline[j[0]]:


                                if citation_counts > 0:
                                    try:
                                        rel = cited_temp.Discussion.connect(main_article_node,{'counts': citation_counts})

                                        rel.save
                                    except:
                                        print(cited_temp)
                                        print("Not Connected - Discussion")
                                        logging.error(traceback.format_exc())
                                        print()
                            else:
                                print("어디에도 속하지 않습니다.")
                        except:
                            print("Some Thing Wrong")
                            logging.error(traceback.format_exc())
                            print()
                    else:
                        print("No")


            except:
                print("Key Error Occured")
                logging.error(traceback.format_exc())
                print()
            print("Finished")
            print()
    except:
        print("Can Not Find Citing Article")
        print("'" + main_article + "'")
        logging.error(traceback.format_exc())
        print()

