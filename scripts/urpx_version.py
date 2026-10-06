# SPDX-FileCopyrightText: The URPX Authors
# SPDX-License-Identifier: Apache-2.0

"""The URPX release a urpx:targetURPXVersion value names.

The ontology defines targetURPXVersion as the ontology version IRI, for
example https://github.com/urpx-org/urpx/raw/v0.5.1/ontology/urpx-ontology.ttl.
A bare 0.5.1 or v0.5.1 is accepted too.
"""

from __future__ import annotations

import re

VERSION_PATTERN = re.compile(r"(?:^|/)v?(\d+\.\d+\.\d+)(?:/|$)")


def release_version(declared: str) -> str:
    """Return the semantic version, e.g. "0.5.1", named by `declared`."""
    match = VERSION_PATTERN.search(declared.strip())
    if not match:
        raise ValueError(
            f"targetURPXVersion {declared!r} names no version; expected the "
            "ontology version IRI, e.g. https://github.com/urpx-org/urpx/raw/"
            "v0.5.1/ontology/urpx-ontology.ttl"
        )
    return match.group(1)
