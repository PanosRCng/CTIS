import time

import jellyfish
from abydos import distance





def sort_distance(scores):
    return sorted(scores.items(), key=lambda x: x[1])



def sort_similarity(scores):
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def __needleman_wunsch(text, texts):

    scores = {}

    cmp = distance.NeedlemanWunsch()

    start_time = time.time()

    for index, t in enumerate(texts):
        scores[index] = cmp.sim(text, t)

    return time.time() - start_time


def __minkowski(text, texts):

    scores = {}

    cmp = distance.Minkowski()

    start_time = time.time()

    for index, t in enumerate(texts):
        scores[index] = cmp.dist_abs(text, t)

    return scores, (time.time() - start_time)


EXCEPTIONS = [
    'minkowski',
    'needleman_wunsch'
]


METRICS = {
    'levenshtein': {
        'metric_function': jellyfish.levenshtein_distance,
        'sort_function': sort_distance
    },
    'damerau_levenshtein': {
        'metric_function': jellyfish.damerau_levenshtein_distance,
        'sort_function': sort_distance
    },
    'jaro': {
        'metric_function': jellyfish.jaro_similarity,
        'sort_function': sort_similarity
    },
    'jaro_winkler': {
        'metric_function': jellyfish.jaro_winkler_similarity,
        'sort_function': sort_similarity
    },
    'hamming': {
        'metric_function': jellyfish.hamming_distance,
        'sort_function': sort_distance
    },
    'minkowski': {
        'metric_function': __minkowski,
        'sort_function': sort_distance
    },


    # too slow
    #
    #'needleman_wunsch': {
    #    'metric_function': __needleman_wunsch,
    #    'sort_function': sort_similarity
    #}
}



def similarity(text, texts, metric):

    if metric in EXCEPTIONS:

        scores, time_passed = METRICS[metric]['metric_function'](text, texts)

        return METRICS[metric]['sort_function'](scores)[0][0], time_passed

    scores = {}

    start_time = time.time()

    for t in texts:
        scores[t] = METRICS[metric]['metric_function'](text, t)

    return METRICS[metric]['sort_function'](scores)[0][0], (time.time() - start_time)








