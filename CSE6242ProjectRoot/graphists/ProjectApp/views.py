# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
import textwrap

from django.http import HttpResponse
from time import gmtime, strftime
from django.views.generic.base import View
from django.template import loader, Context, Template
from ProjectApp.models import *
import sys
from itertools import *
from django.db import connection
from django.views.decorators.csrf import *
import json
import networkx as nx
import operator

class MainPageView(View):

    def dispatch(request, *args, **kwargs):
        t = loader.get_template('ProjectApp/main.html')
        return HttpResponse(t.render())

def searchFunction_graph(request):
        query = request.GET.get('query')
        nodes_max = request.GET.get('nodes')
        hops = request.GET.get('hops')
        minYear = request.GET.get('minYear')
        maxYear = request.GET.get('maxYear')
        t = loader.get_template('ProjectApp/graphView.html')
        result_list = []
        # Perform FTS Search
        links_list = [row
                      for row in runQuery(
                """WITH RECURSIVE links (id1, title1, authors1, journal1, year1, url1, id2, title2, authors2, journal2, year2, url2, counter) AS (
                   SELECT n1.id AS id1, n1.title AS title1, n1.authors, n1.journal, n1.year, n1.url, n2.id AS id2, n2.title AS title2, n2.authors, n2.journal, n2.year, n2.url, 1 as counter
                   FROM nodes AS n1 INNER JOIN edges INNER JOIN nodes AS n2
                   ON n1.id = edges.source_id AND edges.target_id = n2.id
                   WHERE n1.title LIKE """ + """'%""" + query + """%'""" +
                """UNION ALL
                   SELECT links.id2, links.title2, links.authors2, links.journal2, links.year2, links.url2, n3.id, n3.title, n3.authors, n3.journal, n3.year, n3.url, links.counter + 1
                   FROM links INNER JOIN edges INNER JOIN nodes AS n3
                   ON links.id2 = edges.source_id AND edges.target_id = n3.id
                   WHERE links.counter < """ + str(hops) +
                """)
                   SELECT DISTINCT id1, title1, authors1, journal1, year1, url1, id2, title2, authors2, journal2, year2, url2 FROM links LIMIT """ + str(
                    int(int(nodes_max))) +
                """;
                """
            )]
        # links_list2 = [row
        #                for row in runQuery(
        #         """WITH RECURSIVE links (id1, title1, authors1, journal1, year1, url1, id2, title2, authors2, journal2, year2, url2, counter) AS (
        #            SELECT n1.id AS id1, n1.title AS title1, n1.authors, n1.journal, n1.year, n1.url, n2.id AS id2, n2.title AS title2, n2.authors, n2.journal, n2.year, n2.url, 1 as counter
        #            FROM nodes AS n1 INNER JOIN edges INNER JOIN nodes AS n2
        #            ON n1.id = edges.target_id AND edges.source_id = n2.id
        #            WHERE n1.title LIKE """ + """'%""" + query + """%'""" +
        #         """UNION ALL
        #            SELECT links.id2, links.title2, links.authors2, links.journal2, links.year2, links.url2, n3.id, n3.title, n3.authors, n3.journal, n3.year, n3.url, links.counter + 1
        #            FROM links INNER JOIN edges INNER JOIN nodes AS n3
        #            ON links.id2 = edges.target_id AND edges.source_id = n3.id
        #            WHERE links.counter < """ + str(hops) +
        #         """)
        #            SELECT DISTINCT id1, title1, authors1, journal1, year1, url1, id2, title2, authors2, journal2, year2, url2 FROM links LIMIT """ + str(
        #             int(int(nodes_max)/2)) +
        #         """;
        #         """
        #     )]
        # links_list1.extend(links_list2)
        # links_list = links_list1
        nodes_list = set([])
        # for l in links_list:
            # for ll in l:
                # if type(ll) is str:
                    # ll = str(ll).encoding='utf-8'.replace('&',' and ')
                    # ll = str(ll).encoding = 'utf-8'.replace('\\', '`')
                    # ll = str(ll).encoding='utf-8'.replace('\"', '``')
        for l in links_list:
            if type(l[2]) is str:
                nodes_list.add((l[0], l[1], str(l[2]).encode("utf8").replace('&',' and ').replace('\\', '`').replace('\"', '``'), l[3], l[4], l[5]))
            else:
                nodes_list.add((l[0], l[1],l[2],l[3], l[4], l[5]))
            if type(l[8]) is str:
                nodes_list.add((l[6], l[7], str(l[8]).encode("utf8").replace('&',' and ').replace('\\', '`').replace('\"', '``'), l[9], l[10], l[11]))
            else:
                nodes_list.add((l[6], l[7],l[8],l[9], l[10], l[11]))
        nodes_list = list(nodes_list)
        c = Context({
            'links_list': links_list,
            'nodes_list': nodes_list,
        })
        return HttpResponse(t.render(c))

