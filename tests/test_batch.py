from seqdot.batch import generate_pairs, format_pair_name


def test_generate_pairs_without_self():

    sequences = [
        {"name": "A"},
        {"name": "B"},
        {"name": "C"}
    ]

    pairs = generate_pairs(
        sequences,
        include_self=False
    )

    assert len(pairs) == 3

    assert pairs == [
        (sequences[0], sequences[1]),
        (sequences[0], sequences[2]),
        (sequences[1], sequences[2])
    ]


def test_generate_pairs_with_self():

    sequences = [
        {"name": "A"},
        {"name": "B"},
        {"name": "C"}
    ]

    pairs = generate_pairs(
        sequences,
        include_self=True
    )

    assert len(pairs) == 6

    assert pairs == [
        (sequences[0], sequences[0]),
        (sequences[0], sequences[1]),
        (sequences[0], sequences[2]),
        (sequences[1], sequences[1]),
        (sequences[1], sequences[2]),
        (sequences[2], sequences[2]),
    ]


def test_format_pair_name_short():

    seq1 = {"name": "A"}
    seq2 = {"name": "B"}

    assert format_pair_name(seq1, seq2) == "A vs B"


def test_format_pair_name_long():

    seq1 = {
        "name": "VeryLongSequenceNameOne"
    }

    seq2 = {
        "name": "VeryLongSequenceNameTwo"
    }

    result = format_pair_name(seq1, seq2)

    assert "..." in result