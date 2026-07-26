from seqdot.alphabet import DNA, RNA, AA


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