from pathlib import Path
import csv


def write_summary(results, output_dir):
    """
    Write a TSV summary of all comparisons.

    Parameters
    ----------
    results : list
        List of dictionaries returned by run_all_vs_all().

    output_dir : Path
        Output directory.
    """

    output_file = Path(output_dir) / "comparisons.tsv"

    with open(
        output_file,
        "w",
        newline=""
    ) as handle:

        writer = csv.writer(
            handle,
            delimiter="\t"
        )

        writer.writerow([
            "sequence1",
            "sequence2",
            "matching_kmers"
        ])

        for result in results:

            writer.writerow([
                result["seq1"],
                result["seq2"],
                result["matches"]
            ])