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

## Certificação técnica estática — hostile removal and XP conversion (25/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** Fonte fixada [RitualDisintegration.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualDisintegration.java) de `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; ID `ars_nouveau:ritual_disintegration` / classe `RitualDisintegration` comprovados no JAR 5.13.1 SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` **apenas quanto ao registro estático**.

| Campo para perks | Fluxo fonte e risco |
|---|---|
| Timing/targeting | Servidor, a cada `world.getGameTime()%60==0`; busca `LivingEntity` em `new AABB(getPos()).inflate(5.0)`, seleciona `m.getClassification(false).equals(MobCategory.MONSTER)` **ou** `DISINTEGRATION_WHITELIST`, mas exclui `Player` e qualquer `DISINTEGRATION_BLACKLIST` antes do efeito. Alvos são AABB, não esfera/raycast. |
| Remoção, não dano | Para cada alvo chama `m.remove(Entity.RemovalReason.DISCARDED)` e só após `m.isRemoved()` emite `spawnPoof`. Não chama `hurt`, `kill` nem DamageType; não há evidência de morte normal, loot ou death-perks, e não se deve tratar visual ou descarte como kill/XP de combate. |
| Conversão XP | Condicional `m.shouldDropExperience()`, seguida de `exp=m.getExperienceReward((ServerLevel)world,null)*2`. Se `exp>0`, calcula `numGreater=exp/12`, subtrai grupos de 12; `numLesser=expRemaining/3`, **arredonda para cima** se há resto positivo. Cria `ItemEntity` de `ItemsRegistry.GREATER_EXPERIENCE_GEM` e/ou `EXPERIENCE_GEM` se respectivas contagens forem positivas. O teto de grupos de 3 **pode gerar valor de gemas superior ao dobro exato do XP original**, dependendo da equivalência de XP das gemas (não comprovada só pelo nome). |
| Custo e discrepância | `didWorkOnce` fica true **somente** no caminho de `exp>0` dentro de `shouldDropExperience` e `isRemoved`, não em toda remoção. `setNeedsSource(true)` ocorre **uma vez ao final de cada ciclo** com conversão positiva, `getSourceCost()=300`. A descrição diz cobrar por monstro destruído: **discrepância textual/source**; não declarar 300 Source por monstro, XP convertida, partículas ou remoção. |
| Profundidade de integração | `remove(DISCARDED)` pode contornar observadores de morte que dependem de dano/loot; não duplicar entidades, gemas, XP ou Mastery com base em ticks/itens. RPG Skill Tree só provê progressão por boundary real; Arcane Danger e WorldEffectPolicy do Black Arcana permanecem aplicáveis ao próprio runtime, não reclassificam automaticamente o ritual Ars. |
| Segurança/QA | Validar config de tags, `getExperienceReward` por mob, XP gem values, custos reais do brazier, comportamento após unload/reload, entidade imune/modded, XP sem drop, duplicação em multiplayer e respeito ao servidor. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. |

**Gate fail-closed:** não permitir transmutação de dano/drops/XP ou progressão automática sem mutator/source settlement real, orçamento por mob e deduplicação comprovados.
