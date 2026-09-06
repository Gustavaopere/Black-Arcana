# Cloud of Regeneration

- **Status no modpack:** PRESENTE NO PROVIDER, MAS `DEPRECATED` NO DEFAULT CONFIG — fora da contagem ativa de 110 spells
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:cloud_of_regeneration`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Max level:** 5
- **Raridade source:** Common
- **Cast:** Continuous
- **Cast time auditado:** 200 ticks
- **Mana source:** base 10, +3/level
- **Cooldown:** 35 s
- **Raio:** 5 blocos
- **DefaultConfig:** `Deprecated=true`

## Estado atual

O catálogo oficial ativo atual não lista este spell entre os 12 Holy ativos. O source audit 3.16.3 confirma, porém, que a implementação ainda existe e está marcada deprecated no `DefaultConfig`. Esta ficha é histórica/semântica e **não soma** à cobertura ativa 110/110.

## Source audit 3.16.3

- spell power: base 2, +1/level;
- durante o cast percorre living entities no raio;
- elegibilidade por `Utils.shouldHealEntity`;
- `healAmount = getSpellPower(level, caster) * 0.5`;
- publica `SpellHealEvent` por cura, aplica heal e partículas.

## Deduplicação

Mesmo deprecated, bloqueia a falsa conclusão de que “cura contínua Holy de aliados próximos” é uma lacuna inédita. Qualquer substituto novo deve ser deliberado e semanticamente distinto ou assumir explicitamente a função legada.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/` — ausência na lista Holy ativa
- Source audit canônico: `wiki/providers/irons-spellbooks/spells/holy/cloud-of-regeneration.md`
- Changelog histórico oficial registra que Cloud of Regeneration foi desativado por padrão
- Consulta: 2026-09-06.
