# Poison Splash

- **Status:** PRESENTE — ativo
- **Spell ID:** `irons_spellbooks:poison_splash`
- **Provider/JAR:** Iron's Spells / `1.21.1-3.16.3`
- **Escola:** Nature
- **Níveis/raridade:** 1–10 / Uncommon → Legendary
- **Cast:** Long, 15 ticks
- **Mana/cooldown:** 40–130 / 20 s
- **Dano:** 8–17
- **Effect length:** 7–25 s
- **Targeting:** até 32 blocos

## Função e source audit

Resolve uma entidade/posição por target helper ou raycast e cria `PoisonSplash` no local, com owner explícito, damage e effect duration.

- spell power = 8 +1 por nível após o primeiro;
- damage = spell power;
- duration = `100 + spellLevel*40` ticks = 7–25 s;
- fallback raycast = 32 blocos, com ground correction para block/miss;
- sons `POISON_SPLASH_BEGIN` / `POISON_CAST`.

## Authority / deduplicação

`PoisonSplash` é authority da wave/cloud, seleção espacial, poison e hit cadence. Não executar um segundo AoE scanner nem gerar cloud duplicada.

Friendly-fire, PvP, bosses, summons, radius exato e lifecycle da cloud: `NÃO VERIFICADO` nesta ficha.

## Verificação obrigatória

- damage type fino: `NÃO VERIFICADO`;
- alcance 32; radius `NÃO VERIFICADO`; duração 7–25 s;
- scaling: damage +1/level; duration +2s/level;
- obtenção/requisitos/focus/ritual: específicos `NÃO VERIFICADO`;
- VFX/textura/animação/QA client-real: `NÃO VERIFICADO` além dos sons;
- fail-closed: entity provider-native.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- `PoisonSplashSpell.java` — source 3.16.3.
