#!/usr/bin/env python3
"""Read-only, SHA-pinned Galena Gauntlet damage/dig-speed JVM subcontracts.

Observational only: does not certify ACCompat, engine acceptance, physical QA or hooks.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

REPORT_SHA = 'c91a48f9892be09c4ab951c8083703b0c5ffbb026fc43e7d808c2033dde8bba9'
PUBLISHER_SHA = '36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c'
CLASS = 'com/github/alexmodguy/alexscaves/server/entity/item/MagneticWeaponEntity'
CLASS_SHA = 'a26794c9eba89c554e812078886beda6129d5298219f685f6d0e2be315fbf071'
# name: (descriptor, Code SHA-256, canonical instruction SHA-256, count)
SEALS = {
 'getDamageForItem': ('(Lnet/minecraft/world/item/ItemStack;)D', '7cea38edb8811930a46ffea933d4065c53a26d68caa11d1b3a207c75ad42151e', '8b1271d55ab393ed1e3d6ac10116045048521afb94ee8ee21141b55bd325969b', 3),
 'damageItem': ('(I)V', 'aeac8abe1829f866055bf73ad19658a78696a3fa3c434c0dfe1a27654a2d99ad', '26c2f76584dc4fa9e4192adda507ed89b47be3ea482088270436bad30f5126d1', 37),
 'hurtEntity': ('(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/Entity;)V', 'ab23b6e6f56147f5c29cf4fa2cc1677db25a56f1936d4be2e3e6bf31fcc9fd1a', 'aa8e9cce394f23845c672ed73837010f51f067453503dd2f7fd697eaeda29d35', 141),
 'getDigSpeed': ('(Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/level/block/state/BlockState;Lnet/minecraft/core/BlockPos;)F', '3261a23502a9fd8a20ee20b4dd17b1451870eda688117131e4b4874c2ada8c1b', 'edd233b5cee732c5cccc5f935cd96748940b1a036c20423d33c375973ebf4470', 80),
}
# Format: JVM offset, opcode, fragment of symbol or operand ("_" = no fragment).
PIVOTS = {
 'getDamageForItem': '''1 invokestatic ACCompat.attackDamageBonus''',
 'damageItem': '''1 invokevirtual getController:
8 instanceof LivingEntity
21 instanceof Player
33 invokevirtual Player.isCreative:
36 ifne 80
40 invokevirtual getItemStack:
47 invokevirtual isDamageableItem:
50 ifeq 80
55 iload_1 _
57 invokestatic ACCompat.hurtAndBreakUsedHand:
62 invokevirtual getDamageValue:
67 invokevirtual getMaxDamage:
70 if_icmplt 80
77 invokevirtual remove:''',
 'hurtEntity': '''1 invokevirtual getItemStack:
6 getstatic ATTACK_DAMAGE
9 invokevirtual getAttributeValue:
15 invokevirtual getDamageForItem:
19 fadd _
23 getstatic ATTACK_KNOCKBACK
26 invokevirtual getAttributeValue:
33 instanceof LivingEntity
46 invokestatic ACCompat.damageBonus:
49 fadd _
55 getstatic Enchantments.KNOCKBACK
58 invokestatic ACCompat.enchantLevelOn:
62 fadd _
66 getstatic FIRE_ASPECT
69 invokestatic ACCompat.enchantLevel:
76 ifle 88
83 imul _
85 invokevirtual igniteForSeconds:
94 invokevirtual DamageSources.mobAttack:
99 invokestatic ACCompat.hurt:
102 ifeq 194
115 invokestatic ACCompat.postAttackEffects:
120 invokevirtual damageItem:
127 ifle 194
131 instanceof LivingEntity
143 ldc_w 0.5f
173 invokestatic ACCompat.knockback:
181 ldc2_w 0.6d
188 invokevirtual Vec3.multiply:
191 invokevirtual setDeltaMovement:
195 invokevirtual isOnFire:
198 ifeq 208
202 ldc_w 5.0f
205 invokevirtual igniteForSeconds:
209 instanceof Player
222 instanceof LivingEntity
239 invokevirtual ItemStack.hurtEnemy:
247 invokevirtual setLastHurtByPlayer:
252 invokevirtual LivingEntity.getHealth:
257 ifgt 281
263 invokevirtual Player.distanceTo:
266 ldc_w 19.5f
270 iflt 281
273 getstatic KILL_MOB_WITH_GALENA_GAUNTLET
278 invokevirtual triggerForEntity:''',
 'getDigSpeed': '''9 invokevirtual ItemStack.getDestroySpeed:
18 ifle 32
26 invokestatic ACCompat.miningEfficiencyBonus:
29 fadd _
33 invokestatic MobEffectUtil.hasDigSpeed:
36 ifeq 57
43 invokestatic getDigSpeedAmplification:
49 ldc_w 0.2f
53 fadd _
54 fmul _
58 getstatic DIG_SLOWDOWN
61 invokevirtual Player.hasEffect:
64 ifeq 144
71 invokevirtual Player.getEffect:
74 invokevirtual getAmplifier:
77 tableswitch 0 to 3
108 ldc_w 0.3f
116 ldc_w 0.09f
124 ldc_w 0.0027f
132 ldc_w 8.1E-4f
141 fmul _
145 getstatic FluidTags.WATER
148 invokevirtual isEyeInFluid:
157 invokestatic ACCompat.submergedMiningFactor:
160 fmul _
164 invokevirtual onGround:
172 ldc_w 5.0f
175 fdiv _
183 invokestatic EventHooks.getBreakSpeed:
190 freturn _''',
}

def need(ok: bool, msg: str) -> None:
 if not ok:
  raise ValueError(msg)

def no_duplicate_keys(pairs):
 out = {}
 for k, v in pairs:
  need(k not in out, 'duplicate JSON key: ' + k)
  out[k] = v
 return out

def digest(data: bytes) -> str:
 return hashlib.sha256(data).hexdigest()

def canonical(data) -> str:
 return digest((json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf8'))

def pivots_for(name):
 for line in PIVOTS[name].splitlines():
  offset, opcode, fragment = line.split(' ', 2)
  yield int(offset), opcode, fragment

def check_pivots(methods):
 checked = 0
 for name in SEALS:
  ins = methods[name]['instructions']
  by_offset = {row['offset']: row for row in ins}
  need(len(by_offset) == len(ins), name + ': duplicate instruction offsets')
  for offset, opcode, fragment in pivots_for(name):
   need(offset in by_offset, name + f': missing JVM pivot {offset}')
   row = by_offset[offset]
   need(row['opcode'] == opcode, name + f': JVM opcode drift @{offset}')
   if fragment != '_':
    combined = str(row.get('operand', '')) + ' ' + str(row.get('symbol', ''))
    need(fragment in combined, name + f': JVM operand/symbol drift @{offset}')
   checked += 1
 need(checked == 90, f'JVM pivot count drift: {checked}')
 return checked

def validate(raw: bytes, *, enforce_seals: bool = True):
 need(0 < len(raw) <= 2_100_000, 'bounded report size')
 if enforce_seals:
  need(len(raw) == 1_780_492 and digest(raw) == REPORT_SHA, 'exact report SHA/size drift')
 r = json.loads(raw, object_pairs_hook=no_duplicate_keys)
 need(r['scope'] == 'GALENA_GAUNTLET_FULL_CLASS_DISCOVERY_NOT_CERTIFIED', 'discovery scope drift')
 need(r['schema_version'] == 1 and r['mutation'] == 'NO_MUTATION' and
      r['physical_qa'] == 'NOT_TESTED' and r['mutating_hook'] == 'NOT_VERIFIED' and
      r['provider_universe_closed'] is False, 'non-mutating scope drift')
 a = r['artifact']
 need(a['sha256'] == PUBLISHER_SHA and a['size_bytes'] == 75279314 and
      a['version'] == '1.0.10' and a['installed_dump_parity'] == 'NOT_VERIFIED',
      'publisher identity drift')
 need(r['entity_native']['class_entries_scanned'] == 1555, 'class census drift')
 targets = r['entity_native']['targets']
 need(set(targets) == {CLASS} and targets[CLASS]['class_sha256'] == CLASS_SHA,
      'entity class SHA/identity drift')
 all_methods = targets[CLASS]['methods']
 need(len(all_methods) == 24, 'native method census drift')
 methods = {m['declaration']['name']: m for m in all_methods}
 need(len(methods) == len(all_methods), 'duplicate native method name')
 for name, (descriptor, code_sha, instruction_sha, count) in SEALS.items():
  need(name in methods, 'missing method ' + name)
  m = methods[name]
  need(m['declaration']['descriptor'] == descriptor, name + ': descriptor drift')
  if enforce_seals:
   need(m['declaration']['code_sha256'] == code_sha, name + ': Code SHA drift')
   need(m['instruction_sha256'] == instruction_sha, name + ': instruction SHA drift')
  need(m['instruction_count'] == len(m['instructions']) == count,
       name + ': instruction count drift')
  if enforce_seals:
   need(canonical(m['instructions']) == instruction_sha,
        name + ': canonical instruction SHA mismatch')
 count = check_pivots(methods)
 return count

def negative_tests(raw: bytes):
 original = json.loads(raw)
 target = original['entity_native']['targets'][CLASS]['methods']
 attacks = [('hurtEntity', x) for x in (15,46,69,85,94,99,102,115,120,143,173,205,239,247,273)]
 attacks += [('damageItem',57), ('getDigSpeed',183), ('getDamageForItem',1)]
 for name, offset in attacks:
  report = copy.deepcopy(original)
  methods = {m['declaration']['name']:m for m in report['entity_native']['targets'][CLASS]['methods']}
  row = next(i for i in methods[name]['instructions'] if i['offset'] == offset)
  row['opcode'] = 'nop'
  try:
   validate(json.dumps(report, ensure_ascii=False).encode('utf8'), enforce_seals=False)
  except ValueError as exc:
   need('JVM opcode drift' in str(exc), f'wrong rejection for {name}@{offset}: {exc}')
  else:
   raise AssertionError(f'forged JVM opcode accepted: {name}@{offset}')
 # A branch-target forgery must fail even with all cryptographic gates bypassed.
 report = copy.deepcopy(original)
 methods = {m['declaration']['name']:m for m in report['entity_native']['targets'][CLASS]['methods']}
 row = next(i for i in methods['hurtEntity']['instructions'] if i['offset'] == 102)
 row['operand'] = '0'
 try:
  validate(json.dumps(report, ensure_ascii=False).encode('utf8'), enforce_seals=False)
 except ValueError as exc:
  need('JVM operand/symbol drift' in str(exc), f'wrong branch rejection: {exc}')
 else:
  raise AssertionError('forged branch target accepted')
 print('PASS: 18 independent forged opcodes + 1 forged branch target rejected')

if __name__ == '__main__':
 p = argparse.ArgumentParser()
 p.add_argument('--report', type=Path, required=True)
 p.add_argument('--adversarial', action='store_true')
 args = p.parse_args()
 original = args.report.read_bytes()
 n = validate(original)
 print(f'PASS: 4 exact native JVM methods, {n} pinned causal pivots; NO_MUTATION')
 if args.adversarial:
  negative_tests(original)
