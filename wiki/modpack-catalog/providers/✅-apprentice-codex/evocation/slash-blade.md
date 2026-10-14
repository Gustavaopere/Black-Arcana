# Slash Blade

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:slash_blade`
- **School:** Evocation
- **Levels:** 1–10
- **Minimum rarity:** Common
- **Cast type:** Long
- **Cooldown:** 1.5 s
- **Interruptible:** no
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 400`
- `spellPowerPerLevel = 50`
- `baseManaCost = 10`
- `manaCostPerLevel = 3`
- `castTime = 15 ticks`

Damage:

`spellPower / 100 * SLASH_BLADE damage multiplier`

Block-penetration damage multiplier:

`clamp(20 + spellLevel * 5, 10, 90)%`

The displayed/ideal range is defined by the provider's `SlashBladeKatanaEntity.getAttackDepth()` rather than duplicated in the spell class; this catalog does not invent that entity constant without a dedicated entity audit.

## Weapon lifecycle

The spell summons a provider-owned katana. Damage and block-penetration values are written into the katana when it is created and are refreshed again at the initial weapon cast so completion-time spell-power/cast modifiers are reflected.

During the long cast the katana enters its standby state. When the cast completes successfully, the provider calls the katana's own slash sequence and keeps the weapon through that sequence. A cancelled cast releases the weapon without the slash.

The standby animation speed is scaled from the actual Iron's cast duration, so cast-time modifiers affect presentation without creating a second cast timer.

## Authority / deduplication

The summoned katana owns the concrete slash hit geometry and block-penetration settlement. Iron's owns the standard mana/cast/cooldown lifecycle.

Black Arcana must not re-run the slash hitbox, apply a second penetration multiplier, or count multiple entities hit by the area slash as multiple casts.

## Confidence

`SOURCE-PINNED SPELL COEFFICIENTS + CAST/WEAPON HANDOFF / KATANA HIT GEOMETRY DETAIL NOT YET EXPANDED / RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:slash_blade` → `SpellRegistry.reg("slash_blade", SlashBlade::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.slashblade.SlashBlade`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/slashblade/SlashBlade.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — ofensiva/movimento (2026-10-14)

**Source:** [`slashblade/SlashBlade.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/slashblade/SlashBlade.java) · [`slashblade/SlashBladeKatanaEntity.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/slashblade/SlashBladeKatanaEntity.java).

- **Geometria comprovada pelo helper:** `SlashBladeKatanaEntity` usa profundidade `4.5`, deslocamento frontal `0.5` (alcance ideal `5.0`), semilargura `2.75` e semialtura `0.75`; `move(MoverType.SELF,...)` limita posição da arma contra colisão.
- **Fonte do hit:** `slash` usa `RaycastTools.hitsHorizontalOrientedBox`. Alvo atrás de bloco recebe apenas `clamp(20 + level*5,10,90)%` do dano e **sem knockback**; outros recebem dano integral e knockback usual. A entidade grava dano e percentual em NBT.
- **QA:** parede/claims, alvos multipart, PvP, recast e FocusStaffbow; uma ação de lâmina por cast completo (cancelamento libera sem atacar).

🟡 Source-level causal; ⚠️ bytecode do JAR, config e QA modpack/Survival não certificados; ⛔ RPG perks/Mastery sem adapter homologado. Iron's e Apprentice's mantêm mana/casting/efeitos; Black Arcana não duplica runtime.
