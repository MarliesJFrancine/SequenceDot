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
        help="Length of k-mer used for matching, default: 11"
    ),
    output: str = typer.Option(
        "dotplot.png",
        "--output",
        "-o",
        help="Output image file (.png, .pdf, .svg), default: dotplot.png"
    ),
    alphabet: str = typer.Option(
        "DNA",
        "--alphabet",
        "-a",
        help="Sequence alphabet: DNA, RNA, or AA, default: DNA"
    ),
    strand: str = typer.Option(
        "forward",
        "--strand",
        "-s",
        help="Compare forward strand, reverse complement, or both, default: forward"
    ),
    point_size: float = typer.Option(
        1,
        "--point-size",
        help="Size of dots in the plot, default: 1"
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
        "reverse",
        "both"
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

    # Add strand information to forward matches
    matches = [
        (x, y, "forward")
        for x, y in matches
    ]


    if strand in ["reverse", "both"]:

        reverse_seq2 = reverse_complement(
            seq2["sequence"]
        )

        reverse_matches = find_kmer_matches(
            reverse_seq2,
            index,
            kmer
        )

        reverse_matches = [
            (x, y, "reverse")
            for x, y in reverse_matches
        ]

        if strand == "reverse":
            matches = reverse_matches

        elif strand == "both":
            matches.extend(reverse_matches)

    typer.echo(
        f"Found {len(matches)} matching k-mers"
    )

    create_dotplot(
        matches,
        seq1["length"],
        seq2["length"],
        kmer,
        point_size,
        seq1["name"],
        seq2["name"],
        output
    )

    typer.echo(
        "Dotplot saved"
    )

if __name__ == "__main__":
    app()
