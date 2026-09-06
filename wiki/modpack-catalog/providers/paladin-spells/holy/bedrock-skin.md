# Bedrock Skin

## Estado

`EXTERNAL PROVIDER / INSTALLED — SOURCE BEHAVIOR AUDITED; LIVE MODPACK VALIDATION PENDING`

## Identidade

- **ID:** `paladin_spells:bedrock_skin`
- **Escola:** Holy
- **Raridade mínima:** Rare
- **Nível máximo:** 10
- **Função:** defesa extrema com imobilização
- **Cast type:** Instant
- **Animation:** `SELF_CAST_ANIMATION`

## Descrição

Concede redução de dano enquanto prende o caster a uma entidade-âncora de Bedrock Skin, criando a fantasia de transformar-se numa fortaleza imóvel.

## Custo e casting — source 1.21.1

- `baseManaCost = 30`
- `manaCostPerLevel = 15`
- `baseSpellPower = 5`
- `spellPowerPerLevel = 2`
- `castTime = 0`
- **Cooldown:** `25 s`

## Duração

`durationSeconds = 5 + getSpellPower(level, caster)`

## Redução de dano

`normalizedLevel = (level - 1) / (maxLevel - 1)`

`exponent = 1.2 / (1 + 0.05 * getSpellPower)`

`scaledValue = normalizedLevel ^ exponent`

`armorBonus = 0.20 * armor / (armor + 100)`

`damageReduction = min(0.95, 0.10 + scaledValue * 0.50 + armorBonus)`

Cap explícito da função: **95%**.

## Imobilização

No servidor, o spell:

1. grava a redução no persistent data;
2. aplica `BEDROCK_SKIN_EFFECT`;
3. cria `BedrockSkinEntity` na posição do caster;
4. define duration da entidade;
5. adiciona a entidade ao level;
6. força o caster a montar a entidade-âncora.

A semântica completa de movimento/dismount/damage precisa ser confirmada pelo event/entity do provider e teste no pack.

## Dano

Nenhum dano direto na classe do spell.

## Aquisição

`TBD — Iron's generic spell acquisition / pack config`.

## VFX

O provider usa entidade própria para a forma defensiva. A integração Divina pode melhorar material/emissivo, rachaduras luminosas e formação de placas, mas não deve retirar o telegraph essencial de que o caster está fortificado e imóvel.

## Deduplicação

“Grande redução de dano em troca de ficar imóvel” já é um nicho ocupado. Uma nova magia Divina defensiva só se justifica com outra economia/topologia, como ward de área, interceptação geométrica ou sanctum protection.
