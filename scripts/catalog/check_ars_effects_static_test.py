#!/usr/bin/env python3
"""Fail-closed regressions for 28 Ars Nouveau 5.13.1 Effect static dossiers.

No code execution, loaded provider API, runtime effect or perk behavior is
implied by these tests; exact release binary registration remains separately
verified by the Ars 109-ID workflow.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ARS = REPO / "wiki/modpack-catalog/providers/✅-ars-nouveau"
MANIFEST = REPO / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
GATE = ARS / "EFFECT-STATIC-FIRST-FIVE-5.13.1.md"
RELEASE = "5.13.1"
SOURCE = "baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157"
SHA1 = "02782d071ee5fab3b5c4b8ced67b7e1748277dfd"
EVIDENCE = frozenset({"identity", "behavior", "parameters", "targeting",
                      "costs", "integration", "validation"})
CASES = {
    "heal": ("glyph_heal", "EffectHeal",
             ("causeFoodExhaustion(2.5f)", "Player", "DamageTypes.MAGIC", "attemptDamage")),
    "slowfall": ("glyph_slowfall", "EffectSlowfall",
                 ("MobEffects.SLOW_FALLING", "IPotionEffect", "30", "8")),
    "glide": ("glyph_glide", "EffectGlide",
              ("GlidingPerk", "ModPotions.GLIDE_EFFECT", "180", "120", "30/8")),
    "sense-magic": ("glyph_sense_magic", "EffectSenseMagic",
                    ("IPedestalMachine", "MAGIC_FIND_EFFECT", "75", "60")),
    "knockback": ("glyph_gust", "EffectKnockback",
                  ("KNOCKBACK_RESISTANCE", "EnchantedFallingBlock", "Sensitive", "Extract")),
    "harm": ("glyph_harm", "EffectHarm",
             ("MobEffects.POISON", "IDamageEffect.attemptDamage", "Duration Down")),
    "explosion": ("glyph_explosion", "EffectExplosion",
                  ("ANExplosion", "onExplosionStart", "DESTROY_WITH_DECAY", "4096")),
    "lightning": ("glyph_lightning", "EffectLightning",
                  ("LightningEntity", "EntityStruckByLightningEvent", "wetBonus", "EnergyStorage")),
    "freeze": ("glyph_freeze", "EffectFreeze",
               ("calcAOEBlocks", "Frosted Ice", "ShapersFocus", "Sensitive")),
    "ignite": ("glyph_ignite", "EffectIgnite",
               ("setRemainingFireTicks", "MAGIC_FIRE", "destroyRespectsClaim")),
    "blink": ("glyph_blink", "EffectBlink",
              ("TELEPORTING_NOT_SUPPORTED", "blinkForward", "getForward", "WarpScrollData")),
    "leap": ("glyph_leap", "EffectLeap",
             ("force_ground", "setDeltaMovement", "RotatingTurretTile", "Sensitive")),
    "launch": ("glyph_launch", "EffectLaunch",
               ("setDeltaMovement", "0,48", "ShapersFocus", "Sensitive")),
    "pull": ("glyph_pull", "EffectPull",
             ("ParticleUtil.inRange", "shooter.position", "canBlockBeHarvested", "Sensitive")),
    "snare": ("glyph_snare", "EffectSnare",
              ("groundBlock(true)", "SNARE_EFFECT", "IPotionEffect", "setDeltaMovement(0,0,0)")),
    "invisibility": ("glyph_invisibility", "EffectInvisibility",
                     ("MobEffects.INVISIBILITY", "applyConfigPotion", "false", "30", "8")),
    "wither": ("glyph_wither", "EffectWither",
               ("MobEffects.WITHER", "IPotionEffect", "Amplify", "30", "8")),
    "hex": ("glyph_hex", "EffectHex",
            ("ModPotions.HEX_EFFECT", "getBookDescription", "IPotionEffect", "4 Amplify")),
    "bounce": ("glyph_bounce", "EffectBounce",
               ("BOUNCE_EFFECT", "getPotionAugments", "setDeltaMovement")),
    "dispel": ("glyph_dispel", "EffectDispel",
               ("DispelEvent.Pre", "DispelEvent.Post", "IDispellable", "DISPEL_DENY", "DISPEL_ALLOW")),
    "break": ("glyph_break", "EffectBreak",
              ("destroyRespectsClaim", "breakExtraBlock", "CommonHooks.fireBlockBreak",
               "getBaseHarvestLevel", "ShapersFocus")),
    "place-block": ("glyph_place_block", "EffectPlaceBlock",
                    ("BlockEvent.EntityPlaceEvent", "InventoryManager",
                     "ExtractedStack.returnOrDrop", "UnbiasedDirectionalPlaceContext",
                     "isInWorldBounds")),
    "conjure-water": ("glyph_conjure_water", "EffectConjureWater",
                      ("SOAKED_EFFECT", "clearFire", "destroyRespectsClaim",
                       "setBlockAndUpdate", "POTION_TIME")),
    "evaporate": ("glyph_evaporate", "EffectEvaporate",
                  ("SimpleWaterloggedBlock", "LiquidBlock", "Direction.values()",
                   "WATERLOGGED", "ShapersFocus")),
    "exchange": ("glyph_exchange", "EffectExchange",
                  ("EventHooks.onEnderTeleport", "firstBlock",
                   "replaceAndReturnOrDrop", "BlockUtil.breakExtraBlock", "stack.shrink(1)")),
    "crush": ("glyph_crush", "EffectCrush",
               ("DamageTypesRegistry.CRUSH", "CrushRecipe",
                "maxItemCrush", "skip_block_place", "getRolledOutputs")),
    "smelt": ("glyph_smelt", "EffectSmelt",
               ("destroyBlockSafely", "SMOKING", "BLASTING",
                "maxItemSmelt", "addFreshEntity")),
    "craft": ("glyph_craft", "EffectCraft",
               ("CustomWorkbench", "CraftingMenu", "stillValid(Player)",
                "SimpleMenuProvider", "isNotFakePlayer")),
}


class StaticContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cert = json.loads(MANIFEST.read_text(encoding="utf-8"))["objects"]
        cls.index = (ARS / "glyphs/effects/INDEX.md").read_text(encoding="utf-8")
        cls.root_index = (REPO / "wiki/modpack-catalog/providers/INDEX.md").read_text(
            encoding="utf-8"
        )

    def test_twenty_eight_distinct_effect_identities(self):
        self.assertEqual(28, len(CASES))
        self.assertEqual(28, len({v[0] for v in CASES.values()}))
        for slug, (identity, class_name, facts) in CASES.items():
            with self.subTest(effect=slug):
                card = (ARS / "glyphs/effects" / (slug + ".md")).read_text(
                    encoding="utf-8")
                self.assertIn("ars_nouveau:" + identity, card)
                self.assertIn(class_name, card)
                for fact in facts:
                    self.assertIn(fact, card)

    def test_certifications_are_static_and_runtime_fail_closed(self):
        for name in CASES:
            with self.subTest(effect=name):
                key = "✅-ars-nouveau/glyphs/effects/" + name + ".md"
                data = self.cert[key]
                self.assertEqual("COMPLETE_PERK_READY", data["status"])
                self.assertEqual("STATIC_TECHNICAL_CATALOG_ONLY", data["claim_scope"])
                self.assertEqual("PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY",
                                 data["evidence_grade"])
                self.assertEqual(SOURCE, data["source_revision"])
                self.assertEqual(RELEASE, data["version"])
                self.assertEqual(SHA1, data["artifact_sha1"])
                self.assertEqual("NOT_VERIFIED", data["mutating_hook"])
                self.assertEqual("NOT_TESTED", data["physical_qa"])
                self.assertEqual(EVIDENCE, set(data["evidence"]))

    def test_twenty_eight_evidence_paths_exist_in_checkout(self):
        for name in CASES:
            cert = self.cert["✅-ars-nouveau/glyphs/effects/" + name + ".md"]
            for field, evidence in cert["evidence"].items():
                with self.subTest(effect=name, field=field):
                    self.assertIsInstance(evidence.get("path"), str)
                    self.assertIsInstance(evidence.get("reason"), str)
                    self.assertGreater(len(evidence["reason"]), 18)
                    self.assertTrue((REPO / evidence["path"]).is_file())

    def test_all_parent_indexes_use_green_only_for_the_twenty_eight(self):
        nested = [ARS / "glyphs/effects/INDEX.md",
                  ARS / "glyphs/INDEX.md", ARS / "INDEX.md"]
        for parent in nested:
            page = parent.read_text(encoding="utf-8")
            for slug in CASES:
                label = slug.replace("-", " ").title()
                with self.subTest(index=parent.name, effect=slug):
                    self.assertIn("| ✅ | " + label + " |", page)

    def test_counter_without_provider_wide_promotion(self):
        effect_count = sum(
            key.startswith("✅-ars-nouveau/glyphs/effects/")
            for key in self.cert
        )
        self.assertGreaterEqual(effect_count, 35)
        self.assertIn(
            f"Homologadas para perks (somente fichas detectadas): {effect_count}/67.",
            self.index,
        )
        # Other Ars families can gain independent certifications without
        # changing the number of Effect cards reviewed by this test suite.
        self.assertIn(
            f"Fichas com contrato técnico estático certificado: {len(self.cert)}/2075.",
            self.root_index,
        )
        self.assertIn("Mods com escopo integral certificado: 0/164.", self.root_index)
        self.assertGreaterEqual(len(self.cert), 53)

    def test_dossier_avoids_unproved_runtime_claims(self):
        page = GATE.read_text(encoding="utf-8")
        for token in ("5/67", SOURCE, SHA1, "NOT_VERIFIED", "NOT_TESTED",
                      "isInvertedHealAndHarm", "canGlide", "75"):
            self.assertIn(token, page)


    def test_damage_world_dossier_keeps_dynamic_consumers_outside_simple_spell(self):
        page = (ARS / "EFFECT-STATIC-DAMAGE-WORLD-FIVE-5.13.1.md").read_text(
            encoding="utf-8")
        for term in ("10/67", "28/2.075", SOURCE, SHA1, "Poison em vez de dano",
                     "ANExplosion", "LightningEntity", "ShapersFocus",
                     "NOT_VERIFIED", "NOT_TESTED"):
            self.assertIn(term, page)
        # Static catalog never certifies gameplay, real QA, or provider-wide completion.
        self.assertNotIn("✅ 164/164", page)

    def test_damage_world_cards_keep_runtime_fail_closed_and_separate_paths(self):
        examples = {
            "harm": ("em vez de", "SpellDamageEvent.Pre"),
            "explosion": ("DESTROY_WITH_DECAY", "onExplosionDetonate"),
            "lightning": ("hitEntities", "restaurar", "SHOCKED_EFFECT"),
            "freeze": ("seis direções", "MOVEMENT_SLOWDOWN"),
            "ignite": ("destroyRespectsClaim", "setRemainingFireTicks"),
        }
        for slug, facts in examples.items():
            with self.subTest(effect=slug):
                card = (ARS / "glyphs/effects" / (slug + ".md")).read_text(
                    encoding="utf-8")
                for fact in facts:
                    self.assertIn(fact, card)
                self.assertIn("mutating_hook=NOT_VERIFIED", card)
                self.assertIn("physical_qa=NOT_TESTED", card)


    def test_mobility_dossier_keeps_separate_vector_and_teleport_paths(self):
        page = (ARS / "EFFECT-STATIC-MOBILITY-CONTROL-FIVE-5.13.1.md").read_text(
            encoding="utf-8")
        for token in ("15/67", "33/2.075", SOURCE, SHA1, "Blink",
                      "Leap", "Launch", "Pull", "Snare",
                      "substitui", "soma", "NOT_VERIFIED", "NOT_TESTED"):
            self.assertIn(token, page)
        self.assertNotIn("✅ 164/164", page)

    def test_mobility_cards_distinguish_mutation_and_applicability(self):
        examples = {
            "blink": ("getForward", "scroll", "canOcclude", "teleportTo"),
            "leap": ("force_ground", "max(0", "RotatingTurretTile", "setDeltaMovement"),
            "launch": ("0,48", "0,8", "setDeltaMovement", "Sensitive"),
            "pull": ("0,05", "shooter.position", "normal da face", "canBlockBeHarvested"),
            "snare": ("groundBlock(true)", "SNARE_EFFECT", "IPotionEffect",
                      "EntityHitResult"),
        }
        for slug, facts in examples.items():
            with self.subTest(effect=slug):
                card = (ARS / "glyphs/effects" / (slug + ".md")).read_text(
                    encoding="utf-8")
                for fact in facts:
                    self.assertIn(fact, card)
                self.assertIn("mutating_hook", card)
                self.assertIn("NOT_VERIFIED", card)
                self.assertIn("NOT_TESTED", card)


    def test_dossier_separates_status_callback_from_real_downstream_behavior(self):
        page = (ARS / "EFFECT-STATIC-STATUS-DISPEL-FIVE-5.13.1.md").read_text(
            encoding="utf-8")
        for term in ("20/67", "38/2075", SOURCE, SHA1, "Invisibility", "Wither",
                     "Hex", "Bounce", "Dispel", "ICancellableEvent",
                     "mutating_hook=NOT_VERIFIED", "physical_qa=NOT_TESTED"):
            self.assertIn(term, page)

    def test_dispel_public_event_is_not_approval_of_spell_mutation(self):
        dispel = (ARS / "glyphs/effects/dispel.md").read_text(encoding="utf-8")
        for term in ("DispelEvent.Pre", "DispelEvent.Post", "ICancellableEvent",
                     "EffectCures.MILK", "DISPEL_DENY", "DISPEL_ALLOW",
                     "EntityHitResult", "BlockEntity", "isCanceled",
                     "Post", "mutating_hook=NOT_VERIFIED",
                     "physical_qa=NOT_TESTED"):
            self.assertIn(term, dispel)
        self.assertIn("sem Post", dispel)
        self.assertIn("não prova", dispel)

    def test_status_cards_name_downstream_and_deduplicate_event_ticks(self):
        requirements = {
            "invisibility": ("showParticles", "false", "MobEffects.INVISIBILITY"),
            "wither": ("MobEffects.WITHER", "IPotionEffect", "30", "8"),
            "hex": ("HEX_EFFECT", "getBookDescription()", "não", "4 Amplify"),
            "bounce": ("BOUNCE_EFFECT", "setDeltaMovement", "downstream"),
        }
        for name, words in requirements.items():
            with self.subTest(effect=name):
                card = (ARS / "glyphs/effects" / (name + ".md")).read_text(
                    encoding="utf-8")
                for term in words:
                    self.assertIn(term, card)
                self.assertIn("mutating_hook=NOT_VERIFIED", card)
                self.assertIn("physical_qa=NOT_TESTED", card)


    def test_break_claim_preflight_is_not_cancellation_free_mutation(self):
        page = (ARS / "glyphs/effects/break.md").read_text(encoding="utf-8")
        for term in ("SpellUtil.calcAOEBlocks", "1+floor(AOE)",
                     "1+ceil(AOE)", "1+Pierce", "MobEffects.DIG_SLOWDOWN",
                     "getBaseHarvestLevel", "BREAK_WITH_PICKAXE",
                     "AugmentFortune", "AugmentExtract", "Items.SHEARS",
                     "BREAK_BLACKLIST", "destroyRespectsClaim",
                     "CommonHooks.fireBlockBreak", "breakExtraBlock",
                     "ShapersFocus.tryPropagateBlockSpell",
                     "WorldEffectPolicy", "mutating_hook=NOT_VERIFIED",
                     "physical_qa=NOT_TESTED"):
            self.assertIn(term, page)
        self.assertIn("retornar **true**", page)
        self.assertIn("não", page.lower())

    def test_place_block_inventory_callbacks_and_bounds_after_offset(self):
        page = (ARS / "glyphs/effects/place-block.md").read_text(
            encoding="utf-8")
        for term in ("BlockEvent.EntityPlaceEvent", "NeoForge.EVENT_BUS",
                     "BlockSnapshot", "isInWorldBounds",
                     "pos1.relative(hitDirection)", "UnbiasedDirectionalPlaceContext",
                     "InventoryManager.extractItem", "extractRandomItem",
                     "BlockItem.place", "ExtractedStack", "returnOrDrop",
                     "InteractionResult.FAIL", "Sensitive",
                     "ShapersFocus.tryPropagateBlockSpell",
                     "WorldEffectPolicy"):
            self.assertIn(term, page)
        self.assertIn("antes** de mudar", page)
        self.assertIn("mutating_hook=NOT_VERIFIED", page)
        self.assertIn("physical_qa=NOT_TESTED", page)

    def test_conjure_water_gates_adjacent_destination_separately(self):
        page = (ARS / "glyphs/effects/conjure-water.md").read_text(
            encoding="utf-8")
        for term in ("SOAKED_EFFECT", "entity.clearFire()",
                     "getDurationMultiplier()>0", "ultraWarm",
                     "LiquidBlockContainer", "canPlaceLiquid", "placeLiquid",
                     "destroyRespectsClaim", "world.isInWorldBounds",
                     "pos1.relative(direction)", "setBlockAndUpdate",
                     "Blocks.WATER", "ShapersFocus.tryPropagateBlockSpell",
                     "addPotionConfig(builder,20)",
                     "addExtendTimeConfig(builder,10)", "30",
                     "WorldEffectPolicy", "mutating_hook=NOT_VERIFIED",
                     "physical_qa=NOT_TESTED"):
            self.assertIn(term, page)
        self.assertIn("segundo", page)

    def test_evaporate_seven_attempts_do_not_certify_seven_mutations(self):
        page = (ARS / "glyphs/effects/evaporate.md").read_text(
            encoding="utf-8")
        for term in ("Direction.values()", "7 chamadas por candidato AOE",
                     "SimpleWaterloggedBlock", "BlockStateProperties.WATERLOGGED",
                     "LiquidBlock", "Blocks.AIR", "world.setBlock",
                     "ShapersFocus.tryPropagateBlockSpell",
                     "destroyRespectsClaim", "BlockEvent.BreakEvent",
                     "world.isInWorldBounds", "WorldEffectPolicy",
                     "mutating_hook=NOT_VERIFIED", "physical_qa=NOT_TESTED"):
            self.assertIn(term, page)
        self.assertIn("não", page.lower())

    def test_world_mutation_effects_dossier_preserves_provider_authority(self):
        page = (ARS / "EFFECT-STATIC-WORLD-MUTATION-FOUR-5.13.1.md").read_text(
            encoding="utf-8")
        for term in ("39/67", "57/85", "81/138", "81/2075",
                     "0/164", SOURCE, SHA1, "EffectBreak",
                     "EffectPlaceBlock", "EffectConjureWater",
                     "EffectEvaporate", "WorldEffectPolicy",
                     "mutating_hook=NOT_VERIFIED", "physical_qa=NOT_TESTED",
                     "Stage"):
            self.assertIn(term, page)

    def test_four_new_world_effects_not_confused_with_ars_rituals(self):
        for slug in ("break", "place-block", "conjure-water", "evaporate"):
            name = slug.replace("-", " ").title()
            page = (ARS / "glyphs/effects/INDEX.md").read_text(encoding="utf8")
            self.assertIn(f"| ✅ | {name} |", page)
            self.assertIn(f"| ✅ | {name} | [effects/{slug}.md]",
                          (ARS / "glyphs/INDEX.md").read_text(encoding="utf8"))
            self.assertIn(f"| ✅ | {name} | [glyphs/effects/{slug}.md]",
                          (ARS / "INDEX.md").read_text(encoding="utf8"))
        self.assertIn("39/67.", self.index)
        self.assertIn("57/85.", (ARS / "glyphs/INDEX.md").read_text(
            encoding="utf8"))
        self.assertIn("81/138.", (ARS / "INDEX.md").read_text(
            encoding="utf8"))
        self.assertIn("81/2075.", self.root_index)


    def test_exchange_teleport_pair_is_independent_and_block_settlement_unchecked(self):
        text = (ARS / "glyphs/effects/exchange.md").read_text(encoding="utf8")
        for token in ("EventHooks.onEnderTeleport", "TELEPORTING_NOT_SUPPORTED",
                      "FakePlayer", "origLoc", "não há rollback",
                      "SpellUtil.calcAOEBlocks", "origState",
                      "InventoryManager.extractItem", "extractRandomItem",
                      "firstBlock", "getStateForPlacement", "SILK_TOUCH",
                      "BlockUtil.breakExtraBlock", "world.setBlock",
                      "BlockItemAccessor", "stack.shrink(1)",
                      "ExtractedStack.replaceAndReturnOrDrop",
                      "WorldEffectPolicy", "mutating_hook=NOT_VERIFIED",
                      "physical_qa=NOT_TESTED"):
            self.assertIn(token, text)
        self.assertIn("sem conferir seu boolean", text)

    def test_crush_recipe_rolls_and_damage_not_per_rolled_output(self):
        text = (ARS / "glyphs/effects/crush.md").read_text(encoding="utf8")
        for token in ("DamageTypesRegistry.CRUSH", "IDamageEffect",
                      "DAMAGE.get()*3.0", "AMP_VALUE.get()",
                      "maxItemCrush", "getRolledOutputs(world.random)",
                      "skip_block_place", "random.nextInt(maxRange)+1",
                      "RecipeRegistry.CRUSH_TYPE", "setBlockAndUpdate",
                      "addFreshEntity", "stack.shrink(1)",
                      "destroyRespectsClaim", "canBlockBeHarvested",
                      "ShapersFocus.tryPropagateBlockSpell",
                      "WorldEffectPolicy", "mutating_hook=NOT_VERIFIED",
                      "physical_qa=NOT_TESTED"):
            self.assertIn(token, text)
        self.assertIn("Nenhum retorno", text)

    def test_smelt_second_break_event_and_output_without_checked_destroy(self):
        text = (ARS / "glyphs/effects/smelt.md").read_text(encoding="utf8")
        for token in ("getDefaultManaCost()=100", "maxItemSmelt",
                      "RecipeType.SMELTING", "canBlockBeHarvested",
                      "destroyRespectsClaim", "destroyBlockSafely",
                      "BlockEvent.BreakEvent", "setBlockAndUpdate",
                      "addFreshEntity", "safelyUpdateState",
                      "SMOKING", "BLASTING", "AugmentDampen",
                      "AugmentAmplify", "WorldEffectPolicy",
                      "mutating_hook=NOT_VERIFIED", "physical_qa=NOT_TESTED"):
            self.assertIn(token, text)
        self.assertIn("não verifica o boolean de retorno", text)
        self.assertIn("não é exploit comprovado", text)

    def test_craft_ui_is_not_recipe_or_item_transaction(self):
        text = (ARS / "glyphs/effects/craft.md").read_text(encoding="utf8")
        for token in ("shooter instanceof Player", "isNotFakePlayer",
                      "playerEntity.openMenu", "SimpleMenuProvider",
                      "CustomWorkbench extends CraftingMenu",
                      "ContainerLevelAccess.create", "stillValid(Player)",
                      "true", "augmentSetOf()", "getDefaultManaCost()=50",
                      "WorldEffectPolicy", "mutating_hook=NOT_VERIFIED",
                      "physical_qa=NOT_TESTED"):
            self.assertIn(token, text)
        self.assertIn("não comprova craft", text)

    def test_processing_dossier_static_scope_and_85_certifications(self):
        text = (ARS / "EFFECT-STATIC-PROCESSING-EXCHANGE-FOUR-5.13.1.md"
                ).read_text(encoding="utf8")
        for token in ("43/67", "61/85", "85/138", "85/2075",
                      "0/164", SOURCE, SHA1, "EffectExchange", "EffectCrush",
                      "EffectSmelt", "EffectCraft", "destroyBlockSafely",
                      "WorldEffectPolicy", "mutating_hook=NOT_VERIFIED",
                      "physical_qa=NOT_TESTED", "06.05", "09"):
            self.assertIn(token, text)

    def test_processing_index_numbers_are_not_full_provider_certification(self):
        self.assertIn("43/67.", self.index)
        self.assertIn("61/85.", (ARS / "glyphs/INDEX.md").read_text(
            encoding="utf8"))
        self.assertIn("85/138.", (ARS / "INDEX.md").read_text(encoding="utf8"))
        self.assertIn("85/2075.", self.root_index)
        self.assertIn("0/164.", self.root_index)
        for slug in ("exchange", "crush", "smelt", "craft"):
            name = slug.replace("-", " ").title()
            self.assertIn(f"| ✅ | {name} |", self.index)
            self.assertIn(f"| ✅ | {name} | [effects/{slug}.md]",
                          (ARS / "glyphs/INDEX.md").read_text(encoding="utf8"))
            self.assertIn(f"| ✅ | {name} | [glyphs/effects/{slug}.md]",
                          (ARS / "INDEX.md").read_text(encoding="utf8"))


if __name__ == "__main__":
    unittest.main()
