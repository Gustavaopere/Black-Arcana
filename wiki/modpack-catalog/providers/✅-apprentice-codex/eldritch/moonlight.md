# Moonlight

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:moon_light`
- **Iron's school:** Eldritch
- **Levels:** 1–3
- **Minimum rarity:** Legendary
- **Cast type:** Long
- **Cooldown:** 8 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 1200`
- `spellPowerPerLevel = 900`
- `baseManaCost = 120`
- `manaCostPerLevel = 30`
- `castTime = 40 ticks`
- cannot be interrupted
- standby visual starts from a 10-tick base delay, scaled against effective cast duration

Raw damage:

`spellPower / 100`

then multiplied by `DamageMultiplierKey.MOON_LIGHT`.

Attack distance by spell level:

`8 + (spellLevel - 1) * 8` blocks.

## What it does

The spell summons a Moonlight katana during the charge and, on successful completion, performs the blade slash plus a separate spatial charge-cut entity over the configured distance.

Provider guide semantics describe the flash-cut as rending space and severing both magical effects on the target and spellcasting itself. The cast is explicitly uninterruptible.

The provider's katana/charge-cut entities own exact hit, dispel/interruption and damage causality. Black Arcana must not apply a second anti-magic settlement when observing the same hit.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **uninterruptible Eldritch flash-cut / long spatial slash / magic-effect and casting disruption** niche. Black Arcana anti-magic must remain mechanically distinct and must not rebrand this provider spell.

## Confidence

`SOURCE-PINNED SPELL + PROVIDER GUIDE / KATANA+CHARGE-CUT INTERNAL EFFECT DETAILS + RUNTIME CONFIG QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:moon_light` → `SpellRegistry.reg("moon_light", MoonLight::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.moonlight.MoonLight`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/moonlight/MoonLight.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — armas conjuradas e efeitos derivados (2026-10-14)

**Registry ID:** `apprenticecodex:moon_light`. **Source fixado:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (versão declarada 0.9.7.1). Classe e helpers: [MoonLight.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/moonlight/MoonLight.java); [MoonLightKatanaEntity.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/moonlight/MoonLightKatanaEntity.java); [MoonLightChargeCutEntity.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/moonlight/MoonLightChargeCutEntity.java); [MoonLightCounterspellEffect.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/moonlight/MoonLightCounterspellEffect.java).

**Cadeia causal verificada no source:** MoonLight.onCastTickWithWeapon mantém carregamento/standby; onCastCompleteWithWeapon só após sucesso executa slash da katana e instancia uma MoonLightChargeCutEntity. MoonLightKatanaEntity.slash usa hitsAabb e só ativa MoonLightCounterspellEffect após dano bem-sucedido. MoonLightChargeCutEntity.tick avança o segmento ao longo de PROCESS_DURATION_TICKS=15 após delay, guarda damagedEntityIds e causa no máximo um dano por UUID dentro da entidade; após dano chama o mesmo efeito de counterspell. MoonLightCounterspellEffect respeita CounterSpellEvent cancelado e remove casting/recasts/effects apenas no fluxo autorizado.

**QA direcionado (pendente):** Counterspell de terceiros, efeitos de cura/cure removidos, hit double entre katana e segmento (efeitos do mesmo cast), restart durante segmento e restrições de PvP.

**Authority/boundary:** o cast, mana, recast e cooldown base permanecem no Iron's; armas, projetos e efeitos são do Apprentice's Codex. Uma rajada, hit, hitbox, tracer, loot extra ou counterspell derivado **não é novo cast** e não autoriza recompensa/XP/Mastery independente. Black Arcana não replica custos, damage, loot, hit ou efeitos externos. Integração com RPG Skill Tree ⛔ fail-closed até receipt/callback server-side unívoco e homologado. ⚠️ Esta inspeção source-level não comprova o corpo dos métodos no JAR compilado, configs ativas ou QA físico de modpack.
