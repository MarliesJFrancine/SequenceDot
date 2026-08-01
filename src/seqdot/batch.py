import typer
import itertools

from itertools import combinations
from concurrent.futures import ProcessPoolExecutor, as_completed

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

def compare_pair(
    seq1,
    seq2,
    kmer,
    strand,
    output_dir,
    point_size,
):
    """
    Compare a single pair of sequences.
    """

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

    return {
        "seq1": seq1["name"],
        "seq2": seq2["name"],
        "matches": matches
    }


def run_all_vs_all(
    sequences,
    kmer,
    strand,
    output_dir,
    point_size=1,
    include_self=False,
    silent=False,
    threads=1,
    thread_mode="auto"
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

    if not silent:

        typer.echo("SequenceDot batch comparison")
        typer.echo("-" * 50)

        typer.echo(f"Found sequences      : {len(sequences)}")
        typer.echo(f"Comparison mode      : all-vs-all")
        typer.echo(f"Include self         : {'yes' if include_self else 'no'}")
        typer.echo(f"Total comparisons    : {len(pairs)}")
        typer.echo(f"CPU threads          : {threads} ({thread_mode})")

        typer.echo("-" * 50)
        typer.echo()

    results = []

    with ProcessPoolExecutor(
        max_workers=threads
    ) as executor:
    
        future_to_pair = {}

        for seq1, seq2 in pairs:

            future = executor.submit(
                compare_pair,
                seq1,
                seq2,
                kmer,
                strand,
                output_dir,
                point_size
            )

            future_to_pair[future] = (seq1, seq2)

        if not silent:

            with tqdm(
                total=len(future_to_pair),
                desc="Comparisons",
                unit="comparison"
            ) as pbar:
                
                for future in as_completed(future_to_pair):

                    seq1, seq2 = future_to_pair[future]

                    pbar.set_postfix_str(
                        format_pair_name(seq1, seq2)
                    )

                    results.append(
                        future.result()
                    )

                    pbar.update(1)

        else:
            
            for future in as_completed(future_to_pair):

                results.append(
                    future.result()
                )
    
    if not silent:

        typer.echo()
        typer.echo("✔ Batch comparison completed")
        typer.echo(f"Number of dotplots created: {len(results)}")
        typer.echo(f"Plots written to: {output_dir}")

    return results