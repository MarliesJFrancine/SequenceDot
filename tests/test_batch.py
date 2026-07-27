from seqdot.batch import generate_pairs


def test_generate_pairs_without_self():

    sequences = [
        {"name": "A"},
        {"name": "B"},
        {"name": "C"}
    ]

    pairs = generate_pairs(
        sequences
    )

    assert len(pairs) == 3


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