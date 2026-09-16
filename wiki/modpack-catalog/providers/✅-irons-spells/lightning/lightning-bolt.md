# Lightning Bolt

- **Status:** PRESENTE — ativo
- **Provider/mod ID:** Iron's Spells / `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:lightning_bolt`
- **JAR:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Lightning
- **Níveis:** 1–10
- **Raridade:** Epic → Legendary
- **Cast:** Instant / 0 ticks
- **Mana:** 75–210
- **Cooldown:** 25 s
- **Dano publicado:** 10–28

## O que faz

Invoca um bolt de lightning na posição resolvida pelo raycast, causando dano Lightning em área ao redor do impacto.

## Source audit 3.16.3

- raycast até 64 blocos, com blocks e entity hitbox inflation 1;
- entity hit usa posição da entity; block/miss é ajustado para ground level relativo até 10;
- cria `LightningBolt` visual-only com vanilla damage 0;
- raio de dano: 4 blocos;
- dano base do spell = spell power 10 +2/level;
- dano final usa falloff por distância ao centro;
- exige line of sight entre strike e target;
- `canHit` exclui owner, mortos, não-pickable e spectators;
- Creepers atingidos recebem `thunderHit`;
- som final: `ILLUSIONER_PREPARE_BLINDNESS`.

## Targets / PvP / bosses / summons

A spell class não filtra aliados explicitamente além de excluir o owner; enforcement adicional do damage pipeline/configuração é `NÃO VERIFICADO`. PvP, bosses e summons: `NÃO VERIFICADO`.

## Deduplicação

Já cobre targeted heavenly lightning AoE. O bolt vanilla criado é visual-only; uma integração não deve adicionar dano vanilla do bolt além do settlement `DamageSources.applyDamage` do spell.

## Matriz obrigatória

- status/provider/JAR/ID/escola/tipo: confirmado;
- níveis/raridade: 1–10 / Epic→Legendary;
- cast: Instant 0;
- mana/cooldown: 75–210 / 25 s;
- dano: 10–28 no centro, falloff radial; damage type fino além de getDamageSource `NÃO VERIFICADO`;
- alcance/raio: 64 / 4; ground correction 10;
- scaling: power 10 +2/level + distance falloff;
- targets/PvP/boss/summon: parcialmente source-auditado, policy final `NÃO VERIFICADO`;
- obtenção/requisitos/focus: específicos `NÃO VERIFICADO`;
- VFX/audio: lightning visual + som confirmados; demais `NÃO VERIFICADO`;
- bridge/QA: não duplicar bolt/damage/creeper thunderHit.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- Source 3.16.3: `LightningBoltSpell.java` em `e4056af90302d37eb1739f5ff05020b020e6e252`.
