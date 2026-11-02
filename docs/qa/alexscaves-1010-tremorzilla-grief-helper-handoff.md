# Handoff técnico — Tremorzilla Beam: NeoForge grief guard e delegações do mundo (1.0.10)

**Escopo:** análise estática, read-only e SHA-exata de quatro métodos do JAR publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, sem copiar código-fonte proprietário, editar runtime ou presumir proteção de terceiros. Complementa os [relatórios de mundo/LOS](alexscaves-1010-tremorzilla-world-los-handoff.md) e [CFG normal](alexscaves-1010-tremorzilla-normal-cfg-handoff.md).

## Identidade da prova

- Modlist do sibling `neoforge-rpg-skilltree/main@59ff2a0e827fd08faa603f4482f8104ac433383c`: `alexscaves`, versão 1.0.10, Minecraft 1.21.1.
- Artefato publisher: SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, tamanho 75.279.314 bytes.
- Manifesto: [EXACT-TREMORZILLA-GRIEF-HELPERS-1.0.10.json](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-TREMORZILLA-GRIEF-HELPERS-1.0.10.json) · [sonda javap](alexscaves_1010_tremorzilla_grief_helper_probe.py) · [testes sintéticos](alexscaves_1010_tremorzilla_grief_helper_probe_test.py) · [workflow dedicado](../../.github/workflows/alexscaves-1010-tremorzilla-grief-helper.yml).
- O inventário registra SHA-256 das classes e SHA-256 de parse dos métodos, com âncoras exatas de opcode/desvio; não considera transformações dinâmicas, dispatch em dependências nem a classe efetivamente carregada em servidor modpack.

## Guarda inicial do `breakBlocksAround`

O bytecode do `TremorzillaEntity.breakBlocksAround(Vec3,float,boolean,boolean,float):boolean` contém a cadeia:

| Condição observada | Offsets JVM | Resultado no CFG compilado |
|---|---|---|
| `isBaby()` | invocação `@1`, `ifne 28 @4` | `true` desvia para `iconst_0 @28` e `ireturn @29` |
| `ACPlatform.canEntityGrief(Level,Entity)` | chamada `@12`, `ifeq 28 @15` | `false` desvia para retorno `false` em `@28–29` |
| `Level.isClientSide()` | chamada `@22`, `ifeq 30 @25` | `true` leva a `@28–29`; `false` segue para o bloco de processamento em `@30` |

A PR #1006 demonstrou que ambas as chamadas de controle relevantes dominam, no CFG normal intramétodo, os quatro pontos selecionados: `Level.destroyBlock @249`, `ACCompat.onBlockExploded @268`, `ACCompat.createEntity @296` e `Level.addFreshEntity @349`.

**Esse resultado agora sustenta a direção dos ramos iniciais**, além de sua dominância. Não comprova todos os caminhos de exceção, mutações indiretas, callbacks assíncronos, checks de chunk, proteção de claims ou que cada um dos quatro pontos seja executado em toda ativação do feixe.

## Delegações nativas 1.0.10 efetivamente verificadas

| Método próprio do provider | Identidade compilada | Delegação observada | Limite |
|---|---|---|---|
| `ACPlatform.canEntityGrief(Level,Entity):boolean` | `ACPlatform.class` SHA `662a4d2593fe515ed8790bad06d8184d1eb921423033dfd11b3b44142dedc3e6`; 4 instruções no método | `invokestatic net.neoforged.neoforge.event.EventHooks.canEntityGrief @2`, `ireturn @5` | O corpo do `EventHooks` NeoForge 21.1.248, plugins de proteção, cancelamento e configuração **ainda não foi auditado neste recorte** |
| `ACCompat.onBlockExploded(BlockState,Level,BlockPos,Explosion):void` | SHA de classe `333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b`; 6 instruções no método | `BlockState.onBlockExploded @4`, `return @7` | Não garante permissões de explosão, rollback ou comportamento físico |
| `ACCompat.createEntity(EntityType,Level):Entity` | mesma classe compilada `ACCompat`; 4 instruções no método | `EntityType.create @2`, `areturn @5` | Não é confirmação de spawn autorizado, atribuição de dono, nuke final ou política de mundo |

A cadeia estática de delegação é:

`TremorzillaEntity.breakBlocksAround` → `ACPlatform.canEntityGrief` → `NeoForge EventHooks.canEntityGrief` (implementação e integrações externas ainda não verificadas).

`ACCompat.onBlockExploded` e `createEntity` são wrappers de métodos nativos, não uma prova de passagem pelo `WorldEffectPolicy` de Black Arcana.

## Implicação para perks e decisões pendentes

Não interceptar diretamente o método para aumentar raio/destruição, nem usar essa cadeia como prova de compatibilidade universal com claims. Alterar tamanho/volume da área potencialmente aumenta a quantidade de blocos e entidades afetados; dependeria de limites explícitos, respeito às configurações de griefing, verificação de carregamento de chunks, atribuição de origem e aceitação física em modpack.

Próximo alvo concreto: bytecode SHA-exato de **NeoForge 21.1.248 `EventHooks.canEntityGrief`** e do pipeline de eventos que essa função invoca; só então avaliar se a API delegada satisfaz condições de autorização aplicáveis. O argumento `Entity` recebido do `TremorzillaEntity` é evidência de quem é fornecido ao helper; **não** comprova crédito final de player/passageiro nem regras de proteção.

**Status:** ⚠️ `STATIC_SELECTED_JVM_DELEGATION_VERIFIED`, `NOT_CERTIFIED`, `NO_MUTATION`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. +0 fichas e +0 providers certificados; Stage 06 não muda.
