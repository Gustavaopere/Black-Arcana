# Sugar Staff — Hex Cast

- Provider: **Alex's Caves Continued** (`alexscaves`)
- Version: `1.0.10`
- Exact physical/publisher SHA-1: `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`
- Owner: `alexscaves:sugar_staff`
- Trigger: sneaking direct item use
- State: `COUNTED_EXACT`

## Semantic identity

Sneaking use selects the provider Sugar Staff Hex branch and creates one Hex action at the provider-resolved ground position. This is a separate selectable root from Peppermint Cast.

## Exact acquisition

Exact provider data closes Sugar Staff through Licowitch loot.

## Boundary

Numerical tuning, cooldowns, targeting, entities, effects, particles and sounds remain provider authority. Black Arcana catalogs the identity and must not replay provider settlement.

Sources: `../EXACT-1.0.10-ARTIFACT-AUDIT.md`, `../ITEM-ACTION-DISPOSITION-1.0.10.md`.

## Contrato técnico exato — JAR 1.0.10

A leitura estática abaixo usa o JAR físico/publisher de **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Métodos, descritores JVM e offsets de bytecode são localizadores reproduzíveis com `javap -p -s -c`, não APIs externas prometidas. A [prova técnica comum](../EXACT-TECHNICAL-CONTRACTS-1.0.10.md) registra o escopo da evidência. **Parâmetros estáticos: `VERIFIED_EXACT_BINARY`; configuração/hook mutador: `NOT_VERIFIED`; QA no jogo: `NOT_TESTED`.**

O trabalho de fonte público do PR #944 permanece como corroboração: `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **`mod.version = "1.1.1"`** em [`stonecutter.properties.toml:16`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/stonecutter.properties.toml#L16). Esse snapshot não é fonte comprovado da versão física `1.0.10`; os números certificados nesta seção vêm dos bytes do JAR, sem alegação de paridade de build.

### 1. Identidade

`SugarStaffItem.use` com `player.isShiftKeyDown()` seleciona a raiz deliberada `sugar-staff-hex-cast`, distinta da escolha Peppermint. Área, ticks de dano e janela final são settlement da mesma Hex: **0 novas raízes semânticas**. Item `alexscaves:sugar_staff`; entidade `SugarStaffHexEntity`.

### 2. Comportamento e lifecycle

O ramo Hex é server-side (`SugarStaffItem.use @7–18, @35–183`): cria uma entidade, define owner, posição e escala, adiciona-a ao level (`@53–124`) e depois escreve lifespan (`@156–172`). `SugarStaffHexEntity.tick()V @4–49` inicializa `despawnsIn` por `getLifespan()` se `-1`, decrementa valores positivos e descarta quando já não positivo. O corpo **continua após `discard`**, sem return antecipado.

`tick()V @285–299` chama `hurtEntities(despawnsIn < 5)` a cada tick após o decremento, sem guard server-side próprio nessa chamada. A janela final corresponde a chamadas sucessivas; não é prova de uma única explosão nem de todo hit ser aceito. Depois, força `noPhysics=true`, move por delta e o multiplica por `0.7F/0.8F/0.7F` em X/Y/Z (`@302–334`).

As rotinas `readAdditionalSaveData`/`addAdditionalSaveData(Lnet/minecraft/nbt/CompoundTag;)V @0–48, @0–37` persistem `DespawnsIn`, `Lifespan` e `Owner` UUID; **não** persistem `HEX_SCALE`. `getOwner()Lnet/minecraft/world/entity/LivingEntity; @0–58` pode resolver esse UUID no servidor, mas `hurtEntities` lê o campo `owner` diretamente e `tick` não chama o getter. Assim, ler o UUID não prova por si só restauração do dano/escala após reload; QA desse lifecycle continua pendente.

### 3. Parâmetros e getters

| Fato certificado | Localizador binário |
|---|---|
| Exatamente uma entidade no ramo Hex | `SugarStaffItem.use @53–124` |
| Escala `1F + 0.25F * level(HUMUNGOUS_HEX)` | `use @102–118` |
| Lifespan de cast `100 + 60 * level(SPELL_LASTING)` ticks | `use @156–172` |
| Defaults sincronizados: lifespan `100`, escala `1F`; contador `despawnsIn=-1` | `SugarStaffHexEntity.defineSynchedData(Lnet/minecraft/network/syncher/SynchedEntityData$Builder;)V @0–25`; construtor `@6–8` |
| `getLifespan()I` / `getHexScale()F` leem dados sincronizados; `setLifespan(I)V` / `setHexScale(F)V` escrevem esses dados | getters `@0–16`; setters `@0–14` |
| Dimensões: largura `4F*getHexScale()`, altura `0.25F` | `getDimensions(Lnet/minecraft/world/entity/Pose;)Lnet/minecraft/world/entity/EntityDimensions; @0–13` |
| Mudança de `HEX_SCALE` chama `refreshDimensions` | `onSyncedDataUpdated(Lnet/minecraft/network/syncher/EntityDataAccessor;)V @0–19` |
| Dano solicitado `1F` ordinário / `6F` quando `despawnsIn<5`, via `indirectMagic(this, owner)` | `hurtEntities(Z)V @134–162`; `tick()V @285–299` |
| Knockback final `0.9F` ampliado para double, independente do retorno de `hurt` | `hurtEntities(Z)V @159–192` |
| `getYRenderOffset()F` lê offset visual `nextFloat()*0.05F`, sem alterar hitbox | getter `@0–4`; construtor `@11–24` |
| `SugarStaffItem.getEnchantmentValue()I = 1`; `isEnchantable(Lnet/minecraft/world/item/ItemStack;)Z` exige `count == 1` | getters `@0–1`, `@0–13` |

A duração fornecida pelo staff inicializa o contador no primeiro tick. `setLifespan` após essa inicialização não substitui automaticamente `despawnsIn`; existe `setDespawnsIn(I)V @0–5`, mas sua presença não certifica API externa de perk.

### 4. Targeting, área e filtros

`SugarStaffItem.use @40–99` usa `ACMath.getGroundBelowPosition(Lnet/minecraft/world/level/BlockGetter;Lnet/minecraft/world/phys/Vec3;)Lnet/minecraft/world/phys/Vec3;` com o olho do jogador. O helper (`@0–137`) desce do block position até colisão não vazia ou altura mínima, obtém altura da forma e retorna `Vec3.upFromBottomCenterOf`; não é um cast de raio para frente nem posicionamento no alvo Mob. O item também calcula o helper de aquisição do Sea Staff antes de bifurcar, mas o ramo Hex não consome aquele alvo.

`SugarStaffHexEntity.hurtEntities(Z)V @0–134` consulta `LivingEntity` na AABB própria e exige adicionalmente `distanceTo(this) <= 4F`. Exclui aliado da Hex; exige owner não nulo e target diferente dele; owner comum exclui `target.isAlliedTo(owner)`, enquanto `LicowitchEntity` usa `!licowitch.isFriendlyFire(target)`. Não há teste próprio de linha de visão ou `Mob` nesse método.

Largura `4*scale` é dimensão total de hitbox; o teste radial `4F` é uma segunda condição, medida a partir das posições das entidades. Escala maior não prova raio de dano proporcional nem remoção desse cap radial. Não somar cada tentativa periódica de dano como spell independente.

### 5. Custos, recarga e dados do item

`SugarStaffItem.use` tem descritor `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder;`. Em `@175–180` aplica cooldown **100 ticks** com `ACCompat.addCooldown(Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/item/ItemStack;I)V`; o wrapper chama `ItemCooldowns.addCooldown(stack.getItem(),ticks) @0–12`, compartilhado com o ramo Peppermint do mesmo item.

Em `use @464–468`, pede **1** de durabilidade via `ACCompat.hurtAndBreakUsedHand(Lnet/minecraft/world/item/ItemStack;ILnet/minecraft/world/entity/LivingEntity;)V @0–13`, que usa `getUsedItemHand()`, converte para slot e delega `ItemStack.hurtAndBreak`. O ramo do item não checa `instabuild` explicitamente nem cobra mana diretamente; o engine controla a aplicação efetiva. `ACItemRegistry.lambda$static$184()Lnet/minecraft/world/item/Item; @11–22` registra durabilidade `100`, raridade `UNCOMMON`.

`data/alexscaves/loot_table/entities/licowitch.json` (4.120 bytes, SHA-256 `157ba186f052f989fc31bd016ae3352eaa77c58ec1a8a639c91774f239e34526`) inclui o Sugar Staff condicionado a kill pelo jogador e chance base `0.025`, com Looting linear base `0.035` e incremento `0.01` por nível acima do primeiro. `data/alexscaves/tags/item/enchantable/sugar_staff.json` (51 bytes, SHA-256 `eb9f84b401224aba54ba91a239e4dd5b775d82012cecf9b03e8f9608e12b11fc`) contém o item. Dados embarcados limitam Humungous Hex a `2` e Spell Lasting a `3`; isso produz escala `1/1.25/1.5` e lifespan `100/160/220/280` nos níveis normais, sem cap próprio nas fórmulas do item. Overrides efetivos de datapack: `NOT_VERIFIED`.

### 6. Integração e autoridade

`use`, setters, `tick` e `hurtEntities` são superfícies internas observadas. Hook externo de escala/duração com momento de aplicação, recontagem do contador, anti-duplicação e persistência comprovados: **`NOT_VERIFIED`**. A perk fica **⛔ fail-closed**. Black Arcana não reproduz `indirectMagic`, knockback, ticks finais, cooldown ou custo de durabilidade.

### 7. Validação e localizadores

Métodos/valores embarcados: `VERIFIED_EXACT_BINARY`; configuração efetiva, hooks e reload no modpack: `NOT_VERIFIED`; QA física: `NOT_TESTED`. `1F/6F` são pedidos de dano, sem garantia de HP efetivamente perdido ou soma total ao longo da duração.

| Entrada no JAR | Bytes | SHA-256 |
|---|---:|---|
| `com/github/alexmodguy/alexscaves/server/item/SugarStaffItem.class` | 7.145 | `d670f887debdfb95f93a52b0c58b3033154a9aa20777fb8bd2a1673ee1407c3f` |
| `com/github/alexmodguy/alexscaves/server/entity/item/SugarStaffHexEntity.class` | 10.357 | `39f8d11595654ccebcb78540a2772106f0ae30507490570ac6b2cbe28de8e89c` |

Corroboração pública preservada: [`SugarStaffItem.java`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/src/main/java/com/github/alexmodguy/alexscaves/server/item/SugarStaffItem.java), [`SugarStaffHexEntity.java`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/src/main/java/com/github/alexmodguy/alexscaves/server/entity/item/SugarStaffHexEntity.java), snapshot **1.1.1**, sem prova de paridade com 1.0.10.

Static evidence grade: `SHA_EXACT_BINARY_BEHAVIOR`. Claim scope: `STATIC_TECHNICAL_CATALOG_ONLY`. Hook: `NOT_VERIFIED`. Physical QA: `NOT_TESTED`.
