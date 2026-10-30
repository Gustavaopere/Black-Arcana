# Alex's Caves Continued 1.0.10 — Desolate Dagger

O recorte documenta dois objetos integráveis: o [equipamento Desolate Dagger](equipment/desolate-dagger.md), que produz as entidades após o callback de ataque, e o [tipo de dano e a entidade consumidora](damage-types/desolate-dagger.md), que resolvem alvo, movimento, estado de stab e solicitação de dano. Cada ficha cobre identidade, comportamento, parâmetros, targeting, custos, integração e validação. São contratos adicionais do catálogo técnico, sem alterar o inventário histórico de raízes mágicas.

Autoridade: `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A fonte pública `523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**; permanece corroboração adjacente e não fornece os parâmetros certificados de 1.0.10.

## Fronteiras documentadas

O callback do item, as solicitações de spawn, os IDs sincronizados de alvo/jogador, o ItemStack armazenado, a duração de órbita e o avanço de stab têm consumidores distintos. A duração não é alcance, e a conclusão da animação não comprova colisão física. As fichas acompanham a ordem dos operandos, filtros e efeitos após o retorno de `hurt`, preservando o limite entre dano solicitado e dano aceito pelo motor.

O produtor nativo inspecionado não chama `setPlayerId`; o estado padrão e o fallback de autoria são documentados na ficha da entidade. Um setter existente não prova que o lançamento nativo o preencha, nem homologa um hook por jogador. A atribuição e os benefícios condicionados a Player não devem ser inferidos apenas da identidade da arma.

Registro, loot, reparação, encantamentos e os dados opcionais de combate são evidências do artefato. Uma referência ao parent externo `bettercombat:dagger` não fornece por si só alcance ou compatibilidade física com outros mods. Campos delegados ao Minecraft ou a dependências mantêm esses owners explícitos.

## Evidência e reprodução

O [manifesto selado](EXACT-DESOLATE-DAGGER-CONTRACTS-1.0.10.json) associa as duas fichas aos membros exatos do JAR, descritores JVM e instruções selecionadas. Os manifestos anteriores de [recursos](damage-types/EXACT-RESOURCE-MANIFEST-1.0.10.json), [factories](damage-types/EXACT-CONSUMERS-1.0.10.json), [janelas](damage-types/EXACT-DAMAGE-PATH-ANCHORS-1.0.10.json) e [helpers](damage-types/EXACT-DAMAGE-HELPERS-1.0.10.json) permanecem imutáveis. Suas limitações descrevem aqueles recortes, e não substituem a leitura causal das fichas consolidadas.

```sh
python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile desolate_dagger \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-DESOLATE-DAGGER-CONTRACTS-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap /caminho/jdk-21/bin/javap
```

A CI confere artefato, fichas e membros SHA-exatos, owners declarados, descriptors e âncoras. Os perfis Actions, Effects, Dreadbow e Acid mantêm seus manifestos separados. Hashes e instruções não executam o Minecraft nem validam alcance efetivo, frequência de eventos, PvP, persistência no modpack ou integração de perks.

**Certificação: `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. Hooks mutadores: `NOT_VERIFIED`; QA física: `NOT_TESTED`; universo integral do provider: aberto.** Ataques, durabilidade, spawn, dano e demais efeitos continuam sob autoridade nativa. Os índices promovem apenas os dois contratos delimitados; o catálogo dos demais equipamentos e sistemas permanece em Alex's Caves Continued.
