# OGC API - Processes - Part 5: Provenance building blocks

Building blocks for the `GET /jobs/{jobId}/prov` endpoint of the Part 5 provenance extension.
They are modelled on the Part 2 building blocks and build on Part 1 and on `bblocks-prov-jsonld-alt`.

The concept mapping of Part 1 processes, jobs, inputs and results to PROV entities, activities and agents
is documented in the `job-prov` block and formalized in its `ontology` block.

## Build

```shell
./build.sh
```

The sample PROV representations are generated with `scripts/generate_prov_examples.py`
(requires `prov`, `lxml` and `rdflib`).
