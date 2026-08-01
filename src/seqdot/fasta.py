from Bio import SeqIO
from seqdot.utils import clean_sequence


def read_fasta(filename, alphabet="DNA"):
    """
    Read a FASTA file and return sequence information.
    Default is a DNA sequence.
    """
    
    with open(filename, "r") as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            if not line.startswith(">"):
                raise ValueError(
                    "Input file is not in fasta format"
                )

            break
    
    try:
        record = SeqIO.read(filename, "fasta")

    except ValueError:
        raise ValueError(
            "Input file does not contain a sequence"
        )

    return {
        "name": record.id,
        "sequence": clean_sequence(
            str(record.seq),
            alphabet,
            record.id
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

    with open(filename, "r") as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            if not line.startswith(">"):
                raise ValueError(
                    "Input file is not in fasta format"
                )

            break
    
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
                    seq = clean_sequence(
                        "".join(sequence),
                        alphabet
                    )

                    sequences.append(
                        {
                            "name": name,
                            "sequence": seq,
                            "length": len(seq),
                            "index": None
                        }
                    )

                name = line[1:].split()[0]
                sequence = []

            else:
                sequence.append(line)

        # add final sequence
        if name is not None:

            seq = clean_sequence(
                "".join(sequence),
                alphabet,
                name
            )

            sequences.append(
                {
                    "name": name,
                    "sequence": seq,
                    "length": len(seq)
                }
            )
        
        names = [seq["name"] for seq in sequences]

        if len(names) != len(set(names)):
            raise ValueError(
                "Duplicate sequence names found."
            )

    if len(sequences) == 0:
        raise ValueError(
            "Input file contains no sequences"
        )
    
    return sequences