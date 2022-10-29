# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 22:32:31 2022

@author: Pawat Akara-pipattana
"""

from scholarly import scholarly
import networkx as nx

def build_graph(G,sch_id,depth: int,bredth: int,last_author=[]):
    author_search = scholarly.search_author_id(sch_id)
    author = scholarly.fill(author_search,sections=['coauthors','indices','counts'])
    author_name = author['name']
    author_hin = author['hindex']
    author_ncite = author['citedby']
    G.add_node(author_name,hindex=author_hin,name=author_name,ncite=author_ncite)
    print("now at %s, depth=%d"%(author_name,depth))
    if depth>0:
        for coauthor in author['coauthors'][:int(bredth)]:
            G.add_edge(author_name,coauthor['name'])
            if coauthor['name'] not in last_author:
                last_author.append(author_name)
                build_graph(G,coauthor['scholar_id'],depth-1,bredth,last_author)

#input and parameters
name = 'author name here'
sch_id = next(scholarly.search_author(name))['scholar_id']
print(sch_id)
depth = 4
bredth = 6

G = nx.DiGraph()
output_path = '%s_%d_%d.gexf'%(name.replace(' ','_'),depth,bredth)

build_graph(G,sch_id,depth,bredth)
nx.write_gexf(G,output_path)

