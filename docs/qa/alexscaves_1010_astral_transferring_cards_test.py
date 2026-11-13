#!/usr/bin/env python3
"""Bind Astral Transferring's scoped static contract to its native causal path."""
from pathlib import Path
import copy
import json
import unittest

from alexscaves_1010_action_contract_audit import load_manifest, validate_cards, validate_structure

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / 'wiki/modpack-catalog/providers/✅-alexs-caves-continued'
PREFIX = 'com/github/alexmodguy/alexscaves/'
CARD = 'enchantments/astral-transferring.md'
SEAL = 'EXACT-ASTRAL-TRANSFERRING-CONTRACT-1.0.10.json'
TOTEM = 'server/item/TotemOfPossessionItem'
COMPAT = 'server/misc/ACCompat'
PLATFORM = 'server/misc/ACPlatform'
MESSAGE = 'server/message/UpdateItemTagMessage'
UPDATES = 'server/item/UpdatesStackTags'
ILLAGER = 'mixin/IllagerMixin'
LIVING = 'mixin/LivingEntityMixin'
REGISTRY = 'server/enchantment/ACEnchantmentRegistry'
ITEM_REGISTRY = 'server/item/ACItemRegistry'
CONFIG = 'server/config/ACServerConfig'
TAG_INT = '(Lnet/minecraft/nbt/CompoundTag;Ljava/lang/String;)I'


class AstralTransferringContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = load_manifest(P / SEAL)
        cls.card = (P / CARD).read_text(encoding='utf8')

    def anchors(self, owner, name, descriptor=None):
        methods = self.d['classes'][PREFIX + owner + '.class']['methods']
        selected = [m for m in methods if m['name'] == name and
                    (descriptor is None or m['descriptor'] == descriptor)]
        self.assertEqual(len(selected), 1, (owner, name, descriptor))
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
            methods = self.d['classes'][PREFIX + owner + '.class']['methods']
            selected = [m for m in methods if m['name'] == method]
            self.assertEqual(len(selected), 1)
            anchors = selected[0]['anchors']
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

    def test_singleton_exact_scope_and_budgets(self):
        validate_structure(self.d, profile='astral_transferring')
        validate_cards(self.d, P, profile='astral_transferring')
        self.assertEqual(self.d['catalog_family'], 'ASTRAL_TRANSFERRING_ENCHANTMENT_CONTRACT')
        self.assertEqual(set(self.d['cards']), {CARD})
        self.assertEqual(set(self.d['contract_evidence']), {CARD})
        self.assertEqual(set(self.d['classes']), {PREFIX + owner + '.class' for owner in (
            TOTEM, COMPAT, PLATFORM, MESSAGE, UPDATES, ILLAGER, LIVING,
            REGISTRY, ITEM_REGISTRY, CONFIG)})
        methods = [m for cls in self.d['classes'].values() for m in cls['methods']]
        self.assertEqual((len(methods), sum(len(m['anchors']) for m in methods)), (50, 1045))
        self.assertTrue(all(1 <= len(m['anchors']) <= 256 for m in methods))
        self.assertLessEqual(sum(len(m['anchors']) for m in methods), 8192)
        self.assertEqual(self.d['claim_scope'], 'STATIC_TECHNICAL_CATALOG_ONLY')
        self.assertEqual(self.d['evidence_grade'], 'SHA_EXACT_BINARY_BEHAVIOR')
        self.assertEqual(self.d['mutating_hook'], 'NOT_VERIFIED')
        self.assertEqual(self.d['physical_qa'], 'NOT_TESTED')
        self.assertEqual(self.d['semantic_magic_roots'], 8)
        self.assertIs(self.d['provider_universe_closed'], False)

    def test_thirteen_resources_separate_equipment_acquisition_and_resistance(self):
        self.assertEqual(set(self.d['resources']), {
            'META-INF/neoforge.mods.toml', 'assets/alexscaves/lang/en_us.json',
            'assets/alexscaves/lang/pt_br.json', 'alexscaves.mixins.json',
            'data/alexscaves/enchantment/astral_transferring.json',
            'data/alexscaves/enchantment/detonating_death.json',
            'data/alexscaves/tags/item/enchantable/totem_of_possession.json',
            'data/alexscaves/tags/entity_type/resists_totem_of_possession.json',
            'data/alexscaves/recipe/totem_of_possession.json',
            *('data/minecraft/tags/enchantment/' + t + '.json' for t in (
                'in_enchanting_table', 'non_treasure', 'on_random_loot', 'tradeable'))})
        for path, expected in (
            ('data/alexscaves/enchantment/astral_transferring.json',
             '41133c10af9c9e8d5e33d1b8339b734f81547b141f83fc0144aa9cf89f1f04c2'),
            ('data/alexscaves/enchantment/detonating_death.json',
             '8402461954ff5b249ae675b51d7dcc23d933b2b06c494b327bf608371298646e'),
            ('data/alexscaves/tags/item/enchantable/totem_of_possession.json',
             '185a085206993877d91ca6d8c697273c14f945b1d55cb6179e3236c138c357cf'),
            ('data/alexscaves/tags/entity_type/resists_totem_of_possession.json',
             '6ae5d98cd4b12739d3d1d7dc78d37053b2e5b0eb3b1093e3f8a9a6d9768df209'),
            ('data/alexscaves/recipe/totem_of_possession.json',
             '66abfc1425daee7e89b87f145c4148747a00a29fd45b96222869783e42ed710b')):
            self.assertEqual(self.d['resources'][path], expected)
        for t in ('in_enchanting_table', 'non_treasure', 'on_random_loot', 'tradeable'):
            self.assertEqual(self.d['resources']['data/minecraft/tags/enchantment/' + t + '.json'],
                             '6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1')

    def test_all_twenty_two_totem_methods_and_exact_partial_tick_windows(self):
        methods = self.d['classes'][PREFIX + TOTEM + '.class']['methods']
        expected = {
            '<init>': 36, 'getEnchantmentValue': 2, 'isEnchantable': 8, 'use': 66,
            'releaseUsing': 29, 'onUseTick': 254, 'getUseAnimation': 2,
            'getUseDuration': 2, 'acModifiers': 8, 'getDefaultAttributeModifiers': 8,
            'resetBound': 16, 'appendHoverText': 37, 'getBoundEntityUUID': 17,
            'updateEntityIdFromServer': 49, 'getControlledEntity': 44,
            'isEntityLookingAt': 70, 'isBound': 7, 'hurtEnemy': 6, 'acHurtEnemy': 64,
            'setPossessed': 16, 'lambda$getDefaultAttributeModifiers$1': 4,
            'lambda$onUseTick$0': 11}
        self.assertEqual({m['name']: len(m['anchors']) for m in methods}, expected)
        self.assertEqual(len(methods), 22)
        self.assertEqual(sum(len(m['anchors']) for m in methods), 756)
        a = self.anchors(TOTEM, 'onUseTick')
        self.assertEqual(tuple(sum(lo <= o <= hi for o in a) for lo, hi in (
            (0, 39), (106, 284), (651, 655), (714, 1084))), (19, 83, 3, 149))
        self.assertTrue(all(any(lo <= o <= hi for lo, hi in (
            (0, 39), (106, 284), (651, 655), (714, 1084))) for o in a))
        self.assertFalse(any(41 <= o <= 103 or 286 <= o <= 648 or 658 <= o <= 711 for o in a))
        self.assertEqual(self.d['classes'][PREFIX + TOTEM + '.class']['sha256'],
                         'bad9dd8b88eb621b558d1ede477d2b4ba6a21befdec31b4a0233adcac701773e')

    def test_original_local_and_cleanup_precede_continuing_look_and_player_gates(self):
        a = self.anchors(TOTEM, 'onUseTick')
        self.symbol(a, 3, 'getControlledEntity:')
        self.op(a, 6, 'astore', '5')
        self.op(a, 12, 'ifeq', '28')
        self.op(a, 17, 'ifnull', '39')
        self.op(a, 25, 'ifeq', '39')
        self.op(a, 36, 'if_icmplt', '143')
        self.op(a, 106, 'aload', '5')
        self.op(a, 108, 'iconst_0')
        for offset, symbol in ((109, 'setPossessed:'), (113, 'resetBound:'),
                               (117, 'stopUsingItem:'), (139, 'sendMSGToServer:')):
            self.symbol(a, offset, symbol)
        self.op(a, 142, 'return')
        self.symbol(a, 158, 'double 5.0d')
        self.symbol(a, 161, 'isEntityLookingAt:')
        self.op(a, 164, 'ifne', '177')
        self.symbol(a, 168, 'SIGHTLESS:')
        self.op(a, 174, 'ifeq', '203')
        self.symbol(a, 179, 'player/Player')
        self.op(a, 182, 'ifeq', '230')
        self.symbol(a, 188, 'totemOfPossessionPlayers:')
        self.op(a, 200, 'ifne', '230')
        self.symbol(a, 204, 'stopUsingItem:')
        self.op(a, 229, 'return')

    def test_client_even_time_left_wear_is_distinct_from_elapsed_four_tick_transfer(self):
        a = self.anchors(TOTEM, 'onUseTick')
        self.op(a, 230, 'iload', '4')
        self.op(a, 232, 'iconst_2')
        self.op(a, 233, 'irem')
        self.op(a, 234, 'ifne', '275')
        self.symbol(a, 238, 'Level.isClientSide:')
        self.op(a, 241, 'ifeq', '275')
        self.symbol(a, 259, 'Player.isCreative:')
        self.op(a, 262, 'ifne', '275')
        self.symbol(a, 267, 'ItemStack.getDamageValue:')
        self.op(a, 270, 'iconst_1')
        self.op(a, 271, 'iadd')
        self.symbol(a, 272, 'ItemStack.setDamageValue:')
        self.symbol(a, 278, 'getUseDuration:')
        self.op(a, 281, 'iload', '4')
        self.op(a, 283, 'isub')
        self.op(a, 284, 'istore', '6')
        duration = self.anchors(TOTEM, 'getUseDuration')
        self.symbol(duration, 0, 'int 72000')
        self.op(a, 881, 'iload', '6')
        self.op(a, 883, 'iconst_4')
        self.op(a, 884, 'irem')
        self.op(a, 885, 'ifne', '1081')
        transfer = [v['symbol'] for o, v in a.items() if 881 <= o <= 1051]
        self.assertFalse(any(x in symbol for symbol in transfer for x in (
            'setDamageValue:', 'hurtAndBreak', 'addCooldown:', '.hurt:', '.shrink:')))

    def test_enclosing_server_guard_and_both_alliance_directions_bound_query(self):
        a = self.anchors(TOTEM, 'onUseTick')
        self.symbol(a, 652, 'Level.isClientSide:')
        self.op(a, 655, 'ifeq', '717')
        self.op(a, 714, 'goto', '1084')
        self.op(a, 717, 'aload', '5')
        self.symbol(a, 719, 'Entity.getBoundingBox:')
        self.symbol(a, 722, 'double 3.0d')
        self.symbol(a, 725, 'AABB.inflate:(D)')
        self.op(a, 747, 'aload', '5')
        self.symbol(a, 751, 'InvokeDynamic #1:test:()Ljava/util/function/Predicate;')
        self.symbol(a, 756, 'Level.getEntities:(Lnet/minecraft/world/entity/Entity;')
        for offset, expected in ((795, 'ifne'), (805, 'ifne'), (814, 'ifne'),
                                 (824, 'ifne'), (834, 'ifne'), (842, 'ifeq')):
            self.op(a, offset, expected, '1081')
        self.op(a, 798, 'aload', '5')
        self.op(a, 800, 'aload', '15')
        self.symbol(a, 802, 'Entity.isAlliedTo:')
        self.op(a, 817, 'aload', '15')
        self.op(a, 819, 'aload', '5')
        self.symbol(a, 821, 'Entity.isAlliedTo:')
        self.symbol(a, 831, 'Entity.isPassengerOfSameVehicle:')
        self.symbol(a, 839, 'LivingEntity')
        predicate = self.anchors(TOTEM, 'lambda$onUseTick$0')
        self.symbol(predicate, 1, 'Entity.canBeHitByProjectile:')
        self.op(predicate, 4, 'ifeq', '19')
        self.op(predicate, 7, 'aload_1')
        self.op(predicate, 8, 'aload_0')
        self.symbol(predicate, 9, 'Entity.equals:')
        self.op(predicate, 12, 'ifne', '19')

    def test_mob_only_strict_health_resistance_positive_level_and_candidate_loop(self):
        a = self.anchors(TOTEM, 'onUseTick')
        self.op(a, 852, 'aload', '5')
        self.symbol(a, 854, 'entity/Mob')
        self.op(a, 857, 'ifeq', '1054')
        self.op(a, 860, 'aload', '5')
        self.op(a, 865, 'astore', '17')
        self.symbol(a, 871, 'Mob.setTarget:')
        self.symbol(a, 878, 'Mob.setLastHurtByMob:')
        self.op(a, 888, 'aload', '16')
        self.symbol(a, 890, 'LivingEntity.getHealth:')
        self.op(a, 893, 'aload', '17')
        self.symbol(a, 895, 'Mob.getHealth:')
        self.op(a, 898, 'fcmpl')
        self.op(a, 899, 'ifle', '1081')
        self.symbol(a, 910, 'RESISTS_TOTEM_OF_POSSESSION:')
        self.op(a, 916, 'ifne', '1081')
        self.symbol(a, 920, 'ASTRAL_TRANSFERRING:')
        self.symbol(a, 923, 'ACCompat.enchantLevel:')
        self.op(a, 926, 'ifle', '1081')
        self.symbol(a, 1073, 'Player.attack:')
        self.symbol(a, 1078, 'Player.resetAttackStrengthTicker:')
        self.op(a, 1051, 'goto', '1081')
        self.op(a, 1081, 'goto', '766')
        self.op(a, 773, 'ifeq', '1084')
        # The original controlled entity is resolved once and never overwritten in this sealed path.
        stores = [(o, v) for o, v in a.items() if v['opcode'] == 'astore' and v['operand'] == '5']
        self.assertEqual([o for o, _ in stores], [6])
        self.assertFalse(any('distanceTo' in v['symbol'] or 'totemOfPossessionPlayers:' in v['symbol']
                             for o, v in a.items() if 717 <= o <= 1084))
        reader = self.anchors(COMPAT, 'enchantLevel')
        self.assertEqual(len(reader), 24)
        self.symbol(reader, 1, 'ItemStack.getEnchantments:')
        self.symbol(reader, 42, 'Holder.is:')
        self.symbol(reader, 51, 'getIntValue:')
        self.op(reader, 56, 'ireturn')
        self.op(reader, 60, 'iconst_0')
        self.assertFalse(any('clamp' in v['symbol'] for v in reader.values()))

    def test_ordered_transfer_sets_new_marker_then_uuid_snapshot_tag_and_optional_sync(self):
        a = self.anchors(TOTEM, 'onUseTick')
        self.op(a, 929, 'aload', '16')
        self.op(a, 931, 'iconst_1')
        self.symbol(a, 932, 'setPossessed:')
        self.symbol(a, 936, 'ACCompat.getOrCreateTag:')
        self.symbol(a, 943, 'String BoundEntityUUID')
        self.op(a, 946, 'aload', '16')
        self.symbol(a, 948, 'LivingEntity.getUUID:')
        self.symbol(a, 951, 'ACCompat.putUUID:')
        self.op(a, 954, 'aload', '16')
        self.symbol(a, 956, 'ACPlatform.serializeEntity:')
        self.symbol(a, 963, 'String id')
        self.symbol(a, 982, 'CompoundTag.putString:')
        self.symbol(a, 987, 'String BoundEntityTag')
        self.symbol(a, 992, 'CompoundTag.put:')
        self.symbol(a, 999, 'ACCompat.setTag:')
        self.symbol(a, 1018, 'server/level/ServerLevel')
        self.op(a, 1021, 'ifeq', '1051')
        self.symbol(a, 1031, 'player/Player')
        self.op(a, 1034, 'ifeq', '1051')
        self.symbol(a, 1048, 'updateEntityIdFromServer:')
        transfer = {o: v for o, v in a.items() if 929 <= o <= 1051}
        self.assertEqual([o for o, v in transfer.items() if 'setPossessed:' in v['symbol']], [932])
        self.assertFalse(any('resetBound:' in v['symbol'] or 'CompoundTag.remove:' in v['symbol']
                             for v in transfer.values()))
        serialize = self.anchors(PLATFORM, 'serializeEntity')
        self.assertEqual(len(serialize), 5)
        self.symbol(serialize, 2, 'Entity.registryAccess:')
        self.symbol(serialize, 5, 'Entity.serializeNBT:')
        self.op(serialize, 8, 'areturn')

    def test_custom_data_helpers_copy_and_commit_separate_from_entity_marker(self):
        self.assertEqual({m['name']: len(m['anchors']) for m in
                          self.d['classes'][PREFIX + COMPAT + '.class']['methods']}, {
            'getTag': 12, 'getOrCreateTag': 14, 'setTag': 14, 'enchantLevel': 24,
            'getBoolean': 4, 'getInt': 4, 'getUUID': 4, 'putUUID': 5,
            'getPersistentData': 3, 'useConsume': 3, 'usePass': 3,
            'entityTypeFrom': 3, 'displayClientMessage': 5})
        for name, count, copy_offset in (('getTag', 12, 20), ('getOrCreateTag', 14, 26)):
            a = self.anchors(COMPAT, name)
            self.assertEqual(len(a), count)
            self.symbol(a, 1, 'DataComponents.CUSTOM_DATA:')
            self.symbol(a, 4, 'ItemStack.get:')
            self.symbol(a, copy_offset, 'CustomData.copyTag:')
        get = self.anchors(COMPAT, 'getTag')
        self.op(get, 15, 'aconst_null')
        create = self.anchors(COMPAT, 'getOrCreateTag')
        self.symbol(create, 15, 'nbt/CompoundTag')
        put = self.anchors(COMPAT, 'setTag')
        self.op(put, 1, 'ifnonnull', '15')
        self.symbol(put, 8, 'ItemStack.remove:')
        self.symbol(put, 20, 'CustomData.of:')
        self.symbol(put, 23, 'ItemStack.set:')
        reset = self.anchors(TOTEM, 'resetBound')
        self.assertEqual([reset[o]['symbol'] for o in (6, 13, 20)],
                         ['String BoundEntityTag', 'String BoundEntityUUID', 'String ControllingEntityID'])
        for offset in (9, 16, 23):
            self.symbol(reset, offset, 'CompoundTag.remove:')
        self.symbol(reset, 28, 'ACCompat.setTag:')
        self.assertFalse(any('TotemPossessed' in v['symbol'] or 'setPossessed:' in v['symbol']
                             for v in reset.values()))
        possessed = self.anchors(TOTEM, 'setPossessed')
        self.op(possessed, 1, 'ifnonnull', '5')
        self.op(possessed, 6, 'ifeq', '23')
        self.symbol(possessed, 10, 'ACCompat.getPersistentData:')
        self.symbol(possessed, 13, 'String TotemPossessed')
        self.symbol(possessed, 17, 'CompoundTag.putBoolean:')
        self.symbol(possessed, 24, 'ACCompat.getPersistentData:')
        self.symbol(possessed, 30, 'CompoundTag.remove:')
        for helper, symbol in (('getUUID', 'CompoundTag.getUUID:'),
                               ('getBoolean', 'CompoundTag.getBoolean:'),
                               ('getInt', 'CompoundTag.getInt:')):
            self.symbol(self.anchors(COMPAT, helper), 2, symbol)
        self.symbol(self.anchors(COMPAT, 'putUUID'), 3, 'CompoundTag.putUUID:')
        self.symbol(self.anchors(COMPAT, 'getPersistentData'), 1, 'Entity.getPersistentData:')

    def test_client_numeric_id_server_uuid_resolution_and_changed_id_broadcast(self):
        a = self.anchors(TOTEM, 'getControlledEntity')
        self.symbol(a, 1, 'Level.isClientSide:')
        self.op(a, 4, 'ifeq', '55')
        self.symbol(a, 15, 'String ControllingEntityID')
        self.symbol(a, 29, 'ACCompat.getInt:')
        self.op(a, 35, 'iconst_m1')
        self.symbol(a, 51, 'Level.getEntity:(I)')
        self.symbol(a, 56, 'server/level/ServerLevel')
        self.symbol(a, 68, 'getBoundEntityUUID:')
        self.symbol(a, 85, 'ServerLevel.getEntity:(Ljava/util/UUID;)')
        sync = self.anchors(TOTEM, 'updateEntityIdFromServer')
        self.op(sync, 22, 'iconst_m1')
        self.op(sync, 36, 'iconst_m1')
        self.symbol(sync, 45, 'ServerLevel.getEntity:(Ljava/util/UUID;)')
        self.op(sync, 55, 'iconst_m1')
        self.symbol(sync, 61, 'Entity.getId:')
        self.symbol(sync, 73, 'CompoundTag.putInt:')
        self.symbol(sync, 79, 'ACCompat.setTag:')
        self.op(sync, 86, 'if_icmpeq', '104')
        self.symbol(sync, 101, 'sendMSGToAll:')

    def test_release_and_item_defaults_do_not_become_per_transfer_server_cost(self):
        ctor = self.anchors(TOTEM, '<init>')
        self.op(ctor, 8, 'sipush', '1000')
        self.symbol(ctor, 14, 'Rarity.UNCOMMON:')
        self.symbol(ctor, 38, 'double 2.0d')
        self.symbol(ctor, 62, 'double -2.4000000953674316d')
        self.symbol(self.anchors(TOTEM, 'getUseAnimation'), 0, 'UseAnim.BLOCK:')
        release = self.anchors(TOTEM, 'releaseUsing')
        self.symbol(release, 16, 'Entity.setGlowingTag:')
        self.symbol(release, 20, 'Level.isClientSide:')
        self.op(release, 23, 'ifeq', '41')
        self.symbol(release, 38, 'sendMSGToServer:')
        self.symbol(release, 42, 'ItemStack.getDamageValue:')
        self.symbol(release, 46, 'ItemStack.getMaxDamage:')
        self.op(release, 49, 'if_icmplt', '57')
        self.op(release, 53, 'iconst_1')
        self.symbol(release, 54, 'ItemStack.shrink:')
        self.assertFalse(any('resetBound:' in v['symbol'] or 'setPossessed:' in v['symbol']
                             for v in release.values()))

    def test_view_helper_uses_distance_adjusted_dot_product_and_line_of_sight(self):
        a = self.anchors(TOTEM, 'isEntityLookingAt')
        self.assertEqual(len(a), 70)
        self.symbol(a, 4, 'LivingEntity.distanceTo:')
        self.symbol(a, 8, 'double 0.1d')
        self.op(a, 11, 'dmul')
        self.op(a, 12, 'dadd')
        self.op(a, 13, 'dmul')
        self.symbol(a, 17, 'LivingEntity.getViewVector:')
        self.symbol(a, 78, 'Vec3.length:')
        self.symbol(a, 94, 'Vec3.dot:')
        self.op(a, 105, 'ddiv')
        self.op(a, 106, 'dsub')
        self.op(a, 108, 'ifle', '123')
        self.symbol(a, 113, 'LivingEntity.hasLineOfSight:')
        self.op(a, 116, 'ifeq', '123')
        self.op(a, 119, 'iconst_1')
        self.op(a, 123, 'iconst_0')

    def test_packet_resolves_supplied_entity_prefers_mainhand_and_calls_default_tag_writer(self):
        self.assertEqual({m['name']: len(m['anchors']) for m in
                          self.d['classes'][PREFIX + MESSAGE + '.class']['methods']},
                         {'<init>': 9, 'read': 8, 'write': 10, 'handle': 75})
        a = self.anchors(MESSAGE, 'handle')
        self.symbol(a, 8, 'ACNetworkContext.getSender:')
        self.symbol(a, 15, 'ACNetworkContext.isClientSide:')
        self.symbol(a, 39, 'entityId:I')
        self.symbol(a, 42, 'Level.getEntity:(I)')
        self.symbol(a, 47, 'LivingEntity')
        self.op(a, 50, 'ifeq', '179')
        self.symbol(a, 70, 'InteractionHand.MAIN_HAND:')
        self.symbol(a, 81, 'ItemStack.is:(Lnet/minecraft/world/item/Item;)')
        self.op(a, 84, 'ifeq', '100')
        self.op(a, 97, 'goto', '129')
        self.symbol(a, 102, 'InteractionHand.OFF_HAND:')
        self.symbol(a, 113, 'ItemStack.is:(Lnet/minecraft/world/item/Item;)')
        self.symbol(a, 143, 'UpdatesStackTags')
        self.symbol(a, 158, 'ACCompat.getTag:')
        self.op(a, 161, 'ifnull', '179')
        self.symbol(a, 174, 'UpdatesStackTags.updateTagFromServer:')
        self.assertFalse(any('getUUID:' in v['symbol'] or 'sameItemSame' in v['symbol']
                             for v in a.values()))
        default = self.anchors(UPDATES, 'updateTagFromServer')
        self.assertEqual(len(default), 4)
        self.op(default, 0, 'aload_2')
        self.op(default, 1, 'aload_3')
        self.symbol(default, 2, 'ACCompat.setTag:')

    def test_packaged_marker_consumers_modify_alliance_and_targeting(self):
        a = self.anchors(ILLAGER, 'ac_isAlliedTo')
        self.assertEqual(len(a), 14)
        self.symbol(a, 4, 'isPossessed:')
        self.op(a, 7, 'ifne', '21')
        self.op(a, 11, 'ifnull', '29')
        self.symbol(a, 15, 'isPossessed:')
        self.op(a, 18, 'ifeq', '29')
        self.op(a, 22, 'iconst_0')
        self.symbol(a, 26, 'CallbackInfoReturnable.setReturnValue:')
        a = self.anchors(LIVING, 'ac_onSetLastHurtByMob')
        self.assertEqual(len(a), 28)
        self.symbol(a, 1, 'entity/raid/Raider')
        self.op(a, 4, 'ifeq', '62')
        self.symbol(a, 28, 'entity/monster/AbstractIllager')
        self.symbol(a, 35, 'isPossessed:')
        self.op(a, 38, 'ifeq', '62')
        self.symbol(a, 43, 'entity/Mob')
        self.symbol(a, 59, 'Mob.setTarget:')
        for owner in (ILLAGER, LIVING):
            helper = self.anchors(owner, 'isPossessed')
            self.assertEqual(len(helper), 5)
            self.symbol(helper, 1, 'ACCompat.getPersistentData:')
            self.symbol(helper, 4, 'String TotemPossessed')
            self.symbol(helper, 6, 'ACCompat.getBoolean:')

    def test_exact_registry_and_default_true_config_are_bounded_windows(self):
        a = self.anchors(REGISTRY, '<clinit>')
        self.assertEqual(set(a), {347, 350, 353})
        self.symbol(a, 347, 'String astral_transferring')
        self.symbol(a, 350, 'key:')
        self.symbol(a, 353, 'ASTRAL_TRANSFERRING:')
        key = self.anchors(REGISTRY, 'key')
        self.symbol(key, 0, 'Registries.ENCHANTMENT:')
        self.symbol(key, 3, 'String alexscaves')
        self.symbol(key, 9, 'ResourceKey.create:')
        a = self.anchors(ITEM_REGISTRY, '<clinit>')
        self.assertEqual(set(a), {2310, 2313, 2316, 2321, 2324})
        self.symbol(a, 2313, 'String totem_of_possession')
        self.symbol(a, 2316, 'InvokeDynamic #131:get:')
        self.symbol(a, 2324, 'TOTEM_OF_POSSESSION:')
        self.symbol(self.anchors(ITEM_REGISTRY, 'lambda$static$126'), 4,
                    'TotemOfPossessionItem."<init>":()V')
        config = self.anchors(CONFIG, '<init>')
        self.assertEqual(len(config), 10)
        self.assertEqual((min(config), max(config)), (668, 686))
        self.symbol(config, 675, 'String totem_of_possession_works_on_players')
        self.op(config, 682, 'iconst_1')
        self.symbol(config, 683, 'ModConfigSpec$Builder.define:')
        self.symbol(config, 686, 'totemOfPossessionPlayers:')
        acquire = self.anchors(TOTEM, 'acHurtEnemy')
        self.symbol(acquire, 7, 'RESISTS_TOTEM_OF_POSSESSION:')
        self.op(acquire, 13, 'ifne', '41')
        self.symbol(acquire, 26, 'totemOfPossessionPlayers:')
        self.op(acquire, 38, 'ifne', '69')

    def test_semantic_negative_missing_or_reversed_enclosing_server_guard(self):
        check = self.test_enclosing_server_guard_and_both_alliance_directions_bound_query
        self.mutated_manifest_must_fail(TOTEM, 'onUseTick', 655, check, remove=True)
        self.mutated_manifest_must_fail(TOTEM, 'onUseTick', 655, check, opcode='ifne')

    def test_semantic_negative_elapsed_modulo_and_strict_health(self):
        check = self.test_client_even_time_left_wear_is_distinct_from_elapsed_four_tick_transfer
        self.mutated_manifest_must_fail(TOTEM, 'onUseTick', 283, check, opcode='iadd')
        self.mutated_manifest_must_fail(TOTEM, 'onUseTick', 883, check, opcode='iconst_5')
        self.mutated_manifest_must_fail(
            TOTEM, 'onUseTick', 899,
            self.test_mob_only_strict_health_resistance_positive_level_and_candidate_loop,
            opcode='iflt')

    def test_semantic_negative_loop_break_or_overwritten_original_controlled_local(self):
        check = self.test_mob_only_strict_health_resistance_positive_level_and_candidate_loop
        self.mutated_manifest_must_fail(TOTEM, 'onUseTick', 1081, check, operand='1084')
        self.mutated_manifest_must_fail(TOTEM, 'onUseTick', 1051, check,
                                        opcode='astore', operand='5')

    def test_semantic_negative_invented_old_marker_cleanup_and_changed_snapshot_order(self):
        check = self.test_ordered_transfer_sets_new_marker_then_uuid_snapshot_tag_and_optional_sync
        self.mutated_manifest_must_fail(TOTEM, 'onUseTick', 1051, check,
                                        opcode='invokestatic', symbol='Method setPossessed:(Lnet/minecraft/world/entity/Entity;Z)V')
        self.mutated_manifest_must_fail(TOTEM, 'onUseTick', 951, check,
                                        symbol='Method ACCompat.setTag:(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/nbt/CompoundTag;)V')

    def test_semantic_negative_client_id_server_uuid_and_custom_data_copy(self):
        check = self.test_client_numeric_id_server_uuid_resolution_and_changed_id_broadcast
        self.mutated_manifest_must_fail(TOTEM, 'getControlledEntity', 85, check,
                                        symbol='Method net/minecraft/world/level/Level.getEntity:(I)Lnet/minecraft/world/entity/Entity;')
        self.mutated_manifest_must_fail(TOTEM, 'getControlledEntity', 51, check,
                                        symbol='Method net/minecraft/server/level/ServerLevel.getEntity:(Ljava/util/UUID;)Lnet/minecraft/world/entity/Entity;')
        self.mutated_manifest_must_fail(
            COMPAT, 'getTag', 20,
            self.test_custom_data_helpers_copy_and_commit_separate_from_entity_marker,
            symbol='Method net/minecraft/world/item/component/CustomData.getUnsafe:()Lnet/minecraft/nbt/CompoundTag;')

    def test_semantic_negative_packet_offhand_priority_and_unconditional_sync(self):
        self.mutated_manifest_must_fail(
            MESSAGE, 'handle', 97,
            self.test_packet_resolves_supplied_entity_prefers_mainhand_and_calls_default_tag_writer,
            operand='100')
        self.mutated_manifest_must_fail(
            TOTEM, 'updateEntityIdFromServer', 86,
            self.test_client_numeric_id_server_uuid_resolution_and_changed_id_broadcast,
            opcode='if_icmpne')

    def test_workflow_retains_one_download_eight_minutes_and_separate_report(self):
        workflow = (ROOT / '.github/workflows/alexscaves-1010-action-contracts.yml').read_text()
        self.assertEqual(workflow.count('curl --fail'), 1)
        self.assertIn('timeout-minutes: 8', workflow)
        self.assertEqual(workflow.count("'docs/qa/alexscaves_1010_astral_transferring_cards_test.py'"), 2)
        self.assertIn('python3 docs/qa/alexscaves_1010_astral_transferring_cards_test.py -v', workflow)
        self.assertIn('--profile astral_transferring', workflow)
        self.assertIn(SEAL, workflow)
        self.assertEqual(workflow.count('build/alexscaves-1010/astral-transferring-evidence.json'), 2)

    def test_card_preserves_historical_seals_and_static_runtime_boundary(self):
        for artifact in ('EXACT-ASTRAL-TRANSFERRING-1.0.10.json',
                         'EXACT-ASTRAL-TRANSFERRING-LIFECYCLE-1.0.10.json', SEAL):
            self.assertIn(artifact, self.card)
        for phrase in ('STATIC_TECHNICAL_CATALOG_ONLY', 'SHA_EXACT_BINARY_BEHAVIOR',
                       'NOT_TESTED', 'NOT_VERIFIED', 'NO_MUTATION'):
            self.assertIn(phrase, self.card)
        for forbidden in ('COMPLETE_PERK_READY', 'physical_qa=PASS', 'mutating_hook=VERIFIED'):
            self.assertNotIn(forbidden, self.card)

    def test_card_states_causal_limits_without_promoting_omitted_or_runtime_paths(self):
        claims = (
            '**254/478 instruções — PARTIAL**: `@0–39` (19), `@106–284` (83), '
            '`@651–655` (3), `@714–1084` (149)',
            '**224 instruções omitidas**: `@41–103` Detonating Death; '
            '`@286–648` rampa/navegação/movimento; `@658–711` partículas.',
            'A fronteira de seleção `@39` / `@106` omite inclusive `ifnull @41 → 106`; '
            'não é uma sequência linear selada',
            'níveis positivos forçados passam pelo mesmo predicado, '
            '**sem escala por nível ou chance aleatória própria de transferência** nesse ramo.',
            '**`5D` não é raio de cinco blocos**.',
            'Não existe comparação de distância para escolher o mais próximo nem `break` depois de uma troca.',
            'As gravações no UUID **não reatribuem a local 5**: candidatos posteriores no mesmo tick '
            'continuam sendo comparados ao **Mob original**, inclusive sua vida e relações.',
            'Ele **não limpa ali o marcador do controlado anterior**.',
            'o ramo de candidato Astral **não repete um teste independente dela antes de escrever o novo vínculo**.',
            'A instrução é **cliente**, não uma cobrança de durabilidade no servidor demonstrada por esta prova, '
            'e não conta transferências Astral.',
            'O handler inspecionado não contém teste explícito **`entityId == sender.id`**, '
            'nem identidade da mesma stack além do tipo de item.',
            'Aplicação e ordem reais dos mixins, eventos de outros mods, PvP e claims continuam não verificados.',
            'Setter, tag NBT, método chamável ou descriptor JVM observado **não é API mutadora estável**.',
            'Não se declara `onUseTick` integralmente coberto, CFG executado, '
            'engine-base reauditada ou provider integral certificado.',
            'Testes estáticos e mutações negativas verificam o contrato documental; '
            'não executam Minecraft nem homologam hooks.')
        for claim in claims:
            self.assertIn(claim, self.card)

    def test_semantic_negative_card_cannot_omit_cleanup_limit_or_promote_partial_coverage(self):
        original = self.card
        try:
            for old, new in (
                ('Ele **não limpa ali o marcador do controlado anterior**.', ''),
                ('**254/478 instruções — PARTIAL**', '**478/478 instruções — COMPLETE**'),
                ('**sem escala por nível ou chance aleatória própria de transferência**',
                 '**com escala por nível e chance própria de transferência**')):
                with self.subTest(claim=old):
                    self.assertIn(old, original)
                    self.card = original.replace(old, new)
                    with self.assertRaises(AssertionError):
                        self.test_card_states_causal_limits_without_promoting_omitted_or_runtime_paths()
        finally:
            self.card = original

    def test_semantic_negative_card_cannot_promote_physical_or_mutating_claims(self):
        original = self.card
        try:
            for claim in ('physical_qa=PASS', 'mutating_hook=VERIFIED', 'COMPLETE_PERK_READY'):
                with self.subTest(claim=claim):
                    self.card = original + '\n' + claim + '\n'
                    with self.assertRaises(AssertionError):
                        self.test_card_preserves_historical_seals_and_static_runtime_boundary()
        finally:
            self.card = original

    def test_static_certificate_and_dynamic_family_queue_preserve_runtime_limits(self):
        ledger = json.loads((ROOT / 'wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json').read_text())
        certificate = ledger['objects'][P.name + '/' + CARD]
        for key in ('claim_scope', 'evidence_grade', 'mutating_hook', 'physical_qa'):
            self.assertEqual(certificate[key], self.d[key])
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
        self.assertIn('astral_transferring', full)
        self.assertIn('astral_transferring', ids)
        self.assertNotIn('astral_transferring', partial)
        crosswalk = (P / 'ENCHANTMENT-PERK-CROSSWALK-1.0.10.md').read_text()
        self.assertIn('| ✅ | `alexscaves:astral_transferring`', crosswalk)
        for name, count in (('full', len(full)), ('partial', len(partial)),
                            ('existing', len(present & ids))):
            self.assertIn(f'individual_{name}_enchantment_dossiers={count}/{len(ids)}', crosswalk)
        self.assertEqual(len(full) + len(partial) + len(missing), len(ids))
        if missing:
            self.assertIn('A **próxima identidade em ordem alfabética** sem ficha individual é '
                          + f'`alexscaves:{missing[0]}`;', crosswalk)
        elif partial:
            self.assertIn(f'começando por `alexscaves:{partial[0]}`', crosswalk)
        else:
            self.assertNotIn('começando por `alexscaves:', crosswalk)
        self.assertEqual(ledger['known_rosters'][P.name]['total'], self.d['semantic_magic_roots'])
        self.assertNotIn(P.name, ledger['providers'])


if __name__ == '__main__':
    unittest.main()
