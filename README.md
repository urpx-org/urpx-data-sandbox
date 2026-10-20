<!-- SPDX-FileCopyrightText: The URPX Authors -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# urpx-data-sandbox

This repository holds community-contributed rate plan datasets and experiments for URPX, the Utility Rate Plan Exchange ontology. It is the place for a dataset that is unvalidated, in progress, or needs vocabulary that does not exist yet, and for agent-assisted or contributor experiments that do not belong in the standard.

## What this repository is not

Nothing here is normative and nothing here is a released artifact. This is not the standard: the ontology, the SHACL shapes, and the curated test cases live in [`urpx-org/urpx`](https://github.com/urpx-org/urpx). 

A change to the standard's vocabulary or shapes is a pull request against `urpx-org/urpx`, not a submission here.

## Scope

**Each submission is validated on its own.** Gate 1 checks a submission for conformance to the URPX version it declares, and for nothing else. The sandbox does not resolve a rate plan's pricing models into rate plan or modifier version instances, and it does not verify such a resolution. A submission whose documents are only meaningful once resolved should either carry a self-contained resolved snapshot that validates on its own, or be submitted as separate documents that each validate independently. Resolution is the work of a data consumer, not of this repository.

**The catalog indexes files; it does not answer queries over them.** The [catalog index](catalog/README.md) is a generated summary that links to the submitted files so the collection is browsable without opening each one. It is not a graph database or an API, and this repository does not host one. A queryable service over URPX data — one that resolves, joins, and serves rate plans — is the role of a URPX data publisher implementation, not of a dataset repository.

## Disclaimer

This repository is part of the URPX Working Group's draft materials, hosted under LF Energy Standards and Specifications.

LF Energy and the URPX Working Group do not review the datasets in this repository and take no responsibility for their accuracy, completeness, or fitness for any purpose. A submission is checked only for conformance to the URPX version it declares.

**Nothing in this repository is reviewed for data content, completeness, or accuracy.**

Submissions are validated automatically. On a passing check, any member of the `urpx-committers` GitHub team merges the submission; there is no additional human review before it is merged. Peer review may be added later if the community grows.

## Submission structure

A submission is a directory of files under `submissions/`:

```
submissions/
  <submission-name>/     a short slug you choose; its name carries no meaning
    ...the dataset documents and their vendored source documents...
```

You do not encode a country, state, utility, or commodity in the path. Those facts — and the rate plans, service class, effective dates, and URPX version — are read from the metadata in the submitted documents. The [catalog index](catalog/README.md) derives each submission's facets from that metadata, and the browsing hierarchy (utility, commodity, rate plan, version) emerges from them. Keep one submission per directory, and give each schedule you want listed on its own a directory of its own.

[`submissions/pge-e-elec/`](submissions/pge-e-elec/) is a complete worked example — PG&E Schedule E-ELEC, with its tariff PDF vendored and its prices filled in:

```
submissions/pge-e-elec/
  README.md
  data/
    urpx-rate-plan_pge_e-elec.jsonld
  assets/
    PGE_E-ELEC_2026-01-01.pdf
```

The template at [`submissions/_template/`](submissions/_template/) is the same shape as a minimal, already-valid dataset you copy and edit. See [`submissions/README.md`](submissions/README.md) for what each file carries and the step-by-step process.

## How to submit

Copy the template to a directory of your own, swap in your data, and open a pull request:

```
cp -r submissions/_template submissions/<your-submission-name>
```

A submission carries its dataset as URPX JSON-LD, vendors its source document (includes a copy rather than only a link), and declares the URPX version it targets. Validate it locally first, then open a pull request with the [pull request template](.github/PULL_REQUEST_TEMPLATE.md):

```
pip install -r scripts/requirements.txt
python3 scripts/validate_submission.py submissions/
```

[`submissions/README.md`](submissions/README.md) gives the full steps, including a reproducible way to draft the JSON-LD from a tariff, by hand or with a language model.

Gate 1 runs automatically on every pull request: SHACL validation against the shapes of the URPX version the submission declares. A submission that fails gate 1 does not merge. The [catalog index](catalog/README.md) is regenerated from the submitted metadata after a submission merges; you do not edit it or add your submission to it yourself.

## Graduating to the standard

Every dataset starts here. There is no route that skips this repository, including for a dataset that already validates against a released URPX version. A submission can be nominated to be copied into the curated test cases in `urpx-org/urpx`, but only after it passes full review, separate from and later than gate 1.

## License

Prose, source, and meta files are licensed under the Apache License, Version 2.0. Submitted datasets and the catalog index are data, licensed under the Community Data License Agreement - Permissive 2.0 (CDLA-Permissive-2.0). A vendored source document that a submission includes is a public record of a regulatory process, not the contributor's work, and is marked `LicenseRef-PublicRecord`. See [NOTICE](NOTICE), [LICENSE](LICENSE), and `LICENSES/` for the full texts.

Security issues: see [SECURITY.md](SECURITY.md).
