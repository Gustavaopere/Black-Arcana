# Monsters & Spellbooks 0.0.16.3 — publisher SHA-exact binary proof gate

State: **🟡 independent Java21 JAR audit in progress; do not promote `COUNTED_RELEASE_BOUNDED` before PASS.**

## Authority

- Physical sibling modlist: `neoforge-rpg-skilltree@9e6436edb0049a8dcc4e47165db0f6850e5efa68`, position **#406**.
- File `monstersspellbooks-0.0.16.3.jar`; mod ID `monstersspellbooks`; SHA-1 `b3aa89fd081bf4bfaf8d0f4380bcdc393c66ab0e`.
- Official [CurseForge project 1428928, file 8788560](https://www.curseforge.com/minecraft/mc-mods/monsters-spellbooks-iss/files/8788560), NeoForge 1.21.1, 2026-09-01. The workflow verifies publisher bytes equal the physical SHA-1 before inspecting any class.
- Contemporaneous public source `RedReaper28/Monsters-Spellbooks-1.21.1@1ab9b72af2ea44c3c8b816e665d06531ea44ddc2` shows **98** `ModSpellRegistry` statements, but `gradle.properties` still reports **0.0.14**, **not exact 0.0.16.3**. This checkpoint is comparative source evidence only, not an exact release-build authority.
- Full expected `SOURCE_CONSTANT → source class` and family table: [SPELL-CATALOG.md](../wiki/modpack-catalog/providers/✅-monsters-spellbooks/SPELL-CATALOG.md). All 98 semantic roots are **already counted** under `COUNTED_RELEASE_BOUNDED`.

## What the independent SHA-gated auditor is required to prove

1. JAR exact name, regular file, physical SHA-1 match, unique ZIP entries, NeoForge declared mod ID and presence of compiled `net.redreaper.monsterspellbooks.init.ModSpellRegistry`.
2. Exactly **98** unique static `Supplier<AbstractSpell>` fields, each with the direct `new → dup → <init> → registerSpell → putstatic` compiled flow.
3. Every field's actual compiled implementation class agrees with the contemporaneous source inventory. Do not infer spell IDs from constant names.
4. Each compiled spell class has a unique constructor-written literal `monstersspellbooks:<spellId>` read back through its own `getSpellResource` getter; **98 unique resource IDs**, no duplicate.
5. The installed `ModSpellSchools` registry is inspected separately as **diagnostic only**, without promoting the source-head `aero` or `necro` SchoolType to an active, loaded runtime school.

Any mismatch between source and publisher, missing class, school drift, or incompatible bytecode **must fail closed** and be reconciled from compiled evidence; source row count alone is insufficient. This is clean-room, read-only disassembly; no original JAR/implementation/assets are committed.

## No runtime claims

The proof does **not** establish actually loaded `DeferredRegister`, per-spell configuration, spellbook accessibility, mana/cooldown consumption, server tick effects, damage ownership, client/server multiplayer, loot acquisition or Survival. Native Iron's Spells 'n Spellbooks remains casting/cost/cooldown authority. Black Arcana does not duplicate the provider's runtime; RPG Skill Tree remains sibling progression only through proved contracts. Stage 06.05 🟡 and Stage09 physical acceptance ⚠️.

Until exact publisher bytecode and consumer-ledger tests pass: **30/39** exact, **9/39** conditional, strict minima **1,856 global / 1,854 in-scope**.
