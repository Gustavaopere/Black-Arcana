# Ubiquitous

- Provider: **Farmer's Spell 'n Spellbooks** (`farmers_spell`)
- Version: `1.0.5.1-1.21.1`
- Registry id: `farmers_spell:phantom_loot`
- Display name in provider locale: **Ubiquitous**
- Registered class: `PhantomLootSpell`
- Provider school: `farmers_spell:gluttony`
- Host registry: **Iron's SpellRegistry**
- Semantic state: `COUNTED_EXACT` (binary static registry only)
- Strict contribution: `1` (already counted; +0 from exact-registry promotion)

## Identidade semântica

Spell provider-owned registrado no `ModSpells` do source pin exato. A identidade é contada pelo registro ativo sob o namespace `farmers_spell`, não por classes auxiliares, projectiles, entities, effects, items ou receitas de suporte.

## Source-observed cast profile

O inventário canônico classifica esta superfície como: **channelled provider/Foodgeist interaction surface**.

Essa frase é uma classificação comportamental de alto nível do dossiê, não uma reprodução da implementação upstream nem um compromisso com números de balanceamento.

## Exact physical binary evidence

**✅** The physical JAR `farmers-spell-n-spellbook-1.0.5.1-1.21.1.jar`, SHA-1 `f77355e029af39bbaba3854e10cc087a608351ff`, contains `com.chenjdy.farmers_spell.spells.PhantomLootSpell`; its `ModSpells.PHANTOM_LOOT_SPELL` static field registers literal `phantom_loot`. [Audit #38334052069](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38334052069) and [dossier](../EXACT-BINARY-SPELLS-1.0.5.1.md) prove the registry identity without certifying effective casting, balance, configuration or Survival.

## Registration evidence

O registrar contém `SPELLS.register("phantom_loot", PhantomLootSpell::new)` para esta identidade. O registro é ligado ao event bus sem branch provider-side que remova esta identidade.

## Evidence boundary

Esta ficha fecha ID, classe registrada, display name observado, ownership, escola Gluttony e estado semântico source-pinned. Dano, duração, alcance, custos, cooldowns, probabilidades de aquisição, mixins, networking e comportamento assembled-pack permanecem QA separado salvo onde o dossiê os fecha explicitamente.

Source: `../EXACT-1.0.5.1-SPELL-INVENTORY.md`.
