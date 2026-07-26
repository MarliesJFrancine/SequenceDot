from Bio import SeqIO


def read_fasta(filename):
    """
    Read a FASTA file and return sequence information.
    """

    record = SeqIO.read(filename, "fasta")

    return {
        "name": record.id,
        "sequence": str(record.seq),
        "length": len(record.seq)
    }
