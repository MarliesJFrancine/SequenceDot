from itertools import combinations

from seqdot.compare import compare_sequences
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


def run_all_vs_all(
    sequences,
    kmer,
    strand,
    output_dir,
    point_size=1,
    include_self=False
):
    """
    Run all-vs-all sequence comparisons.
    """

    pairs = generate_pairs(
        sequences,
        include_self
    )

    results = []

    for seq1, seq2 in pairs:

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

    return results