# Summon Animals

Status: `SOURCE-PINNED 5.13.1 / FAUNA-SUMMON RITUAL`

- Registry id: `ars_nouveau:ritual_animal_summon`
- Class: `RitualAnimalSummoning`
- Work cadence: every `60` game ticks
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native selection

Without consumed modifiers, the ritual builds a weighted list from the current biome's `MobCategory.CREATURE` spawn table, excluding Ars Nouveau's animal-summon blacklist.

Consumed augment items may instead match a provider `SummonRitualRecipe`. When a recipe matches, its own weighted mob list and required summon count are selected, but the recipe mob-entry type does not satisfy the spawn branch's SpawnerData check in the pinned source (runtime QA required).

`canStart` allows an unmodified ritual immediately; when modifier items are present, a valid summon recipe is mandatory.

## Provider-native lifecycle

Every 60 game ticks on the server, the baseline-biome path (SpawnerData entries) can:

1. picks a nearby randomized summon position;
2. selects a weighted spawn entry;
3. creates and adds the selected entity;
4. increments progress after a non-null entity construction and summon call (addFreshEntity result unchecked).

The default ritual finishes after progress reaches `5`; recipe-driven variants check the recipe's `count`, but their WeightedMobType entries do not pass the SpawnerData type-check in this pinned source (QA blocked).

## Authority / Black Arcana boundary

Biome weighting, summon-recipe overrides, entity identity and completion count remain Ars Nouveau authority. Black Arcana must not reinterpret these entities as Black Arcana familiars, duplicate the spawn, or award one ritual completion per summoned mob.

## QA

Source lifecycle is pinned to 5.13.1. The complete data-driven `SummonRitualRecipe` inventory and interactions with modded biome spawn tables remain separate data/runtime QA.

## Engenharia para perks — contrato de ritual

