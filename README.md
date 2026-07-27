# SeqDot

SeqDot is a command-line tool for generating k-mer based dotplots from biological sequences.

It supports DNA, RNA, and protein sequences and can compare sequences in forward, reverse-complement, or both directions.

## Features

### K-mer based sequence comparison

The default k-mer size is 11.

For shorter sequences, a smaller k-mer size might be required. For longer sequences, larger k-mer values may provide more specific matches.

Values between 1 and 100 are accepted.

### DNA, RNA, and amino acid sequences

The default expectation is DNA sequences.

Sequences are converted to uppercase. K-mers containing ambiguous characters such as `N` (DNA/RNA) or `X` (protein) are ignored during matching.

Other supported alphabets are:

- `RNA`
- `AA` (amino acid sequences)

For amino acid sequences, all valid amino acid characters are accepted.

### Forward and reverse-complement comparisons

The default is forward strand comparison.

Available options are:

- `forward`
- `reverse`
- `both`

Forward matches are shown along the main diagonal. Reverse-complement matches are shown along the anti-diagonal.

### Coloured strand-aware dotplots

When using `--strand both`, forward and reverse-complement matches are shown as different colours on the same dotplot.

### Adjustable dot size

The default dot size is 1.

The optimal dot size depends on sequence length and the desired plot resolution.

Values between 1 and 100 are accepted.

### High-resolution output

The default output format is:

```
dotplot.png
```

Supported output formats are:

- `.png`
- `.pdf`
- `.svg`

Example:

```bash
seqdot sequence1.fasta sequence2.fasta --output comparison.pdf
```

### All-vs-all comparisons

SeqDot can compare all sequences in a multi-sequence FASTA file against each other.

Example:

```bash
seqdot --file sequences.fasta --all-vs-all
```

---

# Installation

## Clone the repository

```bash
git clone https://github.com/MarliesJFrancine/SeqDot.git
cd SeqDot
```

## Create and activate an environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install SeqDot

```bash
pip install .
```

## Developmental installation

For development, install SeqDot in editable mode:

```bash
pip install -e .
```

---

# Basic usage

Generate a dotplot from two sequence files:

```bash
seqdot sequence1.fasta sequence2.fasta
```

By default:

```
--kmer = 11
--alphabet = DNA
--strand = forward
--point-size = 1
--output = dotplot.png
```

For all available options:

```bash
seqdot --help
```

---

# Optional features

## Change k-mer size

```bash
seqdot sequence1.fasta sequence2.fasta --kmer 21
```

## Compare reverse-complement strands

```bash
seqdot sequence1.fasta sequence2.fasta --strand reverse
```

## Compare both strands

```bash
seqdot sequence1.fasta sequence2.fasta --strand both
```

## Compare amino acid sequences

```bash
seqdot sequence1.fasta sequence2.fasta --alphabet AA
```

## Compare RNA sequences

```bash
seqdot sequence1.fasta sequence2.fasta --alphabet RNA
```

## Change dot size

```bash
seqdot sequence1.fasta sequence2.fasta --point-size 5
```

## Change output name and format

```bash
seqdot sequence1.fasta sequence2.fasta --output comparison.pdf
```

## Save output in a directory

```bash
seqdot sequence1.fasta sequence2.fasta --output-dir plots/
```

## Include self-comparisons

To include self-comparisons when plotting a multi-sequence FASTA file with `--all-vs-all`:

```bash
seqdot --file sequences.fasta --all-vs-all --include-self
```

---

# Run tests

SeqDot uses `pytest` for automated testing.

Run:

```bash
pytest
```