#!/usr/bin/env python3
import hashlib
import re
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

URL = "https://www.cursemaven.com/curse/maven/asterism-arcanum-1456947/8157080/asterism-arcanum-1456947-8157080.jar"
EXPECTED_SHA1 = "4a25ba80116168ddcc812f71467c0598127e774a"
REGISTRY_CLASS = "com/birdie/asterismarcanum/registries/ASARSpellRegistry.class"
GATEWAY_CLASS = "com.birdie.asterismarcanum.spells.AstralGatewaySpell"

EXPECTED_REGISTERED_CLASSES = [
    "com/birdie/asterismarcanum/spells/StarfireSpell",
    "com/birdie/asterismarcanum/spells/BrightburstSpell",
    "com/birdie/asterismarcanum/spells/CelestialTetherSpell",
    "com/birdie/asterismarcanum/spells/StarSwarmSpell",
    "com/birdie/asterismarcanum/spells/LuminousBeamSpell",
    "com/birdie/asterismarcanum/spells/AstralGatewaySpell",
    "com/birdie/asterismarcanum/spells/SummonLunarMothsSpell",
    "com/birdie/asterismarcanum/spells/AstralEchoSpell",
    "com/birdie/asterismarcanum/spells/PiercingLightSpell",
    "com/birdie/asterismarcanum/spells/StarcutterSpell",
    "com/birdie/asterismarcanum/spells/SilveryBarbsSpell",
]
EXPECTED_IDS = [
    "starfire",
    "brightburst",
    "celestial_tether",
    "star_swarm",
    "luminous_beam",
    "astral_gateway",
    "summon_lunar_moths",
    "astral_echo",
    "piercing_light",
    "starcutter",
    "silvery_barbs",
]
TRAILBLAZE_CLASS = b"com/birdie/asterismarcanum/spells/TrailblazeSpell"

def digest(data: bytes, name: str) -> str:
    h = hashlib.new(name)
    h.update(data)
    return h.hexdigest()