def searchFunction_list(request):
    query = request.GET.get('query')
    nodes_max = request.GET.get('nodes')
    hops = request.GET.get('hops')
    minYear = request.GET.get('minYear')
    maxYear = request.GET.get('maxYear')
    t = loader.get_template('ProjectApp/listView.html')
    result_list = []
    # Make 50 a parameter
    # Perform FTS Search
    # links_list = [(row[0], row[1].encode("utf8"), row[2].encode("utf8"), row[3].encode("utf8"), row[4],
    #                row[5], row[6].encode("utf8"), row[7].encode("utf8"), row[8].encode("utf8"), row[9])
    #               for row in runQuery(
    links_list = [row
                  for row in runQuery(
            """WITH RECURSIVE links (id1, title1, authors1, journal1, year1, url1, id2, title2, authors2, journal2, year2, url2, counter) AS (
               SELECT n1.id AS id1, n1.title AS title1, n1.authors, n1.journal, n1.year, n1.url, n2.id AS id2, n2.title AS title2, n2.authors, n2.journal, n2.year, n2.url, 1 as counter
               FROM nodes AS n1 INNER JOIN edges INNER JOIN nodes AS n2
               ON n1.id = edges.source_id AND edges.target_id = n2.id
               WHERE n1.title LIKE """ + """'%""" + query + """%'""" +
#             'AND n1.year != 0 AND n1.year >= ' + minYear + 'AND n1.year <= ' + maxYear +
    """UNION ALL
               SELECT links.id2, links.title2, links.authors2, links.journal2, links.year2, links.url2, n3.id, n3.title, n3.authors, n3.journal, n3.year, n3.url, links.counter + 1
               FROM links INNER JOIN edges INNER JOIN nodes AS n3
               ON links.id2 = edges.source_id AND edges.target_id = n3.id
               WHERE links.counter < """ + str(hops) +
            """)
               SELECT DISTINCT id1, title1, authors1, journal1, year1, url1, id2, title2, authors2, journal2, year2, url2 FROM links LIMIT """ + str(
                nodes_max) +
            """;
            """
        )]


    nodes_list = set([])
    for l in links_list:
        nodes_list.add((l[0], l[1], l[2], l[3], l[4], l[5]))
        nodes_list.add((l[6], l[7], l[8], l[9], l[10], l[11]))
    nodes_list = list(nodes_list)
    c = Context({
        'nodes_list': nodes_list,
    })
    return HttpResponse(t.render(c))

def searchFunction_citation(request):
    queryID = request.GET.get('queryID')
    t = loader.get_template('ProjectApp/citationView.html')
    result_list = []
    # Make 50 a parameter
    # Perform FTS Search
    # links_list = [(row[0], row[1].encode("utf8"), row[2].encode("utf8"), row[3].encode("utf8"), row[4],
    #                row[5], row[6].encode("utf8"), row[7].encode("utf8"), row[8].encode("utf8"), row[9])
    #               for row in runQuery(
    links_list = [row
                  for row in runQuery(
            """SELECT n1.id AS id1, n1.title AS title1, n1.authors, n1.journal, n1.year, n1.url, n2.id AS id2, n2.title AS title2, n2.authors, n2.journal, n2.year, n2.url
               FROM nodes AS n1 INNER JOIN edges INNER JOIN nodes AS n2
               ON n1.id = edges.source_id AND edges.target_id = n2.id
               WHERE n1.id = """ + queryID
        )]


    nodes_list = set([])
    for l in links_list:
        nodes_list.add((l[0], l[1], l[2], l[3], l[4], l[5]))
        nodes_list.add((l[6], l[7], l[8], l[9], l[10], l[11]))
    nodes_list = list(nodes_list)
    c = Context({
        'nodes_list': nodes_list,
    })
    return HttpResponse(t.render(c))

