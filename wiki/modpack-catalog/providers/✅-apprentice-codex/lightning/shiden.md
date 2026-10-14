# Shiden

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:shiden`
- **Iron's school:** Lightning
- **Levels:** 1–5
- **Minimum rarity:** Rare
- **Cast type:** Long
- **Cooldown:** 10 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 1600`
- `spellPowerPerLevel = 400`
- `baseManaCost = 50`
- `manaCostPerLevel = 15`
- `castTime = 30 ticks`

Raw slash damage is `spellPower / 100`, then multiplied by `DamageMultiplierKey.SHIDEN`.

Damage multiplier when the slash penetrates block obstruction:

`clamp(20 + spellLevel * 5, 10, 90)%`

For the actual 1–5 level range, this produces **25%, 30%, 35%, 40%, 45%** of normal damage through the provider's block-penetration path.

The ideal range is delegated to `ShidenKatanaEntity.getAttackDepth()`; this catalog does not invent a numeric distance without auditing that entity constant.

## Cast lifecycle

The katana is summoned during the long cast. Before the attack, current spell power and penetration multiplier are refreshed so completion-time provider/Focus Staffbow modifiers are reflected.

The weapon enters its standby animation/state using a speed scale derived from base vs actual cast duration. Cancelling releases the weapon; successful completion executes exactly one provider-owned slash.

## What it does

Provider guide semantics: summons a magical katana and swiftly slashes upward. Blocks do not completely stop the slash, but obstruction reduces its damage and impact.

## Causality

The partially penetrating hit remains one Shiden slash. Black Arcana must not treat the unobstructed and through-block portions as separate attack/proc identities.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **charged Lightning katana rising slash with reduced block penetration** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT ATTACK DEPTH + KATANA COLLISION DETAILS + PACK CONFIG MULTIPLIER QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:shiden` → `SpellRegistry.reg("shiden", Shiden::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.shiden.Shiden`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/shiden/Shiden.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — armas conjuradas e efeitos derivados (2026-10-14)

**Registry ID:** `apprenticecodex:shiden`. **Source fixado:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (versão declarada 0.9.7.1). Classe e helpers: [Shiden.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/shiden/Shiden.java); [ShidenKatanaEntity.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/shiden/ShidenKatanaEntity.java).

**Cadeia causal verificada no source:** Shiden.onCastNoWeapon cria katana com damage e blockPenetrationDamageMultiplier; onInitialCastWithWeapon atualiza os valores e onCastTickWithWeapon coloca standby de acordo com cast-time speed. onCastCompleteWithWeapon executa slash somente quando não cancelado. ShidenKatanaEntity.slash calcula HorizontalOrientedBox e usa hit.blockOccluded para multiplicar dano com blockPenetrationDamageMultiplier e aplicar NO_KNOCKBACK; os hits sem oclusão usam dano/knockback padrão. A espada não precisa alterar blocos para atingir atrás da cobertura.

**QA direcionado (pendente):** Alvos multipart, proteção e PvP atrás de paredes, multiplicador efetivo por config/atributo, anticlip e cancelamentos.

**Authority/boundary:** o cast, mana, recast e cooldown base permanecem no Iron's; armas, projetos e efeitos são do Apprentice's Codex. Uma rajada, hit, hitbox, tracer, loot extra ou counterspell derivado **não é novo cast** e não autoriza recompensa/XP/Mastery independente. Black Arcana não replica custos, damage, loot, hit ou efeitos externos. Integração com RPG Skill Tree ⛔ fail-closed até receipt/callback server-side unívoco e homologado. ⚠️ Esta inspeção source-level não comprova o corpo dos métodos no JAR compilado, configs ativas ou QA físico de modpack.
