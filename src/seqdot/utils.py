from seqdot.alphabet import DNA, RNA, AA
import re


def sanitize_filename(name):
    """
    Convert sequence names into safe filenames.
    """

    name = re.sub(r"[^\w\-\.]", "_", name)

    return name


def make_output_filename(name1, name2, extension="png"):
    """
    Create default output filename from two sequence names.
    """

    name1 = sanitize_filename(name1)
    name2 = sanitize_filename(name2)

    return f"{name1}_{name2}.{extension}"


ALPHABETS = {
    "DNA": DNA,
    "RNA": RNA,
    "AA": AA
}


def clean_sequence(sequence, alphabet="DNA"):
    """
    Clean and validate sequence characters.
    """

    alphabet = alphabet.upper()

    if alphabet not in ALPHABETS:
        raise ValueError(
            f"Unknown alphabet '{alphabet}'. "
            f"Choose DNA, RNA, or AA."
        )

    sequence = (
        sequence
        .replace(" ", "")
        .replace("\n", "")
        .upper()
    )

    allowed = ALPHABETS[alphabet]

    invalid = set(sequence) - allowed

    if invalid:
        raise ValueError(
            f"Invalid characters for {alphabet}: {invalid}"
        )

    return sequence


def reverse_complement(sequence):
    """
    Return the reverse complement of a DNA sequence.
    """

    complement = {
        "A": "T",
        "T": "A",
        "C": "G",
        "G": "C",
        "N": "N"
    }

    try:
        return "".join(
            complement[base]
            for base in reversed(sequence)
        )

    except KeyError as e:
        raise ValueError(
            f"Invalid DNA character: {e.args[0]}"
        )