#!/usr/bin/env python3
import hashlib,json,os,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SEAL=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-ADJACENT-ITEMS-BOUNDARY-1.0.10.json"
def compact(m):return {k:m[k] for k in ("declaration","instruction_count","instruction_sha256")}
class BoundaryReplay(unittest.TestCase):
    def setUp(self):
        self.seal=json.loads(SEAL.read_text())
        raw=Path(os.environ["AC_ADJACENT_BOUNDARY"]).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),self.seal["report_sha256"])
        self.report=json.loads(raw)
    def test_type_sites_and_attributes(self):
        for t,x in self.report["native"]["targets"].items():
            self.assertEqual(x["class_constant_sites"],self.seal["sites"][t])
            self.assertEqual(x["attributes"],self.seal["attributes"][t])
    def test_boundaries(self):
        for t,x in self.report["native"]["native_boundaries"].items():
            self.assertEqual({**{k:x[k] for k in ("class_sha256","missing")},"methods":[compact(m) for m in x["methods"]]},self.seal["boundary_owners"][t])
    def test_anvil_dispatch(self):
        t=next(t for t in self.report["native"]["targets"] if t.endswith("AlwaysCombinableOnAnvil"))
        a=self.report["native"]["targets"][t]
        self.assertEqual([(x["method"],x["offset"],x["opcode"]) for x in a["class_constant_sites"]],[("onUpdateAnvil",7,"instanceof")])
        m=next(iter(a["consumer_bodies"].values()))[0]
        self.assertEqual(compact(m),next(iter(self.seal["type_bodies"][t].values()))[0])
        self.assertTrue(any(x["offset"]==379 and "setCost" in x["symbol"] for x in m["instructions"]))
        self.assertTrue(any(x["offset"]==392 and "setOutput" in x["symbol"] for x in m["instructions"]))
    def test_scope(self):
        self.assertEqual(self.report["initial_sha256"],self.seal["initial_sha256"])
        for k in ("scope","mutation"):self.assertEqual(self.report[k],self.seal[k])
if __name__=="__main__":unittest.main()
