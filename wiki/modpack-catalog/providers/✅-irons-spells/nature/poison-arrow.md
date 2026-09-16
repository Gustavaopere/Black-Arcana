# Poison Arrow

- **Status:** PRESENTE — ativo
- **Spell ID:** `irons_spellbooks:poison_arrow`
- **Provider/JAR:** Iron's Spells / `1.21.1-3.16.3`
- **Escola:** Nature
- **Níveis/raridade:** 1–10 / Common → Legendary
- **Cast:** Long, 20 ticks
- **Mana/cooldown:** 40–85 / 15 s
- **Dano direto:** 5–14
- **AoE damage:** ~0,9–2,5 player-facing

## Função e source audit 3.16.3

Carrega uma flecha mágica venenosa que causa dano direto e cria/aciona o settlement AoE venenoso do projectile no impacto.

- spell power = 5 + 1 por nível após o primeiro;
- `getArrowDamage = spellPower`;
- `getAOEDamage = spellPower * 0.185`;
- cria `PoisonArrow`, posiciona próximo à altura dos olhos, dispara no look angle, injeta damage e AoE damage;
- sons `POISON_ARROW_CHARGE` / `POISON_ARROW_CAST`;
- animação `BOW_CHARGE_ANIMATION`.

O catálogo arredonda o AoE para uma casa decimal; a fórmula source permanece a authority interna.

## Authority / targets / deduplicação

`PoisonArrow` é authority de flight, collision, poison cloud e settlement do impacto. Alcance, velocidade, friendly-fire, PvP/boss/summon policy, cloud lifetime/radius e poison duration finos: `NÃO VERIFICADO` nesta ficha.

Não criar segunda flecha, segundo impacto ou segunda poison cloud em bridge.

## Verificação obrigatória

- recurso: mana; damage type fino: `NÃO VERIFICADO`;
- alcance/área/duração: projectile/cloud provider-native; números finos `NÃO VERIFICADO`;
- scaling: 5–14 direto; AoE = 0.185×power;
- targets/PvP/boss/summon: `NÃO VERIFICADO`;
- obtenção/loot/craft/trade/focus/ritual: específicos `NÃO VERIFICADO`;
- VFX/textura/QA client-real: `NÃO VERIFICADO` além dos sons/animação source-auditados;
- fail-closed: preservar `PoisonArrow` como authority.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- `PoisonArrowSpell.java` — source 3.16.3 pinado.
