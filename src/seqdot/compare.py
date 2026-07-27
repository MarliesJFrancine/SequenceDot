from seqdot.kmer import build_kmer_index, find_kmer_matches
from seqdot.plot import create_dotplot
from seqdot.utils import reverse_complement


def add_strand(matches, strand):
    """
    Add strand information to matching coordinates.

    Converts:
        [(x, y), (x, y)]

    into:
        [(x, y, strand), (x, y, strand)]
    """

    return [
        (x, y, strand)
        for x, y in matches
    ]


def compare_sequences(
    seq1,
    seq2,
    kmer,
    strand,
    output_file,
    point_size=1,
):
    """
    Compare two sequences and create a dotplot.

    Parameters
    ----------
    seq1 : dict
        First sequence dictionary.

    seq2 : dict
        Second sequence dictionary.

    kmer : int
        K-mer size.

    strand : str
        "forward", "reverse", or "both".

    output_file : str
        Output filename.

    point_size : float
        Size of dots in plot.

    Returns
    -------
    int
        Number of matching k-mers.
    """

    matches = []

    # Forward comparison
    if strand in ["forward", "both"]:

        index = build_kmer_index(
            seq1["sequence"],
            kmer
        )

        forward_matches = find_kmer_matches(
            seq2["sequence"],
            index,
            kmer
        )

        matches.extend(
            add_strand(
                forward_matches,
                "forward"
            )
        )


    # Reverse-complement comparison
    if strand in ["reverse", "both"]:

        reverse_seq2 = reverse_complement(
            seq2["sequence"]
        )

        index = build_kmer_index(
            seq1["sequence"],
            kmer
        )

        reverse_matches = find_kmer_matches(
            reverse_seq2,
            index,
            kmer
        )

        matches.extend(
            add_strand(
                reverse_matches,
                "reverse"
            )
        )
    
    create_dotplot(
        matches,
        seq1["length"],
        seq2["length"],
        kmer,
        name1=seq1["name"],
        name2=seq2["name"],
        output_file=output_file,
        point_size=point_size
    )


    return len(matches)