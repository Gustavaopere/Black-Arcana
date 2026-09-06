# Ram

## Estado

`EXTERNAL PROVIDER / INSTALLED — SOURCE BEHAVIOR AUDITED; FRIENDLY-FIRE QA PENDING`

## Identidade

- **ID:** `paladin_spells:ram`
- **Escola:** Holy
- **Raridade mínima:** Rare
- **Nível máximo:** 10
- **Função:** mobilidade ofensiva / charge / armor-scaling damage
- **Cast type:** Instant

## Descrição

Impulsiona o caster para frente e causa dano/knockback aos LivingEntity interceptados pela caixa de carga.

## Custo e casting — source 1.21.1

- `baseManaCost = 15`
- `manaCostPerLevel = 5`
- `baseSpellPower = 4`
- `spellPowerPerLevel = 1`
- `castTime = 0`
- **Cooldown:** `10 s`

## Movimento

`multiplier = getSpellPower(level, caster) / 3`

O vetor de olhar horizontal é normalizado e escalado pelo multiplier. Quando o caster está no chão, o source reposiciona-o `+1.5 Y` antes de aplicar o impulso.

Existe `RamDirectionOverrideCastData` capaz de rotacionar o vetor em ±90° de forma aleatória quando essa cast data está presente.

## Dano

Fórmula exata da classe:

`damage = armor * 1.25 + getSpellPower(level, caster) + level * 2`

O dano é aplicado com `entity.damageSources().mobAttack(entity)`.

## Targeting

Cria uma AABB a partir do bounding box do caster, expande na direção do vetor de charge e aplica `inflate(1.5)`. Seleciona todo `LivingEntity` vivo diferente do caster.

Cada alvo recebe:

- dano da fórmula acima;
- `knockback(1.5, forward.x, forward.z)`.

## Friendly fire / PvP

A classe auditada não contém filtro de party, ally, tame ownership ou PvP antes de chamar `hurt`. É possível que eventos globais do pack/provider alterem settlement, portanto a Wiki não declara comportamento seguro até live validation.

Para integração Black Arcana, não reutilizar Ram como primitive de ally-safe charge sem adapter/admission explícito.

## Aquisição

`TBD — Iron's generic acquisition / pack config`.

## VFX

Candidato a reforço visual com shield/halo frontal, streaks Holy e impacto luminoso orientado à velocidade. O VFX deve manter direção e área de colisão legíveis.

## Deduplicação

Novo spell Divino de “dash que bate com dano escalado por armor” é redundante com Ram salvo se alterar substancialmente targeting, recurso, defesa/interceptação ou consequência.
