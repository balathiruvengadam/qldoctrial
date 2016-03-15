# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..deps import prepare_dependencies
from ..utils import graph_for_items


def bw_plot_group(repo, args):
    group = repo.get_group(args['group']) if args['group'] else None
    if args['show_nodes']:
        nodes = group.nodes if group else repo.nodes
    else:
        nodes = []

    if group:
        groups = [group]
        groups.extend(group.subgroups)
    else:
        groups = repo.groups

    yield "digraph bundlewrap"
    yield "{"

    # Print subgraphs *below* each other
    yield "rankdir = LR"

    # Global attributes
    yield ("node [color=\"#303030\"; "
                 "fillcolor=\"#303030\"; "
                 "fontname=Helvetica]")
    yield "edge [arrowhead=vee]"

    for group in groups:
        yield "\"{}\" [fontcolor=white,style=filled];".format(group.name)

    for node in nodes:
        yield "\"{}\" [fontcolor=\"#303030\",shape=box,style=rounded];".format(node.name)

    for group in groups:
        for subgroup in group.immediate_subgroup_names:
            yield "\"{}\" -> \"{}\" [color=\"#6BB753\",penwidth=2]".format(group.name, subgroup)

    if args['show_nodes']:
        for group in groups:
            for node in group._nodes_from_static_members:
                yield "\"{}\" -> \"{}\" [color=\"#D18C57\",penwidth=2]".format(
                    group.name, node.name)

            for node in group._nodes_from_patterns:
                yield "\"{}\" -> \"{}\" [color=\"#714D99\",penwidth=2]".format(
                    group.name, node.name)

    yield "}"


def bw_plot_node(repo, args):
    node = repo.get_node(args['node'])
    for line in graph_for_items(
        node.name,
        prepare_dependencies(node.items),
        cluster=args['cluster'],
        concurrency=args['depends_concurrency'],
        static=args['depends_static'],
        regular=args['depends_regular'],
        reverse=args['depends_reverse'],
        auto=args['depends_auto'],
    ):
        yield line
