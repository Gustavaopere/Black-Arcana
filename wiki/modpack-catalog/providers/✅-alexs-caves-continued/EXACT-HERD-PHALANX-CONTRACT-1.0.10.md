# Alex's Caves Continued 1.0.10 — Herd Phalanx

A [ficha individual](enchantments/herd-phalanx.md) conclui os sete campos do contrato estático: identidade, comportamento, parâmetros, targeting, custos, integração e validação. O certificado é do encantamento Herd Phalanx e da cadeia defensiva Grottoceratops delimitada; não encerra a Extinction Spear ou os outros tipos de espírito.

Autoridade: JAR publisher CurseForge projeto `1645389`, arquivo `8856293`, 75.279.314 bytes; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A fonte pública adjacente `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara 1.1.1 e não fornece os parâmetros certificados da build instalada.

O [manifesto individual](EXACT-HERD-PHALANX-CONTRACT-1.0.10.json) sela **15 classes, nove recursos, 91 métodos e 1.526 âncoras**. Reaproveita classes/métodos selecionados do [contrato Spirit Dinosaur](EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json), preservando esse manifesto byte a byte; acrescenta idiomas e tags de aquisição do encantamento. Exclui a entidade da lança, factories Spirit Dinosaur/Tephra e corpos dos subtipos ofensivos do novo roster. Métodos de contexto do item/registro não promovem os objetos relacionados a certificados novos.

Diferenças centrais: 3+L tentativas, inclusive três no nível zero; igualdade inicial do callback sem token idempotente; retorno de inserção descartado; órbita visual diferente da AABB30 de seleção; comparador assimétrico de proximidade; head fading excluída antes do descarte; adapter NeoForge Pre solicita dano zero, sem provar cancelamento de todos os efeitos. Não se alegam defeitos ou sucessos físicos a partir desses fatos estáticos.

```sh
python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile herd_phalanx \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-HERD-PHALANX-CONTRACT-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap /caminho/jdk-21/bin/javap
```

Os [testes semânticos](../../../../docs/qa/alexscaves_1010_herd_phalanx_cards_test.py) protegem a identidade, criação/cadência de ingresso, resultado ignorado, seleção/UUID, órbita, evento Pre e estados independentes. Regressões do perfil rejeitam roster/família trocados, hashes/âncoras alterados, evidência inválida e promoção indevida de escopo. O mesmo download do JAR serve aos doze perfis, mantendo os budgets anteriores.

**STATIC_TECHNICAL_CATALOG_ONLY / SHA_EXACT_BINARY_BEHAVIOR; hooks NOT_VERIFIED; QA física NOT_TESTED; NO_MUTATION; provider aberto.** São dois contratos estáticos entre 51 recursos conhecidos de encantamento, com vinte dossiers anteriores ainda parciais e 22 dossiers individuais existentes. Nenhum Stage, fix de ticket nuclear ou integração mutadora é promovido.
