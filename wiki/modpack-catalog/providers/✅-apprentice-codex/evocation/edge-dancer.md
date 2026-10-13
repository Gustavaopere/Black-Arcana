# Edge Dancer

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:edge_dancer`
- **Iron's school:** Evocation
- **Levels:** 1
- **Minimum rarity:** Epic
- **Cast type:** Long
- **Cooldown:** 30 s
- **Resource:** Iron's mana
- **Ordinary crafting:** disabled
- **Ordinary looting:** disabled
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 100`
- `baseManaCost = 50`
- `manaCostPerLevel = 0`
- `castTime = 40 ticks`
- duration: `round(20 * 60 * spellPower / 100)` ticks
- recast count: `2`
- first activation requires a provider `SpellSideEdge` in the main hand

## Provider lifecycle

The initial server cast activates `EdgeDancerManager`; recasting while provider recast state is active deactivates it. The spell is deliberately unavailable through ordinary crafting and loot and requires its provider-specific weapon surface.

Greater Conjurer's Talisman can alter provider cooldown behavior on deactivation/timeout. That remains Iron's/Apprentice authority.

## Causality and progression

The stance/equipment session is one spell activation. Weapon strikes performed while Edge Dancer is active are not automatically additional spell casts. A combat bridge must attribute them through a real provider/combat seam and deduplicate against ordinary melee progression.

## Deduplication

Occupies the **Spell Side Edge-gated timed Evocation weapon/stance session with recast deactivation** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CONFIG+DURATION FORMULA+ITEM GATE+RECAST / EDGE DANCER MANAGER COMBAT MODIFIERS REQUIRE MANAGER AUDIT`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:edge_dancer` → `SpellRegistry.reg("edge_dancer", EdgeDancer::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.edgedancer.EdgeDancer`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/edgedancer/EdgeDancer.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.
