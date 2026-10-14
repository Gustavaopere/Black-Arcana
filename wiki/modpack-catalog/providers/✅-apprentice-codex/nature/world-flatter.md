# World Flatter

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:world_flatter`
- **School:** Nature
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Continuous
- **Cooldown:** 20 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 50`
- `baseManaCost = 10`
- `manaCostPerLevel = 5`
- `castTime = 200 ticks / 10 s`
- block target range: **8 blocks**

Raw combat damage:

`3 + 2 * spellPower / 100`

then multiplied by `DamageMultiplierKey.WORLD_FLATTER`.

Entity reach:

`8 + 4 * spellPower / 100` blocks.

Armor-penetration/reduction tier:

- amplifier = `min(3, max(0, floor(spellPower / 200)))`;
- displayed armor-reduction percent = `(amplifier + 1) * 20`, bounded by implementation to 20–80% across amplifier values.

Base break speed:

`4 * spellPower / 100`

with optional provider Craftsman's Delight break-speed bonus.

## Tool semantics

Without Craftsman's Delight, the provider uses an **Iron Pickaxe / Iron tier** as the dummy tool/harvest baseline. With the accessory equipped it upgrades that baseline to **Netherite Pickaxe / Netherite tier** and may copy eligible main-hand enchantments.

The spell targets a valid living entity first; otherwise it resolves a provider-approved breakable block through outlined/raycast target paths. `WorldFlatterDrillEntity.canBreakTarget(...)` owns the block eligibility check.

## What it does

Provider guide semantics: summons a magical drill that pierces enemies through armor and, when aimed into the ground, excavates a large hole.

## World safety

The drill entity is authoritative for actual break scheduling/protection/drop behavior. Black Arcana must not replay or widen those breaks. Black Arcana-originated excavation remains subject to `WorldEffectPolicy`.

## Deduplication

Occupies the **armor-penetrating magical drill + terrain excavation** niche.

## Confidence

`SOURCE-PINNED SPELL + TOOL/TIER INPUT / DRILL BREAK JOB + PROTECTION/DROP QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:world_flatter` → `SpellRegistry.reg("world_flatter", WorldFlatter::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.worldflatter.WorldFlatter`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/worldflatter/WorldFlatter.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

---

## Engenharia causal aprofundada — lote persistente 0.9.7.1

**Classes verificadas:** [`worldflatter/WorldFlatter.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/worldflatter/WorldFlatter.java) · [`worldflatter/WorldFlatterDrillEntity.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/worldflatter/WorldFlatterDrillEntity.java). Source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` declarado 0.9.7.1; **não** há prova de equivalência bytecode dos métodos com o JAR físico da modlist. A inspeção não é um QA provider-native.

### Execução e integridade

- **Channel e duplo targeting:** `WorldFlatter.onCastNoWeapon` instancia `WorldFlatterDrillEntity` e `onCastTickWithWeapon` atualiza seu target; target de bloco (alcance client indicado de 8) e de `LivingEntity` são tratados por caminhos distintos, com state de perfuração no drill. Os ticks da ferramenta não geram roots adicionais.
- **Progresso da mineração:** `WorldFlatterDrillEntity.processBlockBreak` revalida `breakCenterPos`, normal da superfície, state representativo e hardness. Progresso aumenta `toolSpeed/(hardness*30)` (ou 1 para dureza 0), sincroniza cracks e, quando `breakProgress>=1`, só prossegue com `owner instanceof ServerPlayer`.
- **Plano limitado:** `collectBreakableBlocks` percorre offsets `-1..1` nos dois eixos do plano paralelo à face, máximo **9 posições**. `canBreakTarget` exige estado não ar, tag de pickaxe ou shovel, dureza >=0, bloqueia minério que não corresponde ao bloco representativo, e exige dummy tool correto onde `requiresCorrectToolForDrops`. Antes de cada quebra repete a validação; `BlockTools.breakBlockByPlayerHands` aplica ação do player provider-native.
- **Riscos:** não assumir proteção plena de claim pelo conjunto de tags; preciso testar proteção de terceiros, updates de block state durante channel, ferramenta efetiva, enchantments, offhand, PvP em alvo vivo, limites TPS e world effects. Black Arcana não quebra os nove blocos outra vez nem concede Mastery por cada progresso de crack.

### Interoperabilidade e QA

**Raiz contável:** `apprenticecodex:world_flatter`, já presente nas 83 spells. Efeitos secundários/ticks/entidades continuam provider-owned (Iron's/Apprentice's). **⛔** RPG Skill Tree só pode oferecer progressão/atributos/gates via contrato real; nenhum adapter de perks/Mastery foi implementado. Black Arcana não reexecuta nem debita recursos/cooldowns do provider. **⚠️** Persistem QA físico, modpack Survival, server+client, config, multiplayer, claims, lifecycle NBT e método de JAR. Stage 06.05 sem promoção.

[Matriz técnica da etapa](../PERK-ENGINEERING-MATRIX-PERSISTENT-0.9.7.1.md).
