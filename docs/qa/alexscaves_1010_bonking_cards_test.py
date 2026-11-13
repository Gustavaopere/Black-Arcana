#!/usr/bin/env python3
"""Bind Bonking's individual static contract to its native death-loot boundary."""
from pathlib import Path
import copy
import hashlib
import json
import unittest

from alexscaves_1010_action_contract_audit import load_manifest, validate_cards, validate_structure

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / 'wiki/modpack-catalog/providers/✅-alexs-caves-continued'
PREFIX = 'com/github/alexmodguy/alexscaves/'
CARD = 'enchantments/bonking.md'
SEAL = 'EXACT-BONKING-CONTRACT-1.0.10.json'
EVENTS = 'server/event/CommonEvents'
CLUB = 'server/item/PrimitiveClubItem'
COMPAT = 'server/misc/ACCompat'
MIXIN = 'mixin/MobMixin'
REGISTRY = 'server/enchantment/ACEnchantmentRegistry'
ITEM_REGISTRY = 'server/item/ACItemRegistry'


class BonkingContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = load_manifest(P / SEAL)
        cls.card = (P / CARD).read_text(encoding='utf8')

    def anchors(self, owner, name):
        methods = self.d['classes'][PREFIX + owner + '.class']['methods']
        selected = [m for m in methods if m['name'] == name]
        self.assertEqual(len(selected), 1, (owner, name))
        return {a['offset']: a for a in selected[0]['anchors']}

    def op(self, anchors, offset, opcode, operand=None):
        self.assertEqual(anchors[offset]['opcode'], opcode, offset)
        if operand is not None:
            self.assertEqual(anchors[offset]['operand'], operand, offset)

    def symbol(self, anchors, offset, symbol):
        self.assertIn(symbol, anchors[offset]['symbol'], offset)

    def mutated_manifest_must_fail(self, owner, method, offset, check, *, remove=False, **changes):
        original = self.d
        self.d = copy.deepcopy(original)
        try:
            records = self.d['classes'][PREFIX + owner + '.class']['methods']
            anchors = next(m['anchors'] for m in records if m['name'] == method)
            anchor = next(a for a in anchors if a['offset'] == offset)
            if remove:
                anchors.remove(anchor)
            else:
                anchor.update(changes)
            with self.assertRaises(AssertionError):
                try:
                    check()
                except KeyError as error:
                    raise AssertionError('required causal anchor is absent') from error
        finally:
            self.d = original

    def test_singleton_exact_scope_and_original_budgets(self):
        validate_structure(self.d, profile='bonking')
        validate_cards(self.d, P, profile='bonking')
        self.assertEqual(self.d['catalog_family'], 'BONKING_ENCHANTMENT_CONTRACT')
        self.assertEqual(set(self.d['cards']), {CARD})
        self.assertEqual(set(self.d['contract_evidence']), {CARD})
        self.assertEqual(set(self.d['classes']), {PREFIX + owner + '.class' for owner in (
            EVENTS, CLUB, COMPAT, MIXIN, REGISTRY, ITEM_REGISTRY)})
        methods = [m for cls in self.d['classes'].values() for m in cls['methods']]
        self.assertEqual((len(methods), sum(len(m['anchors']) for m in methods)), (26, 678))
        self.assertTrue(all(1 <= len(m['anchors']) <= 256 for m in methods))
        self.assertLessEqual(sum(len(m['anchors']) for m in methods), 8192)
        self.assertEqual(self.d['claim_scope'], 'STATIC_TECHNICAL_CATALOG_ONLY')
        self.assertEqual(self.d['evidence_grade'], 'SHA_EXACT_BINARY_BEHAVIOR')
        self.assertEqual(self.d['mutating_hook'], 'NOT_VERIFIED')
        self.assertEqual(self.d['physical_qa'], 'NOT_TESTED')
        self.assertEqual(self.d['semantic_magic_roots'], 8)
        self.assertIs(self.d['provider_universe_closed'], False)

    def test_eleven_resources_separate_acquisition_weapon_recipe_and_mixin(self):
        self.assertEqual(set(self.d['resources']), {
            'META-INF/neoforge.mods.toml', 'assets/alexscaves/lang/en_us.json',
            'assets/alexscaves/lang/pt_br.json', 'alexscaves.mixins.json',
            'data/alexscaves/enchantment/bonking.json',
            'data/alexscaves/tags/item/enchantable/primitive_club.json',
            'data/alexscaves/recipe/primitive_club.json',
            *('data/minecraft/tags/enchantment/' + name + '.json' for name in (
                'in_enchanting_table', 'non_treasure', 'on_random_loot', 'tradeable'))})
        for path, expected in (
            ('data/alexscaves/enchantment/bonking.json',
             'f03c4e8c2f8b00b3668b8d7bf14276647b3e0324c159c6336b189a258571a86a'),
            ('data/alexscaves/tags/item/enchantable/primitive_club.json',
             '71829c384be93b8cef1e090b6afafa621dcd4eeb520c7a66ab0e6524e8a6ae43'),
            ('data/alexscaves/recipe/primitive_club.json',
             'b93f005c5632388ca6f34e3a114a8e0a4cf1c2ae99ae9bb0ed2edc2c73dddcc0')):
            self.assertEqual(self.d['resources'][path], expected)
        for name in ('in_enchanting_table', 'non_treasure', 'on_random_loot', 'tradeable'):
            self.assertEqual(self.d['resources']['data/minecraft/tags/enchantment/' + name + '.json'],
                             '6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1')

    def test_full_death_handler_retains_independent_prefix_and_suffix(self):
        a = self.anchors(EVENTS, 'livingDie')
        self.assertEqual((len(a), min(a), max(a)), (229, 0, 547))
        self.symbol(a, 7, 'EntityType.MAGMA_CUBE:')
        self.symbol(a, 41, 'ACFrogRegistry.isPrimordial:')
        self.symbol(a, 55, 'CARMINE_FROGLIGHT:')
        self.op(a, 10, 'if_acmpne', '73')
        self.symbol(a, 436, 'entity/player/Player')
        self.symbol(a, 468, 'GREEN_SOYLENT:')
        self.symbol(a, 528, 'STINKY_FISH:')
        self.op(a, 547, 'return')
        branches = [v for v in a.values() if v['opcode'].startswith('if') or v['opcode'] == 'goto']
        self.assertEqual(len(branches), 21)
        self.assertFalse(any(v['opcode'] in ('tableswitch', 'lookupswitch', 'jsr', 'ret') for v in a.values()))

    def test_server_mob_source_and_direct_living_actor_gate(self):
        a = self.anchors(EVENTS, 'livingDie')
        self.symbol(a, 80, 'Level.isClientSide:')
        self.op(a, 83, 'ifne', '432')
        self.symbol(a, 94, 'entity/Mob')
        self.op(a, 97, 'ifeq', '432')
        self.op(a, 105, 'astore_2')
        self.symbol(a, 107, 'LivingDeathEvent.getSource:')
        self.op(a, 110, 'ifnull', '432')
        self.symbol(a, 117, 'DamageSource.getDirectEntity:')
        self.symbol(a, 124, 'entity/LivingEntity')
        self.op(a, 127, 'ifeq', '432')
        self.op(a, 135, 'astore_3')
        self.assertFalse(any('DamageSource.getEntity:' in v['symbol'] or 'entity/player/Player' in v['symbol']
                             for o, v in a.items() if 73 <= o < 432))

    def test_two_current_mainhand_reads_item_identity_then_positive_level(self):
        a = self.anchors(EVENTS, 'livingDie')
        self.op(a, 136, 'aload_3')
        self.symbol(a, 137, 'InteractionHand.MAIN_HAND:')
        self.symbol(a, 140, 'LivingEntity.getItemInHand:')
        self.symbol(a, 143, 'ACItemRegistry.PRIMITIVE_CLUB:')
        self.symbol(a, 154, 'ItemStack.is:(Lnet/minecraft/world/item/Item;)Z')
        self.op(a, 157, 'ifeq', '432')
        self.op(a, 160, 'aload_3')
        self.symbol(a, 161, 'InteractionHand.MAIN_HAND:')
        self.symbol(a, 164, 'LivingEntity.getItemInHand:')
        self.symbol(a, 167, 'ACEnchantmentRegistry.BONKING:')
        self.symbol(a, 170, 'ACCompat.enchantLevel:')
        self.op(a, 173, 'ifle', '432')
        self.assertEqual([o for o, v in a.items() if 73 <= o < 432 and 'getItemInHand:' in v['symbol']],
                         [140, 164])
        reader = self.anchors(COMPAT, 'enchantLevel')
        self.assertEqual(len(reader), 24)
        self.symbol(reader, 1, 'ItemStack.getEnchantments:')
        self.symbol(reader, 42, 'Holder.is:')
        self.symbol(reader, 51, 'getIntValue:')
        self.op(reader, 56, 'ireturn')
        self.op(reader, 60, 'iconst_0')
        self.assertFalse(any('clamp' in v['symbol'] for v in reader.values()))

    def test_nominal_attempt_guard_does_not_scale_with_level(self):
        a = self.anchors(EVENTS, 'livingDie')
        self.symbol(a, 183, 'Level.getRandom:')
        self.symbol(a, 186, 'RandomSource.nextFloat:()F')
        self.symbol(a, 191, 'float 0.33f')
        self.op(a, 193, 'fcmpg')
        self.op(a, 194, 'ifge', '432')
        region = {o: v for o, v in a.items() if 73 <= o < 432}
        self.assertFalse(any(v['opcode'] in ('fmul', 'dmul', 'imul', 'idiv', 'fdiv') for v in region.values()))
        self.assertEqual([o for o, v in region.items() if 'ACCompat.enchantLevel:' in v['symbol']], [170])

    def test_temporary_creeper_lightning_null_paths_and_visual_setup(self):
        a = self.anchors(EVENTS, 'livingDie')
        self.symbol(a, 197, 'EntityType.CREEPER:')
        self.symbol(a, 204, 'ACCompat.createEntity:')
        self.symbol(a, 207, 'monster/Creeper')
        self.op(a, 210, 'astore', '4')
        self.op(a, 214, 'ifnull', '432')
        self.symbol(a, 228, 'server/level/ServerLevel')
        self.op(a, 231, 'ifeq', '274')
        self.symbol(a, 241, 'EntityType.LIGHTNING_BOLT:')
        self.symbol(a, 246, 'ACCompat.createEntity:')
        self.op(a, 256, 'ifnull', '274')
        self.op(a, 261, 'iconst_1')
        self.symbol(a, 262, 'LightningBolt.setVisualOnly:(Z)V')
        self.symbol(a, 271, 'Creeper.thunderHit:')
        helper = self.anchors(COMPAT, 'createEntity')
        self.assertEqual(len(helper), 4)
        self.symbol(helper, 2, 'EntityType.create:(Lnet/minecraft/world/level/Level;)')
        self.op(helper, 5, 'areturn')
        for v in (v for o, v in a.items() if 73 <= o < 432):
            self.assertNotIn('addFreshEntity', v['symbol'])

    def test_synthetic_source_and_original_victim_keep_distinct_local_roles(self):
        a = self.anchors(EVENTS, 'livingDie')
        self.op(a, 274, 'aload_2')
        self.symbol(a, 278, 'Level.damageSources:')
        self.op(a, 281, 'aload', '4')
        self.symbol(a, 283, 'DamageSources.mobAttack:')
        self.op(a, 286, 'astore', '5')
        self.symbol(a, 288, 'java/util/HashMap')
        self.op(a, 295, 'astore', '6')
        self.op(a, 297, 'aload_2')
        self.symbol(a, 298, 'EntityDropChanceAccessor')
        self.op(a, 301, 'astore', '7')
        region = [v for o, v in a.items() if 73 <= o < 432]
        self.assertFalse(any('.hurt:' in v['symbol'] or 'setSource:' in v['symbol'] or 'Player.attack:' in v['symbol']
                             for v in region))

    def test_all_slot_backup_zero_callback_then_normal_flow_restore(self):
        a = self.anchors(EVENTS, 'livingDie')
        self.symbol(a, 303, 'EquipmentSlot.values:')
        self.op(a, 320, 'if_icmpge', '366')
        self.op(a, 330, 'aload', '6')
        self.op(a, 334, 'aload', '7')
        self.symbol(a, 338, 'EntityDropChanceAccessor.ac_getEquipmentDropChance:')
        self.symbol(a, 346, 'HashMap.put:')
        self.op(a, 354, 'fconst_0')
        self.symbol(a, 355, 'EntityDropChanceAccessor.ac_setDropChance:')
        self.op(a, 363, 'goto', '316')
        self.op(a, 366, 'aload', '7')
        self.op(a, 368, 'aload', '5')
        self.op(a, 370, 'iconst_0')
        self.op(a, 371, 'iconst_0')
        self.symbol(a, 372, 'EntityDropChanceAccessor.ac_dropCustomDeathLoot:')
        self.symbol(a, 377, 'EquipmentSlot.values:')
        self.op(a, 394, 'if_icmpge', '432')
        self.op(a, 404, 'aload', '7')
        self.op(a, 408, 'aload', '6')
        self.symbol(a, 412, 'HashMap.get:')
        self.symbol(a, 418, 'Float.floatValue:')
        self.symbol(a, 421, 'EntityDropChanceAccessor.ac_setDropChance:')
        self.op(a, 429, 'goto', '390')
        region = {o: v for o, v in a.items() if 73 <= o < 432}
        self.assertEqual([o for o, v in region.items() if 'ac_dropCustomDeathLoot:' in v['symbol']], [372])
        self.assertFalse(any('PersistentData' in v['symbol'] or 'CompoundTag.put' in v['symbol']
                             or 'spawnAtLocation:' in v['symbol'] for v in region.values()))

    def test_three_mixin_bridges_delegate_and_ignore_the_integer_argument(self):
        get = self.anchors(MIXIN, 'ac_getEquipmentDropChance')
        put = self.anchors(MIXIN, 'ac_setDropChance')
        loot = self.anchors(MIXIN, 'ac_dropCustomDeathLoot')
        self.assertEqual((len(get), len(put), len(loot)), (4, 5, 8))
        self.symbol(get, 2, 'getEquipmentDropChance:')
        self.symbol(put, 3, 'setDropChance:')
        self.symbol(loot, 2, 'level:()Lnet/minecraft/world/level/Level;')
        self.symbol(loot, 5, 'class net/minecraft/server/level/ServerLevel')
        self.op(loot, 8, 'aload_1')
        self.op(loot, 9, 'iload_3')
        self.symbol(loot, 10, 'dropCustomDeathLoot:(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/damagesource/DamageSource;Z)V')
        self.assertFalse(any(v['opcode'] == 'iload_2' or (v['opcode'] == 'iload' and v['operand'] == '2')
                             for v in loot.values()))

    def test_all_sixteen_club_bodies_are_weapon_context(self):
        methods = self.d['classes'][PREFIX + CLUB + '.class']['methods']
        self.assertEqual({m['name']: len(m['anchors']) for m in methods}, {
            '<init>': 22, 'getStatsForEnchantmentLevel': 33, 'getEnchantmentValue': 2,
            'isEnchantable': 8, 'hurtEnemy': 6, 'acHurtEnemy': 171, 'mineBlock': 15,
            'acExtraRepairMaterials': 9, 'isValidRepairItem': 13, 'acModifiers': 17,
            'getDefaultAttributeModifiers': 8, 'initializeClient': 6,
            'onLeftClickEntity': 16, 'onEntitySwing': 24, 'acInventoryTick': 27,
            'lambda$getDefaultAttributeModifiers$0': 4})
        self.assertEqual(sum(len(m['anchors']) for m in methods), 381)
        self.assertFalse(any('ACEnchantmentRegistry.BONKING:' in a['symbol'] for m in methods for a in m['anchors']))
        self.symbol(self.anchors(CLUB, 'getStatsForEnchantmentLevel'), 15, 'double 8.0d')
        self.symbol(self.anchors(CLUB, 'acModifiers'), 10, 'ACEnchantmentRegistry.SWIFTWOOD:')
        self.symbol(self.anchors(CLUB, 'acHurtEnemy'), 136, 'ACEnchantmentRegistry.DAZING_SWEEP:')

    def test_weapon_wear_requests_precede_separate_stun_sweep_work(self):
        a = self.anchors(CLUB, 'hurtEnemy')
        self.symbol(a, 4, 'acHurtEnemy:')
        a = self.anchors(CLUB, 'acHurtEnemy')
        self.op(a, 0, 'aload_1')
        self.op(a, 1, 'iconst_1')
        self.symbol(a, 3, 'EquipmentSlot.MAINHAND:')
        self.symbol(a, 6, 'ACCompat.hurtAndBreak:')
        self.symbol(a, 13, 'Level.isClientSide:')
        self.op(a, 16, 'ifne', '392')
        self.symbol(a, 51, 'ACEffectRegistry.STUNNED:')
        self.symbol(a, 136, 'ACEnchantmentRegistry.DAZING_SWEEP:')
        mining = self.anchors(CLUB, 'mineBlock')
        self.op(mining, 10, 'ifeq', '23')
        self.op(mining, 14, 'iconst_2')
        self.symbol(mining, 20, 'ACCompat.hurtAndBreak:')
        death = [v for o, v in self.anchors(EVENTS, 'livingDie').items() if 73 <= o < 432]
        self.assertFalse(any(word in v['symbol'] for v in death for word in (
            'hurtAndBreak:', 'addCooldown:', '.shrink:', 'giveExperience', 'setDamageValue:')))

    def test_partial_registries_and_club_supplier_bind_native_identity(self):
        a = self.anchors(REGISTRY, '<clinit>')
        self.assertEqual(set(a), {132, 134, 137})
        self.symbol(a, 132, 'String bonking')
        self.symbol(a, 134, 'key:')
        self.symbol(a, 137, 'BONKING:')
        key = self.anchors(REGISTRY, 'key')
        self.assertEqual(len(key), 6)
        self.symbol(key, 0, 'Registries.ENCHANTMENT:')
        self.symbol(key, 3, 'String alexscaves')
        self.symbol(key, 9, 'ResourceKey.create:')
        a = self.anchors(ITEM_REGISTRY, '<clinit>')
        self.assertEqual(set(a), {967, 970, 973, 978, 981})
        self.symbol(a, 970, 'String primitive_club')
        self.symbol(a, 973, 'InvokeDynamic #52:get:')
        self.symbol(a, 981, 'PRIMITIVE_CLUB:')
        supplier = self.anchors(ITEM_REGISTRY, 'lambda$static$40')
        self.assertEqual(len(supplier), 9)
        self.symbol(supplier, 0, 'class com/github/alexmodguy/alexscaves/server/item/PrimitiveClubItem')
        self.op(supplier, 11, 'bipush', '120')
        self.symbol(supplier, 13, 'Item$Properties.durability:(I)')
        self.symbol(supplier, 16, 'PrimitiveClubItem."<init>":')

    def test_interface_declaration_is_sealed_without_executable_anchors(self):
        interface = self.d['native_metadata']['interface']
        path = PREFIX + 'server/entity/util/EntityDropChanceAccessor.class'
        self.assertEqual(interface['path'], path)
        self.assertEqual(interface['sha256'],
                         'e702802393eda342e252acc517baf735c830d715bcc422a9acdee36bf24ab4ba')
        self.assertNotIn(path, self.d['classes'])
        declaration = interface['declaration']
        self.assertEqual(declaration['access'], 1537)  # public, interface, abstract
        self.assertEqual(declaration['name'], path.removesuffix('.class'))
        self.assertEqual(declaration['super'], 'java/lang/Object')
        self.assertEqual(declaration['interfaces'], [])
        self.assertEqual(declaration['fields'], [])
        self.assertEqual(declaration['annotations'], [])
        expected = {
            'ac_getEquipmentDropChance': '(Lnet/minecraft/world/entity/EquipmentSlot;)F',
            'ac_setDropChance': '(Lnet/minecraft/world/entity/EquipmentSlot;F)V',
            'ac_dropCustomDeathLoot': '(Lnet/minecraft/world/damagesource/DamageSource;IZ)V'}
        self.assertEqual({m['name']: m['descriptor'] for m in declaration['methods']}, expected)
        self.assertTrue(all(m['access'] == 1025 and m['annotations'] == []
                            and 'exception_handlers' not in m and 'anchors' not in m
                            for m in declaration['methods']))

    def test_event_annotation_has_no_explicit_priority_or_cancelled_arguments(self):
        self.assertEqual(self.d['native_metadata']['living_die_annotations'], [{
            'visibility': 'RuntimeVisibleAnnotations',
            'type': 'Lnet/neoforged/bus/api/SubscribeEvent;', 'values': {}}])

    def test_mixin_target_interface_and_all_four_shadow_declarations(self):
        mixin = self.d['native_metadata']['mixin']
        self.assertEqual(mixin['name'], PREFIX + MIXIN)
        self.assertEqual(mixin['super'], 'net/minecraft/world/entity/LivingEntity')
        self.assertEqual(mixin['interfaces'], [PREFIX + 'server/entity/util/EntityDropChanceAccessor'])
        self.assertEqual(mixin['annotations'], [{
            'visibility': 'RuntimeInvisibleAnnotations',
            'type': 'Lorg/spongepowered/asm/mixin/Mixin;',
            'values': {'value': [{'class': 'Lnet/minecraft/world/entity/Mob;'}]}}])
        self.assertEqual({m['name']: m['descriptor'] for m in mixin['shadows']}, {
            'canPickUpLoot': 'Z',
            'getEquipmentDropChance': '(Lnet/minecraft/world/entity/EquipmentSlot;)F',
            'setDropChance': '(Lnet/minecraft/world/entity/EquipmentSlot;F)V',
            'dropCustomDeathLoot': '(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/damagesource/DamageSource;Z)V'})
        self.assertTrue(all(m['annotations'] == [{
            'visibility': 'RuntimeVisibleAnnotations',
            'type': 'Lorg/spongepowered/asm/mixin/Shadow;', 'values': {}}]
            for m in mixin['shadows']))

    def test_bootstrap_52_seals_supplier_implementation_and_item_return_type(self):
        bootstrap = self.d['native_metadata']['item_bootstrap_52']
        self.assertEqual(bootstrap['handle']['reference_kind'], 6)
        self.assertEqual(bootstrap['handle']['reference'][1], 'java/lang/invoke/LambdaMetafactory')
        self.assertEqual(bootstrap['handle']['reference'][2][1], 'metafactory')
        self.assertEqual(bootstrap['arguments'], [
            '()Ljava/lang/Object;', {'reference_kind': 6, 'reference': [
                10, PREFIX + ITEM_REGISTRY, [12, 'lambda$static$40', '()Lnet/minecraft/world/item/Item;']]},
            '()Lnet/minecraft/world/item/Item;'])

    def test_complete_body_fingerprints_and_partial_registry_limits_are_distinct(self):
        records = self.d['native_metadata']['method_coverage']
        full = [m for m in records if m['coverage'] == 'FULL_BODY']
        partial = [m for m in records if m['coverage'] == 'PARTIAL_REGISTRY_WINDOW']
        self.assertEqual((len(full), len(partial)), (24, 2))
        self.assertTrue(all(m['instruction_count'] == m['selected_anchors'] for m in full))
        self.assertEqual({(m['owner'], m['name'], m['instruction_count'], m['selected_anchors']) for m in partial}, {
            (PREFIX + REGISTRY + '.class', '<clinit>', 182, 3),
            (PREFIX + ITEM_REGISTRY + '.class', '<clinit>', 1382, 5)})
        living = next(m for m in records if m['name'] == 'livingDie')
        self.assertEqual(living['parsed_method_sha256'],
                         '40737aefdb49418028737a4b0a8ede771dd68b7baffad512769d58c66ee974cd')
        self.assertEqual(living['instruction_count'], 229)
        self.assertEqual(living['selected_anchors'], 229)
        self.assertEqual(living['exception_handlers'], [])
        a = self.anchors(EVENTS, 'livingDie')
        self.assertEqual(living['branch_edges'], [
            {'offset': o, 'opcode': v['opcode'], 'target': int(v['operand'])}
            for o, v in sorted(a.items()) if v['opcode'].startswith('if') or v['opcode'] == 'goto'])
        old = json.loads((P / 'EXACT-BONKING-CAUSAL-1.0.10.json').read_text())
        self.assertEqual(old['method']['parsed_method_sha256'],
                         '03c56101acdb5aa18c6d253f49b914bef1c1f2723aa5de548b126d4d864020dd')
        self.assertNotEqual(living['parsed_method_sha256'], old['method']['parsed_method_sha256'])
        self.assertEqual(old['parent_manifest_sha256'],
                         hashlib.sha256((P / 'EXACT-BONKING-1.0.10.json').read_bytes()).hexdigest())

    def test_semantic_negative_metadata_cannot_invent_priority_looting_or_full_registries(self):
        original = self.d
        mutations = (
            ('living_die_annotations', self.test_event_annotation_has_no_explicit_priority_or_cancelled_arguments),
            ('interface', self.test_interface_declaration_is_sealed_without_executable_anchors),
            ('item_bootstrap_52', self.test_bootstrap_52_seals_supplier_implementation_and_item_return_type),
            ('method_coverage', self.test_complete_body_fingerprints_and_partial_registry_limits_are_distinct))
        try:
            for name, check in mutations:
                self.d = copy.deepcopy(original)
                native = self.d['native_metadata']
                if name == 'living_die_annotations':
                    native[name][0]['values']['priority'] = 'HIGHEST'
                elif name == 'interface':
                    native[name]['declaration']['methods'][2]['descriptor'] = '(Lnet/minecraft/world/damagesource/DamageSource;IZ)I'
                elif name == 'item_bootstrap_52':
                    native[name]['arguments'][1]['reference'][2][1] = 'lambda$static$41'
                else:
                    next(m for m in native[name] if m['coverage'] == 'PARTIAL_REGISTRY_WINDOW')['coverage'] = 'FULL_BODY'
                with self.subTest(metadata=name), self.assertRaises(AssertionError):
                    check()
        finally:
            self.d = original

    def test_semantic_negative_server_direct_actor_and_current_stack(self):
        self.mutated_manifest_must_fail(EVENTS, 'livingDie', 83,
                                       self.test_server_mob_source_and_direct_living_actor_gate,
                                       opcode='ifeq')
        self.mutated_manifest_must_fail(EVENTS, 'livingDie', 117,
                                       self.test_server_mob_source_and_direct_living_actor_gate,
                                       symbol='Method net/minecraft/world/damagesource/DamageSource.getEntity:()Lnet/minecraft/world/entity/Entity;')
        self.mutated_manifest_must_fail(EVENTS, 'livingDie', 164,
                                       self.test_two_current_mainhand_reads_item_identity_then_positive_level,
                                       remove=True)
        self.mutated_manifest_must_fail(EVENTS, 'livingDie', 173,
                                       self.test_two_current_mainhand_reads_item_identity_then_positive_level,
                                       opcode='iflt')

    def test_semantic_negative_nominal_rng_and_temporary_entity_null_guards(self):
        self.mutated_manifest_must_fail(EVENTS, 'livingDie', 191,
                                       self.test_nominal_attempt_guard_does_not_scale_with_level,
                                       symbol='float 0.66f')
        self.mutated_manifest_must_fail(EVENTS, 'livingDie', 194,
                                       self.test_nominal_attempt_guard_does_not_scale_with_level,
                                       opcode='ifgt')
        self.mutated_manifest_must_fail(EVENTS, 'livingDie', 214,
                                       self.test_temporary_creeper_lightning_null_paths_and_visual_setup,
                                       remove=True)
        self.mutated_manifest_must_fail(EVENTS, 'livingDie', 256,
                                       self.test_temporary_creeper_lightning_null_paths_and_visual_setup,
                                       operand='432')

    def test_semantic_negative_synthetic_actor_and_callback_boolean(self):
        self.mutated_manifest_must_fail(EVENTS, 'livingDie', 281,
                                       self.test_synthetic_source_and_original_victim_keep_distinct_local_roles,
                                       opcode='aload_3', operand='')
        self.mutated_manifest_must_fail(EVENTS, 'livingDie', 371,
                                       self.test_all_slot_backup_zero_callback_then_normal_flow_restore,
                                       opcode='iconst_1')
        self.mutated_manifest_must_fail(MIXIN, 'ac_dropCustomDeathLoot', 9,
                                       self.test_three_mixin_bridges_delegate_and_ignore_the_integer_argument,
                                       opcode='iload_2')

    def test_semantic_negative_loop_targets_and_restore_lookup(self):
        check = self.test_all_slot_backup_zero_callback_then_normal_flow_restore
        self.mutated_manifest_must_fail(EVENTS, 'livingDie', 363, check, operand='366')
        self.mutated_manifest_must_fail(EVENTS, 'livingDie', 429, check, operand='432')
        self.mutated_manifest_must_fail(EVENTS, 'livingDie', 412, check,
                                       symbol='Method java/util/HashMap.remove:(Ljava/lang/Object;)Ljava/lang/Object;')
        self.mutated_manifest_must_fail(EVENTS, 'livingDie', 421, check, remove=True)

    def test_workflow_retains_one_download_eight_minutes_and_separate_report(self):
        workflow = (ROOT / '.github/workflows/alexscaves-1010-action-contracts.yml').read_text()
        self.assertEqual(workflow.count('curl --fail'), 1)
        self.assertIn('timeout-minutes: 8', workflow)
        self.assertEqual(workflow.count("'docs/qa/alexscaves_1010_bonking_cards_test.py'"), 2)
        self.assertIn('python3 docs/qa/alexscaves_1010_bonking_cards_test.py -v', workflow)
        self.assertIn('--profile bonking', workflow)
        self.assertIn(SEAL, workflow)
        self.assertEqual(workflow.count('build/alexscaves-1010/bonking-evidence.json'), 2)

    def test_card_preserves_historical_seals_and_static_runtime_boundary(self):
        for artifact in ('EXACT-BONKING-1.0.10.json', 'EXACT-BONKING-CAUSAL-1.0.10.json', SEAL):
            self.assertIn(artifact, self.card)
        for phrase in ('STATIC_TECHNICAL_CATALOG_ONLY', 'SHA_EXACT_BINARY_BEHAVIOR',
                       'NOT_TESTED', 'NOT_VERIFIED', 'NO_MUTATION'):
            self.assertIn(phrase, self.card)
        for forbidden in ('physical_qa=PASS', 'mutating_hook=VERIFIED'):
            self.assertNotIn(forbidden, self.card)

    def test_card_documents_seven_axes_with_reasons_for_inapplicable_parameters(self):
        axes = ('Targeting', 'Range / area', 'Speed / direction', 'Projectile / size',
                'Damage / type', 'Duration / resources', 'Authorship / protection / procs')
        for axis in axes:
            self.assertIn('| **' + axis + '** |', self.card)
        reasons = {
            'Range / area': 'não executa busca espacial',
            'Speed / direction': 'nenhum movimento',
            'Projectile / size': 'referências temporárias',
            'Duration / resources': 'não há buff temporizado ou contador'}
        for axis, reason in reasons.items():
            row = next(line for line in self.card.splitlines() if line.startswith('| **' + axis + '** |'))
            self.assertIn('N/A', row)
            self.assertIn(reason, row)

    def test_card_states_causal_and_exception_boundaries_without_final_reward_claims(self):
        claims = (
            'duas leituras da mão principal atual',
            'não uma stack salva do golpe original ou um snapshot imutável da arma da kill',
            'não resolve dono de projétil',
            'sem escala por nível',
            'não é a probabilidade final de cabeça',
            'Raio null (`@256 → 274`) também pula somente esse preparo e continua no caminho de loot.',
            'vítima continua sendo o **Mob original da local 2**',
            'zero entradas na tabela JVM de handlers',
            'não há `try/finally` compilado',
            'observação estática condicional de exception-safety',
            'não de bug físico reproduzido, corrupção permanente demonstrada',
            'ignora o argumento int',
            'não é, por isso, um parâmetro efetivo de looting demonstrado',
            'não certifica registro do listener, prioridade, política para evento cancelado',
            'Aplicação e ordem do Mixin no runtime transformado',
            'callback invocado → loot avaliado → ItemEntity inserido no mundo → item coletado → XP/Mastery creditados',
            'HashMap é um backup transitório por slot, não um recibo',
            'seguro para replay ou reentrada',
            'Não reexecutar',
            'não é o estado atual desta ficha',
            'Não executam Minecraft, CFG interprocedural ou loot real',
            'A conclusão estática independe de reproduzir uma cabeça física ou uma exceção em jogo')
        for claim in claims:
            self.assertIn(claim, self.card)
        for declaration in ('ACEnchantmentRegistry.<clinit> @132–137', 'ACItemRegistry.<clinit> @967–981'):
            self.assertIn(declaration, self.card)
        self.assertIn('janelas **PARTIAL**', self.card)
        self.assertIn('conservam seus bytes, hashes e limites **PARTIAL**', self.card)
        self.assertIn('não contém nome nem descrição de Bonking', self.card)
        self.assertIn('não é uma tradução oficial', self.card)

    def test_semantic_negative_card_cannot_promote_runtime_or_remove_causal_limits(self):
        original = self.card
        try:
            for claim in ('physical_qa=PASS', 'mutating_hook=VERIFIED'):
                self.card = original + '\n' + claim + '\n'
                with self.subTest(claim=claim), self.assertRaises(AssertionError):
                    self.test_card_preserves_historical_seals_and_static_runtime_boundary()
            for old, new in (
                ('ignora o argumento int', 'encaminha o argumento int'),
                ('não há `try/finally` compilado', 'há `try/finally` compilado'),
                ('duas leituras da mão principal atual', 'snapshot da arma original'),
                ('não é a probabilidade final de cabeça', 'é a probabilidade final de cabeça')):
                self.assertIn(old, original)
                self.card = original.replace(old, new)
                with self.subTest(claim=old), self.assertRaises(AssertionError):
                    self.test_card_states_causal_and_exception_boundaries_without_final_reward_claims()
            self.card = original.replace('não executa busca espacial', 'tem área de cinco blocos')
            with self.assertRaises(AssertionError):
                self.test_card_documents_seven_axes_with_reasons_for_inapplicable_parameters()
        finally:
            self.card = original

    def test_static_certificate_and_dynamic_family_queue_preserve_runtime_limits(self):
        ledger = json.loads((ROOT / 'wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json').read_text())
        certificate = ledger['objects'][P.name + '/' + CARD]
        for key in ('claim_scope', 'evidence_grade', 'mutating_hook', 'physical_qa'):
            self.assertEqual(certificate[key], self.d[key])
        self.assertEqual(certificate['mutation'], 'NO_MUTATION')
        self.assertEqual(set(certificate['evidence']), {
            'identity', 'behavior', 'parameters', 'targeting', 'costs', 'integration', 'validation'})
        self.assertEqual({v['path'] for v in certificate['evidence'].values()},
                         {str((P / CARD).relative_to(ROOT))})
        inventory = json.loads((P / 'INTEGRATION-SCOPE-INVENTORY-1.0.10.json').read_text())
        ids = set(inventory['remaining_family_inventory']['enchantment_ids'])
        present = {p.stem.replace('-', '_') for p in (P / 'enchantments').glob('*.md')
                   if p.name not in ('INDEX.md', 'README.md')}
        prefix = P.name + '/enchantments/'
        full = {Path(key).stem.replace('-', '_') for key in ledger['objects']
                if key.startswith(prefix) and key.endswith('.md')} & ids
        partial = sorted((present & ids) - full)
        missing = sorted(ids - present)
        self.assertIn('bonking', full)
        self.assertNotIn('bonking', partial)
        self.assertEqual(partial[0], 'bouncing_bolt')
        self.assertEqual((len(full), len(partial), len(present & ids), len(ids)), (33, 18, 51, 51))
        crosswalk = (P / 'ENCHANTMENT-PERK-CROSSWALK-1.0.10.md').read_text()
        self.assertIn('| ✅ | `alexscaves:bonking`', crosswalk)
        for name, count in (('full', len(full)), ('partial', len(partial)), ('existing', len(present & ids))):
            self.assertIn(f'individual_{name}_enchantment_dossiers={count}/{len(ids)}', crosswalk)
        self.assertEqual(len(full) + len(partial) + len(missing), len(ids))
        self.assertFalse(missing)
        self.assertIn(f'começando por `alexscaves:{partial[0]}`', crosswalk)
        self.assertEqual(ledger['known_rosters'][P.name]['total'], self.d['semantic_magic_roots'])
        self.assertNotIn(P.name, ledger['providers'])


if __name__ == '__main__':
    unittest.main()
