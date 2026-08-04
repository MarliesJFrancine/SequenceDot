import gzip

from pathlib import Path
from Bio import SeqIO

from seqdot.utils import clean_sequence


def open_fasta(filename):
    """
    Open plain or gzipped FASTA files.
    """

    filename = Path(filename)

    if filename.suffix.lower() == ".gz":
        return gzip.open(filename, "rt")

    return open(filename, "r")


def validate_fasta(filename):
    """
    Check that the input file is in FASTA format.
    """
    
    filename = Path(filename)

    if filename.suffix.lower() == ".zip":
        raise ValueError(
            "ZIP archives are not supported. "
            "Please extract the FASTA file first "
            "or use gzip-compressed (.gz) FASTA files."
        )

    with open_fasta(filename) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            if not line.startswith(">"):
                raise ValueError(
                    "Input file is not in FASTA format"
                )

            return

    raise ValueError(
        "Input file is empty"
    )


def read_fasta(filename, alphabet="DNA"):
    """
    Read a single FASTA sequence.
    """

    validate_fasta(filename)

    with open_fasta(filename) as handle:
        records = list(SeqIO.parse(handle, "fasta"))

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
    Read a multi-sequence FASTA file.
    """

    validate_fasta(filename)

    with open_fasta(filename) as handle:
        records = list(SeqIO.parse(handle, "fasta"))

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