def main() -> int:
    with tempfile.TemporaryDirectory(prefix="black-arcana-asterism-") as tmp:
        jar = Path(tmp) / "asterismarcanum-1.21.1-0.1.0.jar"
        req = urllib.request.Request(URL, headers={"User-Agent":"Black-Arcana-catalog-audit/1"})
        with urllib.request.urlopen(req, timeout=90) as response:
            blob = response.read()
        jar.write_bytes(blob)

        sha1 = digest(blob, "sha1")
        sha256 = digest(blob, "sha256")
        print(f"ASTERISM_SIZE={len(blob)}")
        print(f"ASTERISM_SHA1={sha1}")
        print(f"ASTERISM_SHA256={sha256}")
        if sha1 != EXPECTED_SHA1:
            raise RuntimeError(f"physical hash mismatch: expected {EXPECTED_SHA1}, got {sha1}")
        print("ASTERISM_PHYSICAL_HASH_MATCH=true")

        with zipfile.ZipFile(jar) as zf:
            names = zf.namelist()
            classes = [n for n in names if n.endswith(".class") and not n.startswith("META-INF/versions/")]
            provider_classes = [n for n in classes if n.startswith("com/birdie/asterismarcanum/")]
            provider_resources = [n for n in names if n.startswith("data/asterismarcanum/") or n.startswith("assets/asterismarcanum/")]

            if REGISTRY_CLASS not in names:
                raise RuntimeError(f"missing registry class {REGISTRY_CLASS}")
            registry_bytes = zf.read(REGISTRY_CLASS)

            present_refs = [c for c in EXPECTED_REGISTERED_CLASSES if c.encode("ascii") in registry_bytes]
            missing_refs = [c for c in EXPECTED_REGISTERED_CLASSES if c.encode("ascii") not in registry_bytes]
            trailblaze_ref = TRAILBLAZE_CLASS in registry_bytes

            spell_classes = sorted(
                n for n in provider_classes
                if n.startswith("com/birdie/asterismarcanum/spells/")
                and n.endswith("Spell.class")
            )
            override_resources = sorted(
                n for n in names
                if "irons_spellbooks_spell_config" in n.lower()
            )
            gateway_override_resources = sorted(
                n for n in override_resources
                if "astral_gateway" in n.lower()
            )
            astromancer_loot = "data/asterismarcanum/loot_table/entities/astromancer.json" in names

            id_hits = {}
            for spell_id in EXPECTED_IDS:
                token = spell_id.encode("ascii")
                id_hits[spell_id] = sum(1 for n in provider_classes if token in zf.read(n))

            metadata_name = "META-INF/neoforge.mods.toml"
            metadata = zf.read(metadata_name).decode("utf-8", errors="replace") if metadata_name in names else ""
            dep_ids = sorted(set(re.findall(r'modId\s*=\s*"([^"]+)"', metadata)))

            print(f"ASTERISM_CLASS_COUNT={len(classes)}")
            print(f"ASTERISM_PROVIDER_CLASS_COUNT={len(provider_classes)}")
            print(f"ASTERISM_PROVIDER_RESOURCE_COUNT={len(provider_resources)}")
            print(f"ASTERISM_SPELL_CLASS_COUNT={len(spell_classes)}")
            for n in spell_classes:
                print(f"ASTERISM_SPELL_CLASS={n}")

            print(f"ASTERISM_EXPECTED_REGISTERED_CLASS_REF_COUNT={len(present_refs)}")
            print(f"ASTERISM_MISSING_REGISTERED_CLASS_REF_COUNT={len(missing_refs)}")
            for n in missing_refs:
                print(f"ASTERISM_MISSING_REGISTERED_CLASS_REF={n}")
            print(f"ASTERISM_TRAILBLAZE_REGISTRY_REF={'true' if trailblaze_ref else 'false'}")

            for spell_id in EXPECTED_IDS:
                print(f"ASTERISM_SPELL_ID_CLASS_HIT={spell_id}|{id_hits[spell_id]}")

            print(f"ASTERISM_HOST_OVERRIDE_RESOURCE_COUNT={len(override_resources)}")
            for n in override_resources:
                print(f"ASTERISM_HOST_OVERRIDE_RESOURCE={n}")
            print(f"ASTERISM_GATEWAY_OVERRIDE_RESOURCE_COUNT={len(gateway_override_resources)}")
            print(f"ASTERISM_ASTROMANCER_LOOT_RESOURCE={'true' if astromancer_loot else 'false'}")
            print("ASTERISM_DEPENDENCY_MOD_IDS=" + ",".join(dep_ids))

            if len(present_refs) != 11 or missing_refs:
                raise RuntimeError("exact binary registry class does not reference all 11 expected registered spell classes")
            if trailblaze_ref:
                raise RuntimeError("TrailblazeSpell unexpectedly referenced by exact binary registry class")
            if any(id_hits[x] == 0 for x in EXPECTED_IDS):
                raise RuntimeError("one or more expected spell IDs are absent from provider classfile constants")
            if gateway_override_resources:
                raise RuntimeError("packaged Astral Gateway host override resource exists; manual review required")
            if not astromancer_loot:
                raise RuntimeError("expected Astromancer loot resource missing")

        javap = subprocess.run(
            ["javap", "-classpath", str(jar), "-p", GATEWAY_CLASS],
            check=True, text=True, capture_output=True
        ).stdout
        methods = [line.strip() for line in javap.splitlines() if "(" in line and ")" in line]
        forbidden = [
            line for line in methods
            if re.search(r"\b(allowLooting|allowCrafting|isEnabled|canBeCraftedBy)\s*\(", line)
        ]
        print(f"ASTERISM_GATEWAY_DECLARED_METHOD_COUNT={len(methods)}")
        for line in forbidden:
            print(f"ASTERISM_GATEWAY_HOST_GATE_OVERRIDE={line}")
        print(f"ASTERISM_GATEWAY_HOST_GATE_OVERRIDE_COUNT={len(forbidden)}")
        if forbidden:
            raise RuntimeError("AstralGatewaySpell declares a host eligibility override; manual review required")

        print("ASTERISM_EXACT_REGISTRY_AND_OVERRIDE_AUDIT=true")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ASTERISM_AUDIT_ERROR={type(exc).__name__}: {exc}", file=sys.stderr)
        raise
