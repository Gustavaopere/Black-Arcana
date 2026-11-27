# Personal Shelf

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:personal_shelf` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Interfaces | `IClientBlockTargetingSpell`, `IClientPlacementPreviewSpell` |
| Escola | `SchoolRegistry.ENDER_RESOURCE` (Ender) |
| Raridade mínima | `SpellRarity.RARE` |
| Níveis | 1 (`DefaultConfig.setMaxLevel(1)`) |
| Tipo de cast | `CastType.LONG` |
| Cooldown declarado | `5.0` s |
| Recurso | Mana do Iron's (`baseManaCost=50`, `manaCostPerLevel=0`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.personalshelf.PersonalShelf` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1.

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("personal_shelf", PersonalShelf::new)` |
| Config | `PersonalShelf.config` (`RARE`, nível 1, cooldown `5.0`) |
| Coeficientes | `PersonalShelf.<init>()`: `baseSpellPower=0`, `spellPowerPerLevel=0`, `baseManaCost=50`, `manaCostPerLevel=0`, `castTime=20` |
| Alcance | `PersonalShelf.getRange()` → `8.0`; replicado em `getClientBlockTargetingRange(...)` e `setLifeRange(...)` |
| Gate de cast | `PersonalShelf.checkPreCastConditions(...)` → `findPlaceData(...)`; falha envia `ui.apprenticecodex.cant_place` |
| Dados de cast | `PersonalShelf.PersonalShelfCastData` (`position`, `exportMode`, `exportFacing`; buffer + NBT `HasPosition`/`PositionX,Y,Z`/`ExportMode`/`HasExportFacing`/`ExportFacing`) |
| Validação de alvo | `BlockTargetingHelper.findClientPlacePos`, `BlockTools.findPlacePos`, `BlockTargetingHelper.validateTarget` |
| Preview | `PersonalShelf.getClientPlacementPreview(...)` → `ClientPlacementPreviewData.singleBlockColumn(...)` |
| Mutação | `PersonalShelf.onCast(...)`: `level.setBlockAndUpdate(..., BlockRegistry.PERSONAL_SHELF_CHEST.defaultBlockState())` |
| Bloco | `PersonalShelfChestBlock` (`EXPORT_MODE` BooleanProperty, `SHAPE=Block.box(2,1,2,14,14,14)`) |
| BlockEntity | `PersonalShelfChestBlockEntity` (`serverTick`, `expireAndCloseOpenMenus`, `exportItem`, `setLifeRange`, `keepOwnerRange=10.0` default) |
| Inventário | `Capabilities.getPersonalInventory(owner).getHandler()` (não os slots transientes do bloco) |

Bytecode: `scratch/javap1011_ender10.txt` (`javap -classpath <JAR> -p -s -c`, `EXIT=0`, SHA-256 `0095E23B21918E38B4BD7D6C47DA8C3503753F0F988C00AB04A786060E2C50E5`); decompilação: `scratch/ender10_sources.txt` (SHA-256 `F3953EB8FCFB793EC501694E054E3C3CBE187E557B09B6CF158828692A97A645`).

## 3. Casting / execução

1. `AbstractSpell` resolve mana/cooldown/nível; `castTime=20`, `CastType.LONG`.
2. `checkPreCastConditions` chama `findPlaceData`: tenta `BlockTargetingHelper.findClientPlacePos` com `getRange()=8`; se vazio, usa `BlockTools.findPlacePos`. Grava `position`, `exportFacing` e `exportMode = entity.isShiftKeyDown()` no `PersonalShelfCastData`. Avisa `ui.apprenticecodex.personal_shelf.for_export_mode` se export.
3. `getClientPlacementPreview` valida `BlockTargetData` e devolve preview de coluna de um bloco em `pos + (0.5,0,0.5)`. O cliente fornece intenção; o servidor revalida.
4. `onCast` relê o cast data, exige `placeState.canBeReplaced()`, coloca `PERSONAL_SHELF_CHEST`, inicializa `chestEntity.setShelfData(caster, exportMode, exportFacing)`, chama `setLifeRange(getRange())` e emite 32 partículas `ParticleTypes.REVERSE_PORTAL`.
5. `onServerCastComplete` reseta e limpa `additionalCastData`.

Valores efetivos de mana/cooldown/cast time e atributos instalados **NÃO VERIFICADOS**.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alcance de targeting/placement | `8.0` blocos, mesmo valor para cliente e servidor |
| Preview | coluna de um bloco centralizada em X/Z |
| Substituição | `BlockState.canBeReplaced()` no destino |
| Bloco criado | `BlockRegistry.PERSONAL_SHELF_CHEST`, `defaultBlockState()` |
| `keepOwnerRange` | default `10.0` no BlockEntity, mas `PersonalShelf.onCast` chama `setLifeRange(8.0)` — o valor efetivo da spell é `8.0` |
| Expiração por distância | três diferenças absolutas `X`, `Y` e `Z` **separadamente** `<= keepOwnerRange`; não é raio euclidiano |
| Export | `exportMode && exportFacing != null`, destino em `pos.relative(exportFacing)` com `IItemHandler` via `Capabilities.ItemHandler.BLOCK` na face oposta |

A distância é uma caixa cúbica em X/Y/Z, não uma esfera. Rotular como raio Euclidiano seria incorreto.

## 5. Resultado (BlockEntity e exportação)

- `serverTick` ressincroniza `EXPORT_MODE` do block state se divergente do `isExportMode` interno.
- Sem owner, owner removido, owner offline ou fora do cubo de `keepOwnerRange`: `expireAndCloseOpenMenus` fecha menus abertos registrados em `openers`, remove o bloco com `removeBlock(pos,false)` e emite partículas `REVERSE_PORTAL` (32, spreads `0.2`) e som `VANILLA_DISAPPEAR_MAGICAL_ENTITY`.
- `exportItem`: se `exportCooldownTick>0`, decrementa; caso contrário obtém `IItemHandler` do inventário pessoal do owner e percorre `slotLimit = Math.min(54, source.getSlots())`. Para cada slot não vazio: simula `insertItem(target,stack,true)`, calcula `inserted`, confirma com `insertItem(...,false)` e só então chama `source.extractItem(i, insertedReal, false)`, toca efeitos e fixa `EXPORT_COOLDOWN_TICK=5`.
- A inserção real ocorre **antes** da extração da origem. Não há rollback no corpo examinado se `extractItem` retornar menos que `insertedReal`; sinalizar como risco de QA com handlers de terceiros, não como exploit comprovado.

**Deltas corrigidos neste lote:** a ficha histórica citava `PersonalInventory.MAX_SIZE`; o JAR `1.0.1.1` usa literalmente `Math.min(54, source.getSlots())`. Também passa a constar o default `keepOwnerRange=10.0` diferenciado do `setLifeRange(8.0)` da spell.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `0 + 0*(level-1)` | sem escalonamento |
| Mana | `50 + 0*(level-1)` | Iron's mana |
| Cast time | `20` ticks | `DefaultConfig` + campo |
| Alcance | `8.0` | blocos, cliente e servidor |
| `keepOwnerRange` | `10.0` default → `8.0` via `setLifeRange` | BlockEntity NBT `KeepOwnerRange` |
| Cooldown de export | `5` ticks | `EXPORT_COOLDOWN_TICK` |
| Slots de export | `min(54, slots)` | por tick |

## 7. Possibilidades de perks

- **A — atributo nativo:** mana/cooldown/cast time via `AbstractSpell`; não há parâmetro de spell power aplicável.
- **B — evento verificado:** `MovementInput`/`BlockTarget` e `serverTick` são pontos de execução do provider; não são hooks de mutação segura demonstrados.
- **C — adapter condicionado:** alterar alcance,janela de posse ou cadência de export exigiria substituir `getRange`, `setLifeRange` e `exportItem`, com contrato de persistência NBT e transação de inventário. **CONDICIONADO**.
- **D — sem hook demonstrado:** não há API segura comprovada para mudar a geometria de posse ou o export sem duplicar o bloco e o storage. **NO_MUTATION / fail-closed**.
- `mutating_hook = NOT_VERIFIED`.

## 8. Causalidade

`um cast → um bloco provider-owned → tick de posse/export → expiração/remoção`.

O bloco, o storage pessoal e o export são consequências da mesma raiz `personal_shelf`; não são casts adicionais. Black Arcana não deve reprocessar a mutação do mundo via `WorldEffectPolicy` nem cobrar mana/XP por slot exportado.

## 9. Concepção de nova magia

Assinatura ocupada: "container temporário pessoal com export mode direcional e posse por proximidade cúbica". Uma magia original precisaria de semântica materialmente distinta para não duplicar a identidade. Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ Identidade/hash, coeficientes, alcance, validação cliente/servidor, cast data, BlockEntity, limites de export e limpeza confirmados no bytecode 1.0.1.1.
- ⚠️ Conteúdo efetivo de `getPersonalInventory`, proteção de claims e handlers de inventário de terceiros não lidos/testados.
- ⚠️ `physical_qa=NOT_TESTED`: sem servidor real, multiplayer/PvP, save/reload ou export transacional.
- ⚠️ Universo integral do provider não encerrado.

## Localizadores para Codex — resumo operacional

- `getRange()=8` é usado tanto no targeting quanto em `setLifeRange`; o default `10.0` do BlockEntity é sobrescrito na criação pela spell.
- `min(54, slots)` é o limite real de varredura de export no JAR 1.0.1.1.
- Nenhum ponto de mutação segura demonstrado; manter fail-closed.
- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
