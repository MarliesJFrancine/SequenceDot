import typer

from itertools import combinations

from tqdm import tqdm

from seqdot.compare import compare_sequences, ensure_index
from seqdot.utils import make_output_filename


def generate_pairs(sequences, include_self=False):
    """
    Generate sequence comparison pairs.

    Parameters
    ----------
    sequences : list
        List of sequence dictionaries.

    include_self : bool
        Include comparisons of sequences against themselves.

    Returns
    -------
    list
        List of sequence pairs.
    """

    if include_self:

        pairs = []

        for i, seq1 in enumerate(sequences):
            for seq2 in sequences[i:]:
                pairs.append((seq1, seq2))

        return pairs

    else:

        return list(
            combinations(sequences, 2)
        )


def format_pair_name(seq1, seq2, max_length=20):
    """
    Format sequence names for the progress bar.
    """

    def shorten(name):
        if len(name) <= max_length:
            return name

        return name[: max_length - 3] + "..."

    return (
        f"{shorten(seq1['name'])} vs "
        f"{shorten(seq2['name'])}"
    )


def run_all_vs_all(
    sequences,
    kmer,
    strand,
    output_dir,
    point_size=1,
    include_self=False,
    silent=False
):
    """
    Run all-vs-all sequence comparisons.
    """

    pairs = generate_pairs(
        sequences,
        include_self
    )
    
    for seq in sequences:

        ensure_index(
            seq,
            kmer
        )
    
    results = []

    if not silent:

        typer.echo(f"Found {len(sequences)} sequences")
        typer.echo()

        typer.echo("Mode: all-vs-all")
        typer.echo("Include self-comparisons: " + ("yes" if include_self else "no"))
        typer.echo()

        typer.echo(f"Total comparisons: {len(pairs)}")
        typer.echo()

        iterator = tqdm(
            pairs,
            total=len(pairs),
            desc="Comparisons",
            unit="comparison"
        )

    else:

        iterator = pairs


    for seq1, seq2 in iterator:
        
        if not silent:

            iterator.set_postfix_str(
                "Current: "
                + format_pair_name(seq1, seq2)
            )

        output_file = make_output_filename(
            seq1["name"],
            seq2["name"]
        )

        output_file = output_dir / output_file

        matches = compare_sequences(
            seq1,
            seq2,
            kmer,
            strand,
            str(output_file),
            point_size
        )

        results.append(
            {
                "seq1": seq1["name"],
                "seq2": seq2["name"],
                "matches": matches
            }
        )
    
    if not silent:

        typer.echo()
        typer.echo("✔ Batch comparison completed")
        typer.echo(f"Number of dotplots created: {len(pairs)}")
        typer.echo(f"Plots written to: {output_dir}")
        typer.eche(f"Summary written to {summary_file}")

    return results