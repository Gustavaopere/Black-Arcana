# Alex's Caves 1.0.10 — auditoria dos tipos de dano

**Status:** ⚠️ recursos JSON `11/11` e **factories compiladas `11/11` mapeadas**, com **14 invocações diretas em 12 classes**. O [contrato Dark Arrow](dark-arrow.md) e o [equipamento Dreadbow](../equipment/dreadbow.md) foram consolidados na [prova estática conjunta](../EXACT-DREADBOW-CONTRACTS-1.0.10.md): **2/11 tipos de dano possuem contratos estáticos certificados**, incluindo agora [Acid e seus dois emissores](../EXACT-ACID-CONTRACT-1.0.10.md). Os demais nove consumidores continuam parciais; hooks, hit counts medidos e QA física permanecem pendentes.

- Artefato oficial: SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, tamanho 75.279.314 bytes.
- Auditor: [`docs/qa/alexscaves_1010_damage_type_probe.py`](../../../../../docs/qa/alexscaves_1010_damage_type_probe.py); [CI da sonda](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40985275338).
- Manifesto: [JSON fixado](EXACT-RESOURCE-MANIFEST-1.0.10.json); inclui hashes por membro do ZIP, valores JSON, seis tag JSONs e memberships textuais diretas.
- Proveniência: os valores são lidos do JAR 1.0.10 verificado, **não** da fonte 1.1.1.
- Contagem de magia: 0 spells/ações novas; estes 11 registros são classificadores de dano, não 11 feitiços.

## Campos literais comparados

| Registry ID | `message_id` | `scaling` | `exhaustion` | Tags diretas | Ficha |
|---|---|---|---:|---:|---|
| `alexscaves:acid` | `acid` | `never` | 0.1 | 0 | [`acid`](acid.md) |
| `alexscaves:dark_arrow` | `desolate_dagger` | `never` | 0.3 | 3 | [`dark_arrow`](dark-arrow.md) |
| `alexscaves:desolate_dagger` | `desolate_dagger` | `never` | 0.3 | 1 | [`desolate_dagger`](desolate-dagger.md) |
| `alexscaves:forsaken_sonic_boom` | `forsaken_sonic_boom` | `never` | 0.3 | 0 | [`forsaken_sonic_boom`](forsaken-sonic-boom.md) |
| `alexscaves:gumball` | `gumball` | `never` | 0.3 | 0 | [`gumball`](gumball.md) |
| `alexscaves:intentional_game_design` | `intentional_game_design` | `never` | 0.3 | 0 | [`intentional_game_design`](intentional-game-design.md) |
| `alexscaves:nuke` | `nuke` | `never` | 0.1 | 3 | [`nuke`](nuke.md) |
| `alexscaves:radiation` | `radiation` | `never` | 0.1 | 0 | [`radiation`](radiation.md) |
| `alexscaves:raygun` | `raygun` | `never` | 0.3 | 3 | [`raygun`](raygun.md) |
| `alexscaves:spirit_dinosaur` | `spirit_dinosaur` | `never` | 0.3 | 2 | [`spirit_dinosaur`](spirit-dinosaur.md) |
| `alexscaves:tremorzilla_beam` | `tremorzilla_beam` | `never` | 0.3 | 0 | [`tremorzilla_beam`](tremorzilla-beam.md) |

## Advertências de contrato

O recurso `dark_arrow` possui `message_id=desolate_dagger`, igual a `desolate_dagger`; ambos os arquivos possuem o mesmo conteúdo e hash, mas **IDs de dano distintos**. Isso deve ser preservado, sem normalização editorial da fonte.

A tag `minecraft:bypasses_cooldown` trata de classificação de dano no Minecraft, não de cooldown de casting de qualquer feitiço. `minecraft:is_explosion`, `minecraft:is_projectile` e `minecraft:is_fire` são declaradas como memberships **textuais**, não como comprovação da aplicação do `DamageSource` no jogo. A tag `alexscaves:deep_one_ignores` é inventariada, mas não lista diretamente nenhum dos onze IDs.

**PENDENTE:** concluir os nove outros contratos de consumidores, owner/causa, fórmulas e targeting. Proteção PvP, mutação segura e QA física continuam pendentes também para Acid e Dark Arrow. Os nove tipos parciais permanecem `NOT_CERTIFIED`; hooks `NOT_VERIFIED` e QA `NOT_TESTED` em todo o recorte.

## Mapa binário SHA-exato de `ACDamageTypes`

**Nova evidência** — [manifesto de bytecode](EXACT-CONSUMERS-1.0.10.json) · [auditoria CI](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40993193816). No JAR publisher fixado 1.0.10, `javap -c -p -s` confirmou 11 factories e 14 pontos de invocação direta (`invokestatic`) em 12 classes. Foram filtradas 16 classes candidatas por presença de referência de constant pool a `ACDamageTypes`. A prova não executa o jogo e não homologa efeitos.

