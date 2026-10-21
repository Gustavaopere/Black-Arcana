# Warp Portal Conjuration

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT` — `PortalScrollItem → WarpPortalManager.spawnPortal` confirmado no JAR físico `21.1.45`; distinct portal creation, not portal traversal. [Java21 #38460510230](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38460510230), [dossiê](../EXACT-BINARY-ACTIONS-21.1.45.md). Sem promoção de custo, multiplayer, persistência ou Survival (⚠️); +0 nova ação.

- Provider: **Waystones** (`waystones`)
- Version: `21.1.45`
- Classificação: **portal-conjuration player action**
- Semantic state: `COUNTED_EXACT` (**identidade física estática somente**)
- Strict contribution: `1`
- Provider surface: **Portal Scroll**

## Identidade semântica

A Portal Scroll executa uma raiz sobrenatural distinta do teleport direto: o jogador seleciona um destino e o provider cria um Warp Portal orientado para esse alvo.

A criação do portal é o resultado causal independente desta ação.

## Deduplicação

A travessia posterior do portal não cria uma quarta identidade. O portal reutiliza a raiz já contada **Waystone Warp / Teleport** para settlement de transporte.

## Evidence boundary

A reconciliação source-pinned fecha a separação causal entre portal spawn e teleport settlement. Duração, lifecycle, multiplayer behavior e policy efetivamente implantada permanecem runtime QA.

Source: `../SOURCE-21.1.45-SEMANTIC-CLOSURE.md`.

## Auditoria técnica para perks — 17/10/2026

**Evidência:** source oficial Waystones 21.1.45 pinado em TwelveIterations/Waystones@c540cfdbb9c1d790fbff397beea7c83f0c6f035f; identity/callsite do JAR físico SHA-1 6ec1a176a102212db4f6391886db52ed103c830f já demonstrados. Apenas semântica, código e defaults da versão fixa; não atesta configuração implantada, ABI de todos os métodos auxiliares, gameplay ou hook de perk.

### Matriz causal por eixo

| Eixo | Mecanismo comprovado no source | Estado para perks |
|---|---|---|
| Ingresso e tempo | PortalScrollItem.getUseDuration lê **general.scrollUseTime** (default **32 ticks**). Em finishUsingItem, exige ServerPlayer, verifica hasSpaceForPortal, abre seleção provider-native e associa post-handler ao destino. | **CONFIG_NATIVE** global; acelerar cast por jogador ainda **SEM_HOOK_SEGURO**. |
| Alcance de posicionamento | WarpPortalManager.findPortalPos procura posições à frente do jogador em **3 e 4 blocos** da projeção horizontal, descendo por candidatos de **dy 0..5**; não é range entre Waystones nem alcance de ataque. | **SEM_HOOK_SEGURO** para ampliar ou deslocar esse algoritmo externamente. |
| Geometria/colisão de bloco | Exige base sólida, dois blocos de portal substituíveis e um terceiro espaço acima substituível; spawnPortal coloca **2 blocos verticais** e inicializa WarpPortalBlockEntity. Não há AOE/hitbox de projétil. | **N/A** projétil e dano; alteração de tamanho/quantidade de portais exigiria hook real, regras de claims e limite de blocos. |
| Custos | Quando spawnPortal retorna true no callback, Portal Scroll é consumida em **1 unidade**; se não houver espaço, o método conserva o item. XP e demais requirements no fluxo de seleção **não foram homologados** neste ponto; não confundir callback de menu com teleport realmente concluído. | Item consumido pelo **provider**; descontos sem seam seguro **⛔**. |
| Duração/persistência | WarpPortalBlockEntity.LIFETIME_TICKS = **6000 ticks** (5 minutos a 20 TPS). Persistência NBT registra **UUID, Target, Age**, e o ticking remove o portal ao expirar; destino por proxy de Waystone quando necessário. | **SEM_HOOK_SEGURO** para alterar duração por jogador; não reutilizar temporizador de portal como cooldown de cast. |
| Travessia | onEntityInside verifica target válido e canUsePortal. canUsePortal usa cooldown por entidade de **20 ticks** em WeakHashMap (estado RAM), com policy de entity deny-list; a travessia chama **tryTeleportAsync** e a raiz de teleport já catalogada. | **HOOK_VERIFICADO no source** apenas para a fase de teleport dos eventos provider-native; não para criação/placement do portal. |
| Dano/status | Criação e travessia não demonstram DamageType ofensivo ou debuff intrínseco. | **N/A** dano, conversão elemental e procs ofensivos. |

### Referências imutáveis e limites de execução

- [PortalScrollItem.java linhas 16–55](https://github.com/TwelveIterations/Waystones/blob/c540cfdbb9c1d790fbff397beea7c83f0c6f035f/common/src/main/java/net/blay09/mods/waystones/item/PortalScrollItem.java#L16-L55): duração, validação server-side, menu e consumo unitário **após** resultado de spawn.
- [WarpPortalManager.java linhas 35–99](https://github.com/TwelveIterations/Waystones/blob/c540cfdbb9c1d790fbff397beea7c83f0c6f035f/common/src/main/java/net/blay09/mods/waystones/core/WarpPortalManager.java#L35-L99): seleção de posição e blocos criados; não foi verificada a intervenção de plugins de claim na chamada a setBlock.
- [WarpPortalManager.java linhas 101–125](https://github.com/TwelveIterations/Waystones/blob/c540cfdbb9c1d790fbff397beea7c83f0c6f035f/common/src/main/java/net/blay09/mods/waystones/core/WarpPortalManager.java#L101-L125): cooldown na travessia e resultado assíncrono; o valor de cooldown é registrado antes do teste final de deny-list, portanto efeitos de falhas/retentativas precisam QA.
- [WarpPortalBlockEntity.java linhas 38–89](https://github.com/TwelveIterations/Waystones/blob/c540cfdbb9c1d790fbff397beea7c83f0c6f035f/common/src/main/java/net/blay09/mods/waystones/block/entity/WarpPortalBlockEntity.java#L38-L89) e [107–145](https://github.com/TwelveIterations/Waystones/blob/c540cfdbb9c1d790fbff397beea7c83f0c6f035f/common/src/main/java/net/blay09/mods/waystones/block/entity/WarpPortalBlockEntity.java#L107-L145): lifetime, NBT, target, expiração e remoção de portal/registro.
- [Config 21.1.45](https://github.com/TwelveIterations/Waystones/blob/c540cfdbb9c1d790fbff397beea7c83f0c6f035f/common/src/main/java/net/blay09/mods/waystones/config/WaystonesConfigData.java#L68-L101): defaults e requisitos são server-configuráveis, não perks individuais.

**Gate obrigatório:** executar teste de ServerPlayer e portal físico com claim/permission, reentrada, restart, target excluído/removido, timeout, item consumido exatamente uma vez, e confirmação de que eventos de teleport não dão Mastery adicional à criação. Não há contrato aprovado para editar geometria, timeout ou criar portais adicionais por perk. Black Arcana WorldEffectPolicy não pode ser assumida como proteção automática dos blocos criados por Waystones.
