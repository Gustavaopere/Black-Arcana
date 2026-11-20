# AlwaysCombinableOnAnvil — combinação na bigorna

**Versão:** Alex's Caves Continued 1.0.10, publisher file 8856293. **Escopo:** contrato técnico estático do marcador e do consumidor nativo. **Hooks:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Perks executáveis:** `NOT_CERTIFIED`. `NO_MUTATION`.

O marcador vazio `server.item.AlwaysCombinableOnAnvil` ativa uma regra de combinação de encantamentos para [Raygun](../damage-types/raygun.md) e [Shot Gum](../damage-types/gumball.md). São os dois implementadores encontrados no censo de 1.555 classes. A interface tem zero campos, métodos ou superinterfaces. SHA-256 da classe: `d6d9ba639692a4e2964eca9163842f2fdfbfc98584b2d1b07155a4c780edf13c`.

## Entradas e aplicação

O construtor de `AlexsCaves` solicita o registro de `CommonEvents` em `NeoForge.EVENT_BUS` nos offsets 155–165. O handler `CommonEvents.onUpdateAnvil(AnvilUpdateEvent)V` tem `@SubscribeEvent` em anotação visível em runtime. O único teste de tipo executável do marcador está no offset 7 desse handler.

1. O item Left deve implementar a interface. Left e Right precisam referenciar o mesmo objeto `Item` (27), com mapas de encantamentos de crafting preenchidos em ambos (40 e 53).
2. Copia Left (60) e percorre os encantamentos de Right. Para níveis Left e Right iguais, pede `Right + 1`. Para níveis diferentes, usa `max(Left, Right)` (145–180). Compara o encantamento corrente aos demais holders na cópia (219–231).
3. Cada par incompatível soma 1 ao custo. A primeira incompatibilidade derruba a flag inicial de aplicação até o fim daquela chamada (85–86, 237–248). Os encantamentos posteriores ainda podem somar penalidades. A ordem de iteração pode, portanto, mudar quais encantamentos chegam à cópia.
4. Enquanto a flag permitir, limita ao `getMaxLevel()`, grava o nível (255–273) e soma o custo da tabela. O handler solicita `setCost(long)` (379), aplica o mapa à cópia (387) e solicita `setOutput(copy)` (392) após o laço, inclusive quando houve incompatibilidade.

| `getWeight()` do encantamento | Coeficiente × nível resultante |
|---:|---:|
| 10 | 1 |
| 5 | 2 |
| 2 | 4 |
| 1 | 8 |
| Demais | 0 |

O `tableswitch` em 284 lê o **peso** e a soma do handler é inteira (362–370) antes de passar para `long`. `setCost` e `setOutput` pedem custo e resultado da receita de bigorna. O débito de XP, a tomada do resultado e a interação com outros listeners pertencem ao menu e ao barramento da versão em execução. O corpo inspecionado escreve o mapa em uma cópia, sem chamada a `setMaterialCost`, `shrink` ou ajuste de durabilidade.

Na referência NeoForge 21.1.250, `CommonHooks.onAnvilChange` usa a saída do evento quando ela está preenchida e o evento segue válido. O menu exige custo positivo em `mayPickup`. A saída com custo zero pode, portanto, ser pedida pelo handler e falhar na retirada pela regra de referência. Em retirada aceita com custo de material zero, o fluxo de referência limpa as duas entradas e cobra níveis de experiência do jogador fora do modo de materiais infinitos. [Fronteira do menu](../EXACT-REPAIRABLE-ITEM-BOUNDARY-1.0.10.md)

## Integração

O alvo da operação é a cópia de Left. Alcance, área, projétil, dano, duração e cooldown ficam fora desse fluxo de combinação. Para uma perk de bigorna, a superfície do provider a considerar é a ordem dos holders, a compatibilidade, o nível e o pedido de custo. O fechamento estático cobre o pedido nativo e deixa a liquidação de recursos, as prioridades em tempo de execução e a aprovação de um hook pendentes.

[Prova, hashes e reprodução](../EXACT-ADJACENT-ITEMS-CATALOG-1.0.10.md)
