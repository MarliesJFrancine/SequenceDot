from seqdot.compare import compare_sequences


def test_forward_comparison(tmp_path):

    seq1 = {
        "name": "seq1",
        "sequence": "ATGCGT",
        "length": 6
    }

    seq2 = {
        "name": "seq2",
        "sequence": "ATGCGT",
        "length": 6
    }

    output = tmp_path / "test.png"

    matches = compare_sequences(
        seq1,
        seq2,
        kmer=3,
        strand="forward",
        output_file=str(output)
    )

    assert matches > 0
    assert output.exists()


def test_reverse_comparison(tmp_path):

    seq1 = {
        "name": "seq1",
        "sequence": "ATGC",
        "length": 4
    }

    seq2 = {
        "name": "seq2",
        "sequence": "GCAT",
        "length": 4
    }

    output = tmp_path / "reverse.png"

    matches = compare_sequences(
        seq1,
        seq2,
        kmer=2,
        strand="reverse",
        output_file=str(output)
    )

    assert matches > 0
    assert output.exists()
