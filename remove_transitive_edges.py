#!/usr/bin/env python

"""
    usage:
        remove_transitive_edges [options] graph.dot
    where the options are:
        -h,--help : print usage and quit

    graph.dot is a file with a directed graph. The first row is always
        
        Digraph G {

    and the last row is always 

        }

    Each row in the middle section describes an edge. For example,

        1 -> 2

    is a directed edge from a node with the label '1' to the node with the label    '2'.
"""

from sys import argv, stderr
from getopt import getopt, GetoptError
from copy import deepcopy
from graph import *


def simplify(G):
    """Simplify the graph S by removing the transitively-inferrible edges.
    
    S is just a copy of G, which is the input graph.
    """

    S = deepcopy(G)

    def has_path(u, v):
        """Return True if there is a path from node u to node v in graph S."""
        stack = [u]
        visited = set()
        while stack:
            current = stack.pop()
            if current == v:
                return True
            if current not in visited:
                visited.add(current)
                # Push all neighbors of current onto the stack.
                stack.extend(list(S.edges[current].keys()))
        return False

    # Iterate over a snapshot of the current edges to avoid modifying during iteration.
    for u in list(S.edges.keys()):
        for v in list(S.edges[u].keys()):
            # Temporarily remove the edge (u, v).
            S.delete_edge(u, v)
            # If there is still a path from u to v, the direct edge is redundant.
            if not has_path(u, v):
                # Otherwise, add the edge back.
                S.add_edge(u, v)
    return S


   

def main(filename):
    # read the graph from the input file
    graph = Graph(filename)
    print(f"Read the graph from {filename}", file=stderr)

    # simplify the graph by removing the transitively-inferrible edges
    simplified = simplify(graph)
    print(f"Simplified the graph", file=stderr)

    # print the simplified graph in the same format as the input file
    print(simplified)

if __name__ == "__main__":
    try:
        opts, args = getopt(argv[1:], "h", ["help"])
    except GetoptError as err:
        print(err)
        print(__doc__, file=stderr)
        exit(1) 

    for o, a in opts:
        if o in ("-h", "--help"):
            print(__doc__, file=stderr)
            exit()
        else:
            assert False, "unhandled option"

    if len(args) != 1:
        print(__doc__, file=stderr)
        exit(2)

    main(args[0])
