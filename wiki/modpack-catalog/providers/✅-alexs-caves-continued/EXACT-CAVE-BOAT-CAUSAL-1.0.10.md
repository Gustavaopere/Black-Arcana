# CaveBoatItem — auditoria causal da versão 1.0.10

**Estado:** ⚠️ `PARTIAL_STATIC_CAUSAL`; inventário das quatro identidades individualizado, mas contrato técnico integral e universo do provider não certificados. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `NO_MUTATION`; sem alteração de runtime nem novas raízes de magia.

## 1. Identidade e autoridade

A modlist do sibling `neoforge-rpg-skilltree/main@2b730debc77e60d94a2da9a3f3d8e889c71d2852` documenta o item #019 `alexscaves-1.0.10-neoforge+1.21.1.jar` (Minecraft 1.21.1, NeoForge 21.1.250 no último snapshot físico, Java 21). O artefato publisher auditado possui 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 8.898 entradas e 1.555 classes. A análise física foi do **artefato publisher**, não de um novo dump da instalação do jogador.

O item é `com.github.alexmodguy.alexscaves.server.item.CaveBoatItem`, SHA-256 do classfile `92fc0840e49f71306bbcafbd3e5f4f5814acbf87846846430007310a2577c18d`, `Item` com três campos (`type`, `hasChest`, `ENTITY_PREDICATE`) e três métodos com Code (`<init>`, `use`, `<clinit>`). Fichas estáveis das identidades distintas: [Pewen Boat](items/pewen-boat.md), [Pewen Chest Boat](items/pewen-chest-boat.md), [Thornwood Boat](items/thornwood-boat.md), [Thornwood Chest Boat](items/thornwood-chest-boat.md). São quatro recursos de transporte, **não quatro casts mágicos**.

| Resource ID | Factory de ACItemRegistry | `type` | `hasChest` | Entidade solicitada |
|---|---|---|---|---|
| `alexscaves:pewen_boat` | `ACItemRegistry.lambda$static$25` | `PEWEN` | `false` | `AlexsCavesBoatEntity` |
| `alexscaves:pewen_chest_boat` | `ACItemRegistry.lambda$static$26` | `PEWEN` | `true` | `AlexsCavesChestBoatEntity` |
| `alexscaves:thornwood_boat` | `ACItemRegistry.lambda$static$145` | `THORNWOOD` | `false` | `AlexsCavesBoatEntity` |
| `alexscaves:thornwood_chest_boat` | `ACItemRegistry.lambda$static$146` | `THORNWOOD` | `true` | `AlexsCavesChestBoatEntity` |

Todas as quatro factories criam `CaveBoatItem` com `Item.Properties.stacksTo(1)`, indexadas no [contrato de ACItemRegistry](systems/item-registry.md). A mesma classe binária implementa as quatro variantes; o escopo de registro não demonstra que o launcher aceitou cada item na registry real.

## 2. Ativação e targeting exatos do método do item

`CaveBoatItem.use(Level, Player, InteractionHand): InteractionResultHolder<ItemStack>` — Code 313 bytes, 137 instruções, SHA-256 do Code `2bdf4638aa04957bf5b9fd7af79ea1dbb93281bad106752addb5d985cba872bb`, hash das instruções `2185420d2c532bc2c742cce6195507aeda3a77679c616efc6e8f83db91870a1c`.

1. Lê a `ItemStack` da mão usada e chama `getPlayerPOVHitResult(level,player,ClipContext.Fluid.ANY)` (`@0–15`); `HitResult.MISS` retorna `ACCompat.usePass` (`@17–33`).
2. Busca entidades pelo predicado `EntitySelector.NO_SPECTATORS` associado a `Entity.isPickable`. A geometria de **obstrução** é `player.getBoundingBox().expandTowards(player.getViewVector(1.0F).scale(5.0D)).inflate(1.0D)` (`@34–73`). Para cada entidade obtida, verifica se a AABB dela inflada pelo `pickRadius` contém `player.getEyePosition()` (`@75–156`); se sim, PASS. **5.0 não é prova do alcance total do raycast**, nem AOE de magia.
3. Só em `HitResult.BLOCK` escolhe `AlexsCavesChestBoatEntity` se `hasChest=true`, senão `AlexsCavesBoatEntity` (`@157–212`); coloca em `hitResult.getLocation()` e aplica yaw do jogador. `Level.noCollision(boat,boat.getBoundingBox())==false` retorna `useFail` (`@214–242`).
4. No lado servidor, solicita `Level.addFreshEntity(boat)` e **descarta seu retorno booleano** imediatamente (`@243–256`); em seguida solicita `GameEvent.ENTITY_PLACE` e `ItemStack.shrink(1)` se `!player.getAbilities().instabuild` (`@257–285`). Logo, o método pode **solicitar consumo mesmo se o spawn for recusado**; sucesso efetivo de spawn, world protection, transações, claims e mods terceiros não foram demonstrados. Depois solicita `Stats.ITEM_USED` e resultado `useSidedSuccess` (`@286–312`), incluindo caminho cliente de resultado, sem prova de mutação no cliente.

