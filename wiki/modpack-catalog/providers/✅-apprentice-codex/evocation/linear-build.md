# Linear Build

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `mutation=NO_MUTATION` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:linear_build` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Interfaces | `ICastDataSerializable` via `LinearBuildCastData`; sem interface de dano |
| Escola | `SchoolRegistry.EVOCATION_RESOURCE` (Evocation) |
| Raridade mínima declarada | `UNCOMMON` |
| Níveis declarados | 1 (`setMaxLevel(1)`) |
| Tipo de cast | `INSTANT` |
| Cooldown declarado | `0.5 s` |
| Recurso | Mana do Iron's (`baseManaCost=20`, `manaCostPerLevel=0`); custo adicional por bloco vem de `ApprenticeCodexServerConfig` via `getAdditionalPlaceManaCost` |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.linearbuild.LinearBuild` |
| Auxiliares da mesma raiz | `LinearBuildCastData`, `BlockTemplateResult`, `PlacementTarget`, `LinearBuildItemSource(s)`, `LinearBuildConfigState`, `CraftsmansDelight` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1. Os coeficientes declarados não são os valores efetivos instalados: mana, cooldown, spell power, nível, raridade e multiplicadores do host permanecem `NÃO VERIFICADOS` (`AbstractSpell` lê `SpellConfigManager`, atributos, Curios e eventos).

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("linear_build", LinearBuild::new)` |
| Config | `UNCOMMON`, nível 1, cooldown `0.5`, `EVOCATION_RESOURCE` |
| Coeficientes | <init>: `baseSpellPower=0`, `spellPowerPerLevel=0`, `baseManaCost=20`, `manaCostPerLevel=0`, `castTime=0` |
| Alcance | `getRange(@Nullable LivingEntity)` → `32` com `CraftsmansDelight.isEquippedBy(caster)`, senão `BASE_RANGE=24`; consumido por `getClientBlockTargetingRange`, `raycastTargetBlock` e `isWithinAxisRange` |
| Template | `resolveHeldBlockTemplate`: offhand primeiro, depois mainhand; aceita `BlockItem` ou `LuminousDevice.getSelectedStack` |
| Validação | `validateBlockTemplate`: rejeita `DoorBlock`/`BedBlock` (`invalid_large_size`) e `Blocks.LINEAR_BUILD_DENYLIST` (`invalid_by_deny_list`) |
| Alvo | `BlockTargetingHelper.getPendingHitTargetIgnoringRange` ou `level.clip(...,COLLIDER,Fluid.NONE)`, com `isWithinAxisRange` em X/Y/Z |
| Custo por bloco | `ApprenticeCodexServerConfig.linearBuildConfig().manaCostPerBlock()` (servidor) / `LinearBuildConfigState.manaCostPerBlock()` (cliente), com `CraftsmansDelight.applyManaCostDiscount` |
| Geometria da linha | `collectLinePositions`: começa em `target.hitPos().relative(hitFace)` e avança no eixo da face até `getRange` ou o eixo do jogador (`PLAYER_INVENTORY_ITEM_SLOTS=36` e `SHULKER_SLOT_COUNT=27` são constantes de inventário das fontes) |
| Estado/ciclo | `LinearBuildCastData` guarda `hitBlockPos`/`hitFace`, serializa em buffer/NBT e é limpo em `onServerCastComplete` |

Bytecode: scratch/javap1011_evocation7.txt (`javap -classpath <JAR> -p -s -c`, 94 classes, EXIT=0, SHA-256 `AF225F42FA1A0295D7339542D49620FBA0D0BE6599147EEDF69B75744730DB41`); decompilação de apoio: scratch/evocation7_sources.txt (46 fontes Vineflower 1.12.0, SHA-256 `05090319D9206171C8C4C38ED1A33479F0F1313F9135B5D70146F5559EB80DB1`). Constantes e fórmulas decisivas foram confrontadas com o bytecode; em divergência, o bytecode prevalece.

## 3. Casting / execução

1. `checkPreCastConditions` exige `Player`, resolve o template e o alvo, grava `hitBlockPos`/`hitFace` em `LinearBuildCastData` e retorna `true`; falhas enviam `sendBlockTemplateError` ou `ui.apprenticecodex.too_far` e retornam `false`.
2. `onCast` executa somente no servidor e para `ServerPlayer`; restaura o alvo do cast data ou o resolve novamente e chama `placeLine`.
3. `placeLine` escolhe fontes: `CreativeItemSource` em `instabuild`, senão `collectItemSources`; calcula `copySourceState` somente se o bloco clicado for o mesmo `BlockItem`; lê `abortOnFailedPlacement` e o custo por bloco com desconto.
4. Para cada posição de `collectLinePositions`, ignora blocos não substituíveis (ou aborta), exige uma fonte com item compatível e, se `castSource.consumesMana()` e não criativo, verifica `mana + 1.0E-4F >= manaCostPerBlock`.
5. `tryPlaceAt` usa `BlockTools.useItemOnBlockByPlayerMainHand`, exige mudança real de `BlockState`, copia propriedades de `FACING`/`HORIZONTAL_FACING`/`AXIS`/`HORIZONTAL_AXIS`, e reverte com `setBlock(pos, before, 3)` se `source.consumeOne` falhar.
6. Em sucesso debita mana com piso `0.0`, marca `manaConsumed`, envia `SyncManaPacket`, notifica fontes e bloqueios restantes e chama `player.getInventory().setChanged()`.
7. `onServerCastComplete` reseta e remove o cast data; nenhuma entidade ou projétil é criado.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alvo inicial | Bloco em até `24` blocos (`32` com Craftsman's Delight), via pending hit do cliente ou raycast de `COLLIDER` |
| Filtro de posição | `isWithinAxisRange`: `|dx|`, `|dy|` e `|dz|` ≤ `getRange` em relação a `blockPosition()` |
| Direção | Eixo de `target.hitFace()`; a linha para ao atingir o eixo do jogador ou ao limite de `getRange` |
| Templates inválidos | `DoorBlock`, `BedBlock`, `Blocks.LINEAR_BUILD_DENYLIST`, `ItemStack` vazio de `LuminousDevice` |
| Fontes de item | `collectItemSources`: Personal Shelf, Ender Chest, Create Toolbox, Companion Trunk, burros/mulas com baú, Curios com handler, itens com `ItemHandler.ITEM`, Malum Pouch, Luminous Device, Shulker Box, Bundle, slots de inventário (`9..36`, `0..9`), mão principal e offhand; em criativo, apenas `CreativeItemSource` |
| Substituição | Somente `level.getBlockState(pos).canBeReplaced()`; falha aborta ou pula conforme config |
| Persistência | `LinearBuildCastData` sobrevive ao pre-cast com serialização NBT/buffer; limpo na conclusão |

## 5. Resultado

- Ação é colocação de blocos: **nenhum dano, tipo de dano, AOE de combate, projétil, invocação ou efeito de status** (`N/A` com justificativa: `placeLine` only chama `BlockTools.useItemOnBlockByPlayerMainHand`).
- Cada bloco aceito consome uma fonte e, se aplicável, mana adicional; falha de consumo reverte o bloco.
- `manaDepleted` envia `ui.apprenticecodex.linear_build.deplete_mana`; nenhuma posição colocada envia `ui.apprenticecodex.cant_place`.
- Estado do cast é por `MagicData`, não por entidade; `castSource.consumesMana()` e `instabuild` alteram o caminho de custo.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `0 + 0*(level-1)` → `getRange` não depende de poder, apenas de `CraftsmansDelight.isEquippedBy` |
| Mana base | `20 + 0*(level-1)` declarado; custo efetivo por bloco vem de config e desconto, **NÃO VERIFICADO** |
| Cooldown | `0.5` s declarado em `DefaultConfig`; valor efetivo **NÃO VERIFICADO** |
| Cast time | `0` ticks com `CastType.INSTANT` |
| Alcance | `24` ou `32` blocos (Craftsman's Delight); consumido em raycast e validação de eixo |
| Custo por bloco | `manaCostPerBlock()` da config servidor; desconto via `CraftsmansDelight.applyManaCostDiscount` |
| Fontes | Múltiplos handlers do jogador/mundo listados em `collectItemSources`; `PLAYER_INVENTORY_ITEM_SLOTS=36` e `SHULKER_SLOT_COUNT=27` aparecem como limites em helpers; criativo sem consumo |

## 7. Possibilidades de perks

- **A — atributo nativo:** `getRange` já consulta Craftsman's Delight; um perk poderia replicar esse padrão, mas não há API de registro de modificador de alcance comprovada. **CONDICIONADO**.
- **B — evento verificado:** `LinearBuildCastData` é estado do provider, não ponto de mutação segura.
- **C — adapter condicionado:** alterar custo por bloco ou geometria exigiria substituir `LinearBuild`/`placeLine` com sincronia de `SyncManaPacket` e validação de fontes. **CONDICIONADO**.
- **D — sem hook demonstrado:** nenhuma API segura para transformar a linha em AOE, alterar o eixo da face ou duplicar blocos sem duplicar custo. **NO_MUTATION** / fail-closed.

- `mutating_hook = NOT_VERIFIED`; `mutation = NO_MUTATION` (fail-closed).

## 8. Causalidade

`validar template → pre-cast grava bloco/face → onCast restaura alvo → placeLine consome fontes/mana por bloco → SyncManaPacket e limpeza do cast data`.


## 9. Concepção de nova magia

Assinatura ocupada: colocação linear de blocos a partir do alvo, com custo por bloco e fontes de inventário/shulker. Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ identidade/hash, construtor `0/0/20/0/0`, raridade `UNCOMMON`, nível `1`, cooldown `0.5`, alcance `24`/`32`, denylist e geometria da linha confirmados no bytecode 1.0.1.1.
- ✅ custo por bloco, `castSource.consumesMana()`, `instabuild`, `SyncManaPacket` e limpeza do cast data confirmados.
- ⚠️ valores efetivos de `manaCostPerBlock`, `abortOnFailedPlacement`, multiplicadores e config do pack permanecem `NÃO VERIFICADOS`.
- ⚠️ `physical_qa=NOT_TESTED`: sem servidor Survival, teste de shulker, criativo, bloqueios, portais ou PvP.
- ⚠️ Universo integral do provider não encerrado; homologação integral permanece `NOT_CERTIFIED`.


## Localizadores para Codex — resumo operacional

Assinatura ocupada: colocação linear de blocos a partir do alvo, com custo por bloco e fontes de inventário/shulker. Nenhuma implementação foi realizada.

- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
