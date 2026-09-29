# Celestial Tether

- ID: `asterismarcanum:celestial_tether`
- escola: Astral
- rarity: Uncommon
- níveis: 1–8
- cast: INSTANT
- mana: 30 / 45 / 60 / 75 / 90 / 105 / 120 / 135
- cooldown: 30 s
- neutral spell power: 5–12
- neutral duration: 26 / 28 / 30 / 32 / 34 / 36 / 38 / 40 s

## Efeito

Cria uma `CelestialTetherEntity`, monta o caster nela e o mantém suspenso. Um handler de `LivingIncomingDamageEvent` cancela hits quando o caster está tethered e o atacante não é friendly segundo o provider; a entidade perde contador de absorção por hit.

Anti-magic e remoção do passenger destroem o tether.

## Divergência estática

O tooltip usa `spellPower + 1` como hits dodged. A spell inicializa a entidade com `spellLevel + 1`, e `absorbHit()` só quebra quando o contador cai abaixo de zero. A leitura estática sugere `level + 2` hits efetivamente cancelados antes da quebra.

Além disso, o handler exige `damageSource.getEntity() != null`; danos sem entity-source podem escapar.

## Obtenção

Fonte concreta: Astral Scroll do Astromancer; crafting conforme config do Iron's.

## Authority e dedup

Authority = tether entity + provider incoming-damage handler. Não criar segunda barreira, segunda pool de charges nem restituição de vida equivalente.

## QA obrigatório

GameTest níveis 1/8, projectile, melee, environmental damage, party/PvP e anti-magic.