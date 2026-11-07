# Sated Blade 1.0.10 — contrato técnico estático individual

A [ficha individual](enchantments/sated-blade.md) conclui identidade, comportamento, parâmetros, targeting, custos, integração e validação estática deste encantamento. Reaproveita as provas de [Desolate Dagger](EXACT-DESOLATE-DAGGER-CONTRACTS-1.0.10.json) e [Impending Stab](EXACT-IMPENDING-STAB-CONTRACT-1.0.10.json), preservando seus bytes e escopos. Não conclui outros encantamentos, combate integrado ou provider integral.

Autoridade: JAR publisher CurseForge projeto `1645389`, arquivo `8856293`, 75.279.314 bytes; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A fonte adjacente `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**, não substituindo o artefato físico.

O [manifesto individual](EXACT-SATED-BLADE-CONTRACT-1.0.10.json) sela **11 classes, 22 recursos, 42 métodos e 768 âncoras**. Conserva todas as 759 âncoras anteriores e acrescenta nove pivôs do tick: `365,375,377,395,397,411,416,424,434`. O trecho Sated `@365–435` tem suas 32 instruções completas, enquanto o tick inteiro permanece delimitado: **254 de 361 instruções**, dentro do mesmo limite de 256. A sequência anterior de fonte/hurt/som também continua com checkpoints; não se declara todo o trecho `@293–435` ou o CFG integral completo.

Dos 42 métodos selecionados, 36 têm corpos completos. As seis seleções parciais são o renderer, quatro inicializadores de registro e o tick da entidade. Registro literal, chave, JSON, tag, idiomas e aquisição foram reexaminados no mesmo JAR. Nenhum budget foi ampliado; hash de classe não substitui evidência causal.

Distinções centrais: benefício depende de hurt aceito, nível positivo, fonte resolvida como Player e saturação anterior menor que 5. O pedido é saturação atual + `0.1F×L`, sem clamp próprio a 5; não é heal/food-level. O produtor não preenche PLAYER_ID, a stack é relida tarde, o descarte não depende do benefício e os campos próprios não têm NBT. Nenhum desses fatos foi promovido a resultado físico ou hook suportado.

```sh
python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile sated_blade \
  --jar /caminho/para/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-SATED-BLADE-CONTRACT-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap "$JAVA_HOME/bin/javap" \
  --output /tmp/sated-blade-evidence.json
```

Os [testes semânticos](../../../../docs/qa/alexscaves_1010_sated_blade_cards_test.py) protegem identidade, completude local, gates, pré-condição versus soma, fonte/fallback, ausência de binding no produtor, servidor/descarte e NBT. O perfil literal rejeita famílias/rosters, hashes/ABI/âncoras e budgets inválidos ou promoção de runtime. O workflow compartilhado acrescenta o perfil aos dezesseis anteriores, mantendo o mesmo download e limites.

Resultado: **`STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`**. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`, oito raízes semânticas e provider integral aberto. Nenhum código Java, Stage, adapter mutador ou resultado físico foi promovido.
