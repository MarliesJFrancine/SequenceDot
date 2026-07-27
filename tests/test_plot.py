from seqdot.plot import separate_strands


def test_reverse_coordinates():

    matches = [
        (1, 0, "reverse"),
        (2, 2, "reverse"),
        (4, 3, "reverse")
    ]

    forward_x, forward_y, reverse_x, reverse_y = separate_strands(
        matches,
        length2=6,
        kmer=2
    )

    assert forward_x == []
    assert forward_y == []

    assert reverse_x == [1, 2, 4]
    assert reverse_y == [4, 2, 1]


def test_both_strands_are_separated():

    matches = [
        (1, 1, "forward"),
        (3, 0, "reverse")
    ]

    forward_x, forward_y, reverse_x, reverse_y = separate_strands(
        matches,
        length2=6,
        kmer=2
    )

    assert forward_x == [1]
    assert forward_y == [1]

    assert reverse_x == [3]
    assert reverse_y == [4]
