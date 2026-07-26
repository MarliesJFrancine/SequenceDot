from seqdot.kmer import build_kmer_index
from seqdot.kmer import find_kmer_matches


def test_kmer_index():

    sequence = "ACGTACGT"

    index = build_kmer_index(
        sequence,
        4
    )

    assert index["ACGT"] == [0,4]
    

def test_kmer_matching():

    index = {
        "ACGT": [0]
    }

    matches = find_kmer_matches(
        "ACGT",
        index,
        4
    )

    assert matches == [(0,0)]