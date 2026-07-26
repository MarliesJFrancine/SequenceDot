import typer

from seqdot.fasta import read_fasta
from seqdot.kmer import build_kmer_index, find_kmer_matches
from seqdot.utils import reverse_complement
from seqdot.plot import create_dotplot


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
    ),
    output: str = typer.Option(
        "dotplot.png",
        "--output",
        "-o",
        help="Output image file (.png, .pdf, .svg)"
    ),
    alphabet: str = typer.Option(
        "DNA",
        "--alphabet",
        "-a",
        help="Sequence alphabet: DNA, RNA, or AA"
    ),
    strand: str = typer.Option(
        "forward",
        "--strand",
        "-s",
        help="Compare forward strand, reverse complement, or both"
    )
):


    """
    Generate a dotplot from two sequence files.
    """

    seq1 = read_fasta(sequence1, alphabet)
    seq2 = read_fasta(sequence2, alphabet)
    
    if strand == "reverse":

        seq2["sequence"] = reverse_complement(
            seq2["sequence"]
        )
    
    if strand not in [
        "forward",
        "reverse"
    ]:
        raise typer.BadParameter(
            "strand must be 'forward' or 'reverse'"
        )

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

    create_dotplot(
        matches,
        seq1["length"],
        seq2["length"],
        seq1["name"],
        seq2["name"],
        output
    )

    typer.echo(
        "Dotplot saved"
    )

if __name__ == "__main__":
    app()
