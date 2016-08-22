# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class EdgeTypes(models.Model):
    name = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'edge_types'


class Edges(models.Model):
    source_id = models.IntegerField(primary_key=True, blank=True, null=False)
    target_id = models.IntegerField(primary_key=True, blank=True, null=False)
    type = models.IntegerField(blank=True, null=True)
    weight = models.TextField(blank=True, null=True)  # This field type is a guess.
    timestamp = models.IntegerField(primary_key=True, blank=True, null=False)

    class Meta:
        managed = False
        db_table = 'edges'
        unique_together = (('source_id', 'target_id', 'timestamp'),)


class NodeTypes(models.Model):
    name = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'node_types'


class Nodes(models.Model):
    id = models.IntegerField(primary_key=True, blank=True, null=False)  # AutoField?
    type = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)  # This field type is a guess.
    google_scholar_id_string = models.TextField(blank=True, null=True)  # This field type is a guess.
    rough_info_crawl_time = models.IntegerField(blank=True, null=True)
    bibtex_crawl_time = models.IntegerField(blank=True, null=True)
    citing_papers_crawl_time = models.IntegerField(blank=True, null=True)
    citing_papers_crawled = models.IntegerField(blank=True, null=True)
    bibtex_url = models.TextField(blank=True, null=True)  # This field type is a guess.
    bibtex = models.TextField(blank=True, null=True)  # This field type is a guess.
    title = models.TextField(blank=True, null=True)  # This field type is a guess.
    source_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    authors = models.TextField(blank=True, null=True)  # This field type is a guess.
    year = models.IntegerField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)  # This field type is a guess.
    pdf_url = models.TextField(blank=True, null=True)  # This field type is a guess.
    cite_count = models.IntegerField(blank=True, null=True)
    cited_by_url = models.TextField(blank=True, null=True)  # This field type is a guess.
    related_articles_url = models.TextField(blank=True, null=True)  # This field type is a guess.
    version_count = models.IntegerField(blank=True, null=True)
    version_url = models.TextField(blank=True, null=True)  # This field type is a guess.
    journal = models.TextField(blank=True, null=True)  # This field type is a guess.
    booktitle = models.TextField(blank=True, null=True)  # This field type is a guess.
    publisher = models.TextField(blank=True, null=True)  # This field type is a guess.
    institution = models.TextField(blank=True, null=True)  # This field type is a guess.
    school = models.TextField(blank=True, null=True)  # This field type is a guess.
    volume = models.IntegerField(blank=True, null=True)
    number = models.TextField(blank=True, null=True)  # This field type is a guess.
    pages = models.TextField(blank=True, null=True)  # This field type is a guess.
    editor = models.TextField(blank=True, null=True)  # This field type is a guess.
    organization = models.TextField(blank=True, null=True)  # This field type is a guess.
    address = models.TextField(blank=True, null=True)  # This field type is a guess.
    series = models.IntegerField(blank=True, null=True)
    edition = models.IntegerField(blank=True, null=True)
    techreport_type = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'nodes'


class Properties(models.Model):
    key = models.TextField(unique=True, blank=True, null=True)  # This field type is a guess.
    value = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'properties'


class Search(models.Model):
    title = models.TextField(blank=True, null=True)  # This field type is a guess.
    authors = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'search'


class SearchContent(models.Model):
    docid = models.IntegerField(primary_key=True, blank=True, null=False)
    c0title = models.TextField(blank=True, null=True)  # This field type is a guess.
    c1authors = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'search_content'


class SearchSegdir(models.Model):
    level = models.IntegerField(primary_key=True, blank=True, null=False)
    idx = models.IntegerField(primary_key=True, blank=True, null=False)
    start_block = models.IntegerField(blank=True, null=True)
    leaves_end_block = models.IntegerField(blank=True, null=True)
    end_block = models.IntegerField(blank=True, null=True)
    root = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'search_segdir'
        unique_together = (('level', 'idx'),)


class SearchSegments(models.Model):
    blockid = models.IntegerField(primary_key=True, blank=True, null=False)
    block = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'search_segments'


class SeedPapers(models.Model):
    id = models.IntegerField(primary_key=True, blank=True, null=False)  # AutoField?

    class Meta:
        managed = False
        db_table = 'seed_papers'
