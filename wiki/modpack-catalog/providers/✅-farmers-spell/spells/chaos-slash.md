# Chaotic Pastry Slash

- Provider: **Farmer's Spell 'n Spellbooks** (`farmers_spell`)
- Version: `1.0.5.1-1.21.1`
- Registry id: `farmers_spell:chaos_slash`
- Display name in provider locale: **Chaotic Pastry Slash**
- Registered class: `ChaosSlashSpell`
- Provider school: `farmers_spell:gluttony`
- Host registry: **Iron's SpellRegistry**
- Semantic state: `COUNTED_SOURCE_PINNED`
- Strict contribution: `1`

## Identidade semântica

Spell provider-owned registrado no `ModSpells` do source pin exato. A identidade é contada pelo registro ativo sob o namespace `farmers_spell`, não por classes auxiliares, projectiles, entities, effects, items ou receitas de suporte.

## Source-observed cast profile

O inventário canônico classifica esta superfície como: **instant provider slash/projectile attack surface**.

Essa frase é uma classificação comportamental de alto nível do dossiê, não uma reprodução da implementação upstream nem um compromisso com números de balanceamento.

## Registration evidence

O registrar contém `SPELLS.register("chaos_slash", ChaosSlashSpell::new)` para esta identidade. O registro é ligado ao event bus sem branch provider-side que remova esta identidade.

## Evidence boundary

Esta ficha fecha ID, classe registrada, display name observado, ownership, escola Gluttony e estado semântico source-pinned. Dano, duração, alcance, custos, cooldowns, probabilidades de aquisição, mixins, networking e comportamento assembled-pack permanecem QA separado salvo onde o dossiê os fecha explicitamente.

Source: `../EXACT-1.0.5.1-SPELL-INVENTORY.md`.
