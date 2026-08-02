from Bio import SeqIO

from seqdot.utils import clean_sequence


def validate_fasta(filename):
    """
    Check that the input file is in fasta format.
    """

    with open(filename) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            if not line.startswith(">"):
                raise ValueError(
                    "Input file is not in fasta format"
                )

            return

    raise ValueError(
        "Input file is empty"
    )


def read_fasta(filename, alphabet="DNA"):
    """
    Read a single fasta sequence.
    """

    validate_fasta(filename)

    records = list(
        SeqIO.parse(filename, "fasta")
    )

    if len(records) == 0:
        raise ValueError(
            "Input file contains no sequences"
        )

    if len(records) > 1:
        raise ValueError(
            "Multiple sequences found "
            "Use '--file' option instead"
        )

    record = records[0]

    return {
        "name": record.id,
        "sequence": clean_sequence(
            str(record.seq),
            alphabet,
            record.id,
        ),
        "length": len(record.seq),
        "index": None,
    }


def read_multi_fasta(filename, alphabet="DNA"):
    """
    Read a multi-sequence fasta file.
    """

    validate_fasta(filename)

    records = list(
        SeqIO.parse(filename, "fasta")
    )

    if len(records) == 0:
        raise ValueError(
            "Input file contains no sequences"
        )

    sequences = []

    for record in records:

        sequences.append(
            {
                "name": record.id,
                "sequence": clean_sequence(
                    str(record.seq),
                    alphabet,
                    record.id,
                ),
                "length": len(record.seq),
                "index": None,
            }
        )

    names = [seq["name"] for seq in sequences]

    if len(names) != len(set(names)):
        raise ValueError(
            "Duplicate sequence headers found"
        )

    return sequences