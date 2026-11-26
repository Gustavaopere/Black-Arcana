"""Verify per-ID seal against the exact binary audit reports; read-only."""
import argparse
import hashlib
import json
from pathlib import Path

def require(condition, message):
    if not condition:
        raise ValueError(message)

def load(path, pin):
    raw = Path(path).read_bytes()
    require(len(raw) == pin["bytes"], "report length")
    require(hashlib.sha256(raw).hexdigest() == pin["sha256"], "report digest")
    return json.loads(raw)

def ordered(rows):
    return sorted(json.dumps(row, sort_keys=True) for row in rows)

def verify(block, food, seal):
    pins = seal["reports"]["block_resource"]
    require(len(block["resources"]) == pins["resources"] == 50, "resource files")
    require(sum(len(row["hits"]) for row in block["resources"].values()) == pins["hits"] == 65, "resource hits")
    require(sum(len(row["sites"]) for row in block["field_consumers"].values()) == pins["field_sites"] == 23, "block field sites")
    require(len(seal["objects"]) == 10, "object count")
    candidates = {key for key, row in seal["objects"].items() if row["static_contract"] == "CERTIFIED_STATIC_7_AXES"}
    require(candidates == {"alexscaves:green_soylent", "alexscaves:slam"}, "certificate scope")
    for key, obj in seal["objects"].items():
        resources = []
        for resource, row in block["resources"].items():
            for hit in row["hits"]:
                if hit["id"] == key:
                    resources.append({"resource": resource, "sha256": row["sha256"], **{k: hit[k] for k in ("path", "token", "kind", "relation")}})
        require(ordered(resources) == ordered(obj["resources"]), f"resource attribution {key}")
        sites = []
        field = obj["registry_field"]
        if obj["registry_kind"] == "block":
            for owner, row in block["field_consumers"].items():
                for site in row["sites"]:
                    if site["field"] == field:
                        sites.append({"owner": owner, **{k: site[k] for k in ("name", "offset", "opcode", "code_sha256")}})
        else:
            for owner, row in food["field_consumers"].items():
                for method in row["sites"]:
                    for site in method["sites"]:
                        if site["member"][2][1] == field:
                            sites.append({"owner": owner, "name": method["name"], "offset": site["offset"], "opcode": site["opcode"], "code_sha256": method["code_sha256"]})
        require(ordered(sites) == ordered(obj["field_sites"]), f"field attribution {key}")
    print("Exact per-ID resource and field-site seal verified; two static candidates, no mutation.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for name in ("report", "food-report", "seal"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    seal = json.loads(Path(args.seal).read_text())
    verify(load(args.report, seal["reports"]["block_resource"]), load(args.food_report, seal["reports"]["food_identity"]), seal)
