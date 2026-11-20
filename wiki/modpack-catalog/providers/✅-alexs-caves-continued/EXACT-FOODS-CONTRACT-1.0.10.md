# ACFoods — contrato estático delimitado de propriedades alimentares 1.0.10

**CERTIFIED_STATIC_7_AXES / STATIC_TECHNICAL_CATALOG_ONLY — candidato #1122.** NO_MUTATION; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; perk_certification=NOT_CERTIFIED; runtime_dispatch=NOT_VERIFIED; provider_universe_closed=false.

## Identidade, evidência e eixos

| Eixo | Evidência |
|---|---|
| identity | JAR publisher 1.0.10 SHA-exato; ACFoods com 63 campos public static final de FoodProperties, 48 métodos, censo tipado de 1555 classfiles. |
| behavior | 606 instruções no clinit, 63 construções únicas, 46 suppliers, resolução eager por ACFoodBuilder e ACCompat.effect delegando wrapAsHolder; 121 leituras em oito owners. Crosswalk por campo e supplier, não certificação de item. |
| parameters | 63 pares de nutrição/modificador de saturação, flags, 46 probabilidades e durações; 45 campos com efeitos, 18 sem declaração; constructor Holder,int referencia amplifier bruto zero; formula float N*m*2F, 32/16 ticks, custos e clamps no contrato de builder. |
| targeting | Suporte declarativo global, nenhum alvo/cast no helper. O consumador de referência é LivingEntity; efeitos downstream e targeting de itens/blocos têm contratos separados. |
| costs | Sem mana, cooldown, recurso, gasto ou transação próprios. Referência de consumo de stack, recipiente e fome no contrato ACFoodBuilder; não equivale a execução dos itens. |
| integration | Censo e crosswalk de 121 referências tipadas em oito owners, ACCompat.effect -> Registry.wrapAsHolder, referências vanilla 1.21.1 e NeoForge 21.1.250 do builder; sem hook mutador ou autoridade sobre efeitos downstream. |
| validation | Job 134904019583: seis testes, replay do relatório de SHA fixa; job 135317637623: boundary nativo e construtores de referência SHA-exatos; testes de crosswalk, identidade, boundary e índices obrigatórios. QA física NOT_TESTED. |

O [crosswalk completo](EXACT-FOODS-DISCOVERY-1.0.10.md) e [manifesto](EXACT-FOODS-DISCOVERY-1.0.10.json) preservam as 63 configurações, os 46 suppliers com code/instruction hashes, os offsets de construção e todos os 121 sites de leitura. O [selo](EXACT-FOODS-CONTRACT-1.0.10.json) fixa os hashes de referência.

## Boundary de valores e efeitos

- O JAR de 75.279.314 bytes tem SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A classe ACFoods tem SHA-256 `a52ec981fe51c97003383a46f7c0b2de06baa5e3ca3f73db988655abce51e12e`.
- Cada supplier usa MobEffectInstance(Holder,int); há 10 identidades de efeito referenciadas, não 46 efeitos diferentes. Os efeitos do provider chegam por supplier e ACCompat.effect. O wrapper tem quatro instruções: busca BuiltInRegistries.MOB_EFFECT @0, carrega o efeito @3, chama Registry.wrapAsHolder @4 e devolve o holder @9. Não é aplicação de efeito, não escolhe entidade nem resolve configuração de perks. Code SHA-256 `a6fcb990359b50a29238d383f13da2a665a0510bbd6dfc4f527e05ef80b47863`.
- Referência oficial Mojang 1.21.1, classe mapeada MobEffectInstance (obf brz): (Ljm;I)V @0–7 encaminha a duração e amplifier 0 para (Ljm;II)V @4; essa sobrecarga repassa booleanos 0 e 1; a próxima duplica a última flag para a terceira flag; a sobrecarga final recebe hidden effect null e chama clamp(0,255) no amplifier. Duração encaminhada sem clamp nessa atribuição. Não inferir comportamento de merge, aplicação ou tick do construtor. Referência não transformada, não execução instalada.
- ACFoodBuilder resolve suppliers eager uma vez na construção; FoodProperties consumido por engine usa cópia da instância e sorteio servidor u<p. A chance e duração não significam efeito aceito. Ver [contrato do builder](EXACT-FOOD-BUILDER-CONTRACT-1.0.10.md) e fichas de [Rage](effects/rage.md), [Irradiated](effects/irradiated.md), [Stunned](effects/stunned.md), [Sugar Rush](effects/sugar-rush.md).

## Reprodução e limites

[Auditor nativo](../../../../docs/qa/alexscaves_1010_foods_probe.py), [boundary](../../../../docs/qa/alexscaves_1010_foods_boundary.py), [regressões](../../../../docs/qa/alexscaves_1010_foods_probe_test.py). Nativo `8310d35563ee74028469f192aada383c35a6cd43f70b288ec5ad93de6d8dfed1`, job 134904019583 (replay na PR #1122); boundary `0fe3473bee455115e568c58f815cc223014ddf5202c828d2634e48d629733320`, [run 44451904667](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44451904667/job/135317637623). Seis regressões passaram no HEAD c6425879 e replay no job complementar; os gates do candidato final incluem a verificação do boundary e os índices canônicos.

O escopo certificado é a classe de suporte declarativa ACFoods, não ACItemRegistry, ACBlockRegistry, seus factories, os itens ou blocos individuais, o sistema de efeitos integral ou a execução em modpack. O inventário dos 63 campos não é um universo de magias. 45 campos com efeito declarado, 18 sem declaração (não ausência de efeito próprio de item); +1 ficha de suporte, +0 raízes mágicas. Autoridade Black Arcana/RPG Skill Tree preservada. Não mutar FoodProperties global, BUILT ou registry por jogador, não reaplicar efeitos no Finish. Sem ação de gameplay nesta PR.
