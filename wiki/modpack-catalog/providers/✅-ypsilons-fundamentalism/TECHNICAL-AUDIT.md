# Auditoria técnica — Ypsilon's Fundamentalism 1.1.7.1

**Adendo JAR SHA-verificado 2026-10-13:** [15 identidades e schools compilados](EXACT-BINARY-SPELLS-1.1.7.1.md), [Java21 #38436717443](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38436717443) PASS, SHA-1 `a2855c253202a8fcc2925fcf5b1bf86d64fbe4da` = registro físico. `StealSummonSpell` existe como classfile, **não** é registrado; os treze Principles não adicionam magias. `COUNTED_EXACT` apenas para registry, mantendo +0 e runtime de Principles/XP, Lapsus, Saeptum, multiplayer e Iron's 3.16.3 ⚠️. Observações source-pinned abaixo permanecem evidência de design/risco, não execução.


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

`PrinciplesLevelsAttachment` é o ledger persistente 0–20. XP do nível atual n para o destino n+1: `(int)(20 + 20 × 1.3^(n+1))`; primeiro threshold=46, pois addExperience chama getExpForLevel(currentLevel+1). A seleção de spells e os unlocks usam esse ledger server-side.

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

## Reauditoria dos 13 Principles — 22/10/2026

[Fichas individuais e boundaries source](principles/README.md) aprofundam os 13 sistemas, **+0 spells**. Pontos críticos: Perceptio troca a base por 8+D/5 antes do bônus; Locus só atua com bbInflation positivo e pode compor depois; Vitale exige getRecastCount(1,player)==2; Repetitio só adiciona em totalRecasts>2; Pertinacia usa nível do receptor ServerPlayer/MagicMobEffect; Expansio modifica uma vez antes do clamp e exclui EchoingStrikeEntity; Potentia pode normalizar direção apenas no ramo accuracy<1; Certum tem guards distintos entre preflight/evento; Remedium não substitui healAmount do evento no ramo de insuficiência. Cada ficha preserva defaults/config/QA separados. Nenhum desses achados constitui prova de bug no modpack, API externa suportada ou integração homologada.


## Reauditoria das 15 spells — 22/10/2026

[Índice e boundaries de implementação](SPELL-PERK-BOUNDARIES-1.1.7.1.md): 15/15 fichas com parâmetros por eixo e consumidores source-causais. Pontos úteis às perks incluem hitbox dinâmica de Pull/Sol versus raio de efeito, Laceration com dano da arma, marcas Thorn anteriores ao resultado do dano, cura LawOfRegression fora de um evento mutador, refinement quadrático de Saeptum e orientação Taunt enviada uma vez. Os roteiros de QA ficam em cada ficha.

A herança `AbstractDomainEntity` tem o mesmo blob nos sources oficiais Ace’s 1.2.6.1 e 1.2.7.2; isso fecha somente a leitura desse arquivo, sem promover equivalência de JAR, ownership persistente, recuperação de barreiras, liberação de tickets ou compatibilidade com Iron’s 3.16.3. A chamada de ticket contém argumento `20` e `forceTicks=true`; não rotular o argumento como ticket level 20 nem presumir alcance efetivo nesta auditoria. A ficha Saeptum separa base e overrides.

O quadro histórico de IDs e os achados anteriores permanecem delimitados por prova. Não houve execução física de Ypsilon nem nova integração/runtime neste lote; build/dev NeoForge 21.1.248 e snapshot físico 21.1.250 são fatos distintos. O [painel atual](../../meta/PROGRESSO-CATALOGO-ATUAL.md) mede spells e Principles separadamente e mantém o denominador técnico global aberto.
