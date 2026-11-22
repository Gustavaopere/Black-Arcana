# Remote Detonator — controle remoto vinculado a bloco

**Status:** ⚠️ **PARCIAL** (`STATIC_DISCOVERY_ONLY`); `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`, **⛔ world safety/tickets bloqueados**. Não contar como novo cast ou raiz mágica individual.

## Identidade, descrição e proveniência

**ID:** `alexscaves:remote_detonator`; registry `ACItemRegistry.REMOTE_DETONATOR`, factory `lambda$static$75` (4 instruções, SHA-256 `a36b3946fd4e79da019dca167b2859e05f58fbf5cf234bd013933b3a0355772f`). **Tipo:** `Item`, stack de tamanho máximo `1`, implementa `ACTickingItem` (não é uma Spell API).

**Provider:** Alex's Caves Continued (`alexscaves`), **1.0.10** instalado conforme `neoforge-rpg-skilltree/PROJECT-INSTRUCTIONS/modlist/World Gen/✅-alexs-caves-continued v1.0.10.md`; Minecraft **1.21.1**, NeoForge, Java 21. Publisher JAR **75.279.314 bytes**, `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`; comparação do dump local da instância com publisher não refeita.

**Descrição funcional elaborada para o catálogo:** vincula uma stack a um bloco elegível e a uma dimensão para posteriormente solicitar seu acionamento a distância. O acionamento nativo invoca `ACCompat.onCaughtFire` no bloco do mundo recuperado pelo servidor; não comprova explosão, dano, drop ou sucesso final. Há uma chamada adicional de alteração de bloco no `Level` original, com risco cross-dimensional descrito abaixo.

**Owner:** `com/github/alexmodguy/alexscaves/server/item/RemoteDetonatorItem.class` SHA-256 `6d6e8cd94df306aec6f99b07af856b477b8e6f34d41aaca06a35921b53f2c4b8`; 11 métodos executáveis, zero campos. [Dossiê por método com offsets, fórmulas e riscos](../EXACT-REMOTE-DETONATOR-DISCOVERY-1.0.10.md) · [manifesto do JAR/consumers/resources](../EXACT-REMOTE-DETONATOR-DISCOVERY-1.0.10.json).

## Ativação e condições em ordem causal

**`useOn(UseOnContext)` (103 instruções, SHA-256 `659147c0f41037f2d3e00d8f9d83a025b13d72badc4dc327bf4a8bf93d83f772`):** lê o bloco clicado; se `!BlockState.is(ACTagRegistry.REMOTE_DETONATOR_ACTIVATES)`, delega à engine sem vínculo. Se elegível, solicita som `LODESTONE_COMPASS_LOCK` e seleciona entre modificar a stack original quando `!instabuild && count==1` ou criar `new ItemStack(REMOTE_DETONATOR,1)`, copiar seus componentes NBT, solicitar `held.shrink(1)`, adicionar a nova stack ao inventário e pedir `Player.drop` se a inserção falhar. `addBombTags` grava `BombPos` e `BombTracked=true`; `BombDimension` é escrita apenas se a codificação de `ResourceKey` produzir NBT. Não há guarda server-side explícita no início de `useOn`; a possibilidade de double-processing e validação de claims permanece aberta.

**`use(Level,Player,InteractionHand)` (91 instruções, SHA-256 `ac995eaff92b4b833cbff5449f490c6fb7a754a2cdcfe3daa7b7fccfbe2e7934`):** exige `isActive(stack)`; `getBombPosition` precisa de `BombPos` e `BombDimension` decodificáveis. Exige `!level.isClientSide` e `level instanceof ServerLevel`, obtém `targetServerLevel = MinecraftServer.getLevel(target.dimension)` e exige mundo válido. Solicita **9 `ACPlatform.forceChunk` com `true,true`**, em offsets `x/z=-1..1` ao redor do chunk do alvo, *antes* de checar a validade do bloco. Se `BlockState.is(tag)`, chama `ACCompat.onCaughtFire`, calcula `distanceToSqr(center)>1000D` para advancement `REMOTE_DETONATION`, remove `BombPos`/`BombDimension`, mantém `BombTracked` e invoca **`level.setBlockAndUpdate(target.pos, AIR)` no `level` do argumento original**, não em `targetServerLevel`. Retorna `useSuccess` mesmo em certas saídas sem onCaughtFire; sucesso de retorno não comprova detonação.

**`acInventoryTick` (75 instruções, SHA `f4cc16efcad69f1d972579c96944647c63101110402e2cbb7bfb2f6da68a896d`):** apenas lado não cliente, item ativo, `BombTracked` não explicitamente falso, dimensão do vínculo igual à do callback e `BombPos` presente; em `(tickCount+entity.getId())%20==0` consulta `isLoaded` e estado da tag quando chunk carregado. Se bloco elegível não estiver mais presente ou posição fora dos limites, apaga `BombPos` e `BombDimension`. Não prova tick garantido de 20 em 20 ticks nem frequência em todos os inventários.

