# SPDX-FileCopyrightText: The URPX Authors
# SPDX-License-Identifier: Apache-2.0

"""Run with: python3 -m pytest scripts/"""

import pytest

from urpx_version import release_version

IRI = "https://github.com/urpx-org/urpx/raw/v0.5.1/ontology/urpx-ontology.ttl"


@pytest.mark.parametrize("declared", [IRI, "0.5.1", "v0.5.1", f"  {IRI}\n"])
def test_names_a_version(declared):
    assert release_version(declared) == "0.5.1"


@pytest.mark.parametrize("declared", ["https://urpx.org/ns/ontology/", "latest", "0.5", ""])
def test_names_no_version(declared):
    with pytest.raises(ValueError):
        release_version(declared)
