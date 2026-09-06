# Taunt

## Estado

`EXTERNAL PROVIDER / INSTALLED — SOURCE BEHAVIOR AUDITED; LIVE MODPACK VALIDATION PENDING`

## Identidade

- **ID:** `paladin_spells:taunt`
- **Escola:** Holy
- **Raridade mínima:** Rare
- **Nível máximo:** 10
- **Função:** crowd control / threat control
- **Cast type:** Instant
- **Animation:** `TOUCH_GROUND_ANIMATION`

## Descrição

Marca mobs hostis próximos para que ataquem o caster, permitindo ao paladino tirar pressão de aliados.

## Custo e casting — source 1.21.1

- `baseManaCost = 30`
- `manaCostPerLevel = 10`
- `baseSpellPower = 10`
- `spellPowerPerLevel = 5`
- `castTime = 0`
- **Cooldown:** `20 s`

## Targeting

A classe infla o AABB do caster e seleciona `Mob` vivo que também seja `Enemy`.

### Fórmula de raio

`radius = 10 + getSpellPower(level, caster) * 2`

### Duração

`durationSeconds = 5 + getSpellPower(level, caster)`

## Efeito mecânico

Para cada mob hostil elegível:

1. aplica `TAUNT_EFFECT`;
2. grava `taunt_target_uuid = caster UUID` no persistent data;
3. durante o effect, a cada tick, o effect recupera o alvo no `ServerLevel`;
4. executa `mob.setTarget(caster)` e `mob.setAggressive(true)`;
5. se o alvo for player, também chama `setLastHurtByPlayer`.

Se o UUID não resolver mais, o persistent data do taunt é removido.

## Dano

Nenhum dano direto.

## PvP

O spell procura `Mob`, não players, portanto o cast não taunta jogadores diretamente pela implementação auditada.

## Aquisição/aprendizado

`TBD — Iron's generic spell acquisition / pack config`. Não foi encontrado loot table próprio do addon.

## VFX

O provider usa `ANGRY_VILLAGER` no cast e durante o effect. Isso é funcional como telegraph, mas entra como `VFX UPGRADE CANDIDATE` para a estética Holy final: selo de desafio, halo/mark sobre inimigos e pulso visual do caster são preferíveis, desde que o servidor continue sendo authority.

## Deduplicação

Novo spell Divino que apenas force hostis próximos a focar o caster é redundante com Taunt. Uma variante só se justifica se introduzir topologia/regra realmente nova, por exemplo challenge pact persistente de alvo único com consequência diferente.
