# OGC API - Processes - Part 5: Provenance

API definition of `GET /jobs/{jobId}/prov`, limited to the job provenance endpoint.

## Representations

| Media type | Format | Block |
|---|---|---|
| `application/provenance+json` (alias `application/json`) | PROV-JSON, default | `ogc.api.processes.v5.provenance.job-prov-json` |
| `application/ld+json` | PROV-JSONLD | `ogc.api.processes.v5.provenance.job-prov-jsonld` |
| `application/provenance+xml` (aliases `application/xml`, `text/xml`) | PROV-XML | `ogc.api.processes.v5.provenance.job-prov-xml` |
| `text/provenance-notation` | PROV-N | `ogc.api.processes.v5.provenance.job-prov-n` |
| `application/n-triples`, `text/turtle` | PROV-O RDF | `ogc.api.processes.v5.provenance.job-prov-rdf` |

The endpoint returns the Job Provenance Response (`ogc.api.processes.v5.responses.jobProv`).
Each format is a profile of that response implementing its W3C PROV serialization.

## Part 1 relations

The endpoint extends the Part 1 `GET /jobs/{jobId}` path (`ogc.api.processes.v1.paths.Job`) and reuses
its `jobId` parameter, `ServerError` response and `exception` schema.
The job and process of Part 1 (`statusInfo`, `process`) are mapped to PROV by `schemas.jobStatus`, `schemas.jobActivity` and `schemas.processProv`.

## Errors

| Status | Exception type |
|---|---|
| 404 | `https://www.opengis.net/def/exceptions/ogcapi-processes-5/1.0/prov-missing` |
| 406 | `https://www.opengis.net/def/exceptions/ogcapi-processes-5/1.0/prov-unsupported-format` |
