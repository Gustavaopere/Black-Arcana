# Ars Morph 2.0.0

## Gate de restauração Identity2 — bytecode físico (17/10/2026)

A auditoria do [JAR publisher Identity2 2.2.4 #39077751784](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39077751784) confirmou `PASS_DIRECT_RESTORE_BOUNDED`: a função compilada `IdentityProgression.restoreMorphFromSavedData(ServerPlayer)` chama `EntityAccessor.setCurrentIdentity` sem chamar `IdentityProgression.morph` **dentro do mesmo método**. Foram aprovados 8/8 + 6/6 autotestes sintéticos no job, com SHA-1 publisher `84c222df0176d7ef83ba7cc361249fe062e29218` confirmado. Artefato de evidência [#12117184517](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39077751784/artifacts/12117184517).

[**Matriz de ingressos e protocolo de teste de revogação/restauração**](IDENTITY2-MORPH-INGRESS-RESTORE-QA-2.2.4.md): requisição C2S, comando, morph automático por kill, transformação diária, `clearMorph`, `morph(minecraft:player)` e restore de NBT comparados com o `IdentityProgressionMixin` presente no RPG Skill Tree. **⚠️ A assinatura e a chamada direta não provam bypass em gameplay nem ausência de controles no caller.** Após respec, relog ou respawn, os resultados reais ainda exigem QA com player conectado. ⛔ Nenhuma perk/cooldown/Mastery homologados; runtime de Black Arcana, RPG e Identity2 permanecem separados.

## Gate de morph do RPG Skill Tree — fonte e publisher (17/10/2026)

A `main` do sibling [RPG Skill Tree](https://github.com/Gustavaopere/neoforge-rpg-skilltree/tree/ed5b65b890767b406ce41127bcb793775263c7bd) já define um `IdentityProgressionMixin` opcional que, no início de `IdentityProgression.morph(ServerPlayer,ResourceLocation,CompoundTag)`, tenta impedir transformações não autorizadas por `MorphIdentityAccess.canMorph`. O publisher Identity2 `2.2.4` para NeoForge 1.21.1 passou à prova do descriptor exato dessa assinatura e dos quatro métodos de cooldown no [workflow Java21 #39075958128](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39075958128): **8/8 autotestes, SHA-1 publisher válido, `PASS_BOUNDED_SIGNATURES`, sem desvios**. [Dossiê causal completo](IDENTITY2-ABILITY-COOLDOWN-SOURCE-BRACKET-2.2.4.md).

**⚠️ A existência do Mixin no código, a assinatura no JAR publicado e o resultado do workflow não comprovam sua aplicação efetiva ao runtime do pack**, nem autorizam redutores de cooldown. O próprio sibling mantém documentação antiga que não descreve a injeção atual, exigindo reconciliar o contrato pelo código e testes de jogador conectado. Sem novos spells/adapters Black Arcana.

## Auditoria do JAR publicado Identity2 — 17/10/2026

**✅ Publisher SHA-1 conferido e quatro métodos inspecionados por bytecode delimitado:** [Java21 #39075533394](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39075533394), Identity2 `2.2.4` NeoForge `1.21.1`, CurseForge `1238155/8792744`, SHA-1 `84c222df0176d7ef83ba7cc361249fe062e29218`. Foram registrados `PASS_BOUNDED_SIGNATURES`, zero desvios e seis autotestes de fail-closed. [Dossiê com detalhes e limites](IDENTITY2-ABILITY-COOLDOWN-SOURCE-BRACKET-2.2.4.md). **⚠️ Paridade do JAR instalado, runtime de cooldown, emissão de efeitos/settlement e contratos de hooks permanecem pendentes.** A evidência anterior `SOURCE_BRACKET` está preservada como contexto histórico, não status atual único. 0 magias novas e 0 adapters homologados.

## Verificação dos cooldowns no Identity2 — 17/10/2026

Avançou a [auditoria dos contadores do host Identity2 2.2.4](IDENTITY2-ABILITY-COOLDOWN-SOURCE-BRACKET-2.2.4.md), fonte oficial `xGabou/Identity2` em dois snapshots que delimitam o release 2.2.4: 27/05/2026 e 02/10/2026 (o segundo declara 2.2.4.1). O servidor executa `max(0,cooldown+useduration)`, decremente a cada `baseTick`, recusa primário se contador positivo e registra cooldown **antes** do callback. Os sete contadores derivados são **120/820/900/120/420/220/160 ticks**, na ordem Weald Walker/Wilden Hunter/Wilden Stalker/Starbuncle/Whirlisprig/Wixie/Firenando. Não confundir com duração real dos efeitos e passivos.

**⚠️ Evidência SOURCE_BRACKET, não verificação do bytecode instalado.** O JAR Identity2 2.2.4 do modpack não foi comparado; versões de código não têm blobs integrais idênticos. Prioridade de QA: Wixie crouch poderá falhar após registro de cooldown, resolver Ars cancelado poderá não executar após consumir contador; validar no pack. Nenhum hook de redução individual de cooldown ou refund foi homologado, e nenhum objeto mágico novo foi contado.

## Engenharia causal das habilidades Identity2 — 17/10/2026

**✅ 7/7 implementações Java** de habilidade Identity2 possuem [fichas individuais em `abilities/`](abilities/) com código-fonte fixo, eventos, target, movimento, projetéis, status, tempo, passivos, riscos e QA. Os **11/11 arquivos JSON de atribuições** foram ligados às respectivas fichas; há cinco variantes Weald Walker compartilhando um único `predef`. [Matriz de integração e barras](ABILITY-PERK-CAUSAL-MATRIX-2.0.0.md). O glifo `ars_morph:glyph_morph` permanece 1/1 independente; **+0 novas identidades de magia**. O registro source-aligned é `Alexthw46/Ars-Morph@4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58`, sem paridade do código com JAR instalada.

**Achados para perks:** Wixie sorteia índice 0–11 para tabela de apenas dez efeitos no ramo agachado (risco source de index out of bounds, não crash físico reproduzido); Whirlisprig executa Grow+AOE×3 e Jump Boost passivo; Wilden Stalker sincroniza `isFlying` no servidor; Firenando projeta homing com filtro `Enemy`, condicionado a Ars Elemental; Wilden Hunter remove Summoning Sickness após `postEvent` não cancelado; Starbuncle aplica Speed 3000 ticks. Os campos Identity2 `cooldown`/`use_duration` são valores brutos e **suas unidades não foram certificadas no host instalado**.

**Barras:** GLOBAL —% (piso 1.857 / 1.855 estritos, denominador global aberto); ARS MORPH 7/7 fichas Java e 11/11 assignments (documentação 100%), glyph 1/1, ⚠️ runtime/cooldowns/permissões pendentes, ⛔ 0 adapters homologados. Stage 06.05 🟡, Stage 09 físico pendente; PR #825 draft.

Status: `PHASE 2X — SOURCE CATALOG CLOSED / INSTALLED RUNTIME QA OPEN`

## Exact installed identity

- Mod id: `ars_morph`
- Physical JAR: `ars_morph-1.21.1-2.0.0.jar`
- Runtime version: `2.0.0`
- Physical SHA-1 / Modrinth hash: `68ff47cc58c0ffe9570bb907f65c2910311ed45f`
- CurseForge hash: `1937242939`
- Loader/game: NeoForge 1.21.1
- Pack NeoForge: `21.1.248`
- Required physical morph provider: Identity2 `2.2.4`
- Current physical Ars host: Ars Nouveau `5.13.1`
- Current physical optional Ars host: Ars Elemental `0.7.10.1`
- Physical support library: Gabou's Libs `1.8.7`
- Phase 2 class: `ARS GLYPH / IDENTITY2 COMPATIBILITY PROVIDER`

Physical modlist/JAR identity is authoritative for installed presence/version. The current Notion row labels `Estado no pack: Removido`, but the physical modlist contains the JAR; Phase 2X therefore treats Ars Morph as installed and the property as stale.

## Release-aligned source checkpoint

Provider source used read-only:

`Alexthw46/Ars-Morph@4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58`

This is the head of upstream branch `1.21.1-v2` on 2026-06-12. Its `gradle.properties` declares `mod_version=2.0.0`, and the publisher's 2.0.0 NeoForge 1.21.1 file was released on the same date. Phase 2X therefore classifies it as `RELEASE-ALIGNED`, not byte-identical: the installed JAR was not extracted/rebuilt and compared byte-for-byte.

The upstream checkpoint builds against:

- NeoForge `21.1.219`;
- Ars Nouveau `5.11.1.1289`;
- Ars Elemental `0.7.9.3.168`;
- Identity2 NeoForge `2.1.1.1` through CurseForge file `8153522`;
- Gabou's Libs `1.4` through CurseForge file `7195722`;
- Sauce `0.0.40.82` as a compile-only seam.

The physical pack is newer on Ars, Ars Elemental, Identity2 and Gabou's Libs. Source-catalog completeness does not imply current-host runtime compatibility PASS.

## Provider role and authority

Ars Morph does not own the player's morph state. Identity2 owns identity acquisition/state, variants, ability dispatch and the `morph`/`clearMorph` operations. Ars Nouveau owns spell grammar, spell context/resolvers, glyph learning and Ars entity behavior. Ars Elemental owns its optional entities and spell behavior.

Ars Morph owns only the bridge it adds:

- one Ars glyph that requests Identity2 morph operations;
- Identity2 builtin ability adapters for Ars entities;
- Identity2 variant adapters for Ars/Ars Elemental entities;
- Identity2 entity-capability tags for supported Ars forms;
- one Wilden Stalker morph-tick synchronization seam.

Black Arcana must not create a parallel identity ledger, unlock list, variant serializer or replacement morph pipeline.

## Closed source catalog surface

### Glyph — 1/1

[`GLYPH-MORPH.md`](GLYPH-MORPH.md) closes the only registered spell part:

- `ars_morph:glyph_morph` / Morph;
- Tier II;
- 200 Ars mana;
- Conjuration;
- no compatible augments;
- server-only mutation path through Identity2;
- Mob Jar → Spawn Egg → struck EntityType selection precedence;
- player-target and self-clear semantics;
- strict max-health gate;
- FamiliarEntity rejection;
- Ars `IDecoratable` cosmetic-copy seam.

### Identity2 abilities

[`ABILITIES.md`](ABILITIES.md) closes 7 Java ability adapters and their 11 committed data assignments:

- Weald Walker;
- Wilden Hunter;
- Wilden Stalker;
- Starbuncle;
- Whirlisprig;
- Wixie;
- optional Ars Elemental Firenando.

The Java adapters reuse Ars spell/effect/entity pipelines. Identity2 data owns cooldown/use-duration assignments; those child Ars resolver executions are descendants of one provider ability action and must not be independently replayed by Black Arcana/RPG systems.

### Variants and passive form tags

[`VARIANTS-TAGS.md`](VARIANTS-TAGS.md) closes:

- 5 Ars Nouveau variant adapters;
- 3 optional Ars Elemental variant adapters;
- 6 additive Identity2 entity-type tags;
- exact persistent/variant fields represented by each adapter;
- optional-provider data entries using `required:false`.

### Acquisition

[`ACQUISITION.md`](ACQUISITION.md) records the single committed generated glyph recipe: Conjuration Essence + Abjuration Essence + two `ars_nouveau:wilden_drop` tag ingredients, 55 XP.

### Mixins/network/config

[`MIXIN-NETWORK-BOUNDARIES.md`](MIXIN-NETWORK-BOUNDARIES.md) records:

- 0 common mixins;
- 0 client mixins;
- no Ars Morph-owned custom payload registration identified in the exact source tree;
- `IdentityApi.syncBoolean(..., "isFlying", ...)` is a call into the Identity2 provider contract, not an Ars Morph protocol;
- the standalone `MorphConfig.COMMON` spec is empty and its registration is commented out;
- `max_hp_morph` is a glyph config value built by `EffectMorph` through the Ars spell-part configuration path.

## Critical source observations

1. `max_hp_morph` default is 100, minimum 20, maximum `Integer.MAX_VALUE`; the executable check is strict `<`, so a candidate whose max health equals the configured limit is rejected.
2. When a struck living target is another `ServerPlayer`, that player is the morph recipient. When the struck living entity is not a player, the caster is the recipient.
3. A player target resolving to `EntityType.PLAYER` calls Identity2 `clearMorph` instead of setting a new morph.
4. A valid offhand Ars Mob Jar takes selection precedence; a Spawn Egg is consulted only when the selected type still equals the struck living entity's type.
5. The source creates a candidate entity and passes serialized NBT to Identity2. Black Arcana must not construct a second independent morph representation.
6. Wixie has a source-risk in its crouching branch: the selected good-effect table has 10 entries, but the random index is always bounded by the 12-entry bad-effect table. This is recorded as a runtime-reproduction hypothesis, not a confirmed installed crash.
7. `MorphEffect` exists in source and would clear Identity2 morph on removal, but `ModRegistry` is empty and no registration/use of this effect is present in the audited production path. It is not counted as active provider content.

## Provenance

The exact checkpoint contains conflicting code-license signals:

- `neoforge.mods.toml`: GNU Lesser General Public License v3.0;
- root `LICENSE`: GNU General Public License v3 text.

The publisher page identifies LGPLv3, but the repository conflict is not resolved by inference. Phase 2X uses source read-only for factual compatibility/deduplication evidence and copies/adapts no implementation or asset. Any future derivation remains fail-closed until exact licensing/provenance is reconciled.

## Remaining validation

- extract/inspect the installed Ars Morph JAR and compare packaged source/data/config surfaces;
- boot client and dedicated server with physical Identity2 2.2.4, Gabou's Libs 1.8.7, Ars 5.13.1 and Ars Elemental 0.7.10.1;
- validate glyph learning and all Mob Jar/Spawn Egg/target-selection paths;
- validate strict max-health boundary below/equal/above configured value;
- validate player-target morph/clear behavior and permission/friendly-target consequences in multiplayer;
- validate FamiliarEntity rejection and cosmetic-item transfer;
- validate all builtin ability assignments/cooldowns and provider event cancellation behavior;
- reproduce or refute the Wixie crouching index-risk;
- validate 8 variant adapters and 6 Identity2 tags under current host versions;
- validate Wilden Stalker `isFlying` sync across login/dimension/death/respawn;
- verify optional Ars Elemental classloading/data behavior when that provider is present and when absent;
- verify no `MorphEffect` registration exists in the packaged installed artifact;
- full-pack conflict test against other morph/scale/combat systems.

None of these installed-runtime checks are reported as PASS by Phase 2X.

## Dossiê individual de engenharia de perks — Morph 1/1

- ✅ Novo arquivo [glyphs/morph.md](glyphs/morph.md) com `EffectMorph` 2.0.0, fonte versionada, gate `isRealPlayer`, seleção via MobJar/SpawnEgg, strict HP limit e servidor→Identity2. [Matriz de engenharia 2.0.0](PERK-ENGINEERING-MATRIX-2.0.0.md).
- ⚠️ Source release-aligned e registry 1/1 não demonstram compatibilidade runtime com Identity2 2.2.4 ou permissões PvP; ⛔ nenhum adapter RPG/Black Arcana. O arquivo é dossiê adicional, não uma magia adicional.
