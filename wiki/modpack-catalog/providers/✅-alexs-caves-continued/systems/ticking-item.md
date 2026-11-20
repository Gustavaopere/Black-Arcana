# ACTickingItem — dispatcher de tick das stacks

**Contrato estático:** ✅ CERTIFIED_STATIC_7_AXES / STATIC_TECHNICAL_CATALOG_ONLY, candidato #1127. Hook NOT_VERIFIED; runtime NOT_VERIFIED; physical_qa NOT_TESTED; perk NOT_CERTIFIED; NO_MUTATION; provider OPEN. Uma ficha de suporte, zero raízes.

## Identidade e ativação

com.github.alexmodguy.alexscaves.server.item.ACTickingItem, alexscaves publisher 1.0.10, Minecraft 1.21.1, Java 21, NeoForge referência 21.1.250. SHA-1 6960b299a39a039ac8a5eb9b07be4ad0e3e0a570, SHA-256 36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c, 75279314 bytes; SHA-256 classe a96fc5427180e594aa59c3272395c207f3570f49165e33af0fdfa429a9922a1e. Censo de 1555 classfiles, 0 campos, 1 método abstrato, 17 diretos e 1 indireto, 1 owner de member ref exato. Modlist sibling 3e39ecd559a6e1ad65502331aa42bb473d2029b8.

Player.aiStep@153 -> Inventory.tick@86 -> ItemStack.inventoryTick, mixin HEAD -> ACTickingItem.acInventoryTick@36, com stack, level, entity e selected. O int slot não é encaminhado. O dispatcher não cancela, não seleciona alvo nem gera scheduler novo. Configuração e anotações nativas auditadas; referências oficiais não transformadas. Inventory tem items 36, armor 4, offhand 1; patch NeoForge corrige selected por índice global, não por compartimento. Não inferir cadência/side real ou todos os callers do modpack.

## Consumidores e parâmetros

[Contrato com tabela causal completa dos 18 implementadores](../EXACT-TICKING-ITEM-CONTRACT-1.0.10.md), [selo](../EXACT-TICKING-ITEM-CONTRACT-1.0.10.json), [manifesto nativo](../EXACT-TICKING-ITEM-DISCOVERY-1.0.10.json), [fronteira](../EXACT-TICKING-ITEM-BOUNDARY-1.0.10.md). Cada corpo direto tem descriptor, code/instruction hash, branches, constantes, campos, calls e retornos. RadioactiveOnDestroyedBlockItem herda de RadioactiveBlockItem. São implementações de um ABI técnico, não 18 casts nem 18 itens completos certificados.

Parâmetros locais relevantes: radiação chance por tentativa N*C*(1−H/4), IRRADIATED 1800 ticks e H contado por identidade das quatro peças Hazmat; Sea Staff min(0,D−1) -> clamp setter oficial -> zero em domínio normal; club decrementa swingTime se selected e condições; Dreadbow cliente UseTime e janela de tiro perfeito; Raygun Solar 0.02F e condições ambientais; ShotGum criação de 1/2 projéteis, dano inicial solicitado 4F, bounces 4+2*L e consumo local; SackOfSating alimentação 1 com m=0.05F, timestamps e ramo de explosão; Cave Map e vínculos Beholder/bomba têm verificações temporais e espaciais próprias. Valores, branching e limites na prova; não herdar certificação de item/entidade integral.

## Targeting, custo, estado e interoperabilidade

A interface não possui causa ofensiva, mana, cooldown, alcance, AOE, dano ou owner/persistência próprios. Recebe portador e stack reais da engine; cada implementador tem condições e writes específicos, com ou sem guard de lado, estado persistente, mensagens, spawn e débito. Separar pedido de aceitação, callbacks visuais e transacionais, frequência efetiva e custo. Não invocar de novo para perk de cadência nem mutar estado global do item. Cálculo e seleção seguros dependem do pipeline autoritativo do provider e boundaries real-tested; Black Arcana runtime mágico, RPG Skill Tree progressão. NO_MUTATION/fail-closed.

Validação: c0c0b479729361af74fb5ca404df6997a792185973455c4e52089773fb84f72b, e230bb2f1df46465d296be7150a263c27bc1fad28f72be2bbe2dc4d54f39d899, 8f03a6adcf0cb2a967f175fbad76e83923b45a87fd38e55a7e901b44881d214d; oito regressões e complemento passaram no job 136073564307, CI final exigida. N/A para ações que não pertencem ao dispatcher; downstream, world safety, execução transformada, sincronização e QA física NÃO VERIFICADOS. Próximo AlexMealItem.
