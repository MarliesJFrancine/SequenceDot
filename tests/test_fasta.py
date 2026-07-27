from seqdot.fasta import read_multi_fasta


def test_read_multi_fasta(tmp_path):

    fasta = tmp_path / "test.fasta"

    fasta.write_text(
        ">seq1\nATGC\n>seq2\nGGTT\n"
    )

    sequences = read_multi_fasta(
        fasta
    )

    assert len(sequences) == 2

    assert sequences[0]["name"] == "seq1"
    assert sequences[0]["length"] == 4

    assert sequences[1]["name"] == "seq2"
