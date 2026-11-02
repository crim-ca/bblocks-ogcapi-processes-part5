# Job Provenance (PROV model)

Representation-independent model of the provenance returned by `GET /jobs/{jobId}/prov`.
Each requirement of [Part 5](https://docs.ogc.org/DRAFTS/26-038.html) is checked with SHACL shapes
on the PROV-O RDF graph, so that every serialization (see `hasFormat`) is validated identically.
Requirements are reported as violations and recommendations as warnings.

## Mapping of Part 1 concepts to PROV

| Part 1 concept | PROV concept | Relation | Requirement |
|---|---|---|---|
| Process (`/processes/{processID}`) | `prov:Entity` typed `wfdesc:Process` | `oap5:ProcessEntity` is a specialization of `oap1:Process` | `REQ_process-entity` |
| Job status (`/jobs/{jobID}`) | plain `prov:Entity` with `prov:location`, related to the job activity by `prov:wasInfluencedBy` or `prov:wasGeneratedBy` | `oap5:JobStatusEntity` is a specialization of `oap1:JobStatus` | `REQ_job-entity` |
| Job execution | `prov:Activity` typed `wfprov:WorkflowRun` or `wfprov:ProcessRun`, associated with the process entity | `oap5:JobActivity` is a specialization of `oap1:Job` | `REQ_job-activity` |
| Input | `prov:Entity` typed `wfprov:Artifact`, `prov:used` with `prov:role` = inputID | `oap5:InputEntity` | `REQ_input-entity` |
| Result / output | `prov:Entity` typed `wfprov:Artifact`, `prov:wasGeneratedBy` with `prov:role` = outputID | `oap5:ResultEntity` | `REQ_result-entity` |
| Multiple-valued data | `prov:Collection` with `prov:hadMember` | `oap5:CollectionEntity` | `REQ_collection-entity` |
| File data | `wf4ever:File` | `oap5:FileEntity` | `REQ_file-entity` |
| Server, engine | `prov:SoftwareAgent` | `oap5:SoftwareAgent` | `REC_agents` |
| User | `prov:Person` | `oap5:UserAgent` | `REC_agents` |
| Metadata profile | `prov:Entity` with `prov:role`, linked with `dct:conformsTo` and `prov:specializationOf` | `oap5:ProfileEntity` | `REC_profile-entity` |

The Part 1 concepts are anchored in the ontology (`ogc.api.processes.v5.provenance.ontology`).
This model is related to the Part 1 blocks as follows. The `oap1` and `oap5` namespaces are provisional.

| Part 1 block | PROV counterpart |
|---|---|
| `ogc.api.processes.v1.schemas.statusInfo` (Job status) | job status entity and job activity, via `ogc.api.processes.v5.schemas.jobStatus` and `ogc.api.processes.v5.schemas.jobActivity` |
| `ogc.api.processes.v1.schemas.process` (process description) | process entity, via `ogc.api.processes.v5.schemas.processProv` |
| `ogc.api.processes.v1.schemas.results` (Output) | result and input data entities, described by `ogc.api.processes.v5.provenance.ontology` |

The model depends on the `ogc.api.processes.v5.responses.jobProv` response, whose serializations carry the formats (`hasFormat`).

## Findings on the standard's example

The `job_prov` example of the standard types some literal-valued input and result entities as `prov:Entity`
only, without `wfprov:Artifact`. These do not meet `REQ_input-entity` and `REQ_result-entity`.
The example of this block is conformant, and the standard's own example reports `REC_data-entity` warnings
for artifacts that carry neither `prov:value` nor `prov:location`.
