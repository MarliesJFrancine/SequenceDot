import pytest
from seqdot.utils import clean_sequence


def test_clean_dna_sequence():
    sequence = "acg t\n"

    cleaned = clean_sequence(
        sequence,
        "DNA"
    )

    assert cleaned == "ACGT"


def test_invalid_dna_character():

    with pytest.raises(ValueError):

        clean_sequence(
            "ACGU",
            "DNA"
        )
        
