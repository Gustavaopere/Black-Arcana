# Auditoria técnica — Ypsilon's Fundamentalism 1.1.7.1

## Provenance

Source authority: `ypsilonM/FundamentalPrinciples-1.21.1@a9b8f8222fb2a800edece8c1568984bd2a764fc2`.
`gradle.properties` declara `minecraft_version=1.21.1`, `mod_id=ypfundamentals`, `mod_version=1.1.7.1`, Iron's `3.16.2`.

## Registry

`ModSpells.java` registra exatamente 15 spells ativos. `YpsSchoolRegistry.java` registra a escola `ypfundamentals:fundamentalism` com spell power, magic resist e damage type próprios.

## Pipeline dos Principles

`SpellCategoriesGenerator` percorre **todo** `SpellRegistry.REGISTRY` no common setup, analisa bytecode por ASM e gera `config/fundamentalism/spell_categories.json`. Mapeamento canônico:

- Concentratio → `createEntity`
- Potentia → `usesShoot`
- Vitale → `usesSummon`
- Locus → `usesTargeting`
- Repetitio → `hasRecasts`
- Apparitio → `usesTeleport`
- Pertinacia → `addEffects`
- Expansio → `createsAoeEntities`
- Motus → `usesMobility`
- Perceptio → `usesRaycast`
- Remedium → `usesHealing`
- Augere → `usesPotentiation`
- Certum → `immutable`

Summons detectados com recast não recebem também `hasRecasts`, evitando dupla categoria nesse caso.

`PrinciplesLevelsAttachment` é o ledger persistente 0–20. XP necessário para cada próximo nível: `floor(20 + 20 × 1.3^level)`. A seleção de spells e os unlocks usam esse ledger server-side.

## Gates confirmados

- Law Of Regression: aprendido em Remedium >= 5; nível selecionado escala com Remedium.
- Saeptum: aprendido/selecionável quando Concentratio >=12, Locus >=10, Perceptio >=12 e Apparitio >=10.
- Tonatiuh (`sol`): `requiresLearning=true`; o event layer da release aprende o spell ao jogador que mata o Fire Boss do Iron's.
- Spellbook leveling é provider-native via Spellbook Covers quando a config está habilitada.

## Authority e deduplicação

- não duplicar XP/níveis de Principles;
- não recalcular categorias por heurística Black Arcana se `spell_categories.json`/provider estiver disponível;
- não adicionar segunda reflexão de projectile sobre Pyrokinesis;
- não criar segundo estado de location/recast para Lapsus;
- não duplicar domain state/barrier/clash de Saeptum;
- não duplicar mark ledger de Thorn;
- respeitar events do Iron's/NeoForge usados pelo provider.

## QA blockers estáticos

1. **Lapsus singleton state:** `private BlockPos location` fica na instância registrada da spell, não em cast data por jogador. Casts concorrentes podem compartilhar/limpar location. Multiplayer/dedicated-server QA obrigatório.
2. **Laceration tooltip vs heal handler:** tooltip mostra redução 40; `LivingHealEvent` aplica `×0.6` e depois `×0.8`, resultando 48% da cura original (52% redução) sem Blight. Com Blight, o handler Ypsilon aplica apenas `×0.8`; interação final com o listener do Blight exige runtime QA.
3. **Burning Spirit lvl 1 pulse:** `damageApplied = 3 × amplifier`; amplifier do nível 1 é 0, então pulse AoE tem dano 0 no nível 1, embora cleanse/ignite continuem ativos.
4. **Pyrokinesis magic projectile classification:** usa `getClass().toString().toUpperCase().contains("FIRE")` para `AbstractMagicProjectile`; compatibilidade com projectiles de fogo cujo nome de classe não contenha FIRE exige QA.
5. **Saeptum world mutation:** DomainEntity força region ticket, constrói/restaura barreira e teleporta entidades de volta. Não sobrepor com um domínio Black Arcana ou cleanup paralelo.
6. **Dependency delta:** source 1.1.7.1 compila contra Iron's 3.16.2; pack usa 3.16.3.

## Fail-closed

Qualquer bridge que não consiga provar caster, owner, target, Principle category, cast source ou provider lifecycle deve se abster. Não inferir sucesso por partículas/HUD.