@csrf_exempt
def analyzeFunction_centralNodes(request):
    t = loader.get_template('ProjectApp/centralityView.html')
    requestDict = dict(request.POST.iterlists())
    centrality = requestDict['centrality'][0]
    graphJsonString = requestDict['graphJson'][0]
    centMax = int(requestDict['centMax'][0])
    graphJson = json.loads(graphJsonString)

    G = nx.DiGraph()
    for n in graphJson['nodes']:
        G.add_node(n['id'].encode('utf-8'))
    for e in graphJson['links']:
        G.add_edge(e['source'].encode('utf-8'), e['target'].encode('utf-8'))

    sortedCentralities = getSortedCentralities(G, centrality)
    # for c in ['pc', 'pcg', 'bw', 'dg', 'pr', 'kz']:
    #     sC = getSortedCentralities(G, c)
    #     removalTrend = pathRemovalTrend(G.copy(), sC)
    #     # print 'REMOVAL TREND ' + c
    #     print removalTrend
    #     # print
    if centMax <= 0:
        centMax = 0
    if centMax > len(sortedCentralities)-1:
        centMax = len(sortedCentralities) - 1
    c = Context({
        'centralNodes': sortedCentralities[0:centMax],
    })
    return HttpResponse(t.render(c))

    # return HttpResponse(t.render())

def getSortedCentralities(G, centrality):
    result = []
    centralityDict = {}

    if centrality == 'pc':
        centralityDict = calculatePathCentrality(G)
        result = sorted([(k, v) for k, v in centralityDict.iteritems()], key=operator.itemgetter(1), reverse=True)
    if centrality == 'pcg':
        [centralityDict, result] = greedyPathCentralityExtraction(G.copy())
    if centrality == 'bw':
        centralityDict = nx.betweenness_centrality(G)
        result = sorted([(k, v) for k, v in centralityDict.iteritems()], key=operator.itemgetter(1), reverse=True)
    if centrality == 'dg':
        centralityDict = nx.degree_centrality(G)
        result = sorted([(k, v) for k, v in centralityDict.iteritems()], key=operator.itemgetter(1), reverse=True)
    if centrality == 'pr':
        centralityDict = nx.pagerank(G)
        result = sorted([(k, v) for k, v in centralityDict.iteritems()], key=operator.itemgetter(1), reverse=True)
    if centrality == 'kz':
        centralityDict = nx.katz_centrality(G)
        result = sorted([(k, v) for k, v in centralityDict.iteritems()], key=operator.itemgetter(1), reverse=True)

    return result

def calculatePathCentrality(G):
    result = {}
    for n in G.nodes():
        result[n] = 0
    stPairs = []
    graphs = list(nx.weakly_connected_component_subgraphs(G))
    for g in graphs:
        d_in = g.in_degree()
        d_out = g.out_degree()
        sources = []
        for n in d_in:
            if d_in[n] == 0:
                sources.append(n)
        targets = []
        for n in d_out:
            if d_out[n] == 0:
                targets.append(n)
        for s in sources:
            for t in targets:
                paths = list(nx.all_simple_paths(G,source=s,target=t))
                if (len(paths) > 0):
                    stPairs.append(((s,t),paths))
    for (st,paths) in stPairs:
        s = st[0]
        t = st[1]
        result[s] += 1
        result[t] += 1
        for p in paths:
            for n in p[1:-1]:
                result[n] += 1
    return result

def greedyPathCentralityExtraction(G):
    centralities = sorted([(k, v) for k, v in calculatePathCentrality(G).iteritems()], key=operator.itemgetter(1), reverse=True)
    result = []
    tmpCentrailities = centralities
    while(len(G.nodes()) > 0):
        result.append(tmpCentrailities[0])
        G.remove_node(tmpCentrailities[0][0])
        tmpCentrailities = sorted([(k, v) for k, v in calculatePathCentrality(G).iteritems()], key=operator.itemgetter(1),reverse=True)
    return (centralities, result)

def pathRemovalTrend(G, centralNodesList):
    result = []
    totalPaths = 0
    graphs = list(nx.weakly_connected_component_subgraphs(G))
    for g in graphs:
        d_in = g.in_degree()
        d_out = g.out_degree()
        sources = []
        for n in d_in:
            if d_in[n] == 0:
                sources.append(n)
        targets = []
        for n in d_out:
            if d_out[n] == 0:
                targets.append(n)
        for s in sources:
            for t in targets:
                totalPaths += len(list(nx.all_simple_paths(G, source=s, target=t)))
    result.append(totalPaths)
    for i in range(len(centralNodesList)):
        G.remove_node(centralNodesList[i][0])
        totalPaths = 0
        graphs = list(nx.weakly_connected_component_subgraphs(G))
        for g in graphs:
            d_in = g.in_degree()
            d_out = g.out_degree()
            sources = []
            for n in d_in:
                if d_in[n] == 0:
                    sources.append(n)
            targets = []
            for n in d_out:
                if d_out[n] == 0:
                    targets.append(n)
            for s in sources:
                for t in targets:
                    totalPaths += len(list(nx.all_simple_paths(G, source=s, target=t)))
        result.append(totalPaths)
    return result

def runQuery(query_string):
    cursor = connection.cursor()
    cursor.execute(query_string)
    rows = cursor.fetchall()

    return rows