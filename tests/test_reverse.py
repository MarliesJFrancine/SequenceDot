from seqdot.utils import reverse_complement


def test_reverse_complement():

    sequence = "ACGT"

    assert reverse_complement(sequence) == "ACGT"


def test_reverse_complement_non_palindrome():

    sequence = "AAGC"

    assert reverse_complement(sequence) == "GCTT"
