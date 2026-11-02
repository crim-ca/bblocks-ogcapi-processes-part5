# Job status as PROV job activity

Profile of the Part 1 status info (`ogc.api.processes.v1.schemas.statusInfo`) and of the plain
PROV Activity (`ogc.api.processes.v5.provenance.prov-activity`).
The JSON-LD context interprets it as the `oap5:JobActivity`, the execution of the process (`REQ_job-activity`).
The `started` and `finished` members align with the `prov:startedAtTime` and `prov:endedAtTime`
of the activity, as recommended by Part 5.
The job status entity is described by `ogc.api.processes.v5.schemas.jobStatus`.

| JSON member | RDF property |
|---|---|
| `started` | `prov:startedAtTime` |
| `finished` | `prov:endedAtTime` |
