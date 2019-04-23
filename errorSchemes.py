def normalize_scheme(sch):
    s = sum(sch.values())
    for key in sch.keys():
        sch[key] /= s
    return sch

def fade_between_schemes(sch1, sch2, pos):
    sch1 = normalize_scheme(sch1)
    sch2 = normalize_scheme(sch2)

    new_scheme = {}
    new_keys = list(sch1.keys()) + list(sch2.keys())

    for nk in new_keys:
        val1 = sch1[nk] if nk in sch1.keys() else 0
        val2 = sch2[nk] if nk in sch2.keys() else 0

        new_scheme[nk] = (val1 * pos) + (val2 * (1 - pos))

    return new_scheme

scheme_diag = {
    (1, 1): 2.0,
    (-1, 1): 2.0,
    (-1, 2): 1.0,
    (2, 1): 1.0,
}

scheme_diag_large = {
    (1, 1): 3.0,
    (-1, 1): 3.0,
    (-1, 2): 2.0,
    (2, 1): 2.0,
    (2, 2): 1.0,
    (-2, 2): 1.0,
    (-2, 1): 1.0,
    (3, 2): 1.0,
}

scheme_rect = {
    (1, 0): 2.0,
    (0, 1): 2.0,
    (0, 2): 1.0,
    (2, 0): 1.0
}

scheme_uniform_small = {
    (1, 0): 1.0,
    (1, 1): 1.0,
    (0, 1): 1.0,
    (-1, 1): 1.0
}

scheme_floyd_steinberg = {
    (1, 0): 7.0,
    (1, 1): 1.0,
    (0, 1): 3.0,
    (-1, 1): 5.0
}
