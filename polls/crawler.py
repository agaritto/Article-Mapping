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


"""
Node Input
"""
def create_article_node(data):
    try:
        node = Article.nodes.get(doi=data['doi'])
    except:
        try:
            temp = Article(
                doi=data['doi'],
                title=data['article_title'],
                journal=data['journal_title'],
                author=data['author'],
                year=data['year'],
                volume=data['volume'],
                issue=data['issue'],
                )

            temp.save()
        except:
            temp = Article(
                doi=data['doi'],
                title=data['article_title'],
                journal=data['journal_title'],
                author=data['author'],
                year=data['year'],
                volume=data['volume'],
                issue=data['issue'],
            )



"""Relationship"""

""" Create Relationship"""
def create_relationship(citing_article, cited_article, changed_outline, citation_counts):
    #Main Article DOI 가져오기
    main_article = citing_article
    try:
        #Main Article Node 가져오기
        main_article_node = Article.nodes.get(doi=main_article)
        cited_article_node = Article.nodes.get(doi=cited_article)
        if changed_outline == "Introduction":
            rel = cited_article_node.Introduction.connect(main_article_node, {'counts': citation_counts})
            rel.save
            return rel
        elif changed_outline == "Data":
            rel = cited_article_node.Data.connect(main_article_node, {'counts': citation_counts})
            rel.save
            return rel
        elif changed_outline == "Method":
            rel = cited_article_node.Method.connect(main_article_node, {'counts': citation_counts})
            rel.save
            return rel
        elif changed_outline == "Result":
            rel = cited_article_node.Result.connect(main_article_node, {'counts': citation_counts})
            rel.save
            return rel
        elif changed_outline == "Conclusion":
            rel = cited_article_node.Conclusion.connect(main_article_node, {'counts': citation_counts})
            rel.save
            return rel
        elif changed_outline == "Discussion":
            rel = cited_article_node.Discussion.connect(main_article_node, {'counts': citation_counts})
            rel.save
            return rel
        else:
            print("Something Wrong")
    except:
        print("Not Connected - Result")
        logging.error(traceback.format_exc())
        print("Not Connected")


""" Create Relationship"""
def create_article_relationship(citing_article, cited_article, intext_citation, changed_outline):
    main_article = citing_article.replace("\n", "")
    main_article = main_article.replace("\r", "")
    main_article = main_article.replace(" ", "")
    try:
        main_article_node = Article.nodes.get(doi=main_article)
        for i in cited_article:
            try:
                for j in intext_citation:
                    if i['key'][26:] in j[1]:
                        try:
                            cited_temp = Article.nodes.get(doi=i["DOI"])
                            citation_counts = j[1].count(i['key'][26:])
                            if "Introduction" == changed_outline[j[0]]:
                                if citation_counts > 0:
                                    try:
                                        rel = cited_temp.Introduction.connect(main_article_node, {'counts': citation_counts})

                                        rel.save
                                    except:
                                        logging.error(traceback.format_exc())

                            #Data
                            elif "Data" == changed_outline[j[0]]:
                            # else:

                                if citation_counts > 0:
                                    try:
                                        rel = cited_temp.Data.connect(main_article_node,{'counts': citation_counts})

                                        rel.save
                                    except:
                                        print("Not Connected - Data")
                                        logging.error(traceback.format_exc())

                            #Methon
                            elif "Method" == changed_outline[j[0]]:

                                if citation_counts > 0:
                                    try:
                                        rel = cited_temp.Method.connect(main_article_node,{'counts': citation_counts})

                                        rel.save
                                    except:
                                        print("Not Connected - Method")
                                        logging.error(traceback.format_exc())

                            #Result
                            elif "Result" == changed_outline[j[0]]:

                                if citation_counts > 0:
                                    try:
                                        rel = cited_temp.Result.connect(main_article_node,{'counts': citation_counts})

                                        rel.save
                                    except:
                                        print("Not Connected - Result")
                                        logging.error(traceback.format_exc())

                            #Conclusion
                            elif "Conclusion" == changed_outline[j[0]]:

                                if citation_counts > 0:
                                    try:
                                        rel = cited_temp.Conclusion.connect(main_article_node,{'counts': citation_counts})

                                        rel.save
                                    except:
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



# def


# def outline_changed():
