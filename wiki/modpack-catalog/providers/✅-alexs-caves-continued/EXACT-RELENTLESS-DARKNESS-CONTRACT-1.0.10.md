# Relentless Darkness 1.0.10 — contrato técnico estático individual

A [ficha individual](enchantments/relentless-darkness.md) conclui identidade, comportamento, parâmetros, targeting, custos, integração e validação estática do encantamento. Reaproveita o [contrato Dreadbow/Dark Arrow](EXACT-DREADBOW-CONTRACTS-1.0.10.json) e as evidências de [Precise Volley](EXACT-PRECISE-VOLLEY-CONTRACT-1.0.10.json), preservando seus bytes e limites. Não conclui os outros encantamentos, factories externas ou provider integral.

Autoridade: JAR publisher CurseForge projeto `1645389`, arquivo `8856293`, 75.279.314 bytes; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A fonte adjacente `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e não substitui o artefato físico.

O [manifesto individual](EXACT-RELENTLESS-DARKNESS-CONTRACT-1.0.10.json) sela **15 classes, 22 recursos, 74 métodos e 1.380 âncoras**. Há 68 corpos selecionados completos; as seis seleções parciais são quatro janelas de registro, o gate de modo do release (`@0–20` e retorno `@899`, 11 instruções) e 26 checkpoints do renderer. `onUseTick` tem 175 instruções e `acInventoryTick` 192, integralmente ancoradas. A interface abstrata ACTickingItem tem apenas o hash, sem corpo executável a certificar. Nenhum budget foi ampliado e nenhum CFG integral de renderer/release/rede é presumido.

Distinções centrais: `remainingUseTicks % 3` governa o disparo; M=5 e incremento cliente +3 governam outra superfície. O callback emite 1/2 tentativas convertíveis com propriedade de dano 2F, usa direção do olhar e speed nominal `[4,7)`, não marca tiro perfeito e cobra custos finais por callback. Retorno de inserção, pickup, factory null, aceitação do dano e side de execução continuam fronteiras próprias.

```sh
python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile relentless_darkness \
  --jar /caminho/para/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RELENTLESS-DARKNESS-CONTRACT-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap "$JAVA_HOME/bin/javap" \
  --output /tmp/relentless-darkness-evidence.json
```

Os [testes semânticos](../../../../docs/qa/alexscaves_1010_relentless_darkness_cards_test.py) protegem modo/cadência, estado visual, quantidade/conversão, direção/dano, inserção/pickup, custos, gate inicial e limites do certificado. O perfil literal rejeita famílias/rosters, hashes, ABI/âncoras e budgets inválidos ou promoção de runtime. O workflow compartilhado acrescenta o perfil aos quinze anteriores, mantendo o mesmo download; workflows específicos já existentes continuam preservados.

Resultado: **`STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`**. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`, oito raízes semânticas e provider integral aberto. Nenhum código Java, Stage, adapter mutador ou resultado físico foi promovido.
