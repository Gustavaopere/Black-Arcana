# Servant Gaze

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:servant_gaze`
- **Iron's school:** Ender
- **Levels:** 1–5
- **Minimum rarity:** Uncommon
- **Cast type:** Long
- **Cooldown:** 150 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 500`
- `spellPowerPerLevel = 200`
- `baseManaCost = 75`
- `manaCostPerLevel = 0`
- `castTime = 50 ticks`
- raw attack damage: `spellPower / 100 * providerDamageMultiplier`
- targeting radius: `20 blocks`
- mana consumed per turret attack: `15 + 5 * (spellLevel - 1)` = **15 / 20 / 25 / 30 / 35**
- lifetime: `20 * 60 * 10 = 12000 ticks = 10 min`
- recast count: `2`

## Provider-owned summon/session

If no recast is active, the server creates an owner-linked `ServantGazeStaffEntity`, snapshots spell level, damage, radius and per-shot mana cost into serializable cast data, and starts a provider recast/session for the full duration.

The public guide describes a following magical staff that autonomously attacks enemies—prioritizing high-health targets—and consumes the caster's mana per attack. Dispelling/removing the caster can remove the staff through provider lifecycle logic.

If the ten-minute session naturally expires while the caster has Iron's **Greater Conjurer's Talisman**, the provider explicitly suppresses the ordinary summon-cooldown completion path. Other completion reasons use the normal provider behavior.

## Authority and progression

The autonomous staff is not a Black Arcana familiar by default. Its owner, lifetime, targeting and per-shot resource consumption are Apprentice's Codex/Iron's authority.

RPG/Black Arcana must not award Mastery per turret tick or per autonomous target scan. Any future causal credit for a staff hit/kill requires an explicit progression attribution contract.

## Acquisition

Registered through Iron's spell registry. Exact survival acquisition remains provider-wide audit work.

## Deduplication

Occupies the **long-lived owner-bound autonomous staff turret that spends caster mana per shot** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT DAMAGE+RADIUS+SHOT COST+10m SESSION+RECAST / TARGET PRIORITY+DISPEL LIFECYCLE+MULTIPLAYER QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:servant_gaze` → `SpellRegistry.reg("servant_gaze", ServantGaze::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.servantgaze.ServantGaze`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/servantgaze/ServantGaze.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.
