# SeqDot

SeqDot is a command-line tool for generating k-mer based dotplots from biological sequences.

It supports DNA, RNA, and protein sequences and can compare sequences in forward, reverse-complement, or both directions.

#### Example output

SeqDot can visualize both forward and reverse-complement sequence similarity.
Forward matches appear as a diagonal, while reverse-complement matches appear as an anti-diagonal.

![SeqDot example dotplot](examples/example.png)

Plot generated with:

```bash
seqdot examples/seq1.fasta examples/seq2.fasta --kmer 7 --point-size 7 --strand both --output examples/example.png
```

---

### Features

#### K-mer based sequence comparison

The default k-mer size is 11. Use `--kmer` to change value. Values between 1 and 100 are accepted.

For shorter sequences, a smaller k-mer size might be required. For longer sequences, larger k-mer values may provide more specific matches.

#### DNA, RNA, and amino acid sequences

The default expectation is DNA sequences.

Sequences are converted to uppercase. K-mers containing ambiguous characters such as `N` (DNA/RNA) or `X` (protein) are ignored during matching.

Other supported alphabets are:

- `RNA`
- `AA` (amino acid sequences)

For amino acid sequences, all valid amino acid characters are accepted.

#### Forward, reverse-complement, and dual-strand comparisons

The default is forward strand comparison.

Available options are:

- `forward`
- `reverse`
- `both`

Forward matches are shown along the main diagonal. Reverse-complement matches are shown along the anti-diagonal.

#### Coloured strand-aware dotplots

When using `--strand both`, forward and reverse-complement matches are shown as different colours on the same dotplot.

#### Adjustable dot size

The default dot size is 1.

The optimal dot size depends on sequence length and the desired plot resolution.

Values between 1 and 100 are accepted.

#### High-resolution output

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

#### All-vs-all batch comparison

SeqDot can compare each sequence in a multi-sequence FASTA file against all other sequences.

Example:

```bash
seqdot --file sequences.fasta --all-vs-all
```

Output plots are written to the output directory, together with summary `.tsv` file.
Default directory is `/seqdot_results/`. Placed in directory where seqdot is run.
This directory can be defined by user, with `--output-dir`.

Note: By default, self-comparisons are skipped. To include them, use `--include-self`.

#### Output file naming

Default for single comparisons:

```text
sequence1_vs_sequence2.png
```

Default for batch comparisons:

```text
seqdot_results/
├── sequence1_vs_sequence2.png
├── sequence1_vs_sequence3.png
├── sequence2_vs_sequence3.png
└── comparisons.tsv
```

#### Summary TSV file generation

A summary TSV file is automatically generated and placed in the output directory.
Generated as part of batch comparison with `--all-vs-all`.

It contains one row per comparison:

| sequence1 | sequence2 | matching_kmers |
|-----------|-----------|---------------:|
| seq1 | seq2 | 153 |
| seq1 | seq3 | 88 |

---

### Installation

#### Clone the repository

```bash
git clone https://github.com/MarliesJFrancine/SeqDot.git
cd SeqDot
```

#### Create and activate an environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Install SeqDot

```bash
pip install .
```

#### Developmental installation

For development, install SeqDot in editable mode:

```bash
pip install -e .
```

---

###  Usage

Generate a dotplot from two sequence files:

```bash
seqdot sequence1.fasta sequence2.fasta
```

Default parameters:

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

###  Input requirements

SeqDot is designed for **unaligned biological sequences**.

Accepted input:

- FASTA files containing DNA, RNA, or amino acid sequences
- One sequence per file (single comparison) or multiple sequences in a FASTA file (batch mode)

The following characters are handled as follows:

| Character | Assumption | Behaviour |
|----------|-----------|-----------|
| N (DNA/RNA) | Unknown nucleotide | k-mers containing N are ignored |
| X (protein) | Unknown amino acid | k-mers containing X are ignored |
| - (gap) | Alignment gap | SeqDot will report an error because the input appears to be an alignment |
| Any other invalid character | Invalid sequence | SeqDot will reprot an error because the input is not recognized as DNA, RNA, or AA |

Gap characters (`-`) indicate an aligned sequence. SeqDot compares raw sequences using k-mers and therefore does not accept aligned sequences containing gaps.

---

### Modify parameters

#### Change k-mer size

```bash
seqdot sequence1.fasta sequence2.fasta --kmer 21
```

#### Compare reverse-complement strands

```bash
seqdot sequence1.fasta sequence2.fasta --strand reverse
```

#### Compare both strands

```bash
seqdot sequence1.fasta sequence2.fasta --strand both
```

#### Compare amino acid sequences

```bash
seqdot sequence1.fasta sequence2.fasta --alphabet AA
```

#### Compare RNA sequences

```bash
seqdot sequence1.fasta sequence2.fasta --alphabet RNA
```

#### Change dot size

```bash
seqdot sequence1.fasta sequence2.fasta --point-size 5
```

#### Change output name and format

```bash
seqdot sequence1.fasta sequence2.fasta --output comparison.pdf
```

#### Save output in a directory

```bash
seqdot sequence1.fasta sequence2.fasta --output-dir plots/
```

#### Include self-comparisons

To include self-comparisons when plotting a multi-sequence FASTA file with `--all-vs-all`:

```bash
seqdot --file sequences.fasta --all-vs-all --include-self
```

---

#### Run tests

SeqDot uses `pytest` for automated testing.

Run:

```bash
pytest
```