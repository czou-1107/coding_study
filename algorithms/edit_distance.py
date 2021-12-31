"""
Collection of edit distance implementations

Edit distances are defined via a set of allowed operations (e.g. delete, insert, substitute)
and an associated cost

Not all are proper metrics (recall they must satisfy the following properties:
    1. d(s1, s2) = 0  <==>  s1 = s2 (strings can be self-transformed using exactly 0 ops)
    2. d(s1, s2) >= 0 (all ops have positive cost)
    3. d(s1, s2) = d(s2, s1) (all ops have an inverse of equal cost)
    4. d(s1, s3) >= d(s1, s2) + d(s2, s3) (triangle inequality)
)
However, all do satisfy the property that common prefixes have no effect on distance:
    - Let a = uv, b = uw. Then d(a, b) = d(v, w)
"""


def hamming(s1: str, s2: str) -> int:
    """ Edit distance considering *only* substitutions at unit cost

    This obviously requires that both strings be same length """
    assert len(s1) == len(s2)
    distance = 0
    for c1, c2 in zip(s1, s2):
        if c1 != c2:
            distance += 1
    return distance


def levenshtein_naive(s1: str, s2: str) -> int:
    """ Naive recursive implementation, following definition of Levenshtein distance

    Levenshtein allows insert, delete, substitute all at unit cost

    It is incredibly inefficient because distances between the same substrings
    are recomputed many times. In particular, it has exponential time complexity
    """
    # If one string is empty, need to insert everything
    if s1 == '':
        return len(s2)
    if s2 == '':
        return len(s1)
    # If first characters match, then we can ignore them in calculation
    if s1[0] == s2[0]:
        return levenshtein_naive(s1[1:], s2[1:])
    # Else edit distance is at least one
    return 1 + min(levenshtein_naive(s1[1:], s2),
                   levenshtein_naive(s1, s2[1:]),
                   levenshtein_naive(s1[1:], s2[1:]))


def levenshtein_wagner_fischer(s1: str, s2: str) -> int:
    """ Dynamic programming approach

    Observation: if we create matrix holding edit distances between all prefixes
    of the 1st and 2nd string, this matrix can be flood-filled, and the bottom-right
    entry is the edit distance between the full strings. The invariant here is that
    the prefix s1[:i] can be transformed to s2[:j] using D[i, j] operations

    Uses numpy to store matrix. It has O(|s1||s2|) complexity """
    import numpy as np

    m, n = len(s1), len(s2)

    # Note: distance matrix is 0-indexed while strings are 1-indexed within matrix
    distances = np.zeros((m + 1, n + 1), dtype=np.int8)
    # prefixes can be transformed into empty string by dropping all characters
    distances[:, 0] = np.arange(m + 1)
    distances[0, :] = np.arange(n + 1)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            sub_cost = s1[i-1] != s2[j-1]  # Make sure indices are consistent!
            distances[i, j] = min(distances[i-1, j] + 1,  # deletion
                                  distances[i, j-1] + 1,  # insertion
                                  distances[i-1, j-1] + sub_cost)  # substitution
            # # A more verbose, but potentially clearer implementation is as follows:
            # if s1[i-1] == s2[j-1]:  # No *incremental* edits need to be made
            #     distances[i, j] = distances[i-1, j-1]
            # else:  # Can be transformed in one of three ways
            #     distances[i, j] = min(
            #         distances[i-1, j] + 1,  # s1[:i-1] -> s2[:j] and INSERT s[i]
            #         distances[i, j-1] + 1,  # DELETE s2[j] and s1[:i] -> s2[:j-1]
            #         distances[i-1, j-1] + 1,  # s1[:i-1] -> s2[:j-1] and SUB s1[i] -> s2[j]
            #     )
    return distances[-1, -1]


def jaro_winkler(s1: str, s2: str) -> int:
    """ Allow only transposition """
    pass


def damerau_levenshtein(s1: str, s2: str) -> int:
    """ Allow insert, delete, substitute, transposition """
    pass
