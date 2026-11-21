# CaveInfoItem — vínculo de bioma e pesquisa

**Versão:** Alex's Caves Continued 1.0.10, publisher 8856293. **Catálogo:** ✅ contrato técnico estático da classe e seus dois bindings. Hooks mutadores `NOT_VERIFIED`, QA física `NOT_TESTED`, `NO_MUTATION`.

O publisher usa a mesma classe `server.item.CaveInfoItem` para **Cave Tablet** e **Cave Codex**. A classe tem sete corpos próprios, um campo de instância `hideCaveId` e herda `Item`. O descendente `BiomeTreatItem` usa a factory de vínculo e mantém sua ficha própria. [Censo e classes](../EXACT-BURROWING-CAVE-MAP-DISCOVERY-1.0.10.md) · [Biome Treat](../items/biome-treat.md)

| Item de registro | Factory em ACItemRegistry | Propriedades solicitadas |
|---|---|---|
| `alexscaves:cave_tablet` | `lambda$static$1`; registro @332 | `UNCOMMON`, `hideCaveId=true` |
| `alexscaves:cave_codex` | `lambda$static$2`; registro @349 | `UNCOMMON`, `hideCaveId=false` |

## Stack, tooltip e cor

`create(Item,ResourceKey<Biome>)` constrói uma stack nova do item. Com chave não nula grava `CaveBiome` em `CUSTOM_DATA` por `ACCompat.setTag` (@18–37). Apenas no caso `BiomeTreatItem` com chave configurada atribui `ACFoods.BIOME_TREAT_DONE` em `FOOD` (@41–58). O componente vincula a identidade do bioma à stack.

`getCaveBiome` lê a string em `CUSTOM_DATA` e cria uma `ResourceKey` de `Registries.BIOME` (@11–33). A leitura é de identidade e depende de resolução de registro nos consumidores. A tooltip usa uma chave `biome.<namespace>.<path>` em cinza apenas com bioma e `hideCaveId=false` (@8–52). `getBiomeColor` consulta primeiro as cores nativas do registro, depois o bioma carregado para cor ambiental. `getBiomeColorOf` também tem apresentação animada com ciclo de **4.000 ms**, incluindo o ramo `Rainbow` com saturação 1 e brilho 0,8. A cor atende a renderização e ao minigame.

## Codex e mesa de pesquisa

1. `use` lê a mão e a chave. Entra no ramo de progressão apenas quando o item é `CAVE_CODEX` e há bioma (@2–43). Tablet e outras variantes ficam no retorno normal do item.
2. Lê `CaveBookProgress` do jogador e solicita `unlockNextFor` usando o ID do bioma (@49–58). `unlockNextFor` parte de `EMPTY` para uma categoria ausente. Quando permitido pelo próximo estágio, grava o ordinal seguinte ou o último permitido por categoria se `only_one_research_needed=true` (default **false**). A sequência de enum é `EMPTY → GENERAL → RESOURCES → MOBS → UTILITIES → SECRETS`. A etapa disponível depende das restrições desse bioma.
3. Em progressão positiva, usa swing e pede `saveCaveBookProgress` e a mensagem de progresso no ramo servidor (@66–213). Os caminhos convergem em @216. Tanto cliente quanto servidor podem pedir a redução de **um Codex** fora de Creative (@217–226), o som e o resultado consume. Quando o avanço falha, o corpo pede a mensagem de término e segue para pass. O pedido local de débito e a persistência Citadel têm verificações próprias. [Cave Book](../items/cave-book.md)
4. Na Spelunkery Table, o método de resultado usa a chave do tablet e pede a criação de um Codex associado em `lambda$setupResultSlot$0` (@27–39). A mesa tem pedidos de consumo de tablet e papel próprios ao processar a pesquisa. A receita de mapa lê a chave via `RecipeCaveMap.assemble` (@92). A obtenção ativa por mundo, a interface completa e o resultado aceito no modpack seguem o estado do ambiente.

O alvo de progressão é a categoria do bioma no registro do jogador que usa o Codex. Dano, área, projétil, cooldown e mana são inaplicáveis ao contrato da classe. O efeito autoritativo a validar para integração é o progresso realmente registrado, com custo e sincronização correspondentes. Uma futura perk deve preservar a chave e a autoridade da mesa/livro, evitando crédito por tooltip ou tentativa de uso. Este catálogo registra um contrato de suporte e as duas variantes que o usam. [Evidência do lote](../EXACT-BURROWING-CAVE-ITEMS-CATALOG-1.0.10.md)
