# Biome Treat — vínculo ao bioma atual

**Versão:** Alex's Caves Continued 1.0.10, publisher file 8856293. **Escopo:** contrato técnico estático do item `alexscaves:biome_treat`. **Hooks:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Perks executáveis:** `NOT_CERTIFIED`. `NO_MUTATION`.

O item registra o bioma na posição do jogador e fornece esse alvo ao [Conversion Crucible](../actions/conversion-crucible-biome-conversion.md). `ACItemRegistry` declara um único ID (literal 3469, chamada 3477, atribuição `BIOME_TREAT` 3480). O bootstrap 199 aponta para `lambda$static$197()Item`, que constrói `BiomeTreatItem`. A forma vinculada usa o mesmo item com componentes distintos. A classe estende `CaveInfoItem`, implementa `ACFoodPropertiesItem` e declara oito métodos, sem campos próprios. SHA-256: `d95121a7506d733bbfd1d61be48945a5f959d2dea43c854b894bb71e3cde6eb7`.

## Uso, seleção e resultado

| Etapa | Regra estática |
|---|---|
| Início (`use`) | Exige FOOD (9) e `getCaveBiome(stack) == null` (17). Consulta `Player.canEat` (33). Se elegível, chama `startUsingItem` (41) e pede resposta consume (46). Com fome inelegível pede fail (52). Com bioma já vinculado ou sem FOOD pede pass (61). |
| Fim (`finishUsingItem`) | Exige stack sem vínculo, entidade Player e `foodLevel == 0 \|\| isCreative()` para seguir a `Level.getBiome` na posição do jogador (42–45). `unwrapKey().get()` (48–53) alimenta `CaveInfoItem.create` (59) e retorna a nova stack (62). Demais casos delegam ao consumo herdado (67). |
| Vínculo (`CaveInfoItem.create`) | Cria stack nova do mesmo item, com `CUSTOM_DATA.CaveBiome` contendo o ID do bioma (0–37); para o Biome Treat com chave, troca FOOD por `BIOME_TREAT_DONE` (40–58). A construção usa propriedades padrão da nova stack e componentes escritos pela fábrica. |
| Leitura e apresentação | `CaveInfoItem.getCaveBiome` lê o componente e converte a string em chave de registro. A ausência de CUSTOM_DATA retorna null. Dados presentes passam pelo leitor de string e pela análise do identificador. O fluxo pressupõe chave válida quando chama `Optional.get` ou `ResourceLocation.parse`. |

## Parâmetros e custos

| Parâmetro | Sem vínculo | Vinculado |
|---|---|---|
| Alimentação declarada | Nutrição 20, modificador de saturação `0.1F` | Nutrição 1, mesmo modificador |
| Tempo e efeitos | Referência de FOOD padrão de 32 ticks. Sem efeito de status ou modificador de uso rápido em ACFoods. | A tentativa de uso normal cai no caminho pass, apesar do componente FOOD. |
| Stack e raridade | Limite 1, `UNCOMMON` | Mesmo ID e propriedades padrão |
| Resultado do fim de uso | A associação retorna uma stack nova antes da liquidação de alimento. O consumo normal delegado usa o mecanismo de Item. | A seleção via Crucible retém o Treat quando feita por interação ou consome uma unidade pelo coletor de itens no chão. |

O modificador `0.1F` tem bits `3dcccccd` nos dois perfis de ACFoods. FOOD é um componente da stack, com consumo herdado da referência já catalogada. A posição do jogador seleciona o alvo do vínculo. Área, dano direto, cooldown e mana ficam fora do fluxo próprio. A mudança de bioma e os custos de oferendas pertencem ao ciclo do Crucible. [ACFoods](../systems/foods.md) · [ACFoodBuilder](../systems/food-builder.md)

A animação usa `DRINK` e o som solicitado é `GENERIC_EAT`. `onUseTick` pede partículas de stack `JELLY_BEAN_EAT` pelos caminhos de servidor e cliente. O texto inglês é “Biome Treat”, com “Unbound” na tooltip quando a chave retorna null. A cor sem vínculo usa matiz variável em um ciclo de 4.000 ms, saturação 1 e brilho 0,8. Com vínculo usa a cor resolvida do bioma. Esses valores dizem respeito à apresentação.

A receita empacotada usa o padrão `RER / RER / ·C·` (· é vazio). São quatro entradas `#alexscaves:rock_candies`, duas `alexscaves:radiant_essence` e uma `alexscaves:candy_cane`. O resultado declara `alexscaves:biome_treat`. O modelo combina `biome_treat` e `biome_treat_color`. Datapacks e componentes efetivos continuam sujeitos ao ambiente carregado.

Perks de alimentação precisam respeitar a distinção entre tentar comer, pedir a stack vinculada e concluir a troca ou o consumo no engine. Vínculo e uso no Crucible compartilham uma única ação de conversão já inventariada. A aceitação da nova stack e o despacho de eventos no modpack continuam pendentes de QA.

[Prova, hashes e reprodução](../EXACT-ADJACENT-ITEMS-CATALOG-1.0.10.md)
