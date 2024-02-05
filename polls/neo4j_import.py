import json
import logging
import traceback

from .models import *
from neomodel import *
from neo4j import *
import re

"""
Node Input
"""
def desktop_create_node(data):
    print("Running")
    print(data)
    try:
        node = Article.nodes.get(doi=data['doi'])
        print(node)
        print("Main Node Already Exists")
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

            print(temp)
            temp.save()
            print("Main Node was created")
        except:
            print("no")

            temp = Article(
                doi=data['doi'],
                title=data['article_title'],
                journal=data['journal_title'],
                author=data['author'],
                year=data['year'],
                volume=data['volume'],
                issue=data['issue'],
            )
            print(temp)

"""Relationship"""

""" Create Relationship"""
def desktop_create_relationship(citing_article, cited_article, changed_outline, citation_counts):
    main_article = citing_article
    print(main_article)
    try:
        print(main_article)
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
            print(main_article, cited_article)
    except:
        print(cited_article, citing_article)
        print("Not Connected - Result")
        logging.error(traceback.format_exc())
        print()
        print("Not Connected")

