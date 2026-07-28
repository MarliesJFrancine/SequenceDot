from pathlib import Path

from seqdot.report import write_summary


def test_write_summary(tmp_path):

    results = [
        {
            "seq1": "A",
            "seq2": "B",
            "matches": 12
        },
        {
            "seq1": "A",
            "seq2": "C",
            "matches": 8
        }
    ]

    write_summary(
        results,
        tmp_path
    )

    summary = tmp_path / "comparisons.tsv"

    assert summary.exists()

    text = summary.read_text()

    assert "sequence1" in text
    assert "A\tB\t12" in text
    assert "A\tC\t8" in text