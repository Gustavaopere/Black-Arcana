# Levitate

- Provider: **Ozymandias Sundries** (`ozymandias_sundries`)
- Distribution version: `0.0.5`
- Embedded runtime metadata: `0.0.1`
- Registry id: `ozymandias_sundries:levitate`
- Registered class: `LevitateSpell`
- Host school: **Iron's Ender**
- Semantic state: `COUNTED_EXACT`
- Strict contribution: `1`

## Identidade semântica

Spell provider-owned registrado no artefato físico/publisher exato. A identidade é fechada pelo registrar atual, não pela mera presença de classe ou localization.

## Registry evidence

O registrar exato instancia `LevitateSpell` e registra o resource root `levitate`. Não há branch condicional no initializer.

O artefato também não empacota override em `irons_spellbooks_spell_config`, e esta classe registrada não fornece overrides provider-specific de `allowCrafting`, `allowLooting`, `isEnabled` ou `canBeCraftedBy`.

## Evidence boundary

A ficha fecha identidade, ownership, school e registro atual. Parâmetros de área, duração, custo, cooldown, aquisição live e comportamento multiplayer permanecem runtime/mechanics QA e não são inferidos aqui.

Source: `../EXACT-0.0.5-ARTIFACT-AUDIT.md`.
