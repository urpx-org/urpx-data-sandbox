<!-- SPDX-FileCopyrightText: The URPX Authors -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Submission template

This directory is a complete, working submission you copy and edit. It is not a bare outline: the dataset in `data/rate-plan.jsonld` is a real, minimal URPX instance that passes gate 1 as it stands. Copy the whole directory to one of your own under `submissions/` — `submissions/<your-submission-name>/` — swap in your data, and open a pull request.

```
cp -r submissions/_template submissions/<your-submission-name>
```

## What the directory holds

```
submissions/<your-submission-name>/
  README.md                 what this submission is (copy this file and rewrite it)
  data/
    rate-plan.jsonld        the dataset, as URPX JSON-LD
  assets/
    source-document.txt     the vendored source document (replace with your tariff or rate PDF)
```

- **`data/rate-plan.jsonld`** — the dataset itself, one URPX package with a rate plan and a single priced version. It declares the URPX version it targets in `urpx:targetURPXVersion`, and carries the metadata the catalog reads: the utility (a `urpx:UtilityOperator` with its `urpx:legalName`), the commodity (`urpx:commodity`), and the rate plan (`urpx:ratePlanUniqueIdentifier` and `urpx:name`). Keep that structure, change the values to your rate plan, and add the rest of your prices and plan elements. Rename the file if you like; any `*.jsonld` under the directory is read as a dataset.
- **`assets/source-document.txt`** — a stand-in for the vendored source document. Replace it with the published tariff or rate document your dataset is built from, keeping its original filename and capture date. A submission includes a copy of its source, not only a link to it.
- **`README.md`** — a short description of the submission, stating the utility, the jurisdiction, the rate plan, the declared URPX version, whether the dataset is built from a real published dataset or is synthetic, and the effective and service-period dates.

The directory's name and place carry no meaning. The catalog reads what the submission is from the metadata above, not from the path, so there is no country, state, utility, or commodity to encode in the directory name.

## A complete worked example

[`submissions/pge-e-elec/`](../pge-e-elec/) is a full submission in this same shape — PG&E Schedule E-ELEC, with its real tariff PDF vendored and 27 priced charges. Read it beside this template to see a dataset filled in. The [repository README](../../README.md) walks through how to produce a submission like it and how an LLM can help draft the JSON-LD.

## Licensing

You do not add `.license` files to a copy of this template. The repository's [`REUSE.toml`](../../REUSE.toml) already licenses a submission's files by category: the dataset (`data/*.jsonld`) as data under CDLA-Permissive-2.0 with you, the contributor, as the copyright holder; the vendored source document under `LicenseRef-PublicRecord` as a public record; and this README under Apache-2.0 from its own header. Add a `.license` sidecar beside a file only to record a different copyright holder, for example to name the issuing utility on the source document.

## Disclaimer

Nothing in this repository is reviewed for data content, completeness, or accuracy. A submission is checked for conformance to the URPX version it states it targets, and for nothing else. See the [repository README](../../README.md).
