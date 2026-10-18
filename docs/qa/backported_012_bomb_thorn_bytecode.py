#!/usr/bin/env python3
"""Exact-hash Backported Spellbooks 0.1.2 Sulfur Bomb/Pale Thorn bounded methods.

Fail-closed proof of selected publisher classfile operands and callsite order.
Not JVM control-flow verification, a real combat experiment, or a public
provider integration hook. No third-party code is copied into the runtime.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import unittest

from backported_012_perk_consumer_bytecode import hash_and_zip, javap, unique

CLASSES = {
    "bomb_spell": "net.redreaper.backported_spellbooks.spells.nature.SulfurBombSPell",
    "bomb_projectile": "net.redreaper.backported_spellbooks.entities.spell.sulfur_bomb.SulfurBombProjectile",
    "thorn_spell": "net.redreaper.backported_spellbooks.spells.nature.PaleThornSpell",
    "thorn_visual": "net.redreaper.backported_spellbooks.entities.spell.pale_thorn.PaleThornVisualEntity",
}

def sequence(ops, expected, label):
    """Ordered opcode AND resolved-operand markers; gaps allowed, reverse rejected."""
    prev = -1
    pcs = []
    for opcode, marker in expected:
        matching = [pc for pc, op, tail in ops
                    if pc > prev and op == opcode and marker in tail]
        if not matching:
            raise ValueError(f"{label}: expected {opcode}/{marker!r} after PC={prev}")
        prev = matching[0]
        pcs.append(prev)
    return pcs

def n_calls(ops, operand, expected, label):
    pcs = [pc for pc, opcode, tail in ops
           if opcode.startswith("invoke") and operand in tail]
    if len(pcs) != expected:
        raise ValueError(f"{label}: {operand} count={len(pcs)}, expected={expected}")
    return pcs

def probe_bomb(spell, proj):
    radius = unique(spell, "getRadius")
    p_radius = sequence(radius, [
        ("ldc", "float 3.0f"),
        ("invokevirtual", "getEntityPowerMultiplier:"),
        ("fadd", ""),
        ("freturn", "")], "SulfurBomb.getRadius")

    damage = unique(spell, "getDamage")
    p_damage = sequence(damage, [
        ("getfield", "baseSpellPower:"),
        ("invokevirtual", "getEntityPowerMultiplier:"),
        ("fmul", ""),
        ("freturn", "")], "SulfurBomb.getDamage")

    aoe = unique(spell, "getAOEDamage")
    p_aoe = sequence(aoe, [
        ("invokevirtual", "getSpellPower:"),
        ("ldc", "float 0.185f"),
        ("fmul", ""),
        ("freturn", "")], "SulfurBomb.getAOEDamage")

    hit = unique(proj, "onHitEntity")
    p_hit = sequence(hit, [
        ("getfield", "Level.isClientSide:"),
        ("ifne", ""),
        ("invokevirtual", "createFireField:"),
        ("invokevirtual", "impactParticles:"),
        ("invokevirtual", "getExplosionRadius:"),
        ("invokevirtual", "AABB.inflate:"),
        ("invokevirtual", "Level.getEntities:"),
        ("invokestatic", "Utils.raycastForBlock:"),
        ("invokevirtual", "Entity.distanceToSqr:"),
        ("dcmpg", ""),
        ("ifge", ""),
        ("invokevirtual", "canHitEntity:"),
        ("invokestatic", "Utils.hasLineOfSight:"),
        ("ddiv", ""),
        ("dsub", ""),
        ("getfield", "Field damage:"),
        ("dmul", ""),
        ("invokestatic", "DamageSources.applyDamage:"),
        ("getstatic", "MobEffects.WITHER:"),
        ("sipush", "200"),
        ("invokevirtual", "LivingEntity.addEffect:"),
        ("getstatic", "MobEffects.CONFUSION:"),
        ("sipush", "200"),
        ("invokevirtual", "LivingEntity.addEffect:"),
        ("invokevirtual", "discard:")], "SulfurBomb.onHitEntity")
    if n_calls(hit, "DamageSources.applyDamage:", 1, "bomb impact") != [p_hit[17]]:
        raise ValueError("SulfurBomb.onHitEntity has unexpected damage call")
    if n_calls(hit, "createFireField:", 1, "bomb impact cloud") != [p_hit[2]]:
        raise ValueError("SulfurBomb.onHitEntity has unexpected cloud call")
    if not any(op == "checkcast" and "LivingEntity" in tail
               for pc, op, tail in hit if p_hit[17] < pc < p_hit[18]):
        raise ValueError("SulfurBomb.onHitEntity: post-damage LivingEntity cast absent")
    # Entity candidates are broad; the class cast below is a QA RISK, not
    # proof of ClassCastException on the game's real canHitEntity candidates.

    block = unique(proj, "onHitBlock")
    p_block = sequence(block, [
        ("invokevirtual", "createFireField:"),
        ("getfield", "Field bounces:"),
        ("iconst_1", ""),
        ("putfield", "Field bounces:"),
        ("iconst_3", ""),
        ("if_icmplt", ""),
        ("invokevirtual", "discard:")], "SulfurBomb.onHitBlock")
    n_calls(block, "setDeltaMovement:", 3, "bomb block bounce branches")

    cloud = unique(proj, "createFireField")
    p_cloud = sequence(cloud, [
        ("getfield", "Level.isClientSide:"),
        ("ifne", ""),
        ("new", "SulfurGasCloud"),
        ("sipush", "200"),
        ("invokevirtual", "SulfurGasCloud.setDuration:"),
        ("getfield", "Field aoeDamage:"),
        ("invokevirtual", "SulfurGasCloud.setDamage:"),
        ("invokevirtual", "SulfurGasCloud.setRadius:"),
        ("invokevirtual", "Level.addFreshEntity:")], "SulfurBomb.createFireField")
    if n_calls(cloud, "Level.addFreshEntity:", 1, "cloud spawn") != [p_cloud[-1]]:
        raise ValueError("SulfurBomb: unexpected extra cloud spawn")
    speed = unique(proj, "getSpeed")
    p_speed = sequence(speed, [
        ("ldc", "float 1.15f"), ("freturn", "")
    ], "SulfurBombProjectile.getSpeed")
    return {
        "radius": "3.0f + getEntityPowerMultiplier(caster)",
        "direct_damage_input": "baseSpellPower * getEntityPowerMultiplier(caster)",
        "cloud_damage_input": "getSpellPower(level,caster) * 0.185f",
        "projectile_speed_declaration": "1.15f; host projectile motion NOT VERIFIED",
        "impact": "server-only; cloud first; AABB.inflate(radius) candidates; square-distance and canHitEntity and LOS filters; damage * (1 - distanceSq/radiusSq); then 200-tick Wither/Confusion callsites",
        "impact_living_cast_after_apply_damage": "present; nonliving applicability NOT VERIFIED",
        "block": "cloud on collision; three velocity reflection branches; discard on third bounce",
        "cloud": "new SulfurGasCloud; duration 200 ticks; setDamage(aoeDamage); setRadius(explosionRadius); addFreshEntity",
        "pcs": {"radius":p_radius, "direct_damage":p_damage,
                "cloud_damage":p_aoe, "impact":p_hit, "bounce":p_block,
                "cloud_spawn":p_cloud, "declared_speed":p_speed},
    }

def probe_thorn(spell, visual):
    rng = unique(spell, "getRange")
    p_range = sequence(rng, [("ldc_w", "float 15.0f"), ("freturn", "")],
                       "PaleThorn.getRange")
    duration = unique(spell, "getDuration")
    p_duration = sequence(duration, [
        ("invokevirtual", "getSpellPower:"),
        ("ldc_w", "float 100.0f"),
        ("fmul", ""),
        ("f2i", ""),
        ("ireturn", "")], "PaleThorn.getDuration")
    damage = unique(spell, "getDamage")
    p_damage = sequence(damage, [
        ("ifnonnull", ""),
        ("invokevirtual", "getSpellPower:"),
        ("ldc_w", "float 1.5f"),
        ("fmul", ""),
        ("freturn", ""),
        ("getstatic", "AttributeRegistry.NATURE_SPELL_POWER:"),
        ("invokevirtual", "LivingEntity.getAttributeValue:"),
        ("getstatic", "AttributeRegistry.ELDRITCH_SPELL_POWER:"),
        ("invokevirtual", "LivingEntity.getAttributeValue:"),
        ("ldc2_w", "double 5.0d"),
        ("ldc2_w", "double 0.4000000059604645d"),
        ("ldc2_w", "double 0.5d"),
        ("ldc2_w", "double 0.5d"),
        ("dadd", ""),
        ("dmul", ""),
        ("dadd", ""),
        ("d2f", ""),
        ("freturn", "")], "PaleThorn.getDamage")
    # This is a bounded source interpretation of the arithmetic. The
    # constants and attribute field refs themselves are from the exact JAR.
    cast = unique(spell, "onCast")
    p_cast = sequence(cast, [
        ("invokestatic", "getRange:"),
        ("iconst_0", ""),
        ("ldc", "float 0.15f"),
        ("invokestatic", "Utils.raycastForEntity:"),
        ("new", "PaleThornVisualEntity"),
        ("invokevirtual", "Level.addFreshEntity:"),
        ("getstatic", "HitResult$Type.ENTITY:"),
        ("if_acmpne", ""),
        ("invokevirtual", "getDuration:"),
        ("invokevirtual", "getDamage:"),
        ("invokestatic", "DamageSources.applyDamage:"),
        ("getstatic", "ModMobEffects.PARANOIA:"),
        ("invokespecial", "MobEffectInstance"),
        ("invokevirtual", "LivingEntity.addEffect:"),
        ("getstatic", "HitResult$Type.BLOCK:"),
        ("invokespecial", "AbstractPaleSpells.onCast:")],
        "PaleThorn.onCast")
    # A direct manual friendly-fire call is not found, but Utils/DamageSources
    # may implement their own; no false claim of unsafe PvP.
    if any("DamageSources.isFriendlyFireBetween:" in tail for _, _, tail in cast):
        raise ValueError("PaleThorn: unexpected direct friendly-fire check changed")
    if n_calls(cast, "DamageSources.applyDamage:", 1, "thorn direct damage") != [p_cast[10]]:
        raise ValueError("PaleThorn: unexpected count of damage calls")
    life = unique(visual, "tick")
    p_life = sequence(life, [
        ("bipush", "30"), ("if_icmple", ""),
        ("invokevirtual", "discard:")], "PaleThornVisualEntity.tick")
    return {
        "range": "15.0f constant",
        "raycast": "Utils.raycastForEntity with boolean false and tolerance 0.15f",
        "duration": "(int)(getSpellPower(level,caster) * 100.0f) ticks",
        "damage_nonnull_caster": "source-interpreted 5 + (float)0.4 * spellPower * (0.5 * NatureSpellPower + 0.5 * EldritchSpellPower)",
        "damage_null_caster": "getSpellPower(level,null) * 1.5f",
        "cast_branch": "raycast then separate VFX spawn; ENTITY guard for one DamageSources.applyDamage and PARANOIA effect; BLOCK branch particles",
        "vfx_lifetime_condition": "discard when tickCount > 30 in tick method; not status duration",
        "friendly_fire": "no direct DamageSources.isFriendlyFireBetween in onCast; host utilities unexamined",
        "pcs": {"range":p_range, "effect_duration":p_duration,
                "damage":p_damage, "cast":p_cast, "vfx_lifetime":p_life},
    }

def analyze(dis):
    if set(dis) != set(CLASSES):
        raise ValueError("REQUIRED_CLASS_SET_MISSING")
    return {
        "status": "PASS_BACKPORTED_012_BOMB_THORN_BOUNDED_BYTECODE",
        "evidence_class": "EXACT_PUBLISHER_BOUND_METHOD_OPERANDS",
        "sulfur_bomb": probe_bomb(dis["bomb_spell"], dis["bomb_projectile"]),
        "pale_thorn": probe_thorn(dis["thorn_spell"], dis["thorn_visual"]),
        "limitations": [
            "No live damage, host projectile physics, server/player or mana/cooldown settlement.",
            "No general CFG/dataflow proof, only named method opcode/reference sequences.",
            "The presence of projectile cloud/damage paths is not proof of exactly one hit or proc.",
            "No provider-native extension hook or RPG Skill Tree/Black Arcana adapter proven."
        ]
    }

class Tests(unittest.TestCase):
    @staticmethod
    def fixture(*ops):
        return [(i*3, op, marker) for i, (op,marker) in enumerate(ops)]

    def test_forward_order(self):
        x=self.fixture(("ldc","float 3.0f"), ("invokevirtual","getEntityPowerMultiplier:"),
                       ("fadd",""), ("freturn",""))
        self.assertEqual(sequence(x, [("ldc","float 3.0f"),
                                       ("invokevirtual","getEntityPowerMultiplier:"),
                                       ("fadd",""),("freturn","")],"radius"),[0,3,6,9])

    def test_reordered_geometry_fails(self):
        x=self.fixture(("invokevirtual","AABB.inflate:"),
                       ("invokevirtual","getExplosionRadius:"))
        with self.assertRaisesRegex(ValueError,"expected"):
            sequence(x,[("invokevirtual","getExplosionRadius:"),
                        ("invokevirtual","AABB.inflate:")],"geometry")

    def test_coeff_drift_fails(self):
        x=self.fixture(("ldc","float 0.18f"),("fmul",""))
        with self.assertRaisesRegex(ValueError,"expected"):
            sequence(x,[("ldc","float 0.185f"),("fmul","")],"coeff")

    def test_radius_drift_fails(self):
        with self.assertRaisesRegex(ValueError,"expected"):
            sequence(self.fixture(("ldc","float 4.0f")),
                     [("ldc","float 3.0f")],"radius")

    def test_effect_ticks_drift_fails(self):
        with self.assertRaisesRegex(ValueError,"expected"):
            sequence(self.fixture(("sipush","180")), [("sipush","200")],"effect ticks")

    def test_thorn_range_drift_fails(self):
        with self.assertRaisesRegex(ValueError,"expected"):
            sequence(self.fixture(("ldc_w","float 14.0f")),
                     [("ldc_w","float 15.0f")],"range")

    def test_thorn_attribute_drift_fails(self):
        with self.assertRaisesRegex(ValueError,"expected"):
            sequence(self.fixture(("getstatic","AttributeRegistry.ARCANE_SPELL_POWER:")),
                     [("getstatic","AttributeRegistry.ELDRITCH_SPELL_POWER:")],"attr")

    def test_damage_call_duplicate_fails(self):
        with self.assertRaisesRegex(ValueError,"count"):
            n_calls(self.fixture(("invokestatic","DamageSources.applyDamage:"),
                                 ("invokestatic","DamageSources.applyDamage:")),
                    "DamageSources.applyDamage:",1,"hit")

    def test_method_missing_fails(self):
        with self.assertRaisesRegex(ValueError,"METHOD_MISSING_OR_AMBIGUOUS"):
            unique("class Empty{}", "onHitEntity")

    def test_class_set_fails(self):
        with self.assertRaisesRegex(ValueError,"REQUIRED_CLASS_SET_MISSING"):
            analyze({})

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--self-test",action="store_true")
    parser.add_argument("--jar",type=Path)
    parser.add_argument("--output",type=Path)
    a=parser.parse_args()
    if a.self_test:
        result=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        return 0 if result.wasSuccessful() else 1
    if not a.jar or not a.output:
        parser.error("--jar and --output required")
    try:
        sha1=hash_and_zip(a.jar)
        report=analyze({key:javap(a.jar,clazz) for key,clazz in CLASSES.items()})
        report["publisher_sha1"]=sha1
        report["deviations"]=[]
    except (OSError, ValueError, subprocess.CalledProcessError) as e:
        report={"status":"FAIL_CLOSED", "deviations":[str(e)]}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["status"],"deviations":report["deviations"]}))
    return 0 if report["status"]=="PASS_BACKPORTED_012_BOMB_THORN_BOUNDED_BYTECODE" else 2

if __name__=="__main__":
    sys.exit(main())
