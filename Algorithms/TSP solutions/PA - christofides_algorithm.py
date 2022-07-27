# from functions.matching import find_minimum_weight_matching


def get_length(p, q):
    return ((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) ** 0.5


def kruskal(g):
    edge_list = {}
    trees = {}
    mst = {}
    mst_edges = []
    t = 0

    for i in range(len(g)):
        for j in range(len(g)):
            d = get_length(g[i], g[j])
            if i < j:
                edge_list[(i, j)] = get_length(g[i], g[j])
    edge_list = dict(sorted(edge_list.items(), key=lambda item: item[1]))

    for key, values in edge_list.items():
        cn1, cn2 = 0, 0
        for k, v in trees.items():
            if key[0] in v:
                cn1 = k
            if key[1] in v:
                cn2 = k

        if cn1 == 0 and cn2 == 0:
            t += 1
            mst.setdefault(key[0], [])
            mst[key[0]].append(key[1])
            mst.setdefault(key[1], [])
            mst[key[1]].append(key[0])
            mst_edges.append(set([key[0], key[1]]))

            trees.setdefault(t, {key[0], key[1]})

        elif cn1 == 0 and cn2 != 0:
            mst.setdefault(key[0], [])
            mst[key[0]].append(key[1])
            mst.setdefault(key[1], [])
            mst[key[1]].append(key[0])
            mst_edges.append(set([key[0], key[1]]))

            trees[cn2].add(key[0])

        elif cn1 != 0 and cn2 == 0:
            mst.setdefault(key[0], [])
            mst[key[0]].append(key[1])
            mst.setdefault(key[1], [])
            mst[key[1]].append(key[0])
            mst_edges.append(set([key[0], key[1]]))

            trees[cn1].add(key[1])

        elif (cn1 != 0) and (cn2 != 0) and (cn1 != cn2):
            mst.setdefault(key[0], [])
            mst[key[0]].append(key[1])
            mst.setdefault(key[1], [])
            mst[key[1]].append(key[0])
            mst_edges.append(set([key[0], key[1]]))

            if len(trees[cn1]) >= len(trees[cn2]):
                trees[cn1] = trees[cn1].union(trees[cn2])
                trees.pop(cn2)
            else:
                trees[cn2] = trees[cn2].union(trees[cn1])
                trees.pop(cn1)

    return mst, mst_edges


def find_odd_nodes(mst):
    odd_nodes = []

    for key, value in mst.items():
        if len(value) % 2 == 1:
            odd_nodes.append(key)

    return odd_nodes


def find_odd_connections(odd_nodes, points):
    odd_connections = [[0] * len(odd_nodes)] * len(odd_nodes)
    for i in range(len(odd_nodes)):
        for j in range(len(odd_nodes)):
            if i == j:
                odd_connections[i][j] = 0
            else:
                odd_connections[i][j] = get_length(points[odd_nodes[i]], points[odd_nodes[j]])

    return odd_connections


def get_length(path, points):
    return sum(get_length(points[path[i]], points[path[i + 1]]) for i in range(len(path) - 1))


def solve_tsp(points):
    # Write code here.
    mst, mst_edges = kruskal(points)
    odd_nodes = find_odd_nodes(mst)
    odd_connections = find_odd_connections(odd_nodes, points)
    min_matching = find_minimum_weight_matching(odd_connections)
    min_matches = []
    for i in min_matching:
        min_matches.append(set([odd_nodes[i[0]], odd_nodes[i[1]]]))

    mst_matches = mst.copy()
    mm_edges = mst_edges + min_matches

    for i in min_matches:
        mst_matches[tuple(i)[0]].append(tuple(i)[1])
        mst_matches[tuple(i)[1]].append(tuple(i)[0])


    start = 0
    path = [0]

    while True:
        found = False
        for i in mst_matches[start]:
            if set([start, i]) in mst_edges:
                if i != 1:
                    back_move = -2
                    path.append(i)
                    mst_edges.remove(set([start, i]))
                    mst_matches[start].remove(i)
                    mst_matches[i].remove(start)
                    start = i
                    found = True
                elif len(mst_edges) == 1 or len(mst_matches[i]) > 1:
                    back_move = -2
                    path.append(i)
                    mst_edges.remove(set([start, i]))
                    mst_matches[start].remove(i)
                    mst_matches[i].remove(start)
                    start = i
                    found = True

        if found == False:
            path.append(path[back_move])
            start = path[-1]
            back_move = back_move - 2
        if len(mst_edges) == 0 and path[0] == path[-1]:
            break


    in_path = set()
    final_path = []
    for i in range(len(path)):
        if path[i] in in_path and i != len(path) - 1:
            pass
        else:
            final_path.append(path[i])
            in_path.add(path[i])


    return final_path


# MAIN ---------------------------------------------------------

def main(input):
    output = solve_tsp(input)
    return output


def find_minimum_weight_matching(graph):
    # Graph should have an even number of vertices to have a perfect
    # matching.
    assert len(graph) % 2 == 0

    import itertools

    def score(matching):
        result = 0
        for u, v in matching:
            result += graph[u][v]
        return result

    best = None
    for permutation in itertools.permutations(range(len(graph))):
        matching = []
        for i in range(0, len(graph), 2):
            matching.append((permutation[i], permutation[i + 1]))
        if best is None or score(matching) < score(best):
            best = matching

    return best


def examples():
    # NB: There are many optimal solutions for TSP instances below, so
    # treat these asserts just as examples of a possible program behaviour.

    # We start at point 0 with coordinates (0, 0), then go to point 1
    # with coordinates (2, 2) and then return to point 0.
    assert solve_tsp([(0, 0), (2, 2)]) == [0, 1, 0]
    print('ok')
    # Here we have four points in the corners of a unit square.
    # One possible tour is (1, 0) -> (0, 0) -> (0, 1) -> (1, 1) -> (1, 0).
    assert solve_tsp([(1, 1), (0, 0), (1, 0), (0, 1)]) == [2, 1, 3, 0, 2]

    # Examples of find_minimum_weight_matching_slow (and find_minimum_weight_matching) usage.

    # Here we have a graph with two vertices and one edge. The single possible perfect matching
    # is just a (0, 1) edge of a graph.
    assert find_minimum_weight_matching_slow([[0, 1], [1, 0]]) == [(0, 1)]

    # In a graph below there are two edges with weight 1 and all the other edges have weight 2.
    # The only possible way to obtain a perfect matching of weight 2 is to select both of the edges
    # with weight 1.
    assert find_minimum_weight_matching_slow([
        [0, 2, 1, 2],
        [2, 0, 2, 1],
        [1, 2, 0, 2],
        [2, 1, 2, 1],
    ]) == [(0, 2), (1, 3)]
