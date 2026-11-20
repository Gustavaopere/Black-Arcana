#!/usr/bin/env python3
import hashlib,json,os,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SEAL=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-BURROWING-CAVE-MAP-DISCOVERY-1.0.10.json"
def compact(m):return {k:m[k] for k in ("declaration","instruction_count","instruction_sha256")}
class SixDiscovery(unittest.TestCase):
    def setUp(self):
        self.seal=json.loads(SEAL.read_text())
        self.raw=Path(os.environ["AC_SIX_REPORT"]).read_bytes()
        self.report=json.loads(self.raw)
    def test_sha_artifact_scope(self):
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(),self.seal["report_sha256"])
        self.assertEqual(self.report["artifact"],self.seal["artifact"])
        self.assertEqual(self.report["native"]["class_entries_scanned"],1555)
        self.assertFalse(self.report["provider_universe_closed"])
        for k in ("scope","mutation","mutating_hook","physical_qa"):self.assertEqual(self.report[k],self.seal[k])
    def test_every_declared_body_and_typed_consumer(self):
        actual=self.report["native"]["targets"]
        self.assertEqual(set(actual),set(self.seal["targets"]))
        for t,v in actual.items():
            x={**v,"methods":[compact(m) for m in v["methods"]],"consumers":{o:{**y,"bodies":[compact(m) for m in y["bodies"]]} for o,y in v["consumers"].items()},"ancestors":{o:{**y,"methods":[compact(m) for m in y["methods"]]} for o,y in v["ancestors"].items()}}
            self.assertEqual(x,self.seal["targets"][t])
    def test_resource_census(self):
        self.assertEqual(self.report["native"]["filename_matched_resources"],self.seal["filename_matched_resources"])
    def test_pivots(self):
        ts=self.report["native"]["targets"]
        def m(t,n):
            return next(y for k,v in ts.items() if k.endswith("/"+t) for y in v["methods"] if y["declaration"]["name"]==n)["instructions"]
        self.assertTrue(any(x["offset"]==6 and "BurrowingArrowEntity" in x["symbol"] for x in m("BurrowingArrowItem","createArrow")))
        self.assertTrue(any(x["offset"]==253 and "addFreshEntity" in x["symbol"] for x in m("CaveBoatItem","use")))
        self.assertTrue(any(x["offset"]==256 and x["opcode"]=="pop" for x in m("CaveBoatItem","use")))
        self.assertTrue(any(x["offset"]==59 and "openBookGUI" in x["symbol"] for x in m("CaveBookItem","use")))
        self.assertFalse(any("shrink" in x["symbol"] for x in m("CaveBookItem","use")))
if __name__=="__main__":unittest.main()
