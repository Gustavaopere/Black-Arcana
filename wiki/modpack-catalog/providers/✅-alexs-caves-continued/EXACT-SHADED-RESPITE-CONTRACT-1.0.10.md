# Shaded Respite 1.0.10 — contrato técnico estático individual

A [ficha individual](enchantments/shaded-respite.md) documenta identidade, comportamento, parâmetros, targeting, custos, integração e validação estática deste encantamento. O recorte cobre os predicados de isenção/fallback do Dreadbow e seus helpers nativos. Preserva os bytes e escopos das provas de [Dreadbow/Dark Arrow](EXACT-DREADBOW-CONTRACTS-1.0.10.json), [Relentless Darkness](EXACT-RELENTLESS-DARKNESS-CONTRACT-1.0.10.json), [Precise Volley](EXACT-PRECISE-VOLLEY-CONTRACT-1.0.10.json) e demais contratos anteriores. Não conclui outros encantamentos, factories externas, combate integrado, rede ou provider integral.

Autoridade: JAR publisher CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A fonte adjacente `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e serve apenas de corroboração; os parâmetros abaixo vêm do artefato físico **1.0.10**.

O [manifesto individual](EXACT-SHADED-RESPITE-CONTRACT-1.0.10.json), SHA-256 `7cec53b16777630e2fa9b9c669201dc84084e9115c3a53a7412565b5d0d4ae59`, sela **uma ficha, 5 classes, 10 recursos, 19 métodos e 522 âncoras**. Há **16 corpos completos, somando 389 instruções**, mais 125 âncoras de `releaseUsing` e oito de dois inicializadores delimitados.

| Classe / método | Cobertura de instruções |
|---|---:|
| `DreadbowItem.<init>`, `getEnchantmentValue`, `isEnchantable` | 10/10, 2/2 e 8/8 |
| `DreadbowItem.use` | 51/51 |
| `DreadbowItem.onUseTick` | 175/175 |
| `DreadbowItem.createArrow`, `isConvertibleArrow` | 29/29 e 14/14 |
| `DreadbowItem.releaseUsing` | **125/391**: janelas locais completas `@0–182` (84 instruções) e `@801–899` (41); 266 instruções omitidas |
| `DarknessIncarnateEffect.isInLight` | 29/29 |
| `ACCompat.enchantLevel`, `sunAboveHorizon` | 24/24 e 16/16 |
| `ACCompat.hurtAndBreakUsedHand`, `slotOf` | 8/8 e 7/7 |
| `ACCompat.useConsume`, `useFail` | 3/3 e 3/3 |
| `ACEnchantmentRegistry.key`, `<clinit>` | 6/6; inicializador 3/182, offsets `419,422,425` |
| `ACItemRegistry.lambda$static$137`, `<clinit>` | 4/4; inicializador 5/1382, offsets `2497,2500,2503,2508,2511` |

O inicializador do registro liga o literal `shaded_respite` à chave `SHADED_RESPITE`. O bootstrap 142 do registro de itens liga `dreadbow` ao supplier `lambda$static$137`; o construtor completo declara durabilidade 500 e o campo `RARITY_DEMONIC`. Essas janelas não declaram todos os registros dos inicializadores auditados. Os outros métodos e consumidores do Dreadbow conservam seus próprios certificados e limites.

O corpo nativo de `releaseUsing` foi contado como 391 instruções, offsets `0–899`, e recebeu fingerprint auxiliar da representação normalizada de owner, nome, descriptor e instruções: SHA-256 `d7784f2d00d859f406c6308cf19eb2cd78c9854fe6f2d6289d595d60ca79a4ca`. Essa representação usa JSON UTF-8 com chaves ordenadas e separadores compactos; cada instrução contém offset, opcode, operand e symbol da saída `javap -p -c -s`. O hash da classe distribuída permanece a autoridade selada pelo auditor. O fingerprint e o censo completo corroboram a delimitação; **não substituem as 266 instruções omitidas por um CFG integralmente auditado**. As duas janelas selecionadas contêm todas as instruções locais da entrada, predicado Shaded, potência mínima, fallback de munição/protótipo, conclusão do loop e cobrança final. O flag local 9 é escrito em `@84` e relido em `@144,865,877`; não há outra atribuição desse local no corpo examinado.

Distinções centrais: elegibilidade é `L>0 && !isInLight(player,11)`, sem escala por nível positivo. O helper completo usa a posição do veículo raiz, luz BLOCK e override para 15 quando há céu e sol acima do horizonte; o predicado exige valor calculado menor que 11. `sunAboveHorizon` testa fase `<0.259F || >0.74F`, com igualdades falsas e sem usar o argumento BlockPos. Chamar esse helper não exige efeito Darkness Incarnate ativo.

O gate inicial completo de `use` continua creative ou munição não vazia e não lê Shaded. O fallback posterior não certifica início survival sem munição. `releaseUsing` tem retorno antecipado para protótipo null; o callback Relentless completo não contém esse retorno. A isenção de desgaste depende do booleano Shaded; a isenção de consumo depende também do Item exato `Items.ARROW`. Munição especial e conversibilidade da entidade são decisões distintas. Custo é por invocação que alcança o bloco final, com creative separado; não é cobrança por flecha tentada ou por hit. Os corpos não têm guarda direta `Level.isClientSide`, sem conclusão de falha física ou autorização para mutar callbacks.

Os dez recursos selam JSON próprio, tag exclusiva Dreadbow, idiomas inglês/português, quatro tags de aquisição, receita do equipamento e TOML. O JSON publica máximo I, peso 1, custo mínimo/máximo 1/41 no nível I, anvil cost 8 e slot `mainhand`; não há `effects` ou `exclusive_set` local. O scan dos 51 JSONs não encontrou exclusão reversa; o censo de Fieldrefs exatos nos 1.555 classfiles encontrou `SHADED_RESPITE` somente no registro e no Dreadbow. Esses censos são restritos ao publisher, sem presumir datapacks ativos, transformadores, reflexão, compatibilidade ou obtenção em jogo.

Reprodução a partir da raiz do repositório, com Java 21 e o mesmo JAR publisher:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile shaded_respite \
  --jar /caminho/para/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-SHADED-RESPITE-CONTRACT-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap "$JAVA_HOME/bin/javap" \
  --output /tmp/shaded-respite-evidence.json
```

