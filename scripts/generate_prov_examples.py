"""
Generate the compact job provenance example in every PROV representation of the Part 5 format blocks.

Requires the ``prov`` (>=3.1), ``lxml`` and ``rdflib`` packages.
The same ``ProvDocument`` is serialized to each representation to guarantee that all blocks
carry the exact same provenance content.
"""

import argparse
import json
from pathlib import Path

from prov.model import ProvDocument, QualifiedName

BASE = "https://example.com/ogcapi/"
JOB_ID = "6c5c7dd0-0b5e-4c4c-9d1e-2a4d3e1f9a10"
PROFILE_ROLE = "http://www.opengis.net/def/glossary/term/Raster"
STATUS_ROLE = "http://www.opengis.net/def/glossary/term/Status"
PROFILE_GENERIC = "https://example.com/def/profile/raster"
PROFILE_SPECIALIZED = "https://example.com/def/profile/raster-cog"

OUTPUTS = {
    "job-prov-json": ("job_prov.json", "json", {}),
    "job-prov-jsonld": ("job_prov.jsonld", "jsonld", {}),
    "job-prov-xml": ("job_prov.xml", "xml", {}),
    "job-prov-n": ("job_prov.provn", "provn", {}),
    "job-prov-rdf": ("job_prov.ttl", "rdf", {"rdf_format": "turtle"}),
}


def flat(attributes: dict) -> list[tuple]:
    """
    Expand attributes with a list of values into repeated ``(name, value)`` tuples.
    """
    return [(key, item) for key, value in attributes.items()
            for item in (value if isinstance(value, list) else [value])]


def build_document() -> ProvDocument:
    doc = ProvDocument()
    for prefix, uri in {
        "wfprov": "http://purl.org/wf4ever/wfprov#",
        "wfdesc": "http://purl.org/wf4ever/wfdesc#",
        "wf4ever": "http://purl.org/wf4ever/wf4ever#",
        "dct": "http://purl.org/dc/terms/",
        "foaf": "http://xmlns.com/foaf/0.1/",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "ex": BASE,
        "job": f"{BASE}jobs/{JOB_ID}/",
        "proc": f"{BASE}processes/",
        "input": f"{BASE}processes/echo/inputs/",
        "output": f"{BASE}processes/echo/outputs/",
        "profile": "https://example.com/def/profile/",
    }.items():
        doc.add_namespace(prefix, uri)
    ns = {p.prefix: p for p in doc.namespaces}
    ex, job, proc = ns["ex"], ns["job"], ns["proc"]
    inp, out, prof = ns["input"], ns["output"], ns["profile"]
    qn = doc.valid_qualified_name

    def agent(identifier, attributes):
        return doc.agent(identifier, flat(attributes))

    def entity(identifier, attributes):
        return doc.entity(identifier, flat(attributes))

    user = agent(ex["agents/alice"], {
        "prov:type": [qn("prov:Person")],
        "prov:label": "Alice (user agent that submitted the job)",
    })
    server = agent(ex["agents/server"], {
        "prov:type": [qn("prov:SoftwareAgent")],
        "prov:label": "Example OGC API - Processes server",
    })
    engine = agent(ex["agents/engine"], {
        "prov:type": [qn("prov:SoftwareAgent"), qn("wfprov:WorkflowEngine")],
        "prov:label": "Example workflow engine",
    })
    doc.actedOnBehalfOf(server, user)
    doc.actedOnBehalfOf(engine, server)

    profile_generic = entity(prof["raster"], {"prov:role": PROFILE_ROLE})
    profile_specialized = entity(prof["raster-cog"], {"prov:role": PROFILE_ROLE})
    doc.specializationOf(profile_specialized, profile_generic)

    process = entity(proc["echo"], {
        "prov:type": [qn("wfdesc:Process")],
        "prov:label": "Process Description",
        "prov:location": f"{BASE}processes/echo",
        "dct:conformsTo": prof["raster"],
    })

    profile_status = entity(prof["status"], {"prov:role": STATUS_ROLE})
    job_status = entity(job["status"], {
        "prov:label": "Job Status",
        "prov:location": f"{BASE}jobs/{JOB_ID}",
        "dct:conformsTo": profile_status.identifier,
    })
    doc.wasAttributedTo(job_status, user)

    activity = doc.activity(job["run"], other_attributes=flat({
        "prov:type": [qn("wfprov:ProcessRun")],
        "prov:label": "Execution of the echo process",
    }))
    doc.wasInfluencedBy(job_status, activity)
    doc.wasAssociatedWith(activity, engine, plan=process)
    doc.wasAssociatedWith(activity, user)
    doc.wasStartedBy(activity, trigger=job_status, time="2026-01-15T16:46:10Z")

    def add_data(identifier: QualifiedName, label: str, file_uri: str | None = None,
                 value: str | None = None, collection: bool = False,
                 profiles: list[QualifiedName] | None = None) -> QualifiedName:
        types = [qn("wfprov:Artifact")]
        attrs: dict = {"prov:label": label}
        if file_uri:
            types.append(qn("wf4ever:File"))
            attrs["prov:location"] = file_uri
        if collection:
            types.append(qn("prov:Collection"))
        if value is not None:
            attrs["prov:value"] = value
        attrs["prov:type"] = types
        if profiles:
            attrs["dct:conformsTo"] = profiles
        return entity(identifier, attrs)

    message = add_data(job["inputs/message"], "Input 'message'", value="hello")
    doc.used(activity, message, other_attributes={"prov:role": inp["message"]})

    image = add_data(job["inputs/image"], "Input 'image'",
                     file_uri="https://example.com/data/image.tif", profiles=[prof["raster"]])
    doc.used(activity, image, other_attributes={"prov:role": inp["image"]})

    output = add_data(job["results/output"], "Result 'output'",
                      file_uri=f"{BASE}jobs/{JOB_ID}/results/output", profiles=[prof["raster-cog"]])
    doc.wasGeneratedBy(output, activity, time="2026-01-15T16:46:12Z",
                       other_attributes={"prov:role": out["output"]})

    images = add_data(job["results/images"], "Result 'images'", collection=True)
    doc.wasGeneratedBy(images, activity, time="2026-01-15T16:46:12Z",
                       other_attributes={"prov:role": out["images"]})
    for index in range(2):
        member = add_data(job[f"results/images/{index}"], f"Result 'images' item {index}",
                          file_uri=f"{BASE}jobs/{JOB_ID}/results/images/{index}")
        doc.hadMember(images, member)

    doc.wasEndedBy(activity, trigger=output, time="2026-01-15T16:46:13Z")
    return doc


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("sources", type=Path, help="Path to the '_sources/v5/provenance' directory.")
    args = parser.parse_args()

    doc = build_document()
    for block, (filename, fmt, options) in OUTPUTS.items():
        target = args.sources / block / "examples" / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        if fmt == "provn":
            target.write_text(doc.get_provn() + "\n", encoding="utf-8")
        else:
            doc.serialize(str(target), format=fmt, **options)
        if fmt in ("json", "jsonld"):
            data = json.loads(target.read_text(encoding="utf-8"))
            target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print(target)
    ntriples = args.sources / "job-prov-rdf" / "examples" / "job_prov.nt"
    doc.serialize(str(ntriples), format="rdf", rdf_format="nt")
    print(ntriples)


if __name__ == "__main__":
    main()
