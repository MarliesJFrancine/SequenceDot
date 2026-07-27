import pytest
from seqdot.utils import clean_sequence, make_output_filename


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


def test_make_output_filename():

    filename = make_output_filename(
        "seq1",
        "seq2"
    )

    assert filename == "seq1_vs_seq2.png"
        

def test_make_output_filename_sanitizes_names():

    filename = make_output_filename(
        "sample/one",
        "sample two"
    )

    assert filename == "sample_one_vs_sample_two.png"