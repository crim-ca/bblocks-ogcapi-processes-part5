# Job Provenance Response

Response of `GET /jobs/{jobId}/prov`. It is a profile of the W3C PROV Representation Base
(`ogc.ogc-utils.prov.w3c-prov-base`). The Job Provenance model (`ogc.api.processes.v5.provenance.job-prov`) depends on it.

It depends on the Part 1 job status (`ogc.api.processes.v1.schemas.statusInfo`) and process description
(`ogc.api.processes.v1.schemas.process`), mapped to PROV by `schemas.jobStatus`, `schemas.jobActivity` and `schemas.processProv`,
to represent the job and process entities of its PROV profile.

Each format is a profile of this response that implements its W3C PROV serialization (`hasFormat`):

| Media type | Block | Implements |
|---|---|---|
| `application/provenance+json` (alias `application/json`), default | `ogc.api.processes.v5.provenance.job-prov-json` | `ogc.ogc-utils.prov.w3c-prov-json` |
| `application/ld+json` | `ogc.api.processes.v5.provenance.job-prov-jsonld` | `ogc.ogc-utils.prov.w3c-prov-jsonld` |
| `application/provenance+xml` (aliases `application/xml`, `text/xml`) | `ogc.api.processes.v5.provenance.job-prov-xml` | `ogc.ogc-utils.prov.w3c-prov-xml` |
| `text/provenance-notation` | `ogc.api.processes.v5.provenance.job-prov-n` | `ogc.ogc-utils.prov.w3c-prov-n` |
| `text/turtle`, `application/n-triples` | `ogc.api.processes.v5.provenance.job-prov-rdf` | `ogc.ogc-utils.prov.w3c-prov-rdf` |