**`isActive(ItemStack)` (17 instruções, SHA `a4206726462cada693fbb76134f1f993eef006fd413472c62a9c875e7bf0f4a7`):** avalia `BombPos OR BombDimension`, não ambos; um item com tag incompleta pode parecer ativo. `getBombPosition` retorna `null` sem ambos e sem dimensão válida. Tooltip `appendHoverText` (58 instruções) exibe coordenadas X/Y/Z apenas com posição e dimensão decodificáveis; `ACItemPredicates.active` (7 instruções) seleciona estado visual com `isActive`, sem teste de jogo.

**Boundary de tick reutilizado:** [ACTickingItem](../systems/ticking-item.md) possui prova estática individual do `ItemStackTickMixin` e do forwarding `ItemStack.inventoryTick -> acInventoryTick`; esse certificado do suporte **não** se transfere à aplicação transformada, nem cria scheduler/hook autorizado para este item.

## Efeitos, parâmetros, alvo e custos

- **Targeting:** uma posição armazenada `GlobalPos` (bloco + dimensão) quando válido, tag `REMOTE_DETONATOR_ACTIVATES`; sem raycast de criatura, AOE de dano, LOS ou limite de distância explícitos para acionar. **Distância quadrada 1000** controla somente advancement, não alcance máximo. Exige mundo de destino resolvível.
- **Chunk window:** nove chamadas `forceChunk` (área 3×3 chunks, 1 chunk de raio em cada eixo), **não raio de explosão**. Não há chamada `loadChunksAround(...,false)` no `use`; liberação de tickets, tempo de vida, deduplicação e orçamento reais **NÃO VERIFICADOS**. Risco de chunkloading não limitado.
- **Dano, tipo de dano, power, AOE de explosão, projétil, velocidade, partículas e entidades afetadas:** ausentes das instruções próprias; `ACCompat.onCaughtFire`/blocos downstream exigem auditoria causal específica antes de documentar resultados. Não inventar valores ou dano final.
- **Som:** `LODESTONE_COMPASS_LOCK` volume 1F/pitch 1F solicitado ao vincular; renderização/sincronização não verificadas.
- **Custos:** não consome mana, atributo, XP nem aplica cooldown no owner. `useOn` pode solicitar decremento de **1 stack** ao construir novo vínculo; `use` não pede `shrink` nem durabilidade. Custos externos/datapacks/engine não auditados.
- **Duração:** vínculo em tag até limpeza por `use` ou `acInventoryTick`; nenhum TTL próprio comprovado. Persistência salva/transmitida por `ACCompat.setTag` depende da API externa; não há campo de instância do item.
- **Owner/identidade:** `Player.getUUID` vira argumento de pedido de chunk force; não prova ownership/quotas nem direito de detonar bloco de outro jogador, PvP ou claims. Sem consulta própria a rank, atributos RPG, Spell Level ou Mastery.

## Bloqueios e integração com Black Arcana

**⛔ World Safety:** há chamada de world-write no mundo **original** após ignição no mundo de destino. Em vínculo entre dimensões, pode haver divergência de mundo; a evidência identifica a chamada, mas o dano real em mundo/servidor **não foi demonstrado**. Validar `ACPlatform.forceChunk` (aquisição, release, persistência), `ACCompat.onCaughtFire` e bloco da tag, `WorldEffectPolicy`, proteção de claims, lifecycle de tickets, authority server-side, limites de chunk/target, network e QA dedicada cross-dimensional. Sem isso, **não intervir no fluxo e não oferecer perks de detonação/chunk loading**.

**Potenciais perks conceituais:** qualidade de vínculo, interface, feedback, alcance condicional ou custo de uso; **nenhum hook per-player mutador real está comprovado**. Ficha técnica estática segue ⚠️ parcial e `NO_MUTATION`. A progressão do RPG Skill Tree não ganha autoridade sobre `Level` ou sobre o `onCaughtFire` do provider.

## Evidências e status

[GitHub Actions #44956716666](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44956716666) aprovou o censo **inicial** de JAR, não a CI da HEAD com manifesto e ficha. Relatório nativo `report.json` **199.424 bytes**, SHA-256 `010a50eec70f2458f20bb2950dbec5b83d000fd177f6391aa90e37137d483ada`, artefato `14728326280`. **Recursos SHA-exatos identificados:** `assets/alexscaves/models/item/remote_detonator.json` e `remote_detonator_active.json`, recipe `data/alexscaves/recipe/remote_detonator.json`, advancement `data/alexscaves/advancement/alexscaves/remote_detonation.json` e tag `data/alexscaves/tags/block/remote_detonator_activates.json`; hashes e bytes no manifesto. Sem confirmação do conteúdo da tag/receita, bootstrap de registry, efeitos externos, configuração, QA física, mundo, segurança ou hook. **+1 ficha parcial, +0 certificados, +0 novos casts.**
