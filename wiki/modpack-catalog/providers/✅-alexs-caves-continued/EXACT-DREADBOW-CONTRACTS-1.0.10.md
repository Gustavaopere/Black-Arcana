# Alex's Caves Continued 1.0.10 — Dreadbow e Dark Arrow

O recorte documenta dois objetos integráveis: o [equipamento Dreadbow](equipment/dreadbow.md), responsável por carga, munição, produção e parâmetros dos projéteis; e o [tipo de dano Dark Arrow e sua entidade consumidora](damage-types/dark-arrow.md), responsáveis pelos dados sincronizados, movimento próprio, filtros de impacto e solicitação de dano. Não são duas novas raízes mágicas.

Autoridade: `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A fonte pública `523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e não fornece os parâmetros certificados do artefato instalado.

## Contratos e limites

As duas fichas documentam identidade, comportamento/lifecycle, parâmetros, targeting, custos, integração e validação. A leitura acompanha operandos, condições e consumidores dos métodos relevantes; uma referência simbólica isolada não é interpretada como execução em jogo. O contador de tiro perfeito, a duração real do uso, o estado visual do item e a velocidade de voo são superfícies diferentes.

O valor passado a `setShadowArrowDamage` também é distinto da solicitação feita por `onHitEntity` e do dano final aceito pelo Minecraft. Os predicados de aliança e owner, o estado de fading e o retorno de `hurt` têm efeitos diferentes sobre essa transição. As fichas mantêm os limites da herança de `AbstractArrow`, dos hooks externos e dos dados resolvidos por datapacks; não alegam dano líquido, permissões ou número de hits medidos no modpack.

Os manifestos anteriores de [decisões](damage-types/EXACT-DREADBOW-DECISIONS-1.0.10.json), [estado sincronizado](damage-types/EXACT-DARK-ARROW-STATE-1.0.10.json), [helpers](damage-types/EXACT-DAMAGE-HELPERS-1.0.10.json), [factories](damage-types/EXACT-CONSUMERS-1.0.10.json), [janelas](damage-types/EXACT-DAMAGE-PATH-ANCHORS-1.0.10.json) e [recursos](damage-types/EXACT-RESOURCE-MANIFEST-1.0.10.json) permanecem imutáveis. Suas flags de prova parcial descrevem aqueles recortes; o novo [manifesto de contratos](EXACT-DREADBOW-CONTRACTS-1.0.10.json) sela as fichas consolidadas e as evidências adicionais.

## Reprodução

```sh
python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile dreadbow \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-DREADBOW-CONTRACTS-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap /caminho/jdk-21/bin/javap
```

O perfil aceita exatamente essas duas fichas e confere hashes do JAR, fichas e membros, owners declarados, descritores JVM e instruções selecionadas por offset. Os perfis `actions` e `effects` mantêm seus manifestos separados. A CI exporta apenas relatórios JSON delimitados.

**Certificação: `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. Hooks mutadores: `NOT_VERIFIED`; QA física: `NOT_TESTED`; universo integral do provider: aberto.** Os índices só promovem o recorte individual documentado. Armas restantes, armaduras, enchantments e outros sistemas ainda precisam de fichas ou disposição explícita; a fila alfabética permanece em Alex's Caves Continued.
