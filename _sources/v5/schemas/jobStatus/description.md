# Job status as PROV job status entity

Profile of the Part 1 status info (`ogc.api.processes.v1.schemas.statusInfo`) and of the plain
PROV Entity (`ogc.api.processes.v5.provenance.prov-entity`).
The JSON-LD context interprets it as the `oap5:JobStatusEntity` (`REQ_job-entity`), a plain `prov:Entity` that reflects the job status.
The timing of the execution is mapped by the job activity (`ogc.api.processes.v5.schemas.jobActivity`).

The `links` member carries the entry to the provenance, with `rel` `https://www.w3.org/ns/prov`,
`href` `/jobs/{jobId}/prov` and `type` `application/provenance+json`. It is not mapped to RDF.

| JSON member | RDF property |
|---|---|
| `jobID` | `dct:identifier` |
| `processID` | `dct:source` |
| `status` | `dct:type` |
| `created` | `dct:created` |
| `updated` | `dct:modified` |
| `message` | `rdfs:comment` |
