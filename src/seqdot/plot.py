import matplotlib.pyplot as plt


def create_dotplot(
    matches,
    length1,
    length2,
    name1="Sequence 1",
    name2="Sequence 2",
    output_file="dotplot.png"
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

    x = [match[0] for match in matches]
    y = [match[1] for match in matches]

    fig, ax = plt.subplots(
        figsize=(8, 8),
        dpi=300
    )

    ax.scatter(
        x,
        y,
        s=0.5,
        marker="."
    )
    
    ax.ticklabel_format(
        style="plain"
    )

    ax.set_xlim(0, length1)
    ax.set_ylim(0, length2)

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
