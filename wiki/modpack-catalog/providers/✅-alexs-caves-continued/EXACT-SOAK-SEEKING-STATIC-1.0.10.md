# Soak Seeking — prova reproduzível SHA-exata do JAR 1.0.10

Escopo: **somente contrato estático individual** `alexscaves:soak_seeking`; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`.

O publisher `alexscaves-1.0.10-neoforge+1.21.1.jar` possui SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` e SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. O recurso Soak Seeking 362 bytes (SHA-256 `cfec967d084e9dc3870b90bc05d62375524af447ae280aa7fea63458e644b66b`) declara max level III, weight 10, anvil cost 1 e `mainhand`.

## Observações e rastreabilidade

- `SOAK_SEEKING` aparece em **2 das 1.555 classes** na busca de símbolo direto: `ACEnchantmentRegistry` e `SeaStaffItem`.
- `SeaStaffItem.use`: **189** instruções, 18 âncoras da prova anterior conferidas; `@63–72` lê o nível; `@314–324` fixa `seekAmount = 0.3F + 0.2F×L` em cada Water Bolt e `@327–348` solicita destino UUID/spawn.
- `WaterBoltEntity.tick`: **362** instruções, 11 âncoras verificadas; `@19–89` limita a correção por alvo, tick, `dieIn` e distância; `@92–155` mistura o vetor atual com a direção do alvo.
- `WaterBoltEntity.onRicochetHit`: **122** instruções, 7 âncoras; o filho tem default `0.3F` e não herda o campo numérico.
- `WaterBoltEntity.damageMobs`: **105** instruções, 7 âncoras; solicita 3F de dano com filtros e AABB base; não há multiplicador de dano de Soak Seeking nesse trecho.
- A interpretação numérica dos testes `(double)seekAmount > 0.3D` requer distinguir `0.3F` (float) do literal double `0.3D`. Mesmo `L=0` pode passar essa comparação.

## Selos

- [Manifesto individual SHA-exato](EXACT-SOAK-SEEKING-STATIC-1.0.10.json), incluindo JSON, locales, digest dos quatro métodos e janelas JVM.
- [Sonda Python read-only](../../../../docs/qa/alexscaves_1010_soak_seeking_static_probe.py) e [10 testes](../../../../docs/qa/alexscaves_1010_soak_seeking_static_probe_test.py).
- [Workflow de comparação](../../../../.github/workflows/alexscaves-1010-soak-seeking-static.yml).
- [Ficha individual](enchantments/soak-seeking.md) com efeitos, custos, autoria, targeting, persistência, segurança e matriz de perks.

O selo não comprova aceitação efetiva da entidade/impacto, QA em multiplayer, comportamento de terceiros, datapacks ativos ou permissões de alteração dos internals do provider. **Nenhum adapter mutador foi criado.**
