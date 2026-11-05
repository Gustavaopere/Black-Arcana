# Alex's Caves Continued 1.0.10 — Impending Stab

A [ficha individual](enchantments/impending-stab.md) fecha identidade, comportamento, parâmetros, targeting, custos, integração e validação do encantamento. Reaproveita os consumidores já certificados de [Desolate Dagger](EXACT-DESOLATE-DAGGER-CONTRACTS-1.0.10.json), sem alterar as duas fichas anteriores ou promover o equipamento inteiro, Double Stab ou Sated Blade como encantamentos concluídos.

Autoridade: JAR publisher CurseForge projeto `1645389`, arquivo `8856293`, 75.279.314 bytes; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Fonte pública adjacente `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara 1.1.1 e não substitui os parâmetros da build física.

O [manifesto individual](EXACT-IMPENDING-STAB-CONTRACT-1.0.10.json) sela **11 classes, 22 recursos, 42 métodos e 759 âncoras**. Os vinte métodos próprios da entidade e seis do item estão representados; o tick longo mantém checkpoints causais dentro do budget existente. São copiados os selos de classes/recursos do contrato anterior, com idiomas/tags de aquisição adicionais, e tudo é reexaminado no mesmo JAR exato. O selo histórico permanece byte a byte preservado.

Distinções centrais: cache inicial positivo escolhe 40–49 em vez de 20–29; o dano relê a stack no stab e calcula `2+2L`; o loop Double Stab relê seu nível por comparação; o produtor não copia a stack nem atribui PLAYER_ID; hurt recusado ainda conduz à solicitação de descarte. O recurso declara exclusividade com Double Stab, mas os corpos Java não a revalidam. Nenhum resultado físico de dano, autoria ou compatibilidade é presumido.

```sh
python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile impending_stab \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-IMPENDING-STAB-CONTRACT-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap /caminho/jdk-21/bin/javap
```

Os [testes semânticos](../../../../docs/qa/alexscaves_1010_impending_stab_cards_test.py) protegem as duas leituras temporais, faixa de espera sem crescimento por nível, dano/factory/descarte, stack/IDs e NBT próprio vazio. O perfil literal rejeita família/roster trocados, hashes ou âncoras alterados, evidência inválida e promoção indevida de escopo. O workflow comum acrescenta o novo perfil aos doze anteriores, usando o mesmo download e os mesmos budgets. A auditoria separada de Humungous Hex continua preservada.

**STATIC_TECHNICAL_CATALOG_ONLY / SHA_EXACT_BINARY_BEHAVIOR; hooks NOT_VERIFIED; QA física NOT_TESTED; NO_MUTATION; provider aberto.** São quatro contratos estáticos entre 51 recursos conhecidos de encantamento; vinte dossiers anteriores permanecem parciais e 24 dossiers individuais existem. Nenhum Stage, fix de ticket nuclear ou integração mutadora é promovido.
