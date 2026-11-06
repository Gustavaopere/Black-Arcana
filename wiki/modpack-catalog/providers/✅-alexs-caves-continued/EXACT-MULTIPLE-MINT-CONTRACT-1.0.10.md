# Multiple Mint 1.0.10 — contrato técnico estático individual

A [ficha individual](enchantments/multiple-mint.md) conclui identidade, comportamento, parâmetros, targeting, custos, integração e validação estática deste encantamento. Reaproveita a [ação Peppermint Cast](actions/sugar-staff-peppermint-cast.md) e a [prova comum](EXACT-TECHNICAL-CONTRACTS-1.0.10.json), mantendo seus bytes e limites. Hex, Punting, Seekcandy, Spell Lasting, renderer e provider integral não são promovidos por associação.

Autoridade: JAR publisher CurseForge projeto `1645389`, arquivo `8856293`, 75.279.314 bytes; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Fonte adjacente `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**; não substitui o artefato físico.

O [manifesto individual](EXACT-MULTIPLE-MINT-CONTRACT-1.0.10.json) sela **7 classes, 12 recursos, 56 métodos e 1.282 âncoras**. Os cinco métodos próprios do Sugar Staff estão integralmente ancorados. Dos 28 métodos próprios de SpinningPeppermintEntity, 27 têm corpos completos e o tick contém **256 checkpoints entre 373 instruções**, sem ampliar o budget. O recorte omite a interpolação cliente `@89–225` e 38 cargas de receiver `aload_0` fora do trecho inicial completo; preserva cálculos/branches relevantes de lifespan, sobrescritas, owner/seeking, órbita, movimento reto e chamada de dano. Não constitui CFG integral nem homologação de rede/render.

Registros de encantamento/item/entidade, dimensões declaradas `0.8F×0.4F`, helper de aquisição e wrappers de custo/cooldown/dano/NBT têm seleções próprias. Hash de classe não substitui o contrato causal. As provas de Humungous Hex e demais fichas anteriores permanecem preservadas.

Distinções centrais: `3+L` determina tentativas e denominador angular; inserção tem booleano descartado; custo e cooldown são pedidos finais por callback; velocidade/raio iniciais são sobrescritos; lifespan e contador são diferentes; remoção não interrompe imediatamente o corpo do tick; seeking não é salvo; e o read do centro utiliza `(X,Z,Z)`. Nenhuma dessas evidências é apresentada como QA física ou DPS medido.

```sh
python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile multiple_mint \
  --jar /caminho/para/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-MULTIPLE-MINT-CONTRACT-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap "$JAVA_HOME/bin/javap" \
  --output /tmp/multiple-mint-evidence.json
```

Os [testes semânticos](../../../../docs/qa/alexscaves_1010_multiple_mint_cards_test.py) protegem identidade, quantidade/ângulo, guarda servidor/ramo sem sneak, inserção/custos, dimensão/AABB/dano, sobrescritas/centro capturado, lifecycle, owner e NBT. O perfil literal rejeita trocas de família/roster, selos ou âncoras inválidos, budgets excedidos e promoção de runtime. O workflow compartilhado acrescenta o perfil aos quatorze anteriores, mantendo o mesmo download; a auditoria separada de Humungous Hex não é alterada.

Resultado: **`STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`**. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`, oito raízes semânticas e provider integral aberto. Nenhum código Java, Stage, adapter mutador ou resultado físico foi promovido.
