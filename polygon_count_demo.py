import polygon_count as pc

A = [((0, 1), (13, 16)),
     ((13, 2), (0, 2)),
     ((13, 5), (0, 8)),
     ((11, -5), (11, 16)),
     ((0, 12), (13, -5)),
     ((8, 12), (12, -6)),
     ((13, 7), (0,7))]

flags = {
    "input": True,
    "graph": False,
    "result": False,
    "verbose": True
}

count, ps, isects, G, Q=pc.polygon_count(A)
pc.show(A, ps, isects, G, Q, flags,count)