import numpy as np
from sklearn.neighbors import NearestNeighbors

# X is the target, Y is the source
def min_diff_pair_mapping(X, Y, normalize=True, finish_early_factor=0.03, max_iter=500, min_change=2):
    n = len(X)
    X = np.array(X)
    Y = np.array(Y)
    i = 0
    amt_left = [len(X)]
    finish_early = int(finish_early_factor * n)

    if X.shape[1:] != Y.shape[1:]:
        raise ValueError(f'X and Y must contain elements of the same dimensionality: {X[0].shape} vs {Y[0].shape}')
    if X.shape[0] > Y.shape[0]:
        raise ValueError('X must have fewer data points than Y')

    if normalize:
        X_avg = np.mean(X, 0)
        Y_avg = np.mean(Y, 0)
        X_std = np.std(X, 0)
        Y_std = np.std(X, 0)

        X = (X - X_avg) / X_std
        Y = (Y - Y_avg) / Y_std

    ind_map = np.repeat(-1, n)
    for i in range(max_iter):

        x_active = [x for x in range(n) if ind_map[x] == -1]
        y_active = np.setdiff1d(range(len(Y)), ind_map)

        neigh = NearestNeighbors(1)
        neigh.fit(Y[y_active])
        best_dists, best_inds = neigh.kneighbors(X[x_active], 1, return_distance=True)

        for yind in range(len(y_active)):
            candidates = [x for x in range(len(best_inds)) if best_inds[x][0] == yind]
            if len(candidates) == 0:
                continue
            elif len(candidates) == 1:
                ind_map[x_active[candidates[0]]] = y_active[yind]
            else:
                chosen_ind = min(candidates, key=lambda x: best_dists[x])
                ind_map[x_active[chosen_ind]] = y_active[yind]

        print('iteration {}, active pts {}'.format(i, sum(ind_map == -1)))
        amt_left.append(sum(ind_map == -1))

        if sum(ind_map == -1) == 0:
            print('finished.')
            break

        change_stop = (np.diff(amt_left)[-1] * -1) < min_change
        if change_stop or sum(ind_map == -1) < finish_early:
            print('finishing early.')
            for indx, indy in enumerate(best_inds):
                indy = indy[0]
                ind_map[x_active[indx]] = y_active[indy]
            break

    return ind_map

if __name__ == '__main__':

    n = 1000
    m = 5
    X = np.random.randint(0, 255, (n, m))
    Y = np.random.randint(0, 255, (n * 2, m))
    mapping = min_diff_pair_mapping(X,Y)

    score = np.average(np.sum((X - Y[mapping]) ** 2, 1))
    print(score)
