# Ace's Spell Utils 1.2.7.2 — provider catalog

Status: `EXACT PHYSICAL VERSION / EXACT OFFICIAL SOURCE VERSION PIN / LIBRARY+RUNTIME PROVIDER / 0 STANDALONE SPELL REGISTRATIONS / CATALOG CLOSED AT SOURCE EVIDENCE CEILING / BINARY+HOST QA FAIL-CLOSED`

## Installed identity

- JAR: `aces_spell_utils-1.2.7.2-1.21.1.jar`
- mod id: `aces_spell_utils`
- runtime: `1.2.7.2-1.21.1`
- Minecraft / loader: `1.21.1` / NeoForge
- physical SHA-1: `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`
- CurseForge project/file: `1299492 / 8789930`
- exact release date: `2026-09-02`
- license: MIT
- provider class: `IRON'S ADDON UTILITY API + SHARED RUNTIME SURFACES`

Physical modlist/JAR metadata remains authority for the installed artifact. Publisher metadata confirms the same public release filename/version. Official source is pinned at `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, whose `gradle.properties` declares exactly `mod_version=1.2.7.2-1.21.1`.

This is an exact **source-version pin**, not a claim that the inspected source tree was independently proven byte-for-byte identical to the physical JAR.

## What this component is

Ace's Spell Utils is primarily an API/library for Iron's Spells 'n Spellbooks addons. Its current source exposes reusable entity, item, attribute, school, VFX, boss/music, summon and domain helpers plus shared event-driven runtime behavior.

It is **not** treated as a standalone player spell pack. Search of the exact source revision finds no `registerSpell(...)` call and no provider spell-registry registration surface. `AbstractSummonSpell` and `ExampleSummonSpell` are helper/example classes, not provider-owned registered spells.

Therefore the complete current standalone spell inventory for this component is:

**0 registered standalone spells.**

## Exact source registry surface

At the exact source revision:

- 3 Iron's `SchoolType` registrations: `aces_spell_utils:ritual`, `aces_spell_utils:hydro`, `aces_spell_utils:technomancy`;
- 19 attributes: 13 general runtime attributes + 6 school power/resistance attributes;
- 3 damage-type keys: `ritual_magic`, `hydro_magic`, `technomancy_magic`;
- 1 serialized/copy-on-death attachment: `keep_inv_on_death`;
- 1 custom particle type: `trail`;
- 14 tag contracts: 9 item, 3 entity, 2 spell tags;
- 8 extended `Rarity` entries;
- 27 `example_*` item registry entries;
- 8 optional protocol `4.0.0` play-to-client VFX payloads;
- 2 required server mixins;
- 5 common config values.

See the dedicated registry/runtime documents for exact identities and authority boundaries.

## School naming correction

Current registry identity is authoritative over comments/variable names:

- `aces_spell_utils:ritual` uses translation key `school.aces_spell_utils.ritual`; publisher UI currently describes this school as **Occult**. There is no separate current `aces_spell_utils:occult` SchoolType registration in the exact source.
- `aces_spell_utils:hydro` is the actual registry ID. The Java supplier is named `ABYSSAL` and carries an old `// Abyssal` comment, but the ResourceLocation, translation key, attributes, focus tag and damage type are all Hydro. Do not manufacture an `aces_spell_utils:abyssal` school from the stale source symbol/comment.
- `aces_spell_utils:technomancy` is direct.

## Example-content boundary

`ExampleItemRegistry.register(...)` runs regardless of production/dev mode, so 27 example item IDs are real source registrations. Only the custom creative tab is gated to non-production. Ten example items are explicitly listed in `c:hidden_from_recipe_viewers`; the rest must not be assumed absent just because they are examples.

For Black Arcana catalog semantics these items are classified as **API examples/support objects**, not 27 new spell/capability identities.

## Host-version boundary

Exact source metadata targets NeoForge `21.1.230` and Iron's `1.21.1-3.11.0`. The physical Black Arcana pack uses NeoForge `21.1.248` and Iron's `1.21.1-3.16.3`.

That mismatch does not erase the exact source-version inventory, but exact runtime compatibility, event ordering and API signature parity against the newer host stack remain QA/fail-closed. No adapter should bind to an internal signature solely because it exists in this source revision.

## Black Arcana authority

Ace's Spell Utils owns the shared behaviors that its attributes, item helpers, mixins, attachments and provider API implement. Iron's remains authority for its spell casting/mana/cooldown substrate.

Black Arcana must not:

- create a second Mana Steal/Mana Rend/Hunger Steal/Evasive/crit/recovery processing path for provider-owned state;
- reinterpret provider `ritual`, `hydro` or `technomancy` as Black Arcana spell domains;
- reuse `AbstractDomainEntity` as a second Black Arcana domain/casting pipeline;
- double-run passive ability proc handlers, magic-gun cast initiation, keep-inventory behavior or provider VFX transport;
- convert helper/example objects into semantic spell counts;
- transfer Black Arcana runtime authority to RPG Skill Tree.

