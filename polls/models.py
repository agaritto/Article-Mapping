from django.utils import timezone
from django.db import models
from django.urls import reverse
from neomodel import *


# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

class CitationLocation(models.Model):
    citing_paper_doi = models.CharField(db_column='citing_paper_DOI', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cited_paper_doi = models.CharField(max_length=100, blank=True, null=True)
    outline = models.CharField(max_length=300, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'citation_location'

class Outline(models.Model):
    paper_doi = models.CharField(db_column='paper_DOI',max_length=100)  # Field name made lowercase.
    original_outline = models.CharField(max_length=200, blank=True, null=True)
    changed_outline = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'outline'

class Paper(models.Model):
    doi = models.CharField(db_column='DOI', primary_key=True, max_length=200)  # Field name made lowercase.
    article_title = models.CharField(db_column='article-title', max_length=200, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    journal_title = models.CharField(db_column='journal-title', max_length=200, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    author = models.CharField(max_length=45, blank=True, null=True)
    year = models.CharField(max_length=5, blank=True, null=True)
    volume = models.CharField(max_length=45, blank=True, null=True)
    issue = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'paper'

class CreateRelation(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    citing_article = models.CharField(max_length=200, blank=True, null=True)
    cited_article = models.CharField(max_length=200, blank=True, null=True)
    changed_outline = models.CharField(max_length=200, blank=True, null=True)
    citation_counts = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'create_relation'



class Introduction(StructuredRel):
    counts = IntegerProperty()

class Data(StructuredRel):
    counts = IntegerProperty()

class Method(StructuredRel):
    counts = IntegerProperty()

class Result(StructuredRel):
    counts = IntegerProperty()

class Conclusion(StructuredRel):
    counts = IntegerProperty()

class Discussion(StructuredRel):
    counts = IntegerProperty()


class Article(StructuredNode):
    uid = UniqueIdProperty()
    doi = StringProperty(unique_index=True)
    title = StringProperty()
    volume = StringProperty()
    issue = StringProperty()
    author = StringProperty()
    year = StringProperty()
    journal = StringProperty()

    Introduction = RelationshipTo('Article', 'Introduction', model=Introduction)
    Data = RelationshipTo('Article', 'Data', model=Data)
    Method = RelationshipTo('Article', 'Method', model=Method)
    Result = RelationshipTo('Article', 'Result', model=Result)
    Conclusion = RelationshipTo('Article', 'Conclusion', model=Conclusion)
    Discussion = RelationshipTo('Article', 'Discussion', model=Discussion)


class Users(models.Model):
    username = models.CharField(max_length=64,verbose_name="사용자이름")
    password = models.CharField(max_length=64, verbose_name="비밀번호")
    registered_dttm = models.DateField(auto_now_add=True, verbose_name="등록시간")

    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"
        verbose_name ="사용자"
        verbose_name_plural = "사용자"
