# Burrowing Arrow a Cave Map — contratos estáticos de item 1.0.10

Publisher file 8856293, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A descoberta preservada percorre 1.555 classes, os 40 corpos próprios das seis classes e os consumidores tipados. O suplemento sela os bindings de itens, as receitas, as tags, as páginas do livro e os consumidores nativos usados nas fichas. [Descoberta e identidades de classe](EXACT-BURROWING-CAVE-MAP-DISCOVERY-1.0.10.md) · [Selo suplementar](EXACT-BURROWING-CAVE-ITEMS-CATALOG-1.0.10.json)

## Escopos e fronteiras

| Classe | Contrato documentado | Evidência complementar |
|---|---|---|
| BurrowingArrowItem | Factory de munição e factory do dispenser, dimensões, base de dano e piercing pedidos, ciclo de escavação e receita | [Causal do projétil](EXACT-BURROWING-ARROW-CAUSAL-1.0.10.md) · [Ficha](items/burrowing-arrow.md) |
| CandyCaneHookItem | Lançamento, estado UUID/reeling, desgaste local, limites e filtros do hook | [Descoberta do hook](EXACT-CANDY-CANE-HOOK-DISCOVERY-1.0.10.json) · [Ficha](items/candy-cane-hook.md) |
| CaveBoatItem | Quatro recursos de item, posição, colisão, custo, tipo e variante de entidade, dimensões e receitas | [Causal de transporte](EXACT-CAVE-BOAT-CAUSAL-1.0.10.md) · [Pewen](items/pewen-boat.md) · [Pewen com baú](items/pewen-chest-boat.md) · [Thornwood](items/thornwood-boat.md) · [Thornwood com baú](items/thornwood-chest-boat.md) |
| CaveBookItem | Abertura da interface, notificação de uso, texto, receita e 68 JSONs de páginas empacotadas | [Causal do livro](EXACT-CAVE-BOOK-CAUSAL-1.0.10.md) · [Ficha](items/cave-book.md) |
| CaveInfoItem | Componente `CaveBiome`, criação e leitura, apresentação e progressão solicitada pelo Codex. Biome Treat mantém sua ficha própria. | [Contrato do Biome Treat](items/biome-treat.md) · [Cave Info](systems/cave-info-item.md) |
| CaveMapItem | Criação e uso, alvo de bioma, worker de busca e preenchimento de dados, callback de atualização | [Dispatcher de inventário](systems/ticking-item.md) · [Ficha](items/cave-map.md) |

### Parâmetros herdados de referência

A referência de desenvolvimento derivada de Minecraft 1.21.1 e NeoForge 21.1.248 tem SHA-256 `0e588600c7c5084989f201f9e5c3a2e74fc4a7c6dccaa970b65a21bd6d004d08`. Seu `Item.getPlayerPOVHitResult(Level,Player,ClipContext.Fluid)` (Code SHA-256 `88a7b3fd5a572707f67b5ca5a89736f0066055683e92049c3edd6577b2fcf1cd`) usa a posição do olho, a direção definida por pitch/yaw e `Player.blockInteractionRange()` (Code SHA-256 `e11bb403121ff340bf74da140dbacee47c251c6e2c63afd26c49b0cb4a30eff8`). O item de barco pede `Fluid.ANY`. A AABB de obstrução de comprimento 5 pertence ao publisher, enquanto o comprimento do raycast usa o atributo do jogador na referência. `ChestBoat.getContainerSize` retorna 27 (Code SHA-256 `fa1c3f5ab3de975f2fbc2dac08278399a3d7fee3cd23ab3f9b98a47d287a2c93`). A capacidade da referência e a persistência após salvar e carregar têm verificações próprias.

Na mesma referência, `ProjectileWeaponItem.createProjectile` (Code SHA-256 `444908b77a8d0c70e13f950e1814a3e5296a081879cb4c92d1c7dc9f52649c21`) despacha `ArrowItem.createArrow`. `AbstractArrow.onHitEntity` (Code SHA-256 `c39610ad844df8bb5e099b7c86df5eaa91c30b3887f4946048af3b6f24212292`) usa comprimento de velocidade convertido a float, fonte de flecha e cálculo de dano separado do pedido de escavação. A classe de dispenser é do publisher e seu método `execute` foi reproduzido no selo.

Os documentos causais anteriores descrevem a descoberta que antecedeu este lote. Seus estados e hashes foram preservados como histórico. As fichas novas ou enriquecidas delimitam a evidência por comportamento: chamadas do publisher, herança de referência e aceitação em jogo.

## Reprodução

O workflow executa o probe das seis classes, roda suas quatro regressões e compara os relatórios com o selo. O suplemento compara os hashes dos oito manifestos anteriores e reproduz os dados do publisher, incluindo as receitas dos quatro barcos, o censo de livros e os corpos e descritores selecionados da fila de mapas. São 164 corpos em 17 classes suplementares. SHA-256 do selo: `0af795caf25433cba7c9c076345dbd857ec23a96b1bf7dc240fc2927e26356b7`. [Workflow](../../../../.github/workflows/alexscaves-1010-burrowing-cave-map-probe.yml) · [Verificador](../../../../docs/qa/alexscaves_1010_burrowing_cave_items_catalog.py)

Os eixos usados no ledger são identidade, comportamento, parâmetros, seleção de alvo, custos, integração e validação. Para aceitação em runtime, continuam pendentes spawn e dano aceitos, proteção de mundo, inventário e persistência após reload, progresso integrado, recursos ativos, rede, hooks mutadores e QA física. As seis classes documentam munição, mobilidade, transporte ou exploração. O contador de oito raízes sobrenaturais permanece no mesmo recorte.

`STATIC_TECHNICAL_CATALOG_ONLY` · `NO_MUTATION` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED` · provider aberto.
