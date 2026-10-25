# Ars Nouveau — Freeze

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_freeze`
- Display name: Freeze
- School: Elemental Water
- Default tier: 1
- Default mana cost: 15
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`), Amplify, AOE, Pierce, Sensitive
- Default Sensitive limit: 1
- Source config default Slow duration: 10 s
- Source config default Extend Time increment: 5 s

## Provider-native behavior

On living targets, Freeze applies vanilla Slowness. On blocks it can convert water to Ice (or Frosted Ice with Sensitive), lava to Obsidian/Cobblestone, extinguish fire, upgrade Ice to Packed Ice and Packed Ice to Blue Ice. AOE/Pierce expand the affected block set.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:water_essence` + `minecraft:snow_block` ×2.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this fluid/ice conversion and slowing primitive. Independent Black Arcana freezing/world mutation must remain `WorldEffectPolicy`-controlled and must not replay Ars conversions.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectFreeze`).

## Dossiê de engenharia para perks — causalidade exata

- **Código versionado:** [`EffectFreeze.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectFreeze.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectFreeze` no Ars 5.13.1, método `onResolveBlock`.
- **Geometria:** percorre `SpellUtil.calcAOEBlocks(... getAoeMultiplier(), count(Pierce))` e aplica `extinguishOrFreeze` **na posição e nas seis direções**; toda alteração pode propagar `ShapersFocus.tryPropagateBlockSpell`. **Mutações:** água acima → Ice/Frosted Ice com Sensitive; lava acima → Obsidian, flowing lava → Cobblestone; fogo acima é removido; Ice→Packed Ice→Blue Ice. **Entidades:** `applyConfigPotion(...MOVEMENT_SLOWDOWN)`; config default duração 10, Extend Time 5; Sensitive limit 1. **Risco:** não há claim check individual em `extinguishOrFreeze`, mas isso não demonstra ausência de admissão externa: verificar o resolver antes de tratar como vulnerabilidade. AOE×vizinhos requer cap.
- **Limite de integração:** ✅ source pin confirmado, ⚠️ config e classes auxiliares demandam QA; ⛔ hook de mutação RPG não verificado. Provider mantém autoridade de mana/efeito/owner; sem segundo cast/proc/settlement. Survival: PENDING.

## Auditoria do executor secundário — limitações verificáveis

- **Java:** [`api/util/SpellUtil.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/SpellUtil.java).
- **Helper de área `SpellUtil.calcAOEBlocks`:** quando recebe `SpellStats`, usa `aoeBonus=stats.getAoeMultiplier()` e `pierceBonus=count(Pierce)`; overload double calcula `width=(int)(1+floor(aoeBonus))`, `height=(int)(1+ceil(aoeBonus))`, `depth=1+pierceBonus`. A implementação monta a grade orientada pelo hit e inclui a origem. `EffectFreeze` ainda chama `extinguishOrFreeze` no centro **e em seis vizinhos** de cada célula, com possíveis overlaps. O número bruto de *tentativas* pode chegar a `7*|calcAOEBlocks|` antes de filtrar casos inválidos, não é número de blocos únicos alterados. Não há cap universal evidente nesse helper; validar limites de augments/config/execução.

**Limite:** fatos lidos do source pin, não prova de comportamento no JAR físico ou de adapter RPG. QA no modpack ainda pendente.

## Certificação estática por pipeline e consumidores — 25/10/2026

**✅ COMPLETE_PERK_READY apenas no escopo `STATIC_TECHNICAL_CATALOG_ONLY` — NÃO é certificação de perk jogável. ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** O ID e a classe no JAR publisher foram auditados separadamente da semântica lida no commit de source.

| Campo exigido | Contrato source-pinned, limites e classificação para perks |
|---|---|
| Identidade/versionamento | Ars Nouveau `5.13.1`; `ars_nouveau:glyph_freeze`; classe `EffectFreeze`; escola Elemental Water, tier I. [Source imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectFreeze.java) e [registry do publisher SHA-exato](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Comportamento, causalidade e settlement | `onResolveEntity` só aplica `MobEffects.MOVEMENT_SLOWDOWN` a LivingEntity via `IPotionEffect`. Em bloco, itera `SpellUtil.calcAOEBlocks(...)`, tenta `extinguishOrFreeze` no centro **e em cada uma das seis direções**, depois `ShapersFocus.tryPropagateBlockSpell` quando há posição modificada. O helper de mutation distingue water→Ice/Frosted Ice(Sensitive), source lava→Obsidian, flowing lava→Cobblestone, fogo removido, Ice→Packed Ice→Blue Ice. |
| Parâmetros, escalas e caps | Config default Slowness base **10 s**, bônus duration **5**; getters fallback sem config **30/8**. `IPotionEffect`: `ticks=20×base+bonus×stats.getDurationInTicks()`; amplifier `(int)ampMultiplier` para target vivo. `SpellUtil.calcAOEBlocks` usa `aoeMultiplier` e `count(Pierce)` para largura/altura/profundidade; para cada posição resultante podem existir **até sete tentativas** locais, com sobreposição e sem garantia de alteração; não são sete blocos únicos por célula. Limite default Sensitive **1**. |
| Targeting, geometria, projétil, tipo e duração | Entity target recebe Slowness, sem projeto/dano próprios; block target dá origem à grade orientada pelo hit e 6 vizinhos por posição. Modificações em água/fogo/ice são world mutation do provider, sem DamageType intrínseco. Claims e admissão antes do helper exigem prova no resolver, já que não há check local visível no método `extinguishOrFreeze`. |
| Custos, aprendizagem e limites da receita | Mana default **15**; tier I; XP receita default 27; starter default não; recipe `ars_nouveau:water_essence` + `minecraft:snow_block` ×2. [Acquisition 85/85](../../ACQUISITION.md). Cast/cooldown e mana efetiva da composição são autoridade/config Ars Nouveau. Augments: Extend Time, Reduce Time, Amplify, AOE, Pierce, Sensitive. Amplify pode alterar amplifier do Slowness; AOE/Pierce afetam grade do ramo de blocos. Sensitive apenas seleciona Frosted Ice em água na implementação vista; não extrapolar imunidade de mundo. |
| Integração e segurança | **⛔** Evitar varredura/amplificação de área sem budget e proteção; não replicar ShapersFocus nem reexecutar operações. Black Arcana world mutations devem passar por `WorldEffectPolicy` próprio; nenhuma ausência de claim check local constitui prova de exploit. Contrato de perks RPG Skill Tree e hook mutador para este caminho não verificados. Não trocar target, type, raio, mana nem recipients com API presumida. Black Arcana conserva seu runtime, hazards e `WorldEffectPolicy` para efeitos próprios. |
| Grau de evidência/testes | Source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; JAR publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` prova **ID/classe registrada**, não todos os métodos do classfile ou gameplay atual. Config final, order de eventos, integrações de outros mods, PvP/claims, servidor e cliente: **NOT_TESTED**. |

**Regra de reauditoria:** alterações de JAR/source, config, modificadores, geometria/ordem de eventos ou consumidor downstream exigem nova verificação técnica antes de liberar qualquer hook. Efeitos/raios/VFX não são eventos novos de cast/Mastery.