A auditoria do artefato real retornou **PASS: 1 ficha, 5 classes, 10 recursos, 19 métodos, 522 âncoras**. A reconstrução externa do manifesto conservou os mesmos bytes, com idempotência verificada sobre os inputs selados. Os [testes semânticos](../../../../docs/qa/alexscaves_1010_shaded_respite_cards_test.py) protegem identidade, janelas locais, flags/branches, fallback, custo comum/especial, callback completo, helpers e limites do certificado. Podem ser executados com `PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/alexscaves_1010_shaded_respite_cards_test.py -v`.

O [auditor literal](../../../../docs/qa/alexscaves_1010_action_contract_audit.py) rejeita família/roster, hashes, ABI/âncoras e budgets inválidos ou promoção de runtime. O [workflow compartilhado](../../../../.github/workflows/alexscaves-1010-action-contracts.yml) acrescenta `shaded_respite` aos **18 perfis anteriores**, preservando suas verificações e o download único do JAR. Permanecem os limites de **256 âncoras por método**, **8.192 por manifesto** e timeout de oito minutos; nenhum budget foi ampliado.

Estado: **`STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`**, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, **`NO_MUTATION`**, oito raízes semânticas e provider integral aberto. A ficha adiciona zero raízes mágicas. Luz/veículo/clima/dimensão, mudança de nível ou stack durante uso, factories externas/null, ammo comum/especial/vazio, creative, reentrada, inserção aceita, custo aplicado, cliente/dedicado, sincronização, persistência e proteção continuam pendências físicas. Nenhum Java de runtime, Stage ou adapter mutador foi promovido.
