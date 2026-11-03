# OGC API - Processes - Part 5: Provenance building blocks

Building blocks for the `GET /jobs/{jobId}/prov` endpoint of the Part 5 provenance extension. They build on
[Building Blocks for OGC API Processes Part 1](https://github.com/ogcincubator/bblocks-ogcapi-processes)
to reuse the core component that Part 5 Provenance profiles are specialized for, and on the
[Building Blocks alternate schemas for the W3C PROV model](https://github.com/ogcincubator/bblocks-prov-jsonld-alt)
to obtain the abstract definitions of the specialized PROV formats.

The concept mapping of Part 1 processes, jobs, inputs and results to PROV entities, activities and agents
is documented in the `job-prov` block and formalized in its `ontology` block.

## Build

```shell
./build.sh
```

The sample PROV representations are generated with `scripts/generate_prov_examples.py`
(requires `prov`, `lxml` and `rdflib`).
