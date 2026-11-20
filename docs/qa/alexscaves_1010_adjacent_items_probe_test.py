#!/usr/bin/env python3
"""Replay exact discovery evidence without conflating discovery and certification."""
import hashlib,json,os,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SEAL=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-ADJACENT-ITEMS-DISCOVERY-1.0.10.json"
def compact(m):
    return {k:m[k] for k in ("declaration","instruction_count","instruction_sha256")}
class AdjacentDiscovery(unittest.TestCase):
    def setUp(self):
        self.seal=json.loads(SEAL.read_text())
        self.raw=Path(os.environ["AC_ADJACENT_REPORT"]).read_bytes()
        self.report=json.loads(self.raw)
    def test_exact_hash_and_artifact(self):
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(),self.seal["report_sha256"])
        self.assertEqual(self.report["artifact"],self.seal["artifact"])
        self.assertEqual(self.report["native"]["class_entries_scanned"],1555)
    def test_all_five_targets(self):
        native=self.report["native"]["targets"]
        self.assertEqual(set(native),set(self.seal["targets"]))
        for owner,data in native.items():
            actual={**data,"methods":[compact(m) for m in data["methods"]],"ancestors":{k:{**v,"methods":[compact(m) for m in v["methods"]]} for k,v in data["ancestors"].items()}}
            self.assertEqual(actual,self.seal["targets"][owner])
    def test_factory_and_resources(self):
        n=self.report["native"]
        self.assertEqual(compact(n["biome_treat_factory"]),self.seal["biome_treat_factory"])
        self.assertEqual(n["biome_treat_resources"],self.seal["biome_treat_resources"])
    def test_no_mutation_or_certification(self):
        for key in ("scope","mutation","mutating_hook","physical_qa"):self.assertEqual(self.report[key],self.seal[key])
if __name__=="__main__":unittest.main()
