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

## Source / clean-room

Nenhum repositório-fonte público controlado pelo publisher e pinável à build 1.0.8-fix foi localizado nas buscas executadas.

Por ser `All Rights Reserved`:

- nenhum bytecode é decompilado para copiar implementação;
- nenhuma classe/método/signature é inferida;
- nenhuma textura/modelo/som/texto é reutilizado;
- changelogs e descrição pública são usados somente como fatos comportamentais/editoriais para catálogo e deduplicação.

Uma eventual inspeção técnica do JAR para interoperabilidade exigiria o artefato exato e continuaria não autorizando cópia da implementação.

## Runtime stack relevante no pack atual

### Base/required publicamente

- Iron's Spells 'n Spellbooks `1.21.1-3.16.3` — presente; casting/school substrate;
- L_Ender's Cataclysm `3.33` — presente; publisher 1.21.1 marca como required;
- Apothic Attributes `2.10.1` — presente; publisher 1.21.1 marca como required.

### Optional/public compatibility

- Magic From the East / `iss_magicfromtheeast` `1.1.5` — presente; o publisher 1.0.8 o marca como opcional e diz que, quando presente, seus spells continuam disponíveis para Symmetry; registry/config activation exata permanece runtime-QA pending;
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

## Public inventory ceiling

Publisher current page:

- `over 50 new spells`;
- Lightning / Fire / Aqua / Symmetry como famílias principais;
- `1 Blood` e `1 Ender` na descrição geral;
- uma `charge` por elemento, com integrações para outros elementos/addons.

Esse texto não permite reconstruir:

- count exato;
- registry IDs;
- current school assignment de todos os spells;
- min/max level / rarity;
- mana/cooldown/cast type;
- formulas de damage/heal;
- acquisition tables;
- item/block/entity/effect registries;
- config defaults completos;
- networking/persistence;
- supported API/hooks.

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

`EXACT ARTIFACT PINNED / PUBLISHER RELEASE-LINE SURFACE ADVANCED / COMPLETE REGISTRY+API UNKNOWN / T.O AQUA COEXISTENCE QA-BLOCKED / ARR CLEAN-ROOM / FAIL-CLOSED`.