| Tipo de dano | Factory Java exata | Chamadas diretas | Classes chamadoras | Ficha |
|---|---|---:|---:|---|
| `alexscaves:acid` | `causeAcidDamage` | 2 | 2 | [acid](acid.md) |
| `alexscaves:dark_arrow` | `causeDarkArrowDamage` | 1 | 1 | [dark_arrow](dark-arrow.md) |
| `alexscaves:desolate_dagger` | `causeDesolateDaggerDamage` | 1 | 1 | [desolate_dagger](desolate-dagger.md) |
| `alexscaves:forsaken_sonic_boom` | `causeForsakenSonicBoomDamage` | 2 | 1 | [forsaken_sonic_boom](forsaken-sonic-boom.md) |
| `alexscaves:gumball` | `causeGumballDamage` | 1 | 1 | [gumball](gumball.md) |
| `alexscaves:intentional_game_design` | `causeIntentionalGameDesign` | 1 | 1 | [intentional_game_design](intentional-game-design.md) |
| `alexscaves:nuke` | `causeNukeDamage` | 1 | 1 | [nuke](nuke.md) |
| `alexscaves:radiation` | `causeRadiationDamage` | 1 | 1 | [radiation](radiation.md) |
| `alexscaves:raygun` | `causeRaygunDamage` | 1 | 1 | [raygun](raygun.md) |
| `alexscaves:spirit_dinosaur` | `causeSpiritDinosaurDamage` | 2 | 2 | [spirit_dinosaur](spirit-dinosaur.md) |
| `alexscaves:tremorzilla_beam` | `causeTremorzillaBeamDamage` | 1 | 1 | [tremorzilla_beam](tremorzilla-beam.md) |

**Divergência relevante:** `NuclearExplosionEntity.tick()` contém referências tanto a `causeIntentionalGameDesign` quanto a `causeNukeDamage`; não se conclui que ambas executem no mesmo tick. `ForsakenAttackGoal.tick()` contém duas referências a `causeForsakenSonicBoomDamage`, mas isso não demonstra dois hits por tick. `dark_arrow` e `desolate_dagger` continuam tipos diferentes embora os JSONs compartilhem `message_id`.

