# Firefly Swarm

- **Status:** PRESENTE — ativo
- **Spell ID:** `irons_spellbooks:firefly_swarm`
- **Provider/JAR:** Iron's Spells / `1.21.1-3.16.3`
- **Escola:** Nature
- **Níveis/raridade:** 1–10 / Uncommon → Legendary
- **Cast:** Long, 30 ticks
- **Mana/cooldown:** 40–130 / 20 s
- **AoE damage:** 2–5
- **Raio público:** 2 blocos
- **Targeting:** até 32 blocos

## Source audit

Pre-cast usa target helper 32. O cast resolve target/position do `TargetEntityCastData` ou faz raycast 32; para block/miss corrige a posição em relação ao chão. Cria `FireflySwarmProjectile(level, owner, target, damage)` e move a swarm para a posição resolvida.

- spell power = 6 +1/level;
- damage = spellPower/3;
- radius mostrado vem de `FireflySwarmProjectile.radius`;
- o catálogo atual confirma que a swarm acompanha o alvo e, se o alvo inicial morrer, passa ao último creature harmed; esse lifecycle pertence ao projectile.

## Authority / dedup

`FireflySwarmProjectile` é authority de follow/retarget/AoE ticks. Não criar scheduler ou retarget paralelo. Friendly-fire, PvP/boss/summon eligibility, tick cadence e lifetime: `NÃO VERIFICADO` nesta ficha.

## Verificação obrigatória

- damage type fino: `NÃO VERIFICADO`;
- range 32, radius público 2; duration/lifetime `NÃO VERIFICADO`;
- scaling damage = power/3;
- obtenção/focus/ritual: específicos `NÃO VERIFICADO`;
- prepare sound `FIREFLY_SPELL_PREPARE`; VFX/finish sound/QA `NÃO VERIFICADO`;
- fail-closed: projectile provider-native.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- `FireflySwarmSpell.java` — source 3.16.3.
