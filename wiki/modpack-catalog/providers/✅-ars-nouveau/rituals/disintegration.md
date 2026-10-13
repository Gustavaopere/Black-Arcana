# Disintegration

Status: `SOURCE-PINNED 5.13.1 / HOSTILE-ENTITY PROCESSING RITUAL`

- Registry id: `ars_nouveau:ritual_disintegration`
- Class: `RitualDisintegration`
- Source cost declaration: `300`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

Every `60` game ticks on the server, Disintegration scans LivingEntities inside an AABB inflated by `5.0` blocks around the ritual. Eligible targets are monsters or entities in Ars Nouveau's disintegration whitelist, excluding players and the provider blacklist.

Eligible targets are discarded rather than killed through a normal damage path. Removed mobs do not drop normal items. When an entity reports XP reward, the ritual doubles that XP value and converts it into Ars Nouveau experience gems (`GREATER_EXPERIENCE_GEM` and `EXPERIENCE_GEM`).

## Source-consumption mismatch

The provider description says Source is consumed each time a monster is destroyed. In the pinned executable path, however, `setNeedsSource(true)` is reached only when at least one removed entity also produced an XP value greater than zero (`didWorkOnce`). The code does not increment that flag once per removed mob.

This is recorded as `SOURCE DESCRIPTION ↔ EXECUTABLE PATH MISMATCH / RUNTIME QA REQUIRED`; Black Arcana must not choose a preferred interpretation.

## Authority / Black Arcana boundary

Removal, XP conversion, Source accounting and experience-gem spawning remain Ars Nouveau authority. Black Arcana must not replay removal/rewards or grant normal death-proc chains for a provider action that explicitly discards entities.

Any observation for Arcane Danger/mastery must preserve one ritual causal identity rather than one action per converted entity.

## QA

Source is pinned to 5.13.1; the exact effective Source settlement and interaction with death/drop event consumers require runtime validation.

## Dossiê de implementação para perks — ritual exato

- **Classe fonte:** [`RitualDisintegration.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualDisintegration.java), fonte `112920ff774831f204031da75b4c4e73d3765157` para Ars 5.13.1.
- **Amostragem:** a cada `60` ticks de jogo no servidor percorre `LivingEntity` em AABB `inflate(5.0)`; exige classificação MONSTER ou `DISINTEGRATION_WHITELIST`, exclui Players e `DISINTEGRATION_BLACKLIST`.
- **Efeito:** usa `remove(Entity.RemovalReason.DISCARDED)`, **não** `hurt/kill`. Se entidade removida reporta `shouldDropExperience` e XP calculado >0, dobra a XP e gera `GREATER_EXPERIENCE_GEM` (grupos de 12) e `EXPERIENCE_GEM` (grupos de 3 com arredondamento para cima para resto); sem drops normais.
- **Ressalva de Source:** `setNeedsSource(true)` ocorre depois de `didWorkOnce`, que só é marcado com XP positiva convertida; a descrição pública diz custo por monstro. Não tratar como prova de taxa de Source por entidade; preservar a discrepância e pedir QA físico. `getSourceCost=300` é declaração, não prova da frequência da cobrança.
- **Perks:** Ritual completion/progress e conversões são provider-owned; não disparar death perks em entidades apenas descartadas.
- **Mutabilidade externa:** ⛔ nenhum adapter RPG provado que altere lifecycle, Source ou raio sem duplicar settlement; 🟡 fórmula/lógica source-pinned; ⚠️ runtime, receitas/config física, addons e Survival pendentes.
