import typer

from seqdot.fasta import read_fasta
from seqdot.kmer import build_kmer_index, find_kmer_matches


app = typer.Typer(
    name="SeqDot",
    help="Create dotplots from sequence files."
)


@app.command()
def main(
    sequence1: str,
    sequence2: str,
    kmer: int = typer.Option(
        11,
        "--kmer",
        "-k",
        help="Length of k-mer used for matching"
    )
):
    """
    Generate a dotplot from two sequence files.
    """

    seq1 = read_fasta(sequence1)
    seq2 = read_fasta(sequence2)

    typer.echo(
        f"Building k-mer index (k={kmer})..."
    )

    index = build_kmer_index(
        seq1["sequence"],
        kmer
    )

    typer.echo(
        "Searching for matches..."
    )

    matches = find_kmer_matches(
        seq2["sequence"],
        index,
        kmer
    )

    typer.echo(
        f"Found {len(matches)} matching k-mers"
    )


if __name__ == "__main__":
    app()