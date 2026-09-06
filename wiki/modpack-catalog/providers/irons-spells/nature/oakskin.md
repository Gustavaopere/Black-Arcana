# Oakskin

- **Status:** PRESENTE — ativo
- **Spell ID:** `irons_spellbooks:oakskin`
- **Provider/JAR:** Iron's Spells / `1.21.1-3.16.3`
- **Escola:** Nature
- **Níveis/raridade:** 1–8 / Common → Legendary
- **Cast:** Instant, 0 ticks
- **Mana/cooldown:** 25–95 / 90 s
- **Damage Reduction:** 20% com power multiplier neutro
- **Speed:** -25%
- **Duração:** 20–41 s

## Source audit

Antes de aplicar o spell, remove OAKSKIN/OakskinData preexistentes para limpar efeitos colaterais de elixir. Aplica `MobEffectRegistry.OAKSKIN` por `spellPower*20`, amplifier fixo 2, envia `OakskinParticlesPacket`.

- spell power = 20 +3/level;
- `OakskinEffect`: base reduction .10 + .05*amplifier, portanto 20% em amplifier 2, multiplicado por entity power e capado em 75%;
- `SLOWNESS_MAGNITUDE=.25`;
- intercepta `LivingIncomingDamageEvent` e multiplica incoming damage por `1-reduction`;
- elixir força multiplier 1 para impedir scaling por spell power;
- partículas de oak log/firefly são emitidas ao reduzir dano.

## Authority / dedup

`OAKSKIN`/`OakskinEffect` é authority de mitigation e slow. Não aplicar 20% de redução novamente fora do event. Interação/ordem com armor, resistances e outros listeners: `NÃO VERIFICADO`.

## Verificação obrigatória

- dano/cura: não aplicável;
- targets/range: self;
- scaling/cap: duration 20–41s; reduction formula + cap75%; amplifier fixo;
- obtenção/focus/ritual: específicos `NÃO VERIFICADO`;
- som `OAKSKIN_CAST`, animação `SELF_CAST_ANIMATION`, packet/impact particles confirmados; textura/QA final `NÃO VERIFICADO`;
- fail-closed: usar effect/data provider, sem segunda mitigation ledger.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- `OakskinSpell.java` + `OakskinEffect.java` — source 3.16.3.
