# Farmer's Spell 'n Spellbooks 1.0.5.1 — fichas canônicas de spells

Este índice materializa as **6 identidades de spell provider-owned** fechadas no source pin exato `GLDYM/Farmers-Spell-n-Spellbook@b7cbb40316a9ccbbc2ce2b56b3023647261ce569`.

O provider permanece **✅ catalogado / COUNTED_EXACT 6/6 no registry estático do JAR físico**, [auditoria #38334052069](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38334052069) e [dossiê](EXACT-BINARY-SPELLS-1.0.5.1.md). A contribuição estrita **+6** é histórica; a promoção adiciona **+0**. A escola `farmers_spell:gluttony`, itens, Foodgeist, projectiles/entities, status effects e receitas de aquisição não criam identidades adicionais.

## Gluttony spells — 6

- [Goodberry](spells/goodberry.md) — `farmers_spell:goodberry`
- [Ubiquitous](spells/phantom-loot.md) — `farmers_spell:phantom_loot`
- [Grease Coating](spells/seal-coat.md) — `farmers_spell:seal_coat`
- [Rotten Apple](spells/bad-apple.md) — `farmers_spell:bad_apple`
- [Chaotic Pastry Slash](spells/chaos-slash.md) — `farmers_spell:chaos_slash`
- [Brining Ritual](spells/preserve-circle.md) — `farmers_spell:preserve_circle`

## Registry authority

`ModSpells` mantém um único `DeferredRegister<AbstractSpell>` sob o namespace `farmers_spell` e registra exatamente os seis IDs acima no Iron's `SpellRegistry`.

A análise Java 21 do **JAR físico 1.0.5.1** provou seis `DeferredRegister.register` sem branches e o bootstrap em `FarmersSpell`, sem inferir compatibilidade/configuração de jogo. [Dossiê](EXACT-BINARY-SPELLS-1.0.5.1.md).

## School and reachability boundary

Todos os seis pertencem à escola provider-owned `farmers_spell:gluttony`. A escola usa `requiresLearning=false` e `allowLooting=false`.

A reachability catalogal foi fechada via focus de Gluttony e Scroll Forge do host, com `#minecraft:foods` e `farmers_spell:foodgeist_seasoning` como superfícies de focus. Probabilidade/economia e comportamento efetivo do modpack permanecem runtime QA.

## Explicit non-spell support

Não são contados como spells adicionais:

- a escola Gluttony;
- Foodgeist e sua progressão/recompensas;
- cooking recipes e estados de cozinha;
- projectiles/entities e status effects de suporte;
- gear/food/items que apenas servem como aquisição ou implementação;
- `BerserkCleaverSpell.java`, presente no source tree mas ausente do registrar exato.

## Authority boundary

Farmer's Spell é authority para os seis spells de Gluttony e conteúdo provider-specific. Iron's continua authority para host registry, mana, casting, cooldowns e Scroll Forge. Farmer's Delight continua authority para o substrato base de food/cooking.

Fontes canônicas: [EXACT-1.0.5.1-SPELL-INVENTORY.md](EXACT-1.0.5.1-SPELL-INVENTORY.md) e [README.md](README.md).
