#!/usr/bin/env python3
"""Bind the Arrow Inducting singleton to native guards, lifecycle, and honest limits."""
from pathlib import Path
import unittest
import json

from alexscaves_1010_action_contract_audit import load_manifest, validate_cards, validate_structure

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / 'wiki/modpack-catalog/providers/✅-alexs-caves-continued'
PREFIX = 'com/github/alexmodguy/alexscaves/'
CARD = 'enchantments/arrow-inducting.md'
SEAL = 'EXACT-ARROW-INDUCTING-CONTRACT-1.0.10.json'
EVENT = 'server/event/CommonEvents'
ARROW = 'server/entity/item/SeekingArrowEntity'
SHIELD = 'server/item/ResistorShieldItem'
ARROW_ITEM = 'server/item/SeekingArrowItem'
COMPAT = 'server/misc/ACCompat'
REGISTRY = 'server/enchantment/ACEnchantmentRegistry'
ITEM_REGISTRY = 'server/item/ACItemRegistry'
ENTITY_REGISTRY = 'server/entity/ACEntityRegistry'
LIVING_CTOR = '(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;)V'
TYPE_CTOR = '(Lnet/minecraft/world/entity/EntityType;Lnet/minecraft/world/level/Level;)V'


class ArrowInductingContract(unittest.TestCase):
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

    def test_literal_singleton_scope_roster_and_seal(self):
        validate_structure(self.d, profile='arrow_inducting')
        validate_cards(self.d, P, profile='arrow_inducting')
        self.assertEqual(self.d['catalog_family'], 'ARROW_INDUCTING_ENCHANTMENT_CONTRACT')
        self.assertEqual(set(self.d['cards']), {CARD})
        self.assertEqual(set(self.d['contract_evidence']), {CARD})
        self.assertEqual(set(self.d['classes']), {PREFIX + n + '.class' for n in (
            EVENT, ARROW, SHIELD, ARROW_ITEM, COMPAT, REGISTRY, ITEM_REGISTRY, ENTITY_REGISTRY)})
        methods = [m for entry in self.d['classes'].values() for m in entry['methods']]
        self.assertEqual((len(methods), sum(len(m['anchors']) for m in methods)), (49, 947))
        self.assertTrue(all(1 <= len(m['anchors']) <= 256 for m in methods))
        self.assertLessEqual(sum(len(m['anchors']) for m in methods), 8192)
        self.assertEqual(self.d['claim_scope'], 'STATIC_TECHNICAL_CATALOG_ONLY')
        self.assertEqual(self.d['evidence_grade'], 'SHA_EXACT_BINARY_BEHAVIOR')
        self.assertEqual(self.d['mutating_hook'], 'NOT_VERIFIED')
        self.assertEqual(self.d['physical_qa'], 'NOT_TESTED')
        self.assertEqual(self.d['semantic_magic_roots'], 8)
        self.assertIs(self.d['provider_universe_closed'], False)

    def test_exact_resource_roster_and_native_item_recipe_separation(self):
        self.assertEqual(set(self.d['resources']), {
            'META-INF/neoforge.mods.toml', 'assets/alexscaves/lang/en_us.json',
            'assets/alexscaves/lang/pt_br.json',
            'data/alexscaves/enchantment/arrow_inducting.json',
            'data/alexscaves/tags/item/enchantable/resistor_shield.json',
            'data/alexscaves/recipe/resistor_shield.json',
            'data/alexscaves/recipe/seeking_arrow.json',
            *('data/minecraft/tags/enchantment/' + t + '.json' for t in (
                'in_enchanting_table', 'non_treasure', 'on_random_loot', 'tradeable'))})
        for path, expected in (
            ('data/alexscaves/enchantment/arrow_inducting.json',
             '80d52e42318ad732b32ba6118dea8f5b315b8d2d702da32d202ff95246a973e5'),
            ('data/alexscaves/tags/item/enchantable/resistor_shield.json',
             '2b5d57ffc709293f994b472c07cd44ed34647efec41106b819621c060366f3e0'),
            ('data/alexscaves/recipe/resistor_shield.json',
             '2d2c648cc1db20b024ba3643c4e3c281b270039299d32ea8a3e9b8e8262f77af'),
            ('data/alexscaves/recipe/seeking_arrow.json',
             'e5fd8fe020f1cbab2fa360bcc644e32b4cd0be82a73018e036c38b505847ae6d')):
            self.assertEqual(self.d['resources'][path], expected)
        for t in ('in_enchanting_table', 'non_treasure', 'on_random_loot', 'tradeable'):
            self.assertEqual(self.d['resources']['data/minecraft/tags/enchantment/' + t + '.json'],
                             '6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1')

    def test_all_thirteen_arrow_executable_methods_include_static_initializer(self):
        methods = self.d['classes'][PREFIX + ARROW + '.class']['methods']
        self.assertEqual(len(methods), 13)
        self.assertEqual(sorted((m['name'], len(m['anchors'])) for m in methods), sorted((
            ('<clinit>', 5), ('<init>', 5), ('<init>', 15), ('<init>', 17),
            ('defineSynchedData', 10), ('getAddEntityPacket', 4), ('tick', 185),
            ('doPostHurtEffects', 4), ('getDefaultPickupItem', 7), ('getArcTowardsID', 7),
            ('setArcTowardsID', 7), ('getDefaultHitGroundSoundEvent', 4), ('lambda$tick$0', 4))))
        names = {m['name'] for m in methods}
        self.assertFalse(names & {'onHitEntity', 'onHitBlock', 'addAdditionalSaveData',
                                  'readAdditionalSaveData', 'setBaseDamage', 'getBaseDamage'})
        init = self.anchors(ARROW, '<clinit>')
        self.assertIn('EntityDataSerializers.INT:', init[2]['symbol'])
        self.assertIn('SynchedEntityData.defineId:', init[5]['symbol'])
        self.assertIn('ARC_TOWARDS_ENTITY_ID:', init[8]['symbol'])

    def test_five_conversion_guards_bind_actual_use_item_and_positive_level(self):
        a = self.anchors(EVENT, 'acLivingAttack')
        self.assertEqual(len(a), 91)
        for call, expected in ((4, 'DamageSource.getDirectEntity:'), (9, 'AbstractArrow'),
                               (24, 'LivingEntity.isBlocking:'), (34, 'LivingEntity.getUseItem:'),
                               (37, 'ACItemRegistry.RESISTOR_SHIELD:'), (48, 'ItemStack.is:'),
                               (58, 'LivingEntity.getUseItem:'), (63, 'ARROW_INDUCTING:'),
                               (66, 'ACCompat.enchantLevel:'), (76, 'ACEntityRegistry.SEEKING_ARROW:')):
            self.assertIn(expected, a[call]['symbol'])
        self.assertEqual([(a[o]['opcode'], a[o]['operand']) for o in (12, 27, 51, 69, 84)],
                         [('ifeq', '158'), ('ifeq', '158'), ('ifeq', '158'),
                          ('ifle', '158'), ('if_acmpeq', '158')])
        reader = self.anchors(COMPAT, 'enchantLevel')
        self.assertEqual(len(reader), 24)
        self.assertIn('ItemStack.getEnchantments:', reader[1]['symbol'])
        self.assertIn('Holder.is:', reader[42]['symbol'])
        self.assertEqual((reader[56]['opcode'], reader[60]['opcode']), ('ireturn', 'iconst_0'))
        self.assertFalse(any('clamp' in v['symbol'] for v in reader.values()))

    def test_conversion_attempt_passes_defender_then_drops_spawn_result_before_discard(self):
        a = self.anchors(EVENT, 'acLivingAttack')
        self.assertIn('getEntity:', a[99]['symbol'])
        self.assertIn('SeekingArrowEntity."<init>":' + LIVING_CTOR, a[102]['symbol'])
        self.assertIn('copyPosition:', a[110]['symbol'])
        self.assertEqual(a[119]['symbol'], 'double -0.4d')
        self.assertIn('Vec3.scale:', a[122]['symbol'])
        self.assertIn('setDeltaMovement:', a[125]['symbol'])
        self.assertEqual(a[134]['symbol'], 'float 180.0f')
        self.assertEqual(a[137]['opcode'], 'fadd')
        self.assertIn('setYRot:', a[138]['symbol'])
        self.assertIn('Level.addFreshEntity:', a[150]['symbol'])
        self.assertEqual(a[153]['opcode'], 'pop')
        self.assertIn('AbstractArrow.discard:', a[155]['symbol'])
        self.assertFalse(any('hurtAndBreak' in v['symbol'] or 'setCanceled:' in v['symbol']
                             for v in a.values()))
        self.assertFalse(any(v['opcode'] == 'ireturn' for o, v in a.items() if o < 158))
        wrapper = self.anchors(EVENT, 'livingAttack')
        self.assertEqual(len(wrapper), 8)
        self.assertIn('acLivingAttack:', wrapper[2]['symbol'])
        self.assertEqual((wrapper[5]['opcode'], wrapper[5]['operand']), ('ifeq', '13'))
        self.assertIn('setCanceled:(Z)V', wrapper[10]['symbol'])

    def test_constructor_owner_routes_and_synced_sentinel_are_explicit(self):
        a = self.anchors(ARROW, '<init>', LIVING_CTOR)
        self.assertEqual(len(a), 15)
        self.assertIn('ACEntityRegistry.SEEKING_ARROW:', a[1]['symbol'])
        self.assertIn('ACItemRegistry.SEEKING_ARROW:', a[18]['symbol'])
        self.assertEqual((a[12]['opcode'], a[13]['opcode'], a[32]['opcode']),
                         ('aload_2', 'aload_1', 'aconst_null'))
        self.assertIn('AbstractArrow."<init>":(Lnet/minecraft/world/entity/EntityType;'
                      'Lnet/minecraft/world/entity/LivingEntity;', a[33]['symbol'])
        coordinate = self.anchors(ARROW, '<init>', '(Lnet/minecraft/world/level/Level;DDD)V')
        self.assertEqual(len(coordinate), 17)
        self.assertNotIn('LivingEntity', coordinate[37]['symbol'])
        sync = self.anchors(ARROW, 'defineSynchedData')
        self.assertIn('AbstractArrow.defineSynchedData:', sync[2]['symbol'])
        self.assertEqual(sync[9]['opcode'], 'iconst_m1')
        self.assertIn('Builder.define:', sync[13]['symbol'])
        setter = self.anchors(ARROW, 'setArcTowardsID')
        self.assertIn('SynchedEntityData.set:', setter[11]['symbol'])

    def test_selection_server_gate_strict_nearest_and_candidate_side_alliance(self):
        a = self.anchors(ARROW, 'tick')
        self.assertEqual(len(a), 185)
        self.assertIn('AbstractArrow.tick:', a[1]['symbol'])
        self.assertEqual([(a[o]['opcode'], a[o]['operand']) for o in (13, 20, 25, 35)],
                         [('ifne', '272'), ('ifne', '272'), ('if_icmpne', '194'), ('ifne', '272')])
        self.assertEqual((a[45]['operand'], a[47]['opcode'], a[52]['opcode'], a[53]['opcode']),
                         ('10', 'iconst_3', 'iconst_4', 'idiv'))
        self.assertIn('Math.min:(II)I', a[55]['symbol'])
        self.assertIn('AABB.inflate:(D)', a[73]['symbol'])
        self.assertEqual((a[130]['opcode'], a[130]['operand']), ('ifge', '158'))
        self.assertIn('ownedBy:', a[136]['symbol'])
        self.assertEqual((a[143]['opcode'], a[143]['operand']), ('ifnull', '155'))
        self.assertEqual((a[146]['operand'], a[148]['opcode']), ('6', 'aload_3'))
        self.assertIn('Entity.isAlliedTo:', a[149]['symbol'])
        predicate = self.anchors(ARROW, 'lambda$tick$0')
        self.assertEqual(len(predicate), 4)
        self.assertIn('canHitEntity:', predicate[2]['symbol'])

    def test_lock_has_no_same_tick_steering_and_stale_id_has_no_reacquire(self):
        a = self.anchors(ARROW, 'tick')
        self.assertEqual((a[177]['symbol'], a[179]['opcode']), ('float 5.0f', 'fconst_1'))
        self.assertIn('setArcTowardsID:', a[188]['symbol'])
        self.assertEqual((a[191]['opcode'], a[191]['operand']), ('goto', '272'))
        self.assertIn('Level.getEntity:(I)', a[199]['symbol'])
        self.assertEqual((a[204]['opcode'], a[204]['operand']), ('ifnull', '272'))
        follow = {o: v for o, v in a.items() if 194 <= o <= 269}
        for absent in ('setArcTowardsID:', 'getOwner:', 'isAlliedTo:', 'isClientSide:', 'canHitEntity:'):
            self.assertFalse(any(absent in v['symbol'] for v in follow.values()), absent)
        self.assertEqual(a[212]['symbol'], 'float 0.65f')
        self.assertEqual((a[242]['opcode'], a[242]['operand']), ('ifle', '272'))
        self.assertEqual((a[250]['symbol'], a[260]['symbol']),
                         ('double 0.30000001192092896d', 'double 0.699999988079071d'))
        self.assertEqual([o for o, v in follow.items() if 'Vec3.normalize:' in v['symbol']], [257])
        self.assertIn('setDeltaMovement:', a[269]['symbol'])
        self.assertIn('Level.isClientSide:', a[276]['symbol'])
        self.assertIn('Level.addParticle:', a[391]['symbol'])

    def test_post_hurt_flag_and_native_pickup_sound_do_not_become_damage_formula(self):
        a = self.anchors(ARROW, 'doPostHurtEffects')
        self.assertEqual([(o, v['opcode']) for o, v in a.items()],
                         [(0, 'aload_0'), (1, 'iconst_1'), (2, 'putfield'), (5, 'return')])
        self.assertIn('stopSeeking:Z', a[2]['symbol'])
        self.assertIn('ACItemRegistry.SEEKING_ARROW:', self.anchors(ARROW, 'getDefaultPickupItem')[4]['symbol'])
        self.assertIn('ACSoundRegistry.SEEKING_ARROW_HIT:',
                      self.anchors(ARROW, 'getDefaultHitGroundSoundEvent')[0]['symbol'])
        self.assertIn('ACPlatform.getEntitySpawningPacket:',
                      self.anchors(ARROW, 'getAddEntityPacket')[2]['symbol'])
        create = self.anchors(ARROW_ITEM, 'createArrow')
        self.assertEqual(len(create), 6)
        self.assertIn('SeekingArrowEntity."<init>":' + LIVING_CTOR, create[6]['symbol'])

    def test_shield_item_properties_use_wrapper_and_separate_tenth_tick_cost(self):
        ctor = self.anchors(SHIELD, '<init>')
        self.assertEqual((ctor[8]['opcode'], ctor[12]['operand']), ('iconst_1', '1000'))
        self.assertIn('Rarity.UNCOMMON:', ctor[18]['symbol'])
        self.assertEqual(self.anchors(SHIELD, 'getEnchantmentValue')[0]['opcode'], 'iconst_1')
        self.assertEqual((self.anchors(SHIELD, 'isEnchantable')[5]['opcode'],
                          self.anchors(SHIELD, 'isEnchantable')[5]['operand']), ('if_icmpne', '12'))
        use = self.anchors(SHIELD, 'use')
        self.assertIn('Player.startUsingItem:', use[9]['symbol'])
        self.assertIn('setPolarity:', use[34]['symbol'])
        self.assertIn('ACCompat.useConsume:', use[54]['symbol'])
        self.assertIn('InteractionResultHolder.consume:', self.anchors(COMPAT, 'useConsume')[1]['symbol'])
        tick = self.anchors(SHIELD, 'onUseTick')
        self.assertEqual((len(tick), min(tick), max(tick)), (143, 0, 604))
        self.assertFalse(any(67 <= o <= 362 for o in tick))
        self.assertEqual((tick[586]['operand'], tick[588]['opcode'], tick[588]['operand']),
                         ('10', 'if_icmpne', '604'))
        self.assertEqual((tick[595]['opcode'], tick[595]['operand']), ('ifne', '604'))
        self.assertEqual(tick[599]['opcode'], 'iconst_1')
        self.assertIn('hurtAndBreakUsedHand:', tick[601]['symbol'])
        helper = self.anchors(COMPAT, 'hurtAndBreakUsedHand')
        self.assertIn('LivingEntity.getUsedItemHand:', helper[4]['symbol'])
        self.assertIn('ItemStack.hurtAndBreak:', helper[10]['symbol'])

    def test_registry_windows_bind_both_items_and_half_block_native_entity(self):
        registry = self.anchors(REGISTRY, '<clinit>')
        self.assertEqual(set(registry), {108, 110, 113})
        self.assertEqual(registry[108]['symbol'], 'String arrow_inducting')
        self.assertIn('ARROW_INDUCTING:', registry[113]['symbol'])
        items = self.anchors(ITEM_REGISTRY, '<clinit>')
        self.assertEqual(set(items), {610, 613, 616, 621, 624, 644, 647, 650, 655, 658})
        self.assertEqual((items[613]['symbol'], items[647]['symbol']),
                         ('String seeking_arrow', 'String resistor_shield'))
        self.assertIn('SeekingArrowItem."<init>":', self.anchors(ITEM_REGISTRY, 'lambda$static$18')[4]['symbol'])
        self.assertIn('ResistorShieldItem."<init>":', self.anchors(ITEM_REGISTRY, 'lambda$static$20')[4]['symbol'])
        entity = self.anchors(ENTITY_REGISTRY, '<clinit>')
        self.assertEqual(set(entity), {211, 214, 217, 222, 225})
        self.assertIn('SEEKING_ARROW:', entity[225]['symbol'])
        factory = self.anchors(ENTITY_REGISTRY, 'lambda$static$11')
        self.assertEqual((factory[11]['symbol'], factory[14]['symbol']), ('float 0.5f', 'float 0.5f'))
        self.assertIn('Builder.sized:(FF)', factory[17]['symbol'])
        self.assertEqual((factory[20]['opcode'], factory[24]['opcode']), ('iconst_1', 'iconst_1'))
        self.assertIn('setUpdateInterval:', factory[21]['symbol'])
        self.assertIn('setShouldReceiveVelocityUpdates:', factory[25]['symbol'])

    def test_workflow_keeps_one_download_eight_minutes_and_exports_separate_report(self):
        workflow = (ROOT / '.github/workflows/alexscaves-1010-action-contracts.yml').read_text()
        self.assertEqual(workflow.count('curl --fail'), 1)
        self.assertIn('timeout-minutes: 8', workflow)
        self.assertEqual(workflow.count("'docs/qa/alexscaves_1010_arrow_inducting_cards_test.py'"), 2)
        self.assertIn('python3 docs/qa/alexscaves_1010_arrow_inducting_cards_test.py -v', workflow)
        self.assertIn('--profile arrow_inducting', workflow)
        self.assertIn(SEAL, workflow)
        self.assertEqual(workflow.count('build/alexscaves-1010/arrow-inducting-evidence.json'), 2)
        self.assertNotIn('alexscaves-1.0.10.jar\n            build/', workflow)

    def test_card_links_preserved_evidence_and_distinguishes_engine_from_physical_qa(self):
        for name in ('EXACT-ARROW-INDUCTING-1.0.10.json',
                     'EXACT-ARROW-INDUCTING-LIFECYCLE-ROSTER-1.0.10.json',
                     'EXACT-ARROW-INDUCTING-CAUSAL-FLOW-1.0.10.json',
                     'EXACT-ARROW-INDUCTING-INHERITED-ENGINE-1.0.10.json', SEAL):
            self.assertIn(name, self.card)
        for phrase in ('STATIC_TECHNICAL_CATALOG_ONLY', 'SHA_EXACT_BINARY_BEHAVIOR',
                       'NOT_TESTED', 'NOT_VERIFIED', 'NO_MUTATION',
                       'universo integral do provider permanece aberto', '1.21.1', '21.1.248'):
            self.assertIn(phrase, self.card)
        for forbidden in ('COMPLETE_PERK_READY', 'physical_qa=PASS', 'mutating_hook=VERIFIED'):
            self.assertNotIn(forbidden, self.card)


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
        self.assertIn('arrow_inducting', full)
        self.assertIn('arrow_inducting', ids)
        crosswalk = (P / 'ENCHANTMENT-PERK-CROSSWALK-1.0.10.md').read_text()
        self.assertIn('| ✅ | `alexscaves:arrow_inducting`', crosswalk)
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
