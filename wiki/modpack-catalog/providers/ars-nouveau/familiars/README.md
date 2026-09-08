# Ars Nouveau — Familiars

State: `6/6 SOURCE-PINNED / INDIVIDUAL PAGES COMPLETE / RUNTIME QA PENDING`

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`.

A registry de produção 5.13.1 registra seis familiar holders. A árvore de source também contém `JabberwogFamiliarHolder`, mas ele **não** é registrado por `APIRegistry.setup()` nesta release e portanto não entra no catálogo ativo.

## Familiars ativos

1. [Starbuncle](starbuncle.md) — `ars_nouveau:familiar_starbuncle`
2. [Drygmy](drygmy.md) — `ars_nouveau:familiar_drygmy`
3. [Whirlisprig](whirlisprig.md) — `ars_nouveau:familiar_whirlisprig`
4. [Wixie](wixie.md) — `ars_nouveau:familiar_wixie`
5. [Bookwyrm](bookwyrm.md) — `ars_nouveau:familiar_bookwyrm`
6. [Amethyst Golem](amethyst-golem.md) — `ars_nouveau:familiar_amethyst_golem`

## Fluxo provider-native de aquisição

1. O Ritual of Binding procura uma entidade elegível segundo os predicates dos holders registrados.
2. A entidade é convertida em um Bound Script ligado ao holder correspondente.
3. Usar o `FamiliarScript` no servidor desbloqueia o familiar no capability Ars do jogador; se ele já for possuído, o script não é consumido.
4. Summon/unsummon e persistent familiar data continuam provider-owned.

## Lifecycle comum

`FamiliarEntity` mantém owner UUID, holder id, nome/cor/cosmético persistentes e um conjunto server-side de familiars ativos. Familiars não despawnam por distância. A cada 20 ticks, um familiar sem owner resolvível é terminado/removido. Quando outro familiar é invocado pelo mesmo owner, o anterior recebe `terminatedFamiliar=true`.

O common entity declara `manaReserveModifier = 0.15`; `FamiliarEvents` adiciona esse valor ao reserve do cálculo de mana do owner. A interpretação/balanceamento desse reserve continua authority do Ars.

## Boundary Black Arcana

- Familiar ownership, unlock, summon, mana reserve e efeitos provider-native pertencem ao Ars Nouveau.
- Black Arcana não deve duplicar o familiar capability nem tratar automação base de Starbuncle/Drygmy/Wixie como se fosse familiar ownership.
- Bonuses disparados por eventos de spell/cost/effect devem ser observados pelo hook real; não conceder bônus paralelos por simples proximidade da entidade.
- Divergências entre textos do livro e paths executáveis permanecem marcadas como QA.
