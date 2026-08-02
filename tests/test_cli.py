from typer.testing import CliRunner

from seqdot.cli import app
from seqdot import __version__

runner = CliRunner()


def test_cli_import():

    assert app is not None


def test_help():

    result = runner.invoke(
        app,
        ["--help"]
    )

    assert result.exit_code == 0
    assert "SequenceDot" in result.stdout
    assert "--kmer" in result.stdout
    assert "--strand" in result.stdout


def test_version():

    result = runner.invoke(
        app,
        ["--version"]
    )

    assert result.exit_code == 0
    assert result.stdout.strip() == f"SequenceDot {__version__}"


def test_version_short():

    result = runner.invoke(
        app,
        ["-v"]
    )

    assert result.exit_code == 0
    assert result.stdout.strip() == f"SequenceDot {__version__}"


def test_invalid_strand():

    result = runner.invoke(
        app,
        [
            "seq1.fasta",
            "seq2.fasta",
            "--strand",
            "banana"
        ]
    )

    assert result.exit_code != 0


def test_missing_input_files():

    result = runner.invoke(
        app,
        [
            "does_not_exist.fasta",
            "also_missing.fasta"
        ]
    )

    assert result.exit_code != 0


def test_kmer_too_large(tmp_path):

    seq1 = tmp_path / "seq1.fasta"
    seq2 = tmp_path / "seq2.fasta"

    seq1.write_text(">seq1\nATGC\n")
    seq2.write_text(">seq2\nATGC\n")

    result = runner.invoke(
        app,
        [
            str(seq1),
            str(seq2),
            "--kmer",
            "10",
        ],
    )

    # assert result.exit_code != 0
    #assert "shortest sequence" in result.stdout

    assert result.exit_code != 0


def test_kmer_zero(tmp_path):

    seq1 = tmp_path / "seq1.fasta"
    seq2 = tmp_path / "seq2.fasta"

    seq1.write_text(">seq1\nATGC\n")
    seq2.write_text(">seq2\nATGC\n")

    result = runner.invoke(
        app,
        [
            str(seq1),
            str(seq2),
            "--kmer",
            "0",
        ],
    )

    assert result.exit_code != 0


def test_kmer_negative(tmp_path):

    seq1 = tmp_path / "seq1.fasta"
    seq2 = tmp_path / "seq2.fasta"

    seq1.write_text(">seq1\nATGC\n")
    seq2.write_text(">seq2\nATGC\n")

    result = runner.invoke(
        app,
        [
            str(seq1),
            str(seq2),
            "--kmer",
            "-4",
        ],
    )

    assert result.exit_code != 0


def test_kmer_above_maximum(tmp_path):

    seq1 = tmp_path / "seq1.fasta"
    seq2 = tmp_path / "seq2.fasta"

    seq1.write_text(">seq1\nATGCATGCATGC\n")
    seq2.write_text(">seq2\nATGCATGCATGC\n")

    result = runner.invoke(
        app,
        [
            str(seq1),
            str(seq2),
            "--kmer",
            "101",
        ],
    )

    assert result.exit_code != 0