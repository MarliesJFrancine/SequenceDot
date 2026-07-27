import matplotlib.pyplot as plt


def separate_strands(matches, length2, kmer):
    """
    Separate forward and reverse matches and transform reverse coordinates.
    """

    forward_x = []
    forward_y = []

    reverse_x = []
    reverse_y = []

    for x, y, strand in matches:

        if strand == "forward":
            forward_x.append(x)
            forward_y.append(y)

        elif strand == "reverse":
            reverse_x.append(x)
            reverse_y.append(length2 - y - kmer)

    return (
        forward_x,
        forward_y,
        reverse_x,
        reverse_y
    )


def create_dotplot(
    matches,
    length1,
    length2,
    kmer,
    name1="Sequence 1",
    name2="Sequence 2",
    output_file="dotplot.png",
    point_size=1
):
    """
    Create a dotplot from matching positions.

    Parameters
    ----------
    matches : list
        List of (x, y) matching coordinates.

    length1 : int
        Length of first sequence.

    length2 : int
        Length of second sequence.

    name1 : str
        Name of first sequence.

    name2 : str
        Name of second sequence.

    output_file : str
        Output image filename.
    """

    
    forward_x, forward_y, reverse_x, reverse_y = separate_strands(
        matches,
        length2,
        kmer
    )

    fig, ax = plt.subplots(
        figsize=(8, 8),
        dpi=300
    )
    
    ax.scatter(
        forward_x,
        forward_y,
        s=point_size,
        marker=".",
        color="steelblue",
        label="Forward"
    )

    ax.scatter(
        reverse_x,
        reverse_y,
        s=point_size,
        marker=".",
        color="darkorange",
        label="Reverse complement"
    )

    ax.legend()
    
    ax.ticklabel_format(
        style="plain"
    )

    ax.set_xlim(0, length1)
    ax.set_ylim(length2, 0)

    ax.set_xlabel(name1)
    ax.set_ylabel(name2)

    ax.set_title(
        f"SeqDot: {name1} vs {name2}"
    )

    ax.set_aspect("equal")

    plt.tight_layout()

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)
