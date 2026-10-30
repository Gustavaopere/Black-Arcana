# Alex's Caves Continued 1.0.10 — contrato estático de Acid

A [ficha Acid](damage-types/acid.md) reúne o tipo de dano já inventariado e seus dois emissores diretos nativos: `AcidBlock.entityInside` e `ThrownWasteDrumEntity.tick`. Ela documenta identidade, comportamento, parâmetros, targeting, custos, integração e validação. Não acrescenta um spell ou outra raiz mágica.

Autoridade: `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A fonte pública `523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e permanece apenas corroboração adjacente. Os parâmetros certificados vêm do JAR 1.0.10.

## Fronteiras dos dois emissores

O contato ambiental combina altura de fluido, tags de entidade, desgaste de armadura, quantidade de peças Hazmat, chance e magnitude de dano. O contato do drum possui seleção e magnitude próprias. Compartilhar `DamageType` não torna esses filtros equivalentes nem comprova imunidade universal. Os auxiliares de altura e equipamento são documentados no alcance necessário para esses consumidores.

A ficha também acompanha movimento, contador de chão, colocação e limpeza de fluido temporário, NBT e o recorte de lançamento pelo Brainiac. Ela distingue dimensões registradas, AABB consultada, movimento e posição de colocação; nenhum desses valores é tratado automaticamente como alcance esférico de um feitiço. Corrosão de blocos, sistema integral de fluidos, equipamento Hazmat completo e toda a AI do Brainiac continuam escopos próprios do provider.

## Evidência e reprodução

O [manifesto do contrato](EXACT-ACID-CONTRACT-1.0.10.json) sela a ficha, classes e recursos, descritores JVM e instruções selecionadas por offset. Os [recursos](damage-types/EXACT-RESOURCE-MANIFEST-1.0.10.json) e o [inventário anterior de factories/callers](damage-types/EXACT-CONSUMERS-1.0.10.json) continuam imutáveis. O novo contrato acrescenta análise dos operandos e caminhos relevantes, sem reinterpretar uma referência simbólica isolada como execução física.

```sh
python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile acid \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-ACID-CONTRACT-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap /caminho/jdk-21/bin/javap
```

A CI verifica artefato e membros SHA-exatos, ficha selada, owner declarado, descriptors e âncoras. Os perfis Actions, Effects e Dreadbow mantêm seus manifestos separados. A interpretação causal acompanha a revisão técnica: hashes e âncoras não executam o Minecraft nem medem DPS, frequência de contato, permissões ou cleanup no modpack.

**Certificação: `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. Hooks mutadores: `NOT_VERIFIED`; QA física: `NOT_TESTED`; universo integral do provider: aberto.** Dano, desgaste, criação de entidade e alterações de mundo permanecem sob autoridade nativa. A certificação não autoriza repetir settlement nem transformar um getter ou campo em hook por jogador.

O [índice dos tipos de dano](damage-types/INDEX.md), o [índice do provider](INDEX.md) e o [índice global](../INDEX.md) mantêm os estados separados. A fila alfabética permanece em Alex's Caves Continued até a conclusão dos demais contratos de equipamentos, dano e sistemas integráveis.
