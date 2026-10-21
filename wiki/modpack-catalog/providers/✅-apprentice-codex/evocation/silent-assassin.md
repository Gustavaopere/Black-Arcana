# Silent Assassin

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:silent_assassin`
- **Iron's school:** Evocation
- **Levels:** 1–3
- **Minimum rarity:** Epic
- **Cast type:** Long
- **Cooldown:** 16 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 100`
- `baseManaCost = 100`
- `manaCostPerLevel = 40`
- `castTime = 50 ticks`
- base damage: `10 * (spellPower / 100) * providerDamageMultiplier`
- headshot multiplier: `min(500, 100 + round(50 * spellPower / 100))%`
- unaware/sneak multiplier: `min(500, 100 + round(75 * spellPower / 100))%`
- range: **128 blocks**
- nearby-awareness suppression radius after a qualifying lethal unaware hit: **16 blocks**

## Provider lifecycle

The long cast summons/holds a rifle entity and continuously updates its reticle from provider-assisted aim. At completion the provider resolves the assisted raycast, determines headshot status, checks whether the target qualifies for the unaware bonus, applies the final damage once through the summoned weapon, then drives the visual hit result.

If an unaware-bonus shot is lethal, provider firearm logic may suppress nearby awareness within the fixed 16-block radius.

## Causality and progression

Headshot and unaware multipliers are modifiers on the same provider shot, not separate damage events for progression. Awareness suppression is a consequence of that shot and must not create additional offensive credit.

## Deduplication

Occupies the **very-long-range summoned sniper rifle with headshot and unaware-target multipliers plus stealth-kill awareness suppression** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CONFIG+DAMAGE+HEADSHOT+UNAWARE+RANGE / ASSISTED-AIM COLLISION AND AWARENESS AI DETAILS REQUIRE UTILITY/ENTITY QA`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:silent_assassin` → `SpellRegistry.reg("silent_assassin", SilentAssassin::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.silentassassin.SilentAssassin`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/silentassassin/SilentAssassin.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — armas conjuradas e efeitos derivados (2026-10-14)

**Registry ID:** `apprenticecodex:silent_assassin`. **Source fixado:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (versão declarada 0.9.7.1). Classe e helpers: [SilentAssassin.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/silentassassin/SilentAssassin.java); [SilentAssassinRifleEntity.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/silentassassin/SilentAssassinRifleEntity.java).

**Cadeia causal verificada no source:** SilentAssassin.onCastNoWeapon conjura rifle e onCastTickWithWeapon mantém retículo com assisted aim. onCastCompleteWithWeapon libera sem disparo quando cancelled, senão calcula dano a partir de spellPower do instante final, headshot e bônus unaware; damageTarget chama CombatTools.applyDamage; há tentativa de suppressNearbyAwareness se condição de unaware e threshold de dano são atendidos. SilentAssassinRifleEntity.fire gera recoil/VFX/tracer, não repete damageTarget.

**QA direcionado (pendente):** Confiabilidade do bônus unaware/condição de awareness, headshot, troca de armadura/atributos durante channel, multiplayer e não duplicar danos por tracer.

**Authority/boundary:** o cast, mana, recast e cooldown base permanecem no Iron's; armas, projetos e efeitos são do Apprentice's Codex. Uma rajada, hit, hitbox, tracer, loot extra ou counterspell derivado **não é novo cast** e não autoriza recompensa/XP/Mastery independente. Black Arcana não replica custos, damage, loot, hit ou efeitos externos. Integração com RPG Skill Tree ⛔ fail-closed até receipt/callback server-side unívoco e homologado. ⚠️ Esta inspeção source-level não comprova o corpo dos métodos no JAR compilado, configs ativas ou QA físico de modpack.
