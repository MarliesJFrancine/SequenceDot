import typer

from seqdot.compare import compare_sequences
from seqdot.fasta import read_fasta
from seqdot.utils import make_output_filename, check_for_gaps
from pathlib import Path


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
    output: str | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Output image file (.png, .pdf, .svg)"
    ),
    output_dir: str | None = typer.Option(
        None,
        "--output-dir",
        help="Directory where output files are saved"
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
    
    for seq in [seq1, seq2]:

        if check_for_gaps(seq["sequence"]):
            typer.echo(
                f"Warning: {seq['name']} contains gap characters (-). "
                "SeqDot is designed for unaligned sequences."
            )
    
    if output is None:
        output = make_output_filename(
            seq1["name"],
            seq2["name"]
        )
    
    if output_dir is not None:
        output_dir = Path(output_dir)

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        output = str(output_dir / output)
    
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

    matches = compare_sequences(
        seq1,
        seq2,
        kmer,
        strand,
        output,
        point_size
    )

    typer.echo(
        f"Found {matches} matching k-mers"
    )

    typer.echo("Dotplot saved")
    

if __name__ == "__main__":
    app()
