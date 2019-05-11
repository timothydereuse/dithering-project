import numpy as np
from sklearn.neighbors import NearestNeighbors

def min_diff_pair_mapping(X, Y):
    n = len(X)
    X = np.array(X)
    Y = np.array(Y)
    i = 0

    if X.shape[1:] != Y.shape[1:]:
        raise ValueError('X and Y must have the same dimensionality')
    if X.shape[0] > Y.shape[0]:
        raise ValueError('X must have more data points than Y')

    ind_map = np.repeat(-1, n)
    while any(ind_map == -1):

        x_active = [x for x in range(n) if ind_map[x] == -1]
        y_active = np.setdiff1d(range(n), ind_map)

        neigh = NearestNeighbors(1)
        neigh.fit(X[x_active])
        best_dists, best_inds = neigh.kneighbors(Y[y_active], 1, return_distance=True)
        for xind in range(len(X)):
            candidates = [x for x in range(len(best_inds)) if best_inds[x][0] == xind]
            if len(candidates) == 0:
                continue
            elif len(candidates) == 1:
                ind_map[x_active[xind]] = y_active[candidates[0]]
            else:
                chosen_ind = min(candidates, key=lambda x: best_dists[x])
                ind_map[x_active[xind]] = y_active[chosen_ind]

        i += 1
        print('iteration {}, active pts {}'.format(i, sum(ind_map == -1)))
    return ind_map

if __name__ == '__main__':

    n = 100
    m = 5
    X = np.random.randint(0, 255, (n, m))
    Y = np.random.randint(0, 255, (n * 2, m))
    mapping = min_diff_pair_mapping(X,Y)

    score = np.average(np.sum((X - Y[mapping]) ** 2, 1))
    print(score)
