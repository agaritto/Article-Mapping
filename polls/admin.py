from django.contrib import admin



# Register your models here.
from polls.models import CitationLocation, Outline, Paper


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = (
        'doi',
        'article_title',
        'journal_title',
        'author',
        'year',
        'volume',
        'issue',
    )

    list_display_links = (
        'doi',
        'article_title',
        'journal_title',
        'author',
        'year',
        'volume',
        'issue',
    )

    search_fields = (
        'doi',
        'article_title',
        'journal_title',
        'author',
        'year',
        'volume',
        'issue',
    )

@admin.register(CitationLocation)
class Intextcitation(admin.ModelAdmin):
    list_display = (
        'id',
        'citing_paper_doi',
        'cited_paper_doi',
        'outline',
        'count',
    )

    list_display_links = (
        'id',
        'citing_paper_doi',
        'cited_paper_doi',
        'outline',
        'count',
    )

    search_fields = (
        'id',
        'citing_paper_doi',
        'cited_paper_doi',
        'outline',
        'count',
    )

@admin.register(Outline)
class OutlineAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'paper_doi',
        'original_outline',
        'changed_outline',
    )

    list_display_links = (
        'id',
        'paper_doi',
        'original_outline',
        'changed_outline',
    )

    search_fields = (
        'id',
        'paper_doi',
        'original_outline',
        'changed_outline',
    )