**Custos/limites diretos:** item comum com stack máxima 1; solicita consumo de uma unidade no servidor para jogador sem `instabuild` quando o caminho de colocação passa pelo filtro. Mana, XP, charges, casting, cooldown próprio, efeitos ofensivos, dano e status são **N/A no corpo local do item**; integrações externas e lógica herdada continuam NÃO VERIFICADAS. Nenhuma chamada local estabelece alcance máximo de projétil, duração, cooldown, dano ou raio ofensivo.

## 3. Entidades de transporte e estado

`AlexsCavesBoatEntity` herda `net.minecraft.world.entity.vehicle.Boat` (class SHA-256 `6052e323ad6881ee3b70e2cabd1da21e1244ed4dde2d5599e165669f44c8f8f3`); `AlexsCavesChestBoatEntity` herda `ChestBoat` (class SHA-256 `35cc4e4787b777ca74301bf4bc724900afeb6a7f6d5c4fdac8eef14c2ae281fd`). Ambos implementam `AlexsCavesBoat`, definem `blocksBuilding=true` em seus construtores e obtêm EntityType respectivamente por `ACEntityRegistry.BOAT` ou `ACEntityRegistry.CHEST_BOAT`. O construtor `(Level,Vec3,Type)` converte coordenadas em `(Level,x,y,z)` e chama `setACBoatType(type)`. O pacote de spawn é solicitado por `ACPlatform.getEntitySpawningPacket`; aceitação e sincronização física não foram testadas.

O tipo customizado passa pelo `DATA_ID_TYPE` de `SynchedEntityData`, com `setACBoatType` salvando o `ordinal()` e `getACBoatType` lendo-o via `Type.byId(int)`. `getVariant()` devolve sempre `Boat.Type.OAK` e `setVariant(Boat.Type)` tem corpo local somente `return`; portanto o tipo nativo customizado está em outro canal, não no enum vanilla exposto por esses métodos. Os consumidores visuais e outras subclasses da engine requerem auditoria própria.

## 4. NBT, fallback e riscos de persistência

Em ambas as entidades, `addAdditionalSaveData(CompoundTag)` grava apenas `ACBoatType` via `getACBoatType().getName()` e `CompoundTag.putString`; `readAdditionalSaveData` procura `ACBoatType`, executa `ACCompat.getString` e `Type.byName`, então grava o ordinal no `SynchedEntityData`. **Os dois corpos de override não contêm chamada explícita à superclasse**. A leitura desse método não comprova que o baú persiste inventário no save/restart; **a persistência herdada e eventual perda/recuperação de itens estão NÃO VERIFICADAS** e exigem teste real com baú preenchido, save, unload/restart e reabertura.

`AlexsCavesBoat$Type` tem duas constantes fixas, `PEWEN=0` e `THORNWOOD=1`. O `byId(int)` usa `values()[0]` para índice negativo ou fora do intervalo; `byName(String)` usa o primeiro valor se não encontra nome. Assim, valores inválidos retornam **PEWEN** no corpo local, em vez de bloquear a desserialização. A compatibilidade de dados modificados por terceiros e regras de migração não foram testadas.

## 5. Drops e dano por queda

