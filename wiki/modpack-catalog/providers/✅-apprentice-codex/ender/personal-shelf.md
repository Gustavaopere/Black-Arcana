# Personal Shelf

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:personal_shelf`
- **Iron's school:** Ender
- **Levels:** 1
- **Minimum rarity:** Rare
- **Cast type:** Long
- **Cooldown:** 5 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 0`
- `spellPowerPerLevel = 0`
- `baseManaCost = 50`
- `manaCostPerLevel = 0`
- `castTime = 20 ticks`
- targeting/placement range: `8 blocks`

## Server-authoritative placement

The client can provide targeting/preview intent, but the provider validates the target again on the server before casting. The server rejects non-placeable locations and creates `PERSONAL_SHELF_CHEST` only after validation.

Sneaking at cast time records an **export mode** plus placement facing in serialized cast data. The created block entity is initialized with the caster/player identity and the provider's shelf/export state.

This is a concrete example of provider-owned client-preview/server-settlement separation; Black Arcana must not add a second placement transaction.

## What it does

The guide describes a temporary personal/private storage interface and a sneaking transfer/export mode toward a container. The exact inventory persistence/storage backing remains provider implementation authority.

## World-effect boundary

Personal Shelf changes the world by creating a provider block. That mutation is already settled by Apprentice's Codex. It is not retroactively re-run through Black Arcana `WorldEffectPolicy`.

A Black Arcana-originated analogous world effect would still require Black Arcana policy and a real semantic gap.

## Acquisition

Registered through Iron's spell registry. Exact survival acquisition remains provider-wide audit work.

## Deduplication

Occupies the **temporary personal magical storage/block interface with export mode** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT COST+RANGE+SERVER TARGET VALIDATION / STORAGE LIFETIME+INVENTORY BACKING+PACK RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:personal_shelf` → `SpellRegistry.reg("personal_shelf", PersonalShelf::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.personalshelf.PersonalShelf`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/personalshelf/PersonalShelf.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

---

## Engenharia causal aprofundada — entidades 0.9.7.1

**Fonte lida:** [`personalshelf/PersonalShelf.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/personalshelf/PersonalShelf.java) · [`personalshelf/PersonalShelfChestBlockEntity.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/personalshelf/PersonalShelfChestBlockEntity.java) · [`personalshelf/PersonalShelfChestBlock.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/personalshelf/PersonalShelfChestBlock.java). Source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` alinhado à release declarada 0.9.7.1. Versão e SHA do JAR são da modlist física; **corpos de bytecode destes métodos não foram provados como equivalentes ao source**.

### Execução, persistência e efeitos secundários

- **Bloco e ownership:** `PersonalShelf` resolve alvo/colocação sob checagens da spell; a `PersonalShelfChestBlockEntity` armazena owner UUID, modo de exportação, face de saída e `keepOwnerRange`. `serverTick` exige owner online/no mesmo nível e não removido; para distância, usa **três diferenças absolutas X/Y/Z <= keepOwnerRange**, não raio euclidiano.
- **Expiração:** owner ausente/fora de alcance leva a `expireAndCloseOpenMenus`: fecha menus de players registrados como `openers`, remove o bloco via `serverLevel.removeBlock(pos,false)`, emite partículas e som. Um state de export mode divergente do block state é ressincronizado. O armazenamento persistente subjacente é `Capabilities.getPersonalInventory(owner)`, não os slots transientes do bloco invocado.
- **Automação:** `exportItem` só roda se modo/face habilitados, cooldown vencido, BlockEntity de destino e `Capabilities.ItemHandler.BLOCK` disponíveis na face oposta; requer owner online. Percorre no máximo `PersonalInventory.MAX_SIZE` slots, simula `ItemHandlerHelper.insertItem(targetHandler,stack,true)` e confirma em `insertItem(...,false)`; em seguida extrai `insertedReal` do source. Quando movimentação foi positiva, fixa `EXPORT_COOLDOWN_TICK=5` e encerra tick.
- **Ponto de concorrência:** inserção no destino ocorre **antes** da extração da origem nesse método, e o trecho não exibe rollback do destino caso `source.extractItem` entregue menos que `insertedReal`. Não afirmar exploit comprovado, mas sinalizar QA com capabilities de inventário de terceiros e transações concorrentes.
- **Risco:** item exportado, fechamento de menu e expiração são consequências provider-native da mesma spell; não cobrar custo de mana/XP por slot adicional via BA, nem confundir UI com autoridade de storage.

### Boundary para perks e QA

- **Raiz:** `apprenticecodex:personal_shelf`, já contabilizada no registry 83/83. Spawn, cleanup, tick, drop, item handling e efeitos causais **não** são novos casts contáveis.
- **Autoridade:** Iron's mantém escola, casting, mana e recast padrão; Apprentice's Codex detém entidades, itens e efeitos auxiliares; Black Arcana mantém apenas sua própria pipeline de magia/rituais, política de efeitos de mundo, Corruption e Strain.
- **Bloqueio:** ⛔ nenhuma API ou bridge de Mastery/perks confirmada para executar intervenções seguras; não deduzir rewards de eventos locais.
- **Pendências:** ⚠️ equivalência source/JAR, configuração, servidor dedicado com modpack real, multiplayer/PvP, inventários de terceiros, proteção de claims, save/reload e edge cases de entidades. Nenhuma prova de QA físico do provider nesta atualização.

[Matriz de lifecycle](../PERK-ENGINEERING-MATRIX-LIFECYCLE-0.9.7.1.md).