A sobrecarga de `DamageSourceRandomMessages` com argumento `Entity` é usada por algumas factories, enquanto outras recebem somente `RegistryAccess`. Isto permite documentar a assinatura compilada, mas **não** comprova attacker attribution, ownership, targeting, fórmulas, mitigação, repetição de impacto, segurança de hook ou elegibilidade para perks. Contratos técnicos estáticos documentados **2/11**, limitados a Acid e Dark Arrow; os manifestos parciais desta seção não homologam hooks; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`.

## Janelas de bytecode dos quatro consumidores prioritários

A auditoria [SHA-exata das janelas](EXACT-DAMAGE-PATH-ANCHORS-1.0.10.json) amplia a auditoria das 11 factories com quatro classes de uso direto: `ForsakenAttackGoal.tick()`, `DarkArrowEntity.onHitEntity()`, `DesolateDaggerEntity.tick()` e `NuclearExplosionEntity.tick()`. A prova do binário 1.0.10 tem **6 invocações de factory e 5 IDs de dano envolvidos**, sem novas identidades mágicas. Os números abaixo são somente o recorte dessas quatro classes.

| Consumer compilado | Instruções do método | Branch opcodes | Factories próximas | Evidência |
|---|---:|---:|---|---|
| `ForsakenAttackGoal.tick` | 826 | 98 | `causeForsakenSonicBoomDamage@108`, `causeForsakenSonicBoomDamage@576` | [snapshot](EXACT-DAMAGE-PATH-ANCHORS-1.0.10.json) |
| `DarkArrowEntity.onHitEntity` | 48 | 7 | `causeDarkArrowDamage@37` | [snapshot](EXACT-DAMAGE-PATH-ANCHORS-1.0.10.json) |
| `DesolateDaggerEntity.tick` | 361 | 20 | `causeDesolateDaggerDamage@339` | [snapshot](EXACT-DAMAGE-PATH-ANCHORS-1.0.10.json) |
| `NuclearExplosionEntity.tick` | 348 | 39 | `causeIntentionalGameDesign@605`, `causeNukeDamage@618` | [snapshot](EXACT-DAMAGE-PATH-ANCHORS-1.0.10.json) |

**Nuclear:** a chamada `isIntentionalGameDesign()` é seguida de um branch local que escolhe `causeIntentionalGameDesign` ou `causeNukeDamage` antes de `LivingEntity.hurt()` (offsets 592–623). Não implica que ambos sejam aplicados ao mesmo alvo ou tick.

**Forsaken:** há duas regiões `causeForsakenSonicBoomDamage()`, com gates distintos. Na segunda, a tag `FORSAKEN_IGNORES`, uma constante `0.65f` e `Math.ceil()` estão presentes no caminho que referencia `LivingEntity.hurt()`. Não se infere frequência nem dano final sem auditoria adicional.

**Projéteis:** `DarkArrowEntity` referencia `getShadowArrowDamage`, `isPerfectShot`, `isAlliedTo` e `ACCompat.hurt`; `DesolateDaggerEntity` referencia o encantamento `IMPENDING_STAB` e `ACCompat.hurt`.

O manifesto de janelas mantém seu escopo `STATIC_BYTECODE_ANCHORS_ONLY`. A certificação posterior de Dark Arrow usa o contrato consolidado e evidências adicionais, sem alterar esse snapshot nem homologar hook seguro.

## Helpers intermediários — evidência exata do bytecode 1.0.10

A inspeção [`EXACT-DAMAGE-HELPERS-1.0.10.json`](EXACT-DAMAGE-HELPERS-1.0.10.json) de cinco métodos em três classes acrescentou contexto ao Sonic Boom, Dark Arrow e Desolate Dagger, sem adicionar cinco magias ou certificar cinco hooks. O método `ForsakenEntity.getSonicDamageAgainst(LivingEntity)` apresenta **45.0f** para a tag `WEAK_TO_FORSAKEN_SONIC_ATTACK` ou **4.0f** para os demais tipos. `ACCompat.hurt` delega à função `Entity.hurt`. `ACCompat.enchantLevel` lê o nível do encantamento do `ItemStack` (retornando zero se não encontra a chave). `DarkArrowEntity.getShadowArrowDamage` e `isPerfectShot` consultam os accessors sincronizados correspondentes.

| Helper binário SHA-exato | ABI JVM | Contrato parcial |
|---|---|---|
| `getSonicDamageAgainst` | `(Lnet/minecraft/world/entity/LivingEntity;)F` | ⚠️ ABI / operações observadas; hook `NOT_VERIFIED` |
| `hurt` | `(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/damagesource/DamageSource;F)Z` | ⚠️ ABI / operações observadas; hook `NOT_VERIFIED` |
| `enchantLevel` | `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/resources/ResourceKey;)I` | ⚠️ ABI / operações observadas; hook `NOT_VERIFIED` |
| `getShadowArrowDamage` | `()F` | ⚠️ ABI / operações observadas; hook `NOT_VERIFIED` |
| `isPerfectShot` | `()Z` | ⚠️ ABI / operações observadas; hook `NOT_VERIFIED` |

**Atenção:** `45.0f` e `4.0f` são retornos da função para uma classificação de target; a operação adicional `ceil(base×0.65)` pertence a **um** dos caminhos de `ForsakenAttackGoal.tick()`, não a todos. Não inferir dano final, controle de autoria, regressão de datapack ou hook mutador a partir das cinco ABIs.

## Dark Arrow — propagação do estado do Dreadbow

A auditoria [`EXACT-DARK-ARROW-STATE-1.0.10.json`](EXACT-DARK-ARROW-STATE-1.0.10.json) adiciona os defaults compilados `SHADOW_ARROW_DAMAGE=0.0f` e `PERFECT_SHOT=false`, dois setters diretos de `SynchedEntityData` e três chamadas em `DreadbowItem` (`releaseUsing`: dano e tiro perfeito; `onUseTick`: dano). A compilação apresenta argumentos `2.0f` / `3.0f` em `releaseUsing` e `2.0f` em `onUseTick`; não estabelece dano efetivo, chance de perfect shot, autorização nem hook estável.

**Escopo:** 5 classes candidatas, 4 selecionadas, 28 referências/anchors simbólicas; sem adicionar raízes mágicas ou contratos `COMPLETE_PERK_READY`. A [ficha Dark Arrow](dark-arrow.md) identifica offsets JVM e limites para perks.


## Encantamentos que definem os flags da Dark Arrow

O [manifesto SHA-exato](EXACT-DREADBOW-DECISIONS-1.0.10.json) rastreia `PRECISE_VOLLEY` até o slot local 8, usado para selecionar `2.0f`/`3.0f` no setter de dano da Dark Arrow, e `TWILIGHT_PERFECTION` mais `getPerfectShotTicks(ItemStack) > 0` até o slot local 10, usado pelo setter `PERFECT_SHOT`. `RELENTLESS_DARKNESS` e `SHADED_RESPITE` também são consultados pelo Dreadbow. Isso não adiciona novas magias ou contratos completos para perks; a implementação do contador e a colisão são descritas agora nas fichas consolidadas, enquanto autoridade de mutação e QA física permanecem pendentes.
