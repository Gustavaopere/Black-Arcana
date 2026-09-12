# Somake Spells 1.0.8-fix — auditoria técnica/proveniência

## Artefato instalado

- JAR: `somakespells-1.0.8-1.21.1-fix.jar`
- Mod id: `somakespells`
- Runtime: `1.0.8`
- Mixin metadata observado na modlist: `somakespells.mixins.json`
- SHA-1 físico: `b0ad94c1504709662bee2d08700375ccecbb5ec7`
- Fingerprint registrado pela modlist: `3385290718`
- CurseForge Project: `1461634`
- CurseForge File: `8417850`
- Upload: `2026-07-12`
- Loader/game: NeoForge / 1.21.1
- Type: Release
- License: All Rights Reserved

A modlist física é authority para identidade/hashes instalados. O publisher CurseForge confirma File ID, filename, runtime line e release date.

## Exact fix delta

O changelog do File ID 8417850 é estreito: corrige as Elemental Charges de **Symmetry** e **Spirit**, que não estavam aplicando buffs.

Não há base para tratar o fix como novo registry snapshot publicado. Ele é a continuidade da release 1.0.8 base (File ID 8399369), cuja documentação fornece ritual/progression/spell changes.

## Phase 2BF exact-artifact facts

The exact File ID `8417850` was materialized from Curse Maven and required to match the physical SHA-1 `b0ad94c1504709662bee2d08700375ccecbb5ec7`. Read-only clean-room inspection establishes:

- `ModSpells` owns a `DeferredRegister<AbstractSpell>`;
- 67 typed `DeferredHolder<AbstractSpell, ...>` fields;
- 67 unique spell `register(String, Supplier)` calls / IDs;
- 67 standalone provider `*Spell` classes;
- 61 registrations are unconditional;
- `blessed_connection`, `guardian_connection`, `cursed_connection` are gated by `ModList.isLoaded("mowziesmobs")`;
- `mirror_strike`, `spirit_empowerment`, `symmetry_empowerment` are gated by `MagicFromTheEastCompat.isLoaded()`, which exactly calls `ModList.isLoaded("iss_magicfromtheeast")`;
- both optional mod IDs are present in the current physical pack, therefore 67/67 registry identities are active for this provider set.

The same exact artifact registers `Config.SPEC` as `ModConfig.Type.COMMON` at `somakespells/general/common.toml`. `enableSpellLockSystem` has code default `false`; when disabled, `PlayerSpellMastery.getUnlockedLevel()` returns `100`. If enabled, Somake's pre-cast path can cancel spell levels above provider mastery, and `/somake` command registration is gated by the same config with command permission level 2. The actual deployed COMMON config file/value is not available in the repository or supplied project files.

Therefore exact registry membership is closed, while current survival usability/acquisition remains `CONDITIONAL` and is not promoted into the strict semantic numerator.

## Source / clean-room

Nenhum repositório-fonte público controlado pelo publisher e pinável à build 1.0.8-fix foi localizado nas buscas executadas.

Por ser `All Rights Reserved`, a inspeção binária é estritamente clean-room e factual:

- o artefato exato foi hash-matched antes da inspeção;
- são retidos somente metadata/hash, paths/IDs de recursos e registry, signatures de classe/membro e fatos estreitos de control-flow/config necessários para interoperabilidade e catálogo;
- nenhuma implementação é copiada, reconstruída ou adaptada;
- nenhuma textura/modelo/som/texto upstream é reutilizado;
- changelogs/descrição pública continuam sendo evidência editorial/comportamental, não licença de derivação.

A inspeção técnica do JAR não autoriza cópia da implementação e não cria um contrato de API que o provider não publique.

## Runtime stack relevante no pack atual

### Base/required publicamente

- Iron's Spells 'n Spellbooks `1.21.1-3.16.3` — presente; casting/school substrate;
- L_Ender's Cataclysm `3.33` — presente; publisher 1.21.1 marca como required;
- Apothic Attributes `2.10.1` — presente; publisher 1.21.1 marca como required.

### Optional/public compatibility