Cada entidade obtém o drop normal por `getDropItem()`: a normal consulta `Type.getDropSupplier`; a com baú consulta `Type.getChestDropSupplier`. No `checkFallDamage` local, se não passageira, no chão, `fallDistance > 3.0F` e `status==Boat.Status.ON_LAND`, solicita `causeFallDamage(fallDistance,1.0F,damageSources.fall())` e **descarta seu booleano**, depois, no servidor e se não foi removida, chama `kill()`. Quando `RULE_DOENTITYDROPS` for true pelo helper `ACCompat.gameRule`, solicita **3 unidades do fornecedor de tábuas** do tipo e **2 unidades de `Items.STICK`** via `ACCompat.spawnAtLocation`. Esses pedidos não garantem drops aceitos nem conferem owner/claim/stack de inventário. A lógica herdada de combate, dano recebido ou drop da ChestBoat continua fora deste recorte.

**Divergência estática verificável:** no `<clinit>` do enum da versão 1.0.10, `PEWEN` e `THORNWOOD` recebem **ambos** `ACBlockRegistry.PEWEN_PLANKS` como `plankSupplier`. Os `dropSupplier` e `chestDropSupplier` de THORNWOOD apontam corretamente para seus próprios itens. Logo, **a tentativa de drops por quebra após queda** de Thornwood usa o fornecedor de tábuas de Pewen, apesar da receita Thornwood usar `alexscaves:thornwood_planks`. É discrepância do binário, não correção implementada por Black Arcana.

## 6. Receitas publisher e aquisição

Quatro JSONs SHA-exatos encontrados em `data/alexscaves/recipe/`. Receitas simples de barco são `minecraft:crafting_shaped` com ingrediente de tábua da madeira correspondente; barcos com baú são `minecraft:crafting_shapeless` com barco da variante e `minecraft:chest`. Os hashes e resource IDs constam no [manifesto](EXACT-CAVE-BOAT-DISCOVERY-1.0.10.json). A auditoria registrou os **identificadores de ingredientes**, não copiou definições JSON; quantidade das tábuas por padrão, desbloqueio por recipe book, condições de datapack e disponibilidade efetiva em Survival continuam NÃO VERIFICADOS.

## 7. Consumers, interoperabilidade e limites

Grafo comprovado: `ACItemRegistry.lambda$static$25/$26/$145/$146` → `CaveBoatItem.<init>` → `CaveBoatItem.use` → `AlexsCavesBoatEntity` ou `AlexsCavesChestBoatEntity` → `AlexsCavesBoat$Type` / `ACCompat` / `ACPlatform` / engine `Boat` e `ChestBoat`. O inventário de classes encontrou também `AlexsCavesBoatRenderer`, modelos e `AlexsCavesBoat` (interface), mas seus corpos e consumidores transitivos completos não foram todos examinados.

Para perks: candidatos conceituais são validação da colocação, custo do item, dano de queda, movimento de passageiros, inventário e drops. Não há prova de um evento mutador único, seguro e server-authoritative, nem permissão para alterar spawn, claims ou inventário de veículos. Esses itens são transporte/utility, **não casts mágicos**. Se Black Arcana integrar sua interação, deve preservar autoridade, `WorldEffectPolicy` para efeitos próprios, custos transacionais e fail-closed. RPG Skill Tree continua sibling de atributos/Mastery/perks por fronteiras reais.

## 8. Reprodução, testes e lacunas

- [Auditor SHA-exato do JAR](../../../../docs/qa/alexscaves_1010_cave_boat_probe.py), [assertivas sobre os transcripts](../../../../docs/qa/alexscaves_1010_cave_boat_static_checks.py), [workflow CI](../../../../.github/workflows/alexscaves-1010-cave-boat-probe.yml).
- Captura CI run **44836620846**, job **136634502582**, aprovada para o **recorte read-only**. Artefato **14677954526**, ZIP SHA-256 `5e5e0e73a18ae3e133ac64c6c9c33cfdae237a481a17a510e3041d24e9fb56af`, retenção até 04/12/2026. Manifesto inclui os cinco classfiles e hashes dos transcripts para reprodução; não usar a transcrição efêmera como prova de QA física.
- Pendências: todos os callers runtime de `Boat` / `ChestBoat`, capacidade/inventário e efeitos após reload; receitas e datapacks ativos/quantidades; proteção de claims e sucesso de `addFreshEntity` / `spawnAtLocation`; remoção, passageiros, water flow, PvP e produção de drops; testes cliente+servidor em modpack instalado, multiplayer. **STATIC=PARTIAL / NO_MUTATION**. Nenhum contrato adicionado ao manifesto `PERK-READY-CERTIFICATIONS.json`.
