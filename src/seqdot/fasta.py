from Bio import SeqIO
from seqdot.utils import clean_sequence


def read_fasta(filename, alphabet="DNA"):
    """
    Read a FASTA file and return sequence information.
    Default is a DNA sequence.
    """

    record = SeqIO.read(filename, "fasta")

    return {
        "name": record.id,
        "sequence": clean_sequence(
            str(record.seq),
            alphabet
        ),
        "length": len(record.seq),
        "index": None
    }


def read_multi_fasta(filename, alphabet="DNA"):
    """
    Read a multi-FASTA file.

    Returns
    -------
    list
        List of sequence dictionaries.
    """

    sequences = []

    with open(filename, "r") as file:

        name = None
        sequence = []

        for line in file:

            line = line.strip()

            if not line:
                continue

            if line.startswith(">"):

                if name is not None:
                    seq = "".join(sequence).upper()

                    sequences.append(
                        {
                            "name": name,
                            "sequence": seq,
                            "length": len(seq)
                        }
                    )

                name = line[1:].split()[0]
                sequence = []

            else:
                sequence.append(line)

        # add final sequence
        if name is not None:

            seq = "".join(sequence).upper()

            sequences.append(
                {
                    "name": name,
                    "sequence": seq,
                    "length": len(seq)
                }
            )

    return sequences