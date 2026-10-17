# Epic Fight 21.17.3.1 — compatibilidade de attribute modifiers legados (16/10/2026)

**Estado:** ⚠️ `RAW_ONLY_NOT_PROVEN_LOADED` nos cinco recursos do JAR físico. A existência dos campos serializados é comprovada; sua aplicação efetiva em entidade **não** foi comprovada. O teste abaixo procura **somente** a aceitação sintática pelo codec de Minecraft do classpath de testes, sem iniciar Epic Fight nem carregar datapack do modpack.

## Autoridade das fontes

- Mod físico instalado: `epic-fight-21.17.3.1-mc1.21.1-neoforge.jar`, mod id `epicfight`, CurseForge `405076/8175609`, SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0` e SHA-256 `8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526`. `42/42` JSONs e seus campos declarados foram comparados no [gate #38983180648](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38983180648) e no [gate #38983851582](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38983851582), ambos `SUCCESS`.
- Fonte comparativa **adjacente**, não exata: [Skill.java L57–71](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/Skill.java#L57-L71) define `ATTRIBUTE_ENTRY_CODEC` com `AttributeModifier.MAP_CODEC`. [Skill.java L128–139](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/Skill.java#L128-L139) limpa os atributos e chama `ATTRIBUTE_ENTRY_CODEC.parse(NbtOps.INSTANCE,...).result().ifPresent(...)`. A revisão upstream declara `21.17.3`, enquanto o JAR do pack declara `21.17.3.1`.
- Prova adicional exata: o [probe de invocações #38983851582](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38983851582) registra `Codec.parse` antes de `Optional.ifPresent` no método compilado `Skill.loadDatapackParameters`, mas **não** observa se o parse devolve sucesso ou se a chamada é alcançada.

## Cinco JSONs de atributos com formato legado, exatos como dados físicos

| Skill core | Forma dos modificadores no JSON físico | Criticidade |
|---|---|---|
| `adaptive_skin` | `max_health`: `addition +6`, `name` e `uuid` | Não assumir bônus de HP |
| `adrenaline_fiend` | `attack_speed`: `multiply_total +0.1`; `attack_damage`: `multiply_total +0.075` | Não assumir DPS/velocidade alterados |
| `catharsis` | `stamina_regen`: `addition +0.15`; `attack_damage`: `multiply_total +0.1` | Não creditar regen/dano automaticamente |
| `bonebreaker` | `attack_speed`: `multiply_total +0.15` | Não assumir ataque mais rápido |
| `vengeance` | `max_health`: `addition +3`; `attack_damage`: `multiply_total +0.075` | Não assumir HP/dano extra |

Os JSONs físicos trazem nomes/UUIDs, mas não o campo moderno `id` que o formato esperado pela API vanilla da revisão sugere. O experimento de codec vanilla abaixo demonstrou que os dois formatos legados representativos testados **não produzem um AttributeModifier decodificado**, enquanto o controle moderno é aceito. É evidência de **incompatibilidade do formato vanilla nessa versão**; continua **não sendo** observação de loading ou atributos finais no runtime físico do Epic Fight.

## Teste controlado em implementação de Minecraft real

- [`EpicFightVanillaAttributeModifierCodecTest.java`](https://github.com/Gustavaopere/Black-Arcana/blob/docs/catalog-perk-causality-20261015/src/test/java/dev/gustavopere/blackarcana/integration/epicfight/EpicFightVanillaAttributeModifierCodecTest.java) usa o tipo real `net.minecraft.world.entity.ai.attributes.AttributeModifier.MAP_CODEC` e `NbtOps.INSTANCE`, do classpath unitário Minecraft **1.21.1 / NeoForge 21.1.248** desta `main` (o pack físico aponta NeoForge 21.1.250, diferença **não ignorada**).
- Controles: shape legado `addition` e `multiply_total` com `name/uuid`, comparados ao shape `id` + `add_value`. Nenhum código/fonte Epic Fight é copiado; são registros NBT independentes reproduzidos a partir de campos públicos do JAR.
- **Status de execução confirmado:** [Black Arcana CI #38984538266](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38984538266), **SUCCESS** no commit com o teste Java. `Unit tests` passou contendo os **três asserts**: `addition` + `name/uuid` -> **sem resultado de parse**; `multiply_total` + `name/uuid` -> **sem resultado de parse**; controle moderno `id` + `add_value` -> **resultado de parse presente**. O job `verify` também teve `Diff sanity`, NeoForge build, **108/108 Foundation GameTests required** e `Dedicated-server smoke test: PASS`; o job separado de companion Stage 05 também terminou **SUCCESS**. Trata-se do codec real de Minecraft **1.21.1 / NeoForge 21.1.248 usado em CI**, **não** do Epic Fight carregado no pack físico com NeoForge 21.1.250. **Cinco skills seguem RAW_ONLY_NOT_PROVEN_LOADED no runtime** até observação direta ou teste dedicado provider-loaded.

## Extensão do teste para oito registros físicos e decoder de listas

- **Prova parcial verificada:** [Black Arcana CI #38985688067](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38985688067), no commit do experimento Java ampliado: `Unit tests=SUCCESS`, `Diff sanity=SUCCESS`, `NeoForge build=SUCCESS`. **O workflow foi cancelado por um commit posterior enquanto ainda faltavam os GameTests**; não é um `SUCCESS` global e não substitui [#38984538266](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38984538266), cuja CI completa estava aprovada.
- **Escopo novo:** todas as **oito linhas serializadas** dos **cinco** JSONs (`adaptive_skin=1`, `adrenaline_fiend=2`, `catharsis=2`, `bonebreaker=1`, `vengeance=2`) foram transformadas em `CompoundTag` individuais e submetidas a `AttributeModifier.MAP_CODEC.codec().parse(NbtOps.INSTANCE,...)`. **Nenhuma das oito produziu resultado de parse completo** no codec vanilla do classpath unitário.
- **Causas isoladas por controles negativos:** registrar `id` moderno mas usar operação `addition`/`multiply_total` continua sem resultado; usar `name/uuid` com operações modernas `add_value`/`add_multiplied_total` também não produz resultado. Portanto o teste mostra incompatibilidades **independentes** tanto na identidade do modifier quanto na operação, na versão de Minecraft/NeoForge usada.
- **Controles positivos:** `id + add_value` e `id + add_multiplied_total` retornam modifier decodificado. Uma lista NBT de **dois modifiers modernos** produz **duas entradas** por `Codec.list(AttributeModifier.MAP_CODEC.codec())`; isso evita que o resultado negativo seja vacuamente causado por falha no decoder geral de listas.
- **Controles da lista negativa:** lista NBT dos oito legados retorna `DataResult.result()` ausente; lista mista com uma entrada moderna válida e uma legada também não produz **resultado completo**. Testa `Codec.list` com codec vanilla de modifier, **não** executa a classe `Skill.ATTRIBUTE_ENTRY_CODEC` própria do Epic Fight, que também decodifica `Holder<Attribute>`.
- **Resultado de escopo:** evidência Java direta para **8/8 linhas físicas de modifier**, mais cenários de lista e controles, **somente** do codec vanilla Minecraft 1.21.1 no CI do Black Arcana (**NeoForge 21.1.248**). Não houve aplicação de atributos em entidades com Epic Fight 21.17.3.1 carregado e NeoForge 21.1.250, nem ensaio de datapack override. Preservar os cinco IDs como **⚠️ `RAW_ONLY_NOT_PROVEN_LOADED`** para o provider.

## Gate de aceitação ainda bloqueado

1. ✅ **Concluído somente para os dois formatos representativos no codec vanilla testado:** NBT legado `name/uuid/addition` e `name/uuid/multiply_total` rejeitados, `id/add_value` aceito; evidência no CI #38984538266, sem reproduzir o runtime Epic Fight.
2. Repetir ou inspecionar parsing **dentro do Epic Fight carregado** na versão física 21.17.3.1 e NeoForge 21.1.250, incluindo override dos cinco JSONs e mudanças reais de atributo.
3. Confirmar event side, lifecycle, eventual fallback/migração de formato e o comportamento correto após reload/death/respawn/dimension.
4. Somente depois formular hooks de perks fail-closed e de progressão do RPG Skill Tree; Black Arcana continua autoridade do próprio runtime mágico.

**Resultado atual:** cinco registros físicos legados ainda classificados `RAW_ONLY_NOT_PROVEN_LOADED` quanto ao runtime do Epic Fight, mesmo após os **3 controles Java unitários aprovados** do codec vanilla. **0 bônus homologados**, **+0 magias**, sem Stage ou merge.