- **Fonte exata:** [`RitualAnimalSummoning.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualAnimalSummoning.java) no Ars 5.13.1.
- **Fonte dos mobs:** sem recipe, `getMobs` lê lista ponderada da biome atual para `MobCategory.CREATURE` e exclui tipos `ANIMAL_SUMMON_BLACKLIST`. Com recipe válido em `RecipeRegistry.SUMMON_RITUAL_TYPE`, substitui por `SummonRitualRecipe.mobs` e usa `recipe.value().count` como objetivo. `canStart` sem input é true; com input, exige recipe.
- **Spawn/cadência:** a cada 60 ticks servidor, calcula offset aleatório perto do brazier, seleciona `mobs.getRandom(rand)`; somente entradas `MobSpawnSettings.SpawnerData` que geram entidade não nula acionam `summon(...)` e `incrementProgress()`. Termina com progress >=5 (default) ou >=recipe count.
- **Perks:** weighted entries/regras de bioma e entradas dos datapacks alteram tipos reais. Não inventar tabela de probabilidades/modded species a partir da classe; nem contar cada mob como uma conclusão separada do ritual.
- **Estado:** ✅ identidade/métodos/source pin; ⚠️ valores no modpack, proteções, Save/Restart e multiplayer não testados nesta branch. ⛔ adapter RPG para mutation, bônus de recursos ou acompanhamento de um cast por ritual não implementado; Ars conserva Source e world authority.

## Certificação técnica estática — base por bioma versus branch de receitas (2026-10-25)

**✅ STATIC_TECHNICAL_CATALOG_ONLY · ⛔ mutating_hook=NOT_VERIFIED · ⚠️ physical_qa=NOT_TESTED.** ID ars_nouveau:ritual_animal_summon e classe RitualAnimalSummoning provados pela identidade compilada do publisher 5.13.1 (SHA-1 JAR 02782d071ee5fab3b5c4b8ced67b7e1748277dfd), **não** pela equivalência integral do bytecode dos métodos. Fontes imutáveis baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157: [RitualAnimalSummoning.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualAnimalSummoning.java), [SummonRitualRecipe.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/crafting/recipes/SummonRitualRecipe.java) e [AbstractRitual.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/ritual/AbstractRitual.java). Exemplo [bats.json](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/ars_nouveau/recipe/summon_ritual/bats.json).

- **Seleção padrão:** usa MobCategory.CREATURE a partir de world.getBiome(getPos()).value().getMobSettings().getMobs(category), filtra EntityTags.ANIMAL_SUMMON_BLACKLIST e constrói WeightedRandomList de MobSpawnSettings.SpawnerData. Quais mobs e probabilidades resultam depende do biome registry do modpack, não de hardcode da ficha.
- **Admissão por receita:** getRecipe() filtra RecipeRegistry.SUMMON_RITUAL_TYPE por r.value().matches(getConsumedItems()), escolhendo o primeiro match. Sem itens, canStart=true; com itens, canStart exige recipe. canConsumeItem admite um item se qualquer receita tiver r.value().augment.test(stack), o que não garante um conjunto final válido. SummonRitualRecipe fornece augment, MobSource, count e mobs.
- **Incompatibilidade source crítica:** SummonRitualRecipe.mobs é WeightedRandomList<WeightedMobType>. WeightedMobType é um record que implementa WeightedEntry, **mas não MobSpawnSettings.SpawnerData**. Em RitualAnimalSummoning.tick, o ramo que executa summon e incrementProgress exige estritamente entry instanceof MobSpawnSettings.SpawnerData. Assim, **no source fixado**, uma entrada selecionada da lista de receita é WeightedMobType e não aciona summon/incrementProgress. A receita gerada bats.json define augment minecraft:amethyst_shard, count 5 e WeightedMobType com minecraft:bat, mas isso não prova spawn funcional. Com count positivo a branch pode permanecer indefinidamente sem avançar. **Esta incongruência exige comparação de métodos compilados e QA provider-live antes de qualquer perk baseada em receita.**
- **Campo não consumido pela seleção:** SummonRitualRecipe.MobSource oferece CURRENT_BIOME e MOB_LIST, mas RitualAnimalSummoning.getMobs não consulta mobSource; seleciona lista da receita quando recipe.isPresent() independentemente do valor do enum. Não inferir que CURRENT_BIOME preserva o caminho default por nome.
- **Geometria, tempo e taxa:** a cada world.getGameTime()%60==0 no servidor, escolhe getPos().above().east(rand.nextInt(3)-rand.nextInt(6)).north(rand.nextInt(3)-rand.nextInt(6)). Deslocamento dos dois eixos varia de -5 a +2 e não deve ser tratado como círculo uniforme. Com SpawnerData válido e EntityType.create(world) não nulo, summon(mob,pos) chama addFreshEntity e envia partículas END_ROD aos ServerPlayer; depois incrementProgress. **O retorno de addFreshEntity não é verificado** e o incremento pode ocorrer apesar de evento/admissão de spawn falhar. O efeito não é projétil nem dano.
- **Término e cache:** sem recipe, termina quando getProgress()>=5; com recipe quando getProgress()>=recipe.value().count, inclusive se nenhuma entidade foi efetivamente aceita pelo mundo. Campos recipe e mobs não são serializados pela classe; após read/tick são reconstruídos de receitas atuais e biome atual, enquanto RitualContext.progress é persistido pelo pai. Lista weighted vazia pode impedir progresso para metas positivas.
- **Custo e authority:** getSourceCost()=0 herdado de AbstractRitual, o que **não equivale a ritual grátis**: consumo de tablet/ingredientes e processo de ativação pertencem ao brazier Ars. Não há hook mutador externo de chance, espécie, count, alcance, Source ou replay neste ramo; nenhuma Mastery por mob nem familiar Black Arcana pode ser creditada por inferência. WorldEffectPolicy rege efeitos próprios do Black Arcana, não é interceptor do spawn Ars; RPG Skill Tree segue sibling de progressão apenas por contrato real.

**Gate fail-closed / QA físico:** testar a receita bats.json e addons, confirmar WeightedMobType versus SpawnerData no bytecode 5.13.1, pesos, MobSource, pools por bioma, count, spawn cancelado, unload/reload, mudanças de datapack e custos de inputs. mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED. O ✅ aqui certifica a **análise estática**, não o funcionamento da variante por receita.
