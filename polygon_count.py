import matplotlib.pyplot as plt
import poly_point_isect
import numpy as np
import sys
import networkx as nx

# helper functions


def proper_divs2(n):
    return {x for x in range(1, (n + 1) // 2 + 1) if n % x == 0 and n != x}


def get_key(item):
    return item[0]


def is_between(a, b, c):
    crossproduct = (c[1] - a[1]) * (b[0] - a[0]) - (c[0] - a[0]) * (b[1] - a[1])
    # compare versus epsilon for floating point values, or != 0 if using integers
    if abs(crossproduct) > sys.float_info.epsilon * 100:
        return False
    dotproduct = (c[0] - a[0]) * (b[0] - a[0]) + (c[1] - a[1]) * (b[1] - a[1])
    if dotproduct < 0:
        return False
    squaredlengthba = (b[0] - a[0]) * (b[0] - a[0]) + (b[1] - a[1]) * (b[1] - a[1])
    if dotproduct > squaredlengthba:
        return False
    return True


def is_above(l1, l2, p):
    if l2[0] < l1[0]:
        l1, l2 = l2, l1
    v1 = (l2[0] - l1[0], l2[1] - l1[1])  # Vector 1
    v2 = (l2[0] - p[0], l2[1] - p[1])  # Vector 1
    xp = v1[0] * v2[1] - v1[1] * v2[0]  # Cross product
    if xp < -sys.float_info.epsilon:  # if xp < 0.0:
        return True
    else:
        return False


def is_below(l1, l2, p):
    if l2[0] < l1[0]:
        l1, l2 = l2, l1
    v1 = (l2[0] - l1[0], l2[1] - l1[1])  # Vector 1
    v2 = (l2[0] - p[0], l2[1] - p[1])  # Vector 1
    xp = v1[0] * v2[1] - v1[1] * v2[0]  # Cross product
    if xp > sys.float_info.epsilon:  # if xp > 0.0:
        return True
    else:
        return False


def sort_vertices(pos, v):
    lv = []
    for vi in v:
        lv.append(pos[vi])
    lv = np.asarray(lv)
    lv_c = np.mean(lv, axis=0)
    lv_s = lv - np.repeat([lv_c], len(v), axis=0)
    a = np.arctan2(lv_s[:, 1], lv_s[:, 0])
    r = []
    for id in np.argsort(a):
        r.append(v[id])
    return r

def polygon_count(A):
    # sort ends from left to right
    for i, a in enumerate(A):
        A[i] = (sorted(a, key=get_key))

    # get interesections
    isects = poly_point_isect.isect_segments(A)

    # sort isects
    isects = sorted(isects, key=get_key)

    # find associate interesections with lines
    passess = []
    for p in isects:
        l_passess = []
        for id, s in enumerate(A):
            if is_between(s[0], s[1], p):
                l_passess.append(id)
        if A[l_passess[0]][0][1] < A[l_passess[1]][0][1]:
            l_passess[0], l_passess[1] = l_passess[1], l_passess[0]
        passess.append(l_passess)

    K = len(isects)
    count = np.zeros([K + 1])
    sigma = np.zeros([len(A), len(A), K + 1])

    G = nx.DiGraph()

    Q = []
    for inter, pas, e in zip(isects, passess, range(0, len(passess))):

        # step a
        for ks in range(0, K + 1):
            if sigma[pas[0], pas[1], ks] > 0:
                count[ks] = count[ks] + sigma[pas[0], pas[1], ks]
                Q.append((pas[0], pas[1], ks))

        # step b
        sigma[pas[1], pas[0], 2] = 1
        # step c
        for u in range(0, len(A)):
            if is_below(A[u][0], A[u][1], inter) and u != pas[1]:
                for j in range(2, K + 1):
                    if sigma[u, pas[0], j] > 0:
                        sigma[u, pas[1], j + 1] = sigma[u, pas[1], j + 1] + sigma[u, pas[0], j]
                        G.add_edge((u, pas[1], j + 1), (u, pas[0], j), weight=e)

        for l in range(0, len(A)):
            if is_above(A[l][0], A[l][1], inter) and l != pas[0]:
                for j in range(2, K + 1):
                    if sigma[pas[1], l, j] > 0:
                        sigma[pas[0], l, j + 1] = sigma[pas[0], l, j + 1] + sigma[pas[1], l, j]
                        G.add_edge((pas[0], l, j + 1), (pas[1], l, j), weight=e)

    # report polygons
    sink_nodes = [node for node, outdegree in G.out_degree(G.nodes()) if outdegree == 0]
    paths = []
    for q in Q:
        for path in nx.all_simple_paths(G, source=q, target=sink_nodes):
            path_p = []
            try:
                v = passess.index(list([q[0], q[1]]))
            except ValueError:
                v = passess.index(list([q[1], q[0]]))
            path_p.append(v)
            pw = len(passess)
            append = True
            for i in range(len(path) - 1):
                if pw > G[path[i]][path[i + 1]]['weight']:
                    pw = G[path[i]][path[i + 1]]['weight']
                    path_p.append(pw)
                else:
                    append = False
            if append:
                r = path[i + 1]
                try:
                    v = passess.index(list([r[0], r[1]]))
                except ValueError:
                    v = passess.index(list([r[1], r[0]]))
                path_p.append(v)
                paths.append(path_p)
    # sort vertices in polygon
    ps = []
    for p in paths:
        ps.append(sort_vertices(isects, p))

    return count, ps, isects, G, Q

def show (A, ps, isects, G, Q, flags,count):
    if flags["input"]:
        fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
        for id, a in enumerate(A):
            ax.plot([a[0][0], a[1][0]], [a[0][1], a[1][1]])
            ax.text(a[0][0], a[0][1], id)
        for id, p in enumerate(isects):
            ax.plot(p[0], p[1], 'o')
            ax.text(p[0], p[1], id)
        plt.axis('off')
        plt.show()

    if flags["result"]:
        l_isects = np.asarray(isects)
        for le, co in enumerate(count):
            if co > 0:
                fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
                for id, a in enumerate(A):
                    ax.plot([a[0][0], a[1][0]], [a[0][1], a[1][1]], 'k')
                    ax.text(a[0][0], a[0][1], id)
                for id, p in enumerate(isects):
                    ax.plot(p[0], p[1], 'or')
                    ax.text(p[0], p[1], id)
                for p in ps:
                    print(p)
                    if len(p) is le:
                        lp = p.copy()
                        lp.append(p[0])
                        ax.plot(l_isects[lp, 0], l_isects[lp, 1], lw=12, alpha=0.5)
                name = "Found " + str(le) + "-gons"
                fig.canvas.set_window_title(name)
                ax.set_title(name)
                plt.axis('off')
                plt.show()

    if flags["verbose"]:
        l_isects = np.asarray(isects)
        for le, co in enumerate(count):
            if co > 1:
                if co > 2:
                    div = proper_divs2(int(co))
                    if len(div) is 1:
                        co = co + 1
                        div = proper_divs2(int(co))
                    div.add(int(co))
                    div = list(div)
                    div.sort()
                    if len(div) % 2 == 0:
                        nrows = div[int(len(div) / 2) - 1]
                        ncols = div[int(len(div) / 2)]
                    else:
                        nrows = div[int(len(div) / 2)]
                        ncols = div[int(len(div) / 2)]
                else:
                    nrows = 1
                    ncols = int(co)
                fig, ax = plt.subplots(nrows=nrows, ncols=ncols, sharex=True, sharey=True)
                name = "Found " + str(le) + "-gons"
                fig.canvas.set_window_title(name)
                i = 0
                for p in ps:
                    if len(p) is le:
                        for id, a in enumerate(A):
                            print(i, int(i / ncols), int(i % ncols))
                            ax[int(i / ncols)][int(i % ncols)].plot([a[0][0], a[1][0]], [a[0][1], a[1][1]], 'k')
                            ax[int(i / ncols)][int(i % ncols)].text(a[0][0], a[0][1], id)
                        for id, ip in enumerate(isects):
                            ax[int(i / ncols)][int(i % ncols)].plot(ip[0], ip[1], 'or')
                            ax[int(i / ncols)][int(i % ncols)].text(ip[0], ip[1], id)
                        lp = p.copy()
                        lp.append(p[0])
                        ax[int(i / ncols)][int(i % ncols)].plot(l_isects[lp, 0], l_isects[lp, 1], lw=12 - i, alpha=0.5)
                        ax[int(i / ncols)][int(i % ncols)].axis('off')
                        i = i + 1
                plt.axis('off')
                plt.show()
            elif co == 1:
                fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
                for id, a in enumerate(A):
                    ax.plot([a[0][0], a[1][0]], [a[0][1], a[1][1]], 'k')
                    ax.text(a[0][0], a[0][1], id)
                for id, p in enumerate(isects):
                    ax.plot(p[0], p[1], 'or')
                    ax.text(p[0], p[1], id)
                for p in ps:
                    print(p)
                    if len(p) is le:
                        lp = p.copy()
                        lp.append(p[0])
                        ax.plot(l_isects[lp, 0], l_isects[lp, 1], lw=12 - i, alpha=0.5)
                name = "Found " + str(le) + "-gons"
                fig.canvas.set_window_title(name)
                plt.axis('off')
                plt.show()

    if flags["graph"]:
        fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
        # pos = nx.spring_layout(G)
        pos = nx.planar_layout(G)
        # nodes
        nx.draw_networkx_nodes(G, pos, node_size=1000)
        nx.draw_networkx_nodes(G, pos, node_size=1000, nodelist=Q, node_color="r")

        # edges
        nx.draw_networkx_edges(G, pos, edgelist=G.edges, width=3)

        # labels
        nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        plt.axis('off')
        plt.show()

