<!-- SPDX-FileCopyrightText: The URPX Authors -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Submissions

**Nothing in this directory is reviewed for data content, completeness, or accuracy.** See the disclaimer in the [repository README](../README.md).

A submission is a directory of files under `submissions/`. The quickest way in is to copy the template and edit it:

```
cp -r submissions/_template submissions/<your-submission-name>
```

The template at [`_template/`](_template/) is a complete, working submission: its dataset passes gate 1 as it stands, so you start from something valid and change it to your rate plan. [`pge-e-elec/`](pge-e-elec/) is the same shape filled in with a real tariff.

## What a submission contains

Three things, in a directory whose name is a short kebab-case slug you choose (for example `pge-e-tou-c` or `con-edison-steam-sc1`):

- **The dataset**, as URPX JSON-LD. It declares the URPX version it targets in `urpx:targetURPXVersion`, and carries the metadata the catalog reads: the utility (a `urpx:UtilityOperator` with its `urpx:legalName`), the commodity (`urpx:commodity`), the rate plans (`urpx:ratePlanUniqueIdentifier` and `urpx:name`), the service class (`urpx:serviceClassName`) when the plan names one, and the effective dates on the rate plan versions.
- **The vendored source document**: a copy of the published tariff or rate document the dataset is built from, included in the directory rather than only linked.
- **A README** stating the utility, the jurisdiction, the rate plan, the declared URPX version, whether the dataset is built from a real published dataset or is synthetic, and the effective and service-period dates.

The worked example lays these out like this:

```
submissions/pge-e-elec/
  README.md
  data/
    urpx-rate-plan_pge_e-elec.jsonld
    urpx-rate-plan_pge_e-elec.jsonld.license
  assets/
    PGE_E-ELEC_2026-01-01.pdf
    PGE_E-ELEC_2026-01-01.pdf.license
```

The `data/` and `assets/` split is a convention the worked example and the template follow; it is not required. The catalog walks the whole directory, reads any `*.jsonld` as a dataset and every other vendored file as a source document, so the arrangement inside the directory is yours to choose. The `.license` sidecars are needed only here because this dataset's copyright holder and the source document's issuer differ from the repository defaults; a submission you author yourself needs none (see the template's [Licensing](_template/README.md#licensing) note).

The directory does not encode a country, state, utility, commodity, or service class. The catalog reads all of those from the metadata in the submitted documents, not from the path. Record those facts in the dataset, not in the directory name. Keep one submission per directory; a schedule you want listed on its own goes in its own directory.

## How to submit

1. **Copy the template** to `submissions/<your-submission-name>/`, or copy the worked example if your rate plan is close to it.
2. **Put your dataset in place.** Edit the JSON-LD to describe your rate plan: the utility, the commodity, the rate plan identifier and name, the version it targets, the effective dates, and the plan elements and prices. The next section describes a reproducible way to draft this from a tariff.
3. **Vendor the source document.** Replace the placeholder with the published tariff or rate document your dataset is built from, keeping its original filename and capture date.
4. **Write the submission README**, following [`_template/README.md`](_template/README.md) and the [`pge-e-elec` README](pge-e-elec/README.md).
5. **Validate locally** (see [How gate 1 and the catalog work](#how-gate-1-and-the-catalog-work)), then **open a pull request** using the [pull request template](../.github/PULL_REQUEST_TEMPLATE.md), which asks for the utility, the jurisdiction, the source-document reference, the declared URPX version, whether the dataset was built from a real dataset, and the effective and service-period dates.

## Building a submission from a tariff

A dataset is a URPX graph. You can write it by hand, generate it with your own tooling, or ask a language model to draft it. Whichever you use, the path is the same, and nothing in it is specific to this repository:

1. **Pick the URPX version you will target** and get its ontology and SHACL shapes. Each urpx-org/urpx release publishes them as assets — for example the v0.5.1 release carries `urpx-ontology-v0.5.1.ttl` and `urpx-shacl-v0.5.1.ttl` — and the JSON-LD context it uses is served at `https://urpx.org/ns/context/releases/v0.5.1/jsonld/urpx-context.jsonld`. The ontology defines the vocabulary; the shapes define what a valid instance must carry.
2. **Follow the required structure.** A minimal valid instance is a `urpx:URPXPackage` that names its `urpx:targetURPXVersion` and holds a `urpx:RatePlan` (with `urpx:ratePlanUniqueIdentifier`, `urpx:name`, and `urpx:initialEffectiveDate`), plus a `urpx:RatePlanVersion` for the priced version (with `urpx:forRatePlan`, `urpx:changeReason`, `urpx:serviceRole`, a `urpx:CoverageClaim`, and the plan elements and prices). The template's `data/rate-plan.jsonld` is exactly this minimum; the worked example extends it to a full tariff with time-of-use periods, ledgers, and 27 priced charges.
3. **Draft the JSON-LD against the shapes.** If you ask a language model to do it, give it the ontology, the SHACL shapes, the template, and your tariff, and ask it to produce a JSON-LD instance that declares the version and validates against those shapes. Treat its output as a draft to check against the source document, not as a finished dataset.
4. **Validate and iterate** with gate 1 locally until the instance conforms. Gate 1 is the arbiter: an instance that passes it is a valid submission, however it was produced.

## How gate 1 and the catalog work

Validate before you open the pull request, and again on every push once it is open:

```
pip install -r scripts/requirements.txt
python3 scripts/validate_submission.py submissions/
```

Gate 1 reads the version each dataset declares, fetches that version's ontology and SHACL shapes from the matching urpx-org/urpx release, and validates the dataset against them. A dataset is validated against the version it declares, never against whatever is current. A submission that fails gate 1 does not merge.

The [catalog index](../catalog/README.md) is machine-owned: you do not edit it, and you do not need to add your submission to it in your pull request. The gate-1 workflow regenerates both projections of the index after your submission merges, reading each entry's facets — the utility, commodity, rate plans, service class, version, and dates — from your dataset's metadata. You can preview the row your submission will produce by running the generator over your own copy:

```
python3 scripts/update_catalog_index.py build submissions/ catalog/
```

Every dataset goes through this process, including one that already validates against a released URPX version and needs no ontology change. There is no route that skips the sandbox. A submission can later be nominated to be copied into the curated test cases in `urpx-org/urpx`, but only after it passes full review, separate from and later than gate 1.
