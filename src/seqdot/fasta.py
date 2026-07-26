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
        "length": len(record.seq)
    }
