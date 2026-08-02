import pytest

from seqdot.fasta import read_fasta, read_multi_fasta


def test_read_multi_fasta(tmp_path):

    fasta = tmp_path / "test.fasta"

    fasta.write_text(
        ">seq1\n"
        "ATGC\n"
        ">seq2\n"
        "GGTT\n"
    )

    sequences = read_multi_fasta(fasta)

    assert len(sequences) == 2

    assert sequences[0]["name"] == "seq1"
    assert sequences[0]["sequence"] == "ATGC"
    assert sequences[0]["length"] == 4
    assert sequences[0]["index"] is None

    assert sequences[1]["name"] == "seq2"
    assert sequences[1]["sequence"] == "GGTT"
    assert sequences[1]["length"] == 4


def test_read_multi_fasta_empty(tmp_path):

    fasta = tmp_path / "empty.fasta"

    fasta.write_text("")

    with pytest.raises(ValueError, match="empty"):

        read_multi_fasta(fasta)


def test_read_multi_fasta_not_fasta(tmp_path):

    fasta = tmp_path / "bad.txt"

    fasta.write_text(
        "ATGC\n"
        "ATGC\n"
    )

    with pytest.raises(ValueError, match="fasta"):

        read_multi_fasta(fasta)


def test_read_multi_fasta_duplicate_headers(tmp_path):

    fasta = tmp_path / "duplicate.fasta"

    fasta.write_text(
        ">seq1\n"
        "ATGC\n"
        ">seq1\n"
        "GGTT\n"
    )

    with pytest.raises(ValueError, match="Duplicate"):

        read_multi_fasta(fasta)


def test_read_multi_fasta_invalid_dna(tmp_path):

    fasta = tmp_path / "invalid.fasta"

    fasta.write_text(
        ">seq1\n"
        "ATGCM\n"
    )

    with pytest.raises(ValueError, match="seq1"):

        read_multi_fasta(
            fasta,
            alphabet="DNA"
        )


def test_read_fasta_multiple_sequences(tmp_path):

    fasta = tmp_path / "multi.fasta"

    fasta.write_text(
        ">seq1\n"
        "AAAA\n"
        ">seq2\n"
        "TTTT\n"
    )

    with pytest.raises(ValueError, match="Multiple sequences"):

        read_fasta(fasta)


def test_read_fasta(tmp_path):

    fasta = tmp_path / "single.fasta"

    fasta.write_text(
        ">seq1\n"
        "ATGC\n"
    )

    sequence = read_fasta(fasta)

    assert sequence["name"] == "seq1"
    assert sequence["sequence"] == "ATGC"
    assert sequence["length"] == 4
    assert sequence["index"] is None