# Alex's Caves Continued 1.0.10 — contrato estático do Forsaken Sonic Boom

O recorte conclui a [ficha existente de Forsaken Sonic Boom](damage-types/forsaken-sonic-boom.md), sem acrescentar uma nova magia ao inventário histórico. A ficha relaciona identidade, comportamento, parâmetros, targeting, custos, fronteiras de integração e validação. O contrato é do ataque e de seus consumidores delimitados; não encerra todo o mob, seus sistemas ou o provider.

Autoridade: `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**; serve apenas como corroboração adjacente, sem fornecer os parâmetros certificados da versão instalada.

## Fluxo e fronteiras documentadas

A seleção inicial, a tentativa de dano direcionado, a varredura em área e o processamento de cada vítima são etapas distintas. A caixa de consulta não define um raio esférico, o alvo principal não equivale à vítima iterada e a duração declarada da animação não garante frequência ou quantidade de hits. Os parâmetros de dano são argumentos solicitados ao mecanismo nativo, sujeitos aos consumidores herdados e às alterações do pack.

A ficha acompanha aquisição e início/encerramento do goal, contador de tentativa, escolha de animação, carga Sonic, filtros, valores-base, multiplicação do caminho em área, knockback e custos nativos. O produtor da carga que reconhece `minecraft:sonic_boom` permanece distinto da factory do tipo `alexscaves:forsaken_sonic_boom`. Eventos de animação, sincronização e dados finais de tags conservam seus owners e limites explícitos.

O registro de dimensões e tracking não substitui geometria de dano. O caminho separado de destruição de blocos pela IA não se transforma em um efeito do Sonic. A documentação não concede ao Black Arcana autoridade sobre a IA, o dano ou a proteção de mundo de terceiros.

## Evidência reproduzível

O [manifesto consolidado](EXACT-FORSAKEN-CONTRACT-1.0.10.json) sela a ficha, as classes, os recursos, os descritores JVM e as instruções selecionadas. Os cinco manifestos parciais anteriores permanecem imutáveis: [ataques](damage-types/EXACT-FORSAKEN-SONIC-1.0.10.json), [helpers](damage-types/EXACT-FORSAKEN-HELPERS-1.0.10.json), [lifecycle](damage-types/EXACT-FORSAKEN-LIFECYCLE-1.0.10.json), [temporização](damage-types/EXACT-FORSAKEN-TIMING-1.0.10.json) e [targeting](damage-types/EXACT-FORSAKEN-TARGETING-1.0.10.json). Seus limites descrevem aqueles recortes históricos e não promovem hooks ou QA.

```sh
python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile forsaken \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-FORSAKEN-CONTRACT-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap /caminho/jdk-21/bin/javap
```

A CI compara o artefato exato, os hashes das fichas e dos membros e as âncoras JVM. Os cinco perfis anteriores preservam manifestos separados. Essas verificações não executam o modpack completo nem demonstram resultados físicos de targeting, permissões, hits, animação ou multiplayer.

**Certificação: `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. Hooks mutadores: `NOT_VERIFIED`; QA física: `NOT_TESTED`; política desta entrega: `NO_MUTATION`; universo integral do provider: aberto.** O índice promove apenas uma ficha delimitada. Não promove Stage, integração executável ou fechamento alfabético do provider.
