# Mana Slash

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:mana_slash`
- **Iron's school:** Ender
- **Levels:** 1
- **Minimum rarity:** Rare
- **Cast type:** Instant
- **Cooldown:** 0 s
- **Resource:** Iron's mana
- **Crafting:** disabled by spell config
- **Looting:** explicitly disabled
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 50`
- `spellPowerPerLevel = 25`
- `baseManaCost = 30`
- `manaCostPerLevel = 0`
- `castTime = 0`

Raw damage is weapon-referenced rather than a fixed spell coefficient:

`max(1, referencedWeaponDamage * spellPowerPercent / 100) * providerDamageMultiplier`

For normal fallback casting, the referenced value comes from the caster's current weapon damage. For Swingcast Staff context, the provider captures the actual casting catalyst stack and resolves its displayed attack-damage modifiers through NeoForge's `ItemAttributeModifierEvent`.

## Provider/item binding

The guide describes Mana Slash as a latent Crystal Bladed Staff spell. The source confirms an item/cast-context path: if Swingcast context exists but the catalyst stack cannot be resolved, casting fails rather than silently using another weapon.

The cast creates a provider `MANA_SLASH_PROJECTILE` and stores the resolved damage on that projectile.

## Acquisition

The spell is explicitly non-craftable and non-lootable. Its registered presence must not be interpreted as ordinary scroll availability.

## Causality

The projectile and any later mana-orb consequences remain one provider cast chain. Black Arcana/RPG must not treat projectile spawn, hit and orb creation as separate player-authored spell casts.

## Deduplication

Occupies the **item-bound mana blade/projectile whose damage scales from the casting weapon's attack damage** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT ITEM-DAMAGE RESOLUTION+ACQUISITION EXCLUSIONS / PROJECTILE HIT+MANA-ORB NUMBERS+PACK MULTIPLIER QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:mana_slash` → `SpellRegistry.reg("mana_slash", ManaSlash::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.manaslash.ManaSlash`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/manaslash/ManaSlash.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — ofensiva/movimento (2026-10-14)

**Source:** [`manaslash/ManaSlash.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/manaslash/ManaSlash.java) · [`manaslash/ManaSlashProjectileEntity.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/manaslash/ManaSlashProjectileEntity.java).

- **Catalisador:** `resolveCatalystWeaponDamage` resolve dano de `ItemStack` de Swingcast via `ItemAttributeModifierEvent` postado no event bus; acumula `ADD_VALUE`, `ADD_MULTIPLIED_BASE` e `ADD_MULTIPLIED_TOTAL`. `canBeCastedBy` falha se existe contexto Swingcast sem catalisador; fora dele usa `Utils.getWeaponDamage`.
- **Entidade:** projétil cresce de raio `0.5` até `5` (+`0.45`/tick), expira em `20 ticks`, usa box fixa `0.5 × 0.5` contra blocos e `victimIds` por ID resolvido (multipart). AntiMagic descarta.
- **Proc derivado:** `CrystalBladedStaff.spawnManaSiphonOrbsForSpell` só após `CombatTools.applyDamage` verdadeiro e apenas com player segurando Crystal Bladed Staff. QA de modificadores de item, dono do alvo, orbs e crédito causal.

🟡 Source-level causal; ⚠️ bytecode do JAR, config e QA modpack/Survival não certificados; ⛔ RPG perks/Mastery sem adapter homologado. Iron's e Apprentice's mantêm mana/casting/efeitos; Black Arcana não duplica runtime.
