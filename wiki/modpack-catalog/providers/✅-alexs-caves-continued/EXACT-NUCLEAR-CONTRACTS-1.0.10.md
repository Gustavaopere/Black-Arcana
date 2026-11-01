# Alex's Caves Continued 1.0.10 — Intentional Game Design e Nuke

O recorte conclui as fichas de [Intentional Game Design](damage-types/intentional-game-design.md) e [Nuke](damage-types/nuke.md) nos sete campos: identidade, comportamento, parâmetros, targeting, custos, integração e validação. São dois tipos de dano selecionados por uma flag no mesmo consumidor `NuclearExplosionEntity`, sem duas aplicações por essa bifurcação nem duas novas magias.

Autoridade: `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A fonte `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara 1.1.1 e serve somente como corroboração adjacente.

## Consumidor e fronteiras

A leitura cobre os 20 membros próprios do consumidor, incluindo construtor e inicializador estático, mais os quatro emissores e helpers delimitados. Os probes antigos contavam 19 corpos por excluir `<clinit>`; seus snapshots permanecem imutáveis. A geração de fila, o processamento de blocos, o laço de vivos, a escolha de DamageSource, a escrita de movimento e a solicitação de Irradiated conservam condições e unidades diferentes. Recusa ou ausência de `hurt` não é presumida como cancelamento dessas etapas posteriores.

Os emissores Sack of Sating, bomba, Nucleeper e fornalha fornecem parâmetros e custos próprios. A documentação não encerra toda a IA, equipamento, fornalha, sistema de blocos ou provider. As factories recebem RegistryAccess sem argumento Entity; não se inventa uma ponte de autoria para player, kills ou Mastery.

## Tickets: achado preservado, aceitação física pendente

A [prova exata NeoForge 21.1.248](EXACT-NEOFORGE-TICKETS-21.1.248.json) permanece inalterada: aquisição `add=true,ticking=true` e tentativa de remoção `add=false,ticking=false` usam categorias distintas nos caminhos selecionados. `native_release_ticket_bucket_mismatch=CONFIRMED_SELECTED_STATIC_BRANCHES_NOT_LIVE_RUNTIME`; `actual_persistent_ticket_leak=NOT_OBSERVED`. O retorno descartado pelo adapter não comprova aceitação da operação.

O novo selo acrescenta a ligação estática do registro e callback do controller. Isso não prova entrega em runtime, liberação de tickets vivos ou sucesso de reinício. O [plano físico NT-01…NT-07](../../../../docs/qa/alexscaves-1010-nuclear-ticket-physical-acceptance.md) continua NOT_TESTED. A certificação estática não declara o mismatch corrigido nem um vazamento persistente reproduzido.

O gate distingue estados pendentes de uma dupla de contratos estáticos selados. Mantém os checks de artefato, operandos, mismatch e limites físicos em ambos os ramos; exige ambos os certificados, sete eixos, hashes reais e índices com hooks/QA pendentes. Gate, manifesto, ledger e índices são revisados juntos nesta entrega.

## Reprodução e preservação

O [manifesto consolidado](EXACT-NUCLEAR-CONTRACTS-1.0.10.json) sela fichas, classes, recursos, descritores e instruções selecionadas. As provas anteriores permanecem separadas: [envelope](EXACT-NUCLEAR-ENVELOPE-1.0.10.json), [emissores](EXACT-NUCLEAR-PRODUCERS-1.0.10.json), [números](EXACT-NUCLEAR-NUMERIC-1.0.10.json), [alvos/blocos](EXACT-NUCLEAR-TARGET-WORLD-1.0.10.json), [chunks](EXACT-NUCLEAR-CHUNK-LIFECYCLE-1.0.10.json) e [NeoForge](EXACT-NEOFORGE-TICKETS-21.1.248.json). Classes externas ao provider continuam sob a prova específica do loader; não são inseridas no roster canônico deste manifesto.

```sh
python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile nuclear \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-NUCLEAR-CONTRACTS-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap /caminho/jdk-21/bin/javap
```

**STATIC_TECHNICAL_CATALOG_ONLY / SHA_EXACT_BINARY_BEHAVIOR. Hooks NOT_VERIFIED; QA física NOT_TESTED; NO_MUTATION; universo integral do provider aberto.** Tamanho, blocos, chunks, dano, status e attribution continuam sem autorização mutadora pelo catálogo. Nenhum Stage ou integração executável é promovido.
