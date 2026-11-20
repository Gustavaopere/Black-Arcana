# Burrowing Arrow 1.0.10 — handoff de causalidade nativa (sem certificação)

**Estado:** ⚠️ captura binária SHA-exata concluída; análise de causalidade da entidade ainda pendente. `DISCOVERY_NOT_CERTIFIED`; `NO_MUTATION`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `provider_universe_closed=false`. Documento de auditoria, **não** ficha ✅, alteração de ledger, nova raiz de magia ou QA de runtime.

## Identidade e evidências já existentes

- Provider: Alex's Caves Continued, mod ID `alexscaves`; Minecraft 1.21.1, NeoForge, Java 21.
- Artefato publisher da instalação documentada: `alexscaves-1.0.10-neoforge+1.21.1.jar`, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- ID de registro estático: `alexscaves:burrowing_arrow`; binding `ACItemRegistry.BURROWING_ARROW` via `lambda$static$129()Item`. Esse binding é um pedido de registro, não prova autônoma de aceitação pelo loader.
- Classe exata `com/github/alexmodguy/alexscaves/server/item/BurrowingArrowItem`, SHA-256 `be5e566fc89b01c311d70d8d2a0fbbe7387601c9b07e70417135bd668b51fded`; herda `net/minecraft/world/item/ArrowItem`, sem campos próprios e com dois corpos declarados.
- Fontes: [descoberta SHA-exata do lote](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-BURROWING-CAVE-MAP-DISCOVERY-1.0.10.md), [manifesto](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-BURROWING-CAVE-MAP-DISCOVERY-1.0.10.json), [binding e dispenser](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/systems/item-registry.md), [auditoria de registro](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-ITEM-REGISTRY-CONTRACT-1.0.10.md). A descoberta anterior tem o job `136078919330` e sela um relatório sem certificar este objeto individualmente.

## Dois caminhos de construção, uma fronteira de entidade

| Superfície | Prova de corpo próprio | Limite da inferência |
|---|---|---|
| Fábrica de munição `BurrowingArrowItem.createArrow(Level, ItemStack, LivingEntity, ItemStack):AbstractArrow` | Corpo de 10 bytes, SHA-256 `b006d85505577c41d8f4be8729e6a7ad6c8b7c06da12829286a202a314b89a07`. O método instancia `BurrowingArrowEntity(Level, LivingEntity)` e devolve a entidade; os dois argumentos `ItemStack` não são usados **dentro deste corpo**. | A chamada local não prova disparo aceito, consumo de munição, velocidade, precisão, dano, persistência, permissão de modificar blocos, nem ausência desses comportamentos no chamador ou na entidade. |
| Dispenser `ACItemRegistry$6` | Callback de projétil registra construção de `BurrowingArrowEntity`, recebendo parâmetros do dispenser, e escreve `AbstractArrow.pickup=ALLOWED`; há uma janela de bytecode já auditada em `systems/item-registry.md` (`@0–38`). | O callback não é um segundo cast mágico. O fluxo de acionamento, posicionamento, velocidade, consumo, entidade efetivamente adicionada e efeitos subsequentes pertencem a outros consumidores/engine. |
| Registro `ACItemRegistry.lambda$static$129` | `new BurrowingArrowItem` em `@0` e `invokespecial <init>` em `@4`; o SHA-256 do corpo Code da factory é `6ba1983282a777582b1768407e8d5fa5ccc3afc88285edbf63935d9ec62a3859`. | Registro não executa disparo nem cria uma nova raiz semântica. |

O construtor `BurrowingArrowItem.<init>()` tem 12 bytes de Code e hash `8be36d6241481f2aa744705cb8bf58543a3d2d603628b0a2626b73949973458c`. O censo da descoberta detectou dois owners tipados e dois sites, ambos do binding local e da própria classe; **não** equivale a censo transitivo de consumidores de `BurrowingArrowEntity`.

## Eixos ainda não certificados

- **Ativação/recursos:** método nativo de arco/besta, checagem de ammo, encantamentos, dispensers, débito real da stack, estatísticas e eventuais cooldowns — `NÃO VERIFICADO`.
- **Dano e efeito:** damage type, dano base, escalonamento, hit entity/block, knockback, escavação, world griefing, proteção de claims e resultado efetivamente aceito — `NÃO VERIFICADO`.
- **Geometria:** targeting, intervalo de seleção, trajetória, velocidade, gravidade, hitbox, AOE e duração — `NÃO VERIFICADO`.
- **Autoria/persistência:** owner persistido, atribuição de dano, serialização, sincronização, ciclo de descarte e drop/pickup após os callbacks — `NÃO VERIFICADO`.
- **Perks/Mastery:** possível influência sobre munição, projétil ou dano é **hipótese de design**, não `mutating_hook=VERIFIED`; não autorizar mutação antes de localizar o boundary seguro, server-authoritative, único e causal.
- **Classificação:** item/entidade de projétil identificados, mas não demonstrados como uma raiz mágica independente. Não aumentar contador de magias sem prova semântica.

## Continuação auditável

O novo [probe read-only](alexscaves_1010_burrowing_entity_probe.py) localiza `BurrowingArrowItem.class`, `BurrowingArrowEntity.class` e `ACItemRegistry$6.class` **por basename único dentro do JAR SHA-exato**, sem presumir pacote da entidade; valida hash/tamanho/roster e grava `javap -v -p -c -s`, hash de cada classfile e hash das transcrições num artefato de CI. Não declara certificação, não executa o modpack e não guarda bytes de terceiro no repositório.

Próxima passagem: ler a transcrição real da entidade, construir o grafo transitivo de métodos e consumidores, conferir constantes/CFG/callbacks e distinguir efeito solicitado de efeito aceito. Depois elaborar ficha individual canônica com todos os eixos aplicáveis e somente então atualizar ledger e índices via gerador. **Sem evidência suficiente: permanecer ⚠️ parcial e `NO_MUTATION`.**

## Captura binária adicional (job `136615116371` — sucesso)

O workflow [burrowing_arrow_entity_discovery](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44830850816/job/136615116371) validou JAR SHA-exato e 1.555 classes, produziu as três transcrições integrais `javap -v -p -c -s` e arquivou quatro arquivos. O [manifesto compacto](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-BURROWING-ARROW-ENTITY-DISCOVERY-1.0.10.json) fixa os hashes dos classfiles e das transcrições.

| Classe física | SHA-256 do classfile | Linhas da transcrição |
|---|---|---:|
| `BurrowingArrowItem` | `be5e566fc89b01c311d70d8d2a0fbbe7387601c9b07e70417135bd668b51fded` | 93 |
| `BurrowingArrowEntity` | `2fc54e3d320e716e2ccd39bca598c1d4be6a1a1fc3bfbe3e01a6b5bd6690b975` | 1149 |
| `ACItemRegistry$6` | `721d302ffe9969fd15510f63035c2d338be5a962a91f88519c0b527efe8b53a6` | 127 |

Artefato de CI `14675699386`, SHA-256 do ZIP `4f291e7d6a6240002be04bbfa354a2a71718a32be2a8c0ab7a5aa42dd3f3df65`, retenção até 04/12/2026. A transcrição foi **capturada**, mas os 1.149 registros de linha da entidade ainda não foram individualmente analisados/convertidos em contrato de comportamento. Não confundir esse resultado com certificação de dano, colisão, block safety, targeting ou persistência.

