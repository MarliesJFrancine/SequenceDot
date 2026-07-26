from collections import defaultdict


def build_kmer_index(sequence, k):
    """
    Build an index of k-mers and their positions.

    Returns:
        dictionary:
        k-mer -> list of positions
    """

    index = defaultdict(list)

    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i+k]
        index[kmer].append(i)

    return index


def find_kmer_matches(sequence, index, k):
    """
    Find matching k-mers between a sequence and an index.

    Returns:
        list of (position_in_indexed_sequence,
                 position_in_sequence)
    """

    matches = []

    for j in range(len(sequence) - k + 1):

        kmer = sequence[j:j+k]

        if kmer in index:

            for i in index[kmer]:
                matches.append((i, j))

    return matches