- Magic From the East / `iss_magicfromtheeast` `1.1.5` — presente; o gate exato `MagicFromTheEastCompat.isLoaded()` testa esse mod id e ativa os três registros ISS-gated no pack atual; runtime mechanics/config continuam separados;
- Born in Chaos `1.7.6` — presente;
- GTBC's Geomancy Plus `1.1.0-1.21.1` — presente;
- Tunes 'n Tomes `1.1.0-HOTFIX` — presente;
- Mowzie's Mobs `1.8.2` — presente; 1.0.7 documentava gate para três Connection spells;
- Better Combat — não localizado na modlist atual.

### Coexistência com T.O Magic n' Extras

A modlist física também contém:

- `traveloptics-4.4.0.1-1.21.1.jar`;
- mod id `traveloptics`;
- runtime `4.4.0.1-1.21.1`;
- nome runtime `T.O Magic n' Extras`.

A página oficial atual de T.O Magic classifica essa build 1.21.1 como **`DEPRECATED DONT USE Alpha-4.4.0.1-1.21.1`**. Ao mesmo tempo, Somake diz que Aqua foi criado para suprir a ausência de T.O Magic 1.21.1 e que conteúdo Aqua seria migrado se T.O Magic atualizasse oficialmente.

Portanto o pack tem uma coexistência física real, mas isso **não** prova que a build alpha/deprecated de T.O Magic seja o destino de migração mencionado pelo Somake. A compatibilidade/ownership exata Aqua entre esses dois artefatos deve permanecer QA-blocked/fail-closed, não automaticamente transferida.

## CurseForge relation inconsistency

A página corrente do Somake descreve 1.21.1 assim:

- Cataclysm required;
- Apothic Attributes required;
- Magic From the East optional;
- Born in Chaos optional;
- Geomancy Plus optional;
- Tunes 'n Tomes optional.

A página genérica `relations/dependencies` ainda apresenta classificações que refletem estados anteriores e entram em conflito com o changelog 1.0.8. O changelog 1.0.8 declara explicitamente a remoção da obrigatoriedade de Magic From the East e Born in Chaos.

Para a linha 1.0.8, o catálogo usa a evidência mais específica/recente: current description + exact release changelog. A página de relações genérica não é usada para reintroduzir obrigatoriedade removida.

## Exact registry / remaining runtime ceiling

The old publisher-only `over 50 new spells` ceiling is superseded for registry identity by the exact artifact: **67 current registrations** under the physical optional-provider set. The publisher text remains useful for release semantics but not for registry totals.

The exact artifact audit still does not close:

- deployed `somakespells/general/common.toml` values;
- complete object-level survival acquisition/reachability;
- authoritative current school/runtime semantics for every identity;
- complete min/max level / rarity / mana / cooldown / cast-type tables;
- formulas de damage/heal;
- complete item/block/entity/effect inventories;
- stable supported integration API/hooks;
- networking/persistence contracts;
- Somake↔T.O Aqua runtime ownership on the dual-installed stack.

## Current contradiction requiring runtime QA

A descrição geral atual diz `1 Blood` e `1 Ender`, mas o changelog 1.0.8 nomeia múltiplos spells Blood (por exemplo Fragmented Requiem e The Rose's Secret), e 1.0.7 também nomeia Bloodmark/Cursed Connection. Isso mostra que o resumo `1 Blood / 1 Ender` não pode ser interpretado literalmente como total de registry atual sem contexto.

Consequência: **não usar a frase do projeto como count escolar exato**. Ela é descrição de escopo, enquanto changelogs demonstram que o conteúdo evoluiu.

## Gates para uma integração Black Arcana

Antes de qualquer adapter Somake-specific:

1. confirmar artefato exato/metadata em runtime;
2. identificar IDs reais das schools/spells/charges alvo;
3. identificar API/hook estável ou provider-native state exposure;
4. demonstrar server authority e causal owner;
5. testar configs e presença/ausência de optional providers;
6. testar coexistência real com `traveloptics` alpha/deprecated;
7. verificar deduplicação e impedir double-processing;
8. se não houver hook seguro, fail-closed.

## Estado

`EXACT HASH-MATCHED ARTIFACT / 67 CURRENT REGISTRY IDENTITIES CLOSED / EFFECTIVE COMMON CONFIG + SURVIVAL REACHABILITY UNVERIFIED / SEMANTIC CONDITIONAL +0 / T.O AQUA COEXISTENCE QA-BLOCKED / ARR CLEAN-ROOM / FAIL-CLOSED`.