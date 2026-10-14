# Palette Shift

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:palette_shift`
- **Iron's school:** Eldritch
- **Levels:** 1
- **Minimum rarity:** Legendary
- **Cast type:** Instant
- **Cooldown:** 30 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source config

- `baseManaCost = 50`
- `manaCostPerLevel = 0`
- `baseSpellPower = 0`
- `spellPowerPerLevel = 0`
- `castTime = 0`
- `setAllowCrafting(false)`
- `requiresLearning() = false`

## Preconditions and effect

Casting is allowed only while a **Pastel Staff** is held in either hand. Otherwise the provider rejects the cast and sends an action-bar error.

A successful cast applies `Palette Reception` for **600 ticks / 30 s**.

Provider guide semantics: this is a latent Pastel Staff spell that makes the staff receive the color/affinity of the **next** spell cast. Palette Shift cannot color the staff by itself.

## Acquisition

This is an item-bound latent spell, not a normal craftable spell-scroll path. `setAllowCrafting(false)` and `requiresLearning=false` are exact source facts; other provider-internal ways the Pastel Staff exposes it remain owned by the item implementation.

## Deduplication

Occupies the **staff attunement / next-spell affinity capture** niche. It should not be interpreted as a generic Black Arcana school-conversion mechanic.

## Confidence

`SOURCE-PINNED ITEM-BOUND SPELL / FULL RUNTIME EQUIPMENT QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:palette_shift` → `SpellRegistry.reg("palette_shift", PaletteShift::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.paletteshift.PaletteShift`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/paletteshift/PaletteShift.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — fechamento das nove fichas (2026-10-14)

**Source:** [`paletteshift/PaletteShift.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/paletteshift/PaletteShift.java) · [`paletteshift/PaletteShiftReceptionEvent.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/paletteshift/PaletteShiftReceptionEvent.java).

- **Duas etapas e cancelamento:** `PaletteShift.checkPreCastConditions` requer `PastelStaff` na mão principal ou secundária, então `onCast` aplica `PALETTE_RECEPTION` por **600 ticks**. `PaletteShiftReceptionEvent.onSpellPreCast` roda em `EventPriority.HIGHEST`, ignora a própria Palette Shift e, quando o efeito está ativo, tenta gravar `SchoolType` e cor na(s) Pastel Staff(s) empunhada(s).
- **Consumo do próximo spell:** se ao menos um `PastelStaff` é modificado, o handler aplica efeitos de recepção, remove `PALETTE_RECEPTION` e chama **`event.setCanceled(true)`**, interrompendo o cast que forneceu a escola. Sem staff modificada, retorna sem consumir o efeito nesse handler.
- **QA:** order de prioridade dos hooks de `SpellPreCastEvent`, cooldown/mana do spell interceptado, duas mãos e cores de escolas de outros mods, re-login e expiração. Não liquidar como duas magias bem-sucedidas no BA.

🟡 Dossiê causal source-level; ⚠️ equivalência bytecode/JAR/config, PvP/claims e QA Survival/dedicated pendentes; ⛔ sem adapter Mastery/perks real. Black Arcana não apropria casts, mana ou efeitos do provider.
