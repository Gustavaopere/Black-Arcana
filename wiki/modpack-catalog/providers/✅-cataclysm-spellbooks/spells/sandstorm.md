# cataclysm_spellbooks:sandstorm

- Provider: **Cataclysm: Spellbooks** (`cataclysm_spellbooks`)
- Current runtime: `1.1.14-1.21`
- Registry id: `cataclysm_spellbooks:sandstorm`
- Registry field: `SANDSTORM`
- Exact registered class: `SandstormSpell`
- Observed implementation package group: **Nature**
- Semantic state: `COUNTED_EXACT`
- Strict contribution: `1`

## Identity closure

Identidade provider-owned registrada no `SpellRegistries.class` exato da release 1.1.14. O registry class atual é byte-identical ao controle físico hash-matched 1.1.13 que fechou 59 campos, 59 chamadas de registro, 59 instâncias e zero branches condicionais no initializer.

## Counting boundary

Esta ficha conta somente `cataclysm_spellbooks:sandstorm`. Field, classe, projectile/entity/effect de suporte, localization e conteúdo Cataclysm consumido pelo addon não são identidades extras. O package group **Nature** é evidência estrutural e não é usado para inventar school, custo, dano, cooldown ou mecânica.

## Authority boundary

Cataclysm: Spellbooks mantém authority sobre este spell e seu estado provider-local. Iron's mantém cast/mana/cooldown. Black Arcana não duplica settlement, recurso, cooldown, projectile/summon ou dano.

## Evidence boundary

Identidade, field, classe, package group, versão e presença no registry são exatos para o artefato físico atual. Mecânicas numéricas, acquisition detalhada, balance e hooks runtime permanecem QA separado quando não fechados por evidência release-exata.

Sources: `../EXACT-1.1.14-SPELL-INVENTORY.md`, `../EXACT-1.1.14-RELEASE-REVALIDATION.md`.
