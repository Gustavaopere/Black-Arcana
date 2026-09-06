# Sworn Protector

## Estado

`EXTERNAL PROVIDER / INSTALLED — WIP UPSTREAM — AUTHORITY QA BLOCKER`

## Identidade

- **ID:** `paladin_spells:sworn_protector`
- **Escola:** Holy
- **Raridade mínima:** Rare
- **Nível máximo:** 10
- **Função:** proteção de aliados / redirecionamento de dano
- **Cast type:** Instant
- **Animation:** `CHARGE_RAISED_HAND`

O README upstream marca explicitamente o spell como `WIP`.

## Custo e casting — source 1.21.1

- `baseManaCost = 30`
- `manaCostPerLevel = 15`
- `baseSpellPower = 10`
- `spellPowerPerLevel = 5`
- `castTime = 0`
- **Cooldown:** `35 s`

## Duração

`durationSeconds = 15 + 20 * getSpellPower(level, caster) / 100`

## Raio

A implementação chama `getRange(spellLevel)` e a função calcula:

`range = (10 + spellLevel * 2) * 3`

Observação: o parâmetro da função é nomeado `spellPower`, mas recebe `spellLevel` no call site auditado.

## Percentual de redirecionamento

`normalizedLevel = (level - 1) / (maxLevel - 1)`

`scaledValue = normalizedLevel ^ (0.6 / (1 + 0.1 * getSpellPower))`

`armorBonus = 0.20 * armor / (armor + 100)`

`redirect = min(1.0, 0.20 + scaledValue * 0.60 + armorBonus)`

Logo, o contrato pretendido começa em torno de uma base de 20% antes do componente da curva/armor e possui cap técnico de 100%.

## Event de redirecionamento

O event server-side:

- só considera vítima `Player`;
- ignora dano já classificado como redirect para evitar recursão;
- procura protectors com o effect em raio bruto de 64;
- filtra pelo range persistido de cada protector;
- escolhe o protector elegível mais próximo;
- impede redirect quando o próprio protector é o atacante;
- reduz o dano da vítima pela parcela redirecionada;
- aplica essa parcela ao protector usando damage type próprio `REDIRECT`.

## Authority blocker

Na fonte 1.21 auditada, `onCast` grava `sworn_protector_redirect`, `sworn_protector_range` e aplica `SWORN_PROTECTOR_EFFECT` **somente dentro de `if (level.isClientSide)`**.

Já o event que executa a mecânica retorna quando está no cliente e exige o effect/persistent data no servidor. Isso é uma inconsistência aparente forte.

Até GameTest/live-JAR demonstrar comportamento válido ou uma correção ser aplicada, Black Arcana não deve depender deste spell para contratos server-authoritative.

## Aquisição

`TBD — Iron's generic acquisition / pack config`.

## VFX

A fantasia de juramento/protetor combina com tether dourado entre protector e aliados protegidos. Qualquer tether deve ser puramente presentation de relações server-confirmed; o cliente não escolhe quem recebe redirect.

## Deduplicação

O conceito “redirecionar dano de aliados próximos para o caster” já existe. Novos vínculos Divinos de proteção devem reutilizar/corrigir este provider quando possível ou possuir delta explícito.
