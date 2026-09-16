# Blight

- **Status:** PRESENTE — ativo
- **Spell ID:** `irons_spellbooks:blight`
- **Provider/JAR:** Iron's Spells / `1.21.1-3.16.3`
- **Escola:** Nature
- **Níveis/raridade:** 1–8 / Rare → Legendary
- **Cast:** Long, 50 ticks
- **Mana/cooldown:** 60–200 / 90 s
- **Target helper:** até 32 blocos
- **Reduced Healing:** 10%–80%
- **Reduced outgoing Damage:** 5%–40%
- **Duração:** 30 s

## Source audit

Pre-cast usa `Utils.preCastTargetHelper(...,32,.35f)`. Com `TargetEntityCastData` válido, aplica `MobEffectRegistry.BLIGHT` por `spellPower*20*30`, amplifier `level-1`.

`BlightEffect` usa dois hooks:
- `LivingHealEvent`: healing multiplier = `1 - 0.10*level`;
- `LivingIncomingDamageEvent`: quando o atacante está Blighted, outgoing damage multiplier = `1 - 0.05*level`.

## Authority / dedup

`BLIGHT`/`BlightEffect` é authority dos dois debuffs. Não reduzir heal ou damage novamente em bridge. A ordem com outros modifiers/event listeners e floors finais: `NÃO VERIFICADO`.

## Verificação obrigatória

- dano direto/cura do cast: não aplicável;
- target/PvP/boss/summon: helper confirmado; eligibility final específica `NÃO VERIFICADO`;
- área: single target; range 32;
- scaling: amplifier level-1, duração 30 s; caps/floors adicionais `NÃO VERIFICADO`;
- obtenção/focus/ritual: específicos `NÃO VERIFICADO`;
- sons `BLIGHT_BEGIN`/`POISON_CAST`; VFX/animação final `NÃO VERIFICADO`;
- QA client-real: `NÃO VERIFICADO`; fail-closed pelo effect nativo.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- `BlightSpell.java` + `BlightEffect.java` — source 3.16.3.
