# Process description as PROV process entity

Profile of the Part 1 process (`ogc.api.processes.v1.schemas.process`) description.
The JSON-LD context interprets it as the `oap5:ProcessEntity` of the job provenance, which is both
a `prov:Entity` and a `wfdesc:Process` (`REQ_process-entity`).
The `prov:location` of the entity is the absolute URL of the process, `{root}/processes/{id}`.

| JSON member | RDF property |
|---|---|
| `id` | `dct:identifier` |
| `title` | `rdfs:label` |
| `description` | `dct:description` |
| `version` | `owl:versionInfo` |
| `keywords` | `dct:subject` |

`links`, `inputs` and `outputs` are not mapped.
The concept mapping is documented in Job Provenance (`ogc.api.processes.v5.provenance.job-prov`).