Black Arcana Corruption, Strain, Arcane Danger, casting pipeline and destructive `WorldEffectPolicy` remain Black Arcana-owned.

## Fichas individuais indexadas — lote alfabético de 27/10/2026

**🟡 Em implementação:** 19 atributos registrados em [`attributes/`](attributes/INDEX.md) e 3 escolas `SchoolType` em [`schools/`](schools/INDEX.md) foram materializados em **22 fichas técnicas individuais**, cada uma com ID, registros, parâmetros conhecidos, targeting, fluxo consumidor ou limites, fonte da release `1.2.7.2-1.21.1` e QA pendente. [Índice do provider](INDEX.md).

Esses objetos eram previamente conhecidos no inventário agregado; **não** representam 22 magias novas. Continuam **0 spells standalone**, e as demais famílias de sistemas/itens/API descritas nos dossiês agregados ainda precisam de desmembramento, evidência e reconciliação para fechar o escopo total de Ace. O lote **não** altera a certificação estática: `0/22` das fichas agora detectadas possuem manifesto `COMPLETE_PERK_READY`; há requisitos físicos e de integração ainda não verificados.

**Correção de build-host:** [`build.gradle` na fonte pinada](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/build.gradle) fixa `io.redspace:irons_spellbooks:1.21.1-3.16.2` na dependência efetiva; a propriedade `irons_spells_version=1.21.1-3.11.0` em `gradle.properties` está obsoleta nesse local de build. A linha do modpack registrada é `3.16.3`; não há prova de compatibilidade runtime em assemble. [Análise causal dos eventos](SOURCE-1.2.7.2-COMBAT-CAUSALITY-AND-DOUBLE-SETTLEMENT-20261027.md).

**Sem promoção alfabética:** `ALPHABETICAL-CATALOG-STATUS.json` continua apontando Ace como o segundo provider pendente. A prova source-pinned não substitui testes no host/JAR nem cataloga os sistemas compartilhados restantes.

## Sistemas compartilhados — fichas individuais (27/10/2026)

**🟡 14/14 famílias deste recorte** foram desmembradas em [`systems/`](systems/INDEX.md): domínio/clash, base de summon/recast, mobs conjuradores animados, bosses/fases/música, AI combos, keep-inventory, curios com imbuement, curios passivos/sheaths, spellbooks passivos, staves, espadas com API ativa/passiva, magic gun casting, mace/mace-staffs e transporte visual de payloads. São **famílias de classes**, não 14 spell registrations; não são prova de completude de todos os helper classes do provider.

Ao lado dos [19 atributos](attributes/INDEX.md) e [três escolas](schools/INDEX.md), o recorte tem **36 fichas individuais candidatas, 0 certificadas**. O índice de perks é **`0/36`**; o contador semântico do Ace continua **0 spells standalone**. Os riscos source-level identificados incluem `TicketType.FORCED` em domínio, equip/trigger/cooldown delegado a subclasses, preservação de inventário em clone/death e VFX **somente cliente**. Os demais registros menores (tags, damage types, attachment, rarities, examples, partículas, configs e seus consumers) permanecem documentados nos inventários agregados e não devem ser presumidos integralmente desmembrados.

Nenhuma ficha deste lote estabelece paridade compilada de JAR, contrato mutador verificado no Iron's 3.16.3 ou QA física. **A fila alfabética continua em Ace's Spell Utils**, não em Acolyte, até revisão do restante e resolução transparente dos gates. Nenhuma Stage foi promovida.

## Catalog files

- [REGISTRIES-AND-ATTRIBUTES.md](REGISTRIES-AND-ATTRIBUTES.md)
- [API-AND-RUNTIME-SURFACES.md](API-AND-RUNTIME-SURFACES.md)
- [NETWORK-MIXINS-AND-EXAMPLES.md](NETWORK-MIXINS-AND-EXAMPLES.md)
- [EVIDENCE-AND-PROVENANCE.md](EVIDENCE-AND-PROVENANCE.md)

## Evidence ceiling

Closed for catalog/deduplication:

- installed identity/version/hash;
- exact official source version;
- complete provider registry identities listed above;
- zero standalone spell registrations at the source pin;
- reusable API/runtime families and provider-owned event/mixin surfaces;
- example-item classification;
- source-level config/network contracts.

Still fail-closed for runtime integration:

- independent source↔physical-JAR byte equivalence;
- exact behavior on the pack's newer Iron's/NeoForge versions;
- cross-mod event ordering with every other installed attribute/proc provider;
- stable public API guarantees beyond what the publisher/source explicitly exposes;
- full-modpack client/dedicated-server interaction QA.
