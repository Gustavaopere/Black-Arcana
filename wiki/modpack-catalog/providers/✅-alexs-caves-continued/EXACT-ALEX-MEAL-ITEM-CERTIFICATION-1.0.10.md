# AlexMealItem — certificação estática individual 1.0.10

`STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `CERTIFIED_STATIC_7_AXES` · `NO_MUTATION`. Runtime/hook `NOT_VERIFIED`; QA `NOT_TESTED`; perks `NOT_CERTIFIED`; provider `OPEN`; zero novas raízes.

[Ficha individual](items/alex-meal.md) · [Selo novo](EXACT-ALEX-MEAL-ITEM-CERTIFICATION-1.0.10.json) · [Evidência candidata preservada](EXACT-ALEX-MEAL-ITEM-CONTRACT-1.0.10.json).

## Sete eixos verificáveis

| Eixo | Prova e alcance |
|---|---|
| `identity` | JAR publisher 1.0.10, 75.279.314 bytes; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Classe `AlexMealItem` SHA-256 `6b7046627fb4ec7cd5a6e02e6aa6997ed26a0b2133fdeb808ccaf0178c6065da`, duas declarações/corpos próprios, parent Item e censo de 1555 classes. Binding literal `alexscaves:alex_meal`, factory, recipe e modelo exatos. |
| `behavior` | Construtor de 12 instruções anexa ACFoods.ALEX_MEAL, alias de raridade e pilha1; tooltip de 16 instruções adiciona texto traduzível cinza/itálico e chama super. Nenhum override próprio de consumo/tick/uso. Composição do consumo herdado pela referência já auditada, sem executar classes do jogo. |
| `parameters` | N40, m5F/bits40a00000, saturação nominal400 antes dos clamps; pilha1; tigela; uso referencial32ticks, sem fast/alwaysEat; CONFUSION200ticks e BAD_OMEN48000ticks, p1F/bits3f800000. Amplifier zero pertence à referência oficial do construtor, não é argumento explícito passado pelo supplier publisher. |
| `targeting` | Entidade consumidora como recebedor no pipeline externo. Nenhuma seleção hostil, alcance, AOE, LOS, projétil, dano direto ou summon próprios. Não transfere a certificação aos efeitos vanilla downstream. |
| `costs` | Próprios métodos não liquidam recursos. A referência pede consume1, preserva materiais infinitos e trata conversãoBOWL; custo efetivo, componentes externos, crafting remainders e transações permanecem separados. Mana/cooldown/XP N/A no código próprio. |
| `integration` | Reutiliza contratos de FoodBuilder, Foods e registry por arquivos imutáveis selados; não altera FoodProperties/Suppliers compartilhados por jogador. getFoodProperties e eventos são superfícies de referência, sem hook seguro ou settlement de Mastery homologados. |
| `validation` | Relatório nativo original reproduzido por SHA-256, todos os corpos próprios e factory preservados, recipe/modelo/lang selecionados conferidos; cinco pré-requisitos pinados. Novos testes negativos e duas execuções reais verificam determinismo e inputs intactos. Índices gerados não promovem provider/hook/QA. |

## Composição de evidências

O relatório original tem SHA-256 `7259e2bedc779f0f21574ddb599e06038bd62aa2344d591f34ad89483e34c25e`, [job 136073823658](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44671670490/job/136073823658). Seus cinco arquivos de descoberta continuam preservados, inclusive o estado candidato. O novo selo contém os corpos reais, o binding causal de ALEX_MEAL, o perfil binary32, referências e hashes dos pré-requisitos; não renomeia a evidência antiga como QA.

- [ACFoods nativo](EXACT-FOODS-NATIVE-CONTRACT-1.0.10.json): perfil e dois suppliers.
- [ACFoods/referência de efeitos](EXACT-FOODS-CONTRACT-1.0.10.json): construtor vanilla com amplifier zero.
- [ACFoodBuilder](EXACT-FOOD-BUILDER-CONTRACT-1.0.10.json): preparação eager, fórmula, clamps, tempo de uso, consumo e eventos oficiais.
- [ACItemRegistry](EXACT-ITEM-REGISTRY-CONTRACT-1.0.10.json): namespace/caminho/factory do item, sem execução de registro presumida.

Os pins dos pré-requisitos são verificados antes da reprodução. A fonte adjacente 1.1.1 não substitui nenhum desses artefatos 1.0.10. A composição não prova modificações do pack, tags/componentes carregados, aceitação de status, healing/regeneração, efeitos de BAD_OMEN, lado real de execução ou ordem de listeners.

## Reprodução

[Auditor](../../../../docs/qa/alexscaves_1010_alex_meal_item_certification.py) · [Testes](../../../../docs/qa/alexscaves_1010_alex_meal_item_certification_test.py) · [Workflow](../../../../.github/workflows/alexscaves-1010-alex-meal-item-certification.yml).

```sh
python docs/qa/alexscaves_1010_alex_meal_item_certification.py \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --javap /caminho/jdk-21/bin/javap \
  --seal 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-ALEX-MEAL-ITEM-CERTIFICATION-1.0.10.json' \
  --output /tmp/new-alex-meal-certification.json
```

Output deve ser novo. A comparação literal é acompanhada de guardas de causalidade e de alegação; inputs não são sobrescritos. CI precisa passar antes do merge. Permanecem pendentes QA física, integração executável de perks e fechamento do universo integral do provider.
