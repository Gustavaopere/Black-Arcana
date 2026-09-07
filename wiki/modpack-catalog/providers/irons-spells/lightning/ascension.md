# Ascension

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:ascension`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Lightning
- **Níveis:** 1–10
- **Raridade:** Rare → Legendary
- **Cast:** Instant
- **Cast time source:** 0 ticks
- **Mana:** 50–59
- **Cooldown:** 15 s
- **Dano publicado:** 5–14

## O que faz

Golpeia o chão sob o caster com lightning visual, causa dano/knockback em área e impulsiona o caster para cima, aplicando redução de gravidade temporária.

## Source audit 3.16.3

- `baseSpellPower=5`, `spellPowerPerLevel=1`;
- aplica `MobEffectRegistry.ASCENSION` por 80 ticks / 4 s;
- procura chão até 32 blocos abaixo para a posição do strike;
- cria `LightningBolt` visual-only, damage vanilla 0;
- raio de processamento: 5 blocos;
- dano = spell power com falloff quadrático por distância ao strike;
- usa `DamageSources.applyDamage` com damage source do spell;
- Creepers atingidos recebem `thunderHit`;
- LivingEntity atingida recebe knockback escalado pelo dano final;
- aplica `ImpulseCastData` e impulso vertical/forward ao caster.

## Targets / PvP / bosses / summons

- **Target primário:** self + área ao redor da posição de strike.
- A spell class não implementa filtro explícito de friendly-fire na enumeração da área; policy final adicional de `DamageSources`/configuração fica `NÃO VERIFICADO`.
- PvP, bosses e summons: comportamento específico `NÃO VERIFICADO`.

## Obtenção / requisitos

- pipeline geral de scrolls/spellbooks do Iron's;
- rotas específicas de loot/trade/craft: `NÃO VERIFICADO`;
- foco Lightning existente no provider: Bottle o' Lightning, mas requisito específico deste spell: `NÃO VERIFICADO`;
- itens/rituais adicionais: `NÃO VERIFICADO`.

## Integrações / deduplicação / fail-closed

- authorities: `MobEffectRegistry.ASCENSION`, `DamageSources.applyDamage`, `ImpulseCastData` e lightning visual do provider;
- não criar segundo launch, segundo lightning-AoE ou segundo knockback para o mesmo cast;
- perks de mobilidade devem reagir ao cast/hook causal comprovado, não inferir ascensão por mudança de coordenada;
- QA client-real/VFX final: `NÃO VERIFICADO`.

## Matriz obrigatória

- status/provider/JAR/ID/escola: confirmado;
- descrição: catálogo + source;
- níveis/raridade: 1–10 / Rare→Legendary;
- cast/channel: Instant / 0 / não channel;
- recurso/custo: mana 50–59;
- cooldown: 15 s;
- dano/tipo: 5–14 nominal no centro, com falloff source; damage family específica além do `getDamageSource` Lightning: `NÃO VERIFICADO`;
- alcance/raio/duração: raio 5; efeito Ascension 4 s; busca de chão até 32 abaixo;
- scaling/caps: spell power 5 +1/level; falloff pela distância; caps extras `NÃO VERIFICADO`;
- targets/PvP/boss/summon: conforme acima;
- obtenção/requisitos/itens: específicos `NÃO VERIFICADO`;
- VFX/animação/áudio: lightning visual confirmado; demais assets `NÃO VERIFICADO`;
- bridges/QA: `NÃO VERIFICADO`, fail-closed.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- Source 3.16.3: `AscensionSpell.java` em `e4056af90302d37eb1739f5ff05020b020e6e252`.
