import typer

from seqdot.compare import compare_sequences
from seqdot.fasta import read_fasta, read_multi_fasta
from seqdot.batch import run_all_vs_all
from seqdot.utils import make_output_filename, check_for_gaps
from seqdot.report import write_summary
from pathlib import Path


app = typer.Typer(
    name="SeqDot",
    help="""
Create k-mer-based dotplots from unaligned sequences

Supports:
- comparison of two FASTA files
- all-vs-all comparison from a multi-sequence FASTA file
"""
)


@app.command()
def main(
    sequence1: str | None = typer.Argument(
        None,
        help="First sequence FASTA file"
    ),
    sequence2: str | None = typer.Argument(
        None,
        help="Second sequence FASTA file"
    ),
    input_file: str | None = typer.Option(
        None,
        "--file",
        help="Multiple FASTA input file for batch comparison"
    ),
    all_vs_all: bool = typer.Option(
        False,
        "--all-vs-all",
        help="Compare every sequence against every other sequence in --file, default does NOT include self (add --include-self)"
    ),
    include_self: bool = typer.Option(
        False,
        "--include-self",
        help="Include self-comparisons in all-vs-all mode"
    ),
    kmer: int = typer.Option(
        11,
        "--kmer",
        "-k",
        help="Length of k-mer used for matching"
    ),
    output: str | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file for single comparisons (.png, .pdf, .svg)"
    ),
    output_dir: str | None = typer.Option(
        None,
        "--output-dir",
        help="Directory where output files are written, specifically useful for batch mode"
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
    ),
    point_size: float = typer.Option(
        1,
        "--point-size",
        help="Size of dots in the plot"
    )
):


    """
    Generate a dotplot from two sequence files.
    """
    if all_vs_all:

        if input_file is None:
            raise typer.BadParameter(
                "--all-vs-all requires --file"
            )

        sequences = read_multi_fasta(
            input_file,
            alphabet
        )

        if output_dir is None:
            output_dir = Path("seqdot_results")

        output_dir = Path(output_dir)

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        results = run_all_vs_all(
            sequences,
            kmer,
            strand,
            output_dir,
            point_size,
            include_self
        )
        
        write_summary(
            results,
            output_dir
        )

        typer.echo(
            f"Created {len(results)} dotplots"
        )

        raise typer.Exit()

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
            "strand must be 'forward' or 'reverse', or 'both'"
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
