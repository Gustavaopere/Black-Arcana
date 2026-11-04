# Alex's Caves Continued 1.0.10 — Heavy Slam

A [ficha individual](enchantments/heavy-slam.md) conclui os sete campos do contrato estático: identidade, comportamento, parâmetros, targeting, custos, integração e validação. O certificado pertence a Heavy Slam, sem encerrar o Resistor Shield inteiro ou certificar Arrow Inducting por associação ao mesmo item.

Autoridade: JAR publisher CurseForge projeto `1645389`, arquivo `8856293`, 75.279.314 bytes; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Fonte pública adjacente `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara 1.1.1 e não fornece os parâmetros certificados da 1.0.10.

O [manifesto consolidado](EXACT-HEAVY-SLAM-CONTRACT-1.0.10.json) sela **cinco classes, nove recursos, 36 métodos e 666 âncoras**. Todos os 20 membros próprios do item estão representados; o método de uso possui seleção causal de instruções dentro do budget de 256, enquanto o hash do classfile vincula o bytecode completo à release exata. Os recursos incluem JSON do encantamento, tag do item, receita, arquivos de idioma e quatro tags de aquisição. Nenhum asset binário/JAR do provider é redistribuído.

Diferenças centrais: janela de slam10..12 intersecta a cadência5 apenas em10; primeiro dano solicitado6+3L e seguintes2F; retorno de hurt descartado antes de knockback; componente AzureX lê userX duas vezes; durabilidade1 no t10 servidor independentemente de alvos. O laço de dano não está sob a guarda cliente que cobre os visuais. São fatos estáticos, não resultados físicos de dano/knockback ou prova de duplicação no jogo.

```sh
python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile heavy_slam \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-HEAVY-SLAM-CONTRACT-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap /caminho/jdk-21/bin/javap
```

Os [testes semânticos](../../../../docs/qa/alexscaves_1010_heavy_slam_cards_test.py) protegem identidade, fórmula/cadência, alvos, aceitação/efeitos, gates de lado lógico, custo e operandos Azure. O perfil literal rejeita roster ou família trocados, evidência inválida, hashes alterados e promoção de escopo. Os outros dez perfis e seus manifestos históricos permanecem preservados.

**STATIC_TECHNICAL_CATALOG_ONLY / SHA_EXACT_BINARY_BEHAVIOR; hooks NOT_VERIFIED; QA física NOT_TESTED; NO_MUTATION; provider aberto.** Heavy Slam é 1/51 contratos estáticos de encantamento; vinte dossiers individuais anteriores permanecem parciais. O denominador observado do provider passa a 51 fichas de várias famílias, não 51 encantamentos concluídos. Mismatch dos tickets nucleares, testes físicos e Stage permanecem inalterados.
