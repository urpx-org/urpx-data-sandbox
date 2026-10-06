#!/usr/bin/env python3
# SPDX-FileCopyrightText: The URPX Authors
# SPDX-License-Identifier: Apache-2.0

"""Regenerate catalog/submissions-index.csv from the submissions that pass gate 1.

Runs the SPARQL summary queries gate 1 promises: counts of the principal
classes, the effective-date range, and whether the submission carries an
externally-priced reference. This file is machine-owned output; it never
shares a commit path with a hand-edited file, and a hand edit to the CSV is
overwritten on the next run.
"""

from __future__ import annotations

import csv
import datetime
import pathlib
import sys

from rdflib import Graph

from urpx_version import release_version

URPX = "https://urpx.org/ns/ontology/"

CLASS_COUNT_QUERY = """
PREFIX urpx: <https://urpx.org/ns/ontology/>
SELECT
  (COUNT(DISTINCT ?ratePlan) AS ?ratePlanCount)
  (COUNT(DISTINCT ?ratePlanVersion) AS ?ratePlanVersionCount)
  (COUNT(DISTINCT ?pricingModel) AS ?pricingModelCount)
  (COUNT(DISTINCT ?priceDefinition) AS ?priceDefinitionCount)
  (COUNT(DISTINCT ?price) AS ?priceCount)
WHERE {
  OPTIONAL { ?ratePlan a urpx:RatePlan }
  OPTIONAL { ?ratePlanVersion a urpx:RatePlanVersion }
  OPTIONAL { ?pricingModel a urpx:PricingModel }
  OPTIONAL { ?priceDefinition a urpx:PriceDefinition }
  OPTIONAL { ?price a urpx:Price }
}
"""

EFFECTIVE_DATE_QUERY = """
PREFIX urpx: <https://urpx.org/ns/ontology/>
SELECT (MIN(?date) AS ?minDate) (MAX(?date) AS ?maxDate)
WHERE { ?s urpx:effectiveDate ?date }
"""

EXTERNAL_REFERENCE_QUERY = """
PREFIX urpx: <https://urpx.org/ns/ontology/>
ASK { ?ref urpx:referenceInclusion urpx:retrievedElsewhere }
"""

VERSION_QUERY = """
PREFIX urpx: <https://urpx.org/ns/ontology/>
SELECT ?version WHERE { ?s urpx:targetURPXVersion ?version } LIMIT 1
"""

CSV_HEADER = [
    "submission_path",
    "utility",
    "jurisdiction",
    "urpx_version",
    "rate_plan_count",
    "rate_plan_version_count",
    "pricing_model_count",
    "price_definition_count",
    "price_count",
    "effective_date_start",
    "effective_date_end",
    "has_external_price_reference",
    "date_added",
]


def find_submission_dirs(root: pathlib.Path) -> list[pathlib.Path]:
    """A submission lives four levels deep: country/state/utility/commodity."""
    dirs = []
    for commodity_dir in root.glob("*/*/*/*"):
        if "_template" in commodity_dir.parts:
            continue
        if commodity_dir.is_dir() and any(commodity_dir.glob("*.jsonld")):
            dirs.append(commodity_dir)
    return sorted(dirs)


def load_graph(submission_dir: pathlib.Path) -> Graph:
    graph = Graph()
    for jsonld_file in sorted(submission_dir.glob("*.jsonld")):
        graph.parse(data=jsonld_file.read_text(), format="json-ld")
    return graph


def summarize(submission_dir: pathlib.Path, root: pathlib.Path) -> dict[str, str]:
    graph = load_graph(submission_dir)
    relative = submission_dir.relative_to(root.parent)
    country, state, utility, commodity = submission_dir.parts[-4:]

    counts = next(iter(graph.query(CLASS_COUNT_QUERY)))
    dates = next(iter(graph.query(EFFECTIVE_DATE_QUERY)))
    has_external_reference = bool(next(iter(graph.query(EXTERNAL_REFERENCE_QUERY))))
    version_rows = list(graph.query(VERSION_QUERY))
    version = release_version(str(version_rows[0].version)) if version_rows else ""

    return {
        "submission_path": str(relative),
        "utility": utility,
        "jurisdiction": f"{state} ({country})",
        "urpx_version": version,
        "rate_plan_count": str(counts.ratePlanCount),
        "rate_plan_version_count": str(counts.ratePlanVersionCount),
        "pricing_model_count": str(counts.pricingModelCount),
        "price_definition_count": str(counts.priceDefinitionCount),
        "price_count": str(counts.priceCount),
        "effective_date_start": str(dates.minDate) if dates.minDate else "",
        "effective_date_end": str(dates.maxDate) if dates.maxDate else "",
        "has_external_price_reference": "yes" if has_external_reference else "no",
        "commodity": commodity,
    }


def load_existing_dates(csv_path: pathlib.Path) -> dict[str, str]:
    if not csv_path.exists():
        return {}
    with csv_path.open(newline="", encoding="utf-8") as handle:
        return {
            row["submission_path"]: row["date_added"]
            for row in csv.DictReader(handle)
        }


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: update_catalog_index.py <submissions-dir> <csv-out>", file=sys.stderr)
        return 2

    root = pathlib.Path(argv[1])
    csv_path = pathlib.Path(argv[2])
    existing_dates = load_existing_dates(csv_path)
    today = datetime.date.today().isoformat()

    rows = []
    for submission_dir in find_submission_dirs(root):
        try:
            row = summarize(submission_dir, root)
        except Exception as error:  # a submission that fails to parse is skipped, not fatal
            print(f"{submission_dir}: skipped ({error})", file=sys.stderr)
            continue
        row.pop("commodity", None)
        row["date_added"] = existing_dates.get(row["submission_path"], today)
        rows.append(row)

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_HEADER)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"Wrote {len(rows)} submission(s) to {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
