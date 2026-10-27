# Spirit — ISS: Magic From The East 1.1.5

Status: `✅ 11/11 COUNTED_EXACT STATIC REGISTRY; RUNTIME/SURVIVAL ⚠️`

[Dossiê físico 1.1.5](../EXACT-BINARY-SPELLS-1.1.5.md) e [Java21 #38449995162](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38449995162): 11 IDs/classes Spirit incondicionais e escola padrão confirmados; +0 novos.

Fonte candidata `RELEASE_BOUNDED_SOURCE` (sem equivalência integral com o JAR): `WarPhan78/ISS_MagicFromTheEast-1.21.x@f2a095cbbc89f8d8428dca758140663adf54ae88`.

**Dossiês deste lote: 11/11.** `████████████████████ 100.0%` editorial; certificação estrita **0/11**. [Contratos comuns](../SPELL-PERK-BOUNDARIES-1.1.5.md) e [reconciliação](../RELEASE-SOURCE-RECONCILIATION-1.1.5.md).

## Spells ativos

1. `soul_catalyst`
2. `soul_burst`
3. `spirit_challenging`
4. `bone_hands`
5. `calamity_cut`
6. `kitsune_pack`
7. `revenant_of_honor`
8. `ashigaru_squad`
9. `phantom_charge`
10. `anchoring_kunai`
11. `splitting_shuriken`

## Assinaturas mecânicas

Spirit ocupa um conjunto próprio de contracts: multi-projectile Soulburn, radial Soulburn burst, linked proxy damage por ExtractedSoul, summons persistentes com lifecycle Iron's, weapon-scaled line slash, pack de kitsunes sem ramo de alpha separado no cast da fonte candidata; a classe de alpha da fonte posterior não consta do JAR auditado, samurai summon, formação híbrida Ashigaru melee/ranged, cavalry wave, teleport-triggered soul anchor e hit-triggered radial projectile split.

Essas identidades devem ser tratadas como provider-native first. Black Arcana não deve recriar o mesmo outcome apenas com outro nome/VFX.

## Aquisição

O registry e as classes de spell auditadas neste passe não definem uma regra provider-specific suficiente para afirmar com precisão onde cada scroll/spell é aprendido ou obtido. Aquisição detalhada permanece `NÃO VERIFICADO` até o passe de loot/structure/trade/datagen do provider.
