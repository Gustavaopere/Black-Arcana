# Lasting Morale 1.0.10 — contrato técnico estático individual

A [ficha individual](enchantments/lasting-morale.md) conclui identidade, comportamento, parâmetros, targeting, custos, integração e validação estática deste encantamento. Reaproveita o [contrato Magic Conch](EXACT-TECHNICAL-CONTRACTS-1.0.10.json) e o [recorte Charting Call](EXACT-CHARTING-CALL-1.0.10.json) como pontos de partida, preservando seus bytes e limites. Não conclui os outros encantamentos, ataques das entidades ou o provider integral.

Autoridade: JAR publisher CurseForge projeto `1645389`, arquivo `8856293`, 75.279.314 bytes; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Fonte pública adjacente `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**; não substitui os parâmetros da build física.

O [manifesto individual](EXACT-LASTING-MORALE-CONTRACT-1.0.10.json) sela **5 classes, 11 recursos, 45 métodos e 1121 âncoras**. Os nove métodos próprios do Conch estão integralmente ancorados. No tick extenso de DeepOneBaseEntity, o recorte `@0–340` mais o retorno `@783` mantém 164 checkpoints; os trechos posteriores não são apresentados como CFG completo. Registros, helpers, defaults, acesso ao contador, UUID, persistência, aliança e AI têm seus consumidores próprios. Os budgets do auditor permanecem inalterados; hashes de classe não substituem evidência causal.

Distinções centrais: leitura do nível depois do custo; mesma variável `1200+400L` fornecida aos três grupos e ao cooldown por Item; retorno não nulo após `addFreshEntity` cujo booleano é descartado; remoção `DISCARDED` condicionada ao fade; e NBT de UUID/tempo condicionado à existência de owner. Duração de combate, autoria de kills e aceitação de spawn não são presumidas a partir desses parâmetros.

```sh
python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile lasting_morale \
  --jar /caminho/para/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-LASTING-MORALE-CONTRACT-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap "$JAVA_HOME/bin/javap" \
  --output /tmp/lasting-morale-evidence.json
```

Os [testes semânticos](../../../../docs/qa/alexscaves_1010_lasting_morale_cards_test.py) protegem carga/custo/side guard, fórmula e variável compartilhada, resultado de inserção, progresso/remoção, condições de NBT e filtros direcionais de alvo. O perfil literal rejeita trocas de família/roster, selos/âncoras inválidos, limites excedidos e promoção de runtime. O workflow comum acrescenta o novo perfil aos treze anteriores, com o mesmo download do JAR. A auditoria separada de Humungous Hex permanece preservada.

Resultado: **`STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`**. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`, oito raízes semânticas e provider integral aberto. Nenhuma implementação Java, Stage, hook mutador ou QA física foi promovida.
