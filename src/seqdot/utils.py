from seqdot.alphabet import DNA, RNA, AA

import re
import os


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

    return f"{name1}_vs_{name2}.{extension}"


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


def check_for_gaps(sequence, name="sequence"):
    """
    Check whether a sequence contains alignment gap characters.
    """

    if "-" in sequence:
        return True

    return False


def resolve_threads(threads, total_jobs):
    """
    Resolve the number of worker processes to use.

    Parameters
    ----------
    threads : str
        Either an integer as a string (e.g. "4") or "auto".

    total_jobs : int
        Total number of comparisons.

    Returns
    -------
    tuple
        (number of worker processes, mode)
    """

    if threads == "auto":
        workers = os.cpu_count() or 1
        mode = "auto"

    else:
        try:
            workers = int(threads)
        except ValueError:
            raise ValueError(
                "threads must be an integer or 'auto'"
            )
        
        if workers < 1:
            raise ValueError(
                "threads must be a minimal value of 1"
                )
        
        mode = "user"

    workers = min(workers, total_jobs)

    return workers, mode