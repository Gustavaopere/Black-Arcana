# Alex's Caves Continued 1.0.10 — Shot Gum e Gumball

O recorte conclui dois objetos técnicos: o [equipamento Shot Gum](equipment/shot-gum.md) e o [projétil/tipo de dano Gumball](damage-types/gumball.md). Cada ficha cobre identidade, comportamento, parâmetros, targeting, custos, fronteiras de integração e validação. Os emissores Gumbeeper e os descendentes da divisão entram como consumidores de apoio; não recebem uma certificação do mob inteiro ou uma nova raiz mágica.

Autoridade: `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**; serve apenas como corroboração e não fornece os parâmetros certificados de 1.0.10.

## Consumidores e parâmetros relacionados

O equipamento, o projétil e o mob emissor mantêm caminhos próprios de munição, estado, dano e movimento. O contrato acompanha as fórmulas e os limites empacotados de quatro encantamentos, sem transportar automaticamente valores da arma para todos os Gumballs. O número de solicitações de spawn não comprova quantidade de entidades inseridas, hits ou aplicação de perks.

A origem primária e a fábrica dos descendentes têm contratos distintos de autoria. Uma referência a `createEntity` ou um setter público não estabelece uma ponte segura para dano, kills ou Mastery. A lista de entidades anteriores usada pelo homing não deve ser reinterpretada como um mecanismo de deduplicação de dano.

O impacto que usa `causeGumballDamage` permanece separado do caminho que solicita `Level.explode`. O modo de interação da explosão, as tags de dano e os filtros locais não homologam permissões de mundo, PvP ou integração com a `WorldEffectPolicy` do Black Arcana. Os parâmetros solicitados permanecem sob os owners nativos.

O mixin de tick e a interface de atualização são evidências de ativação da arma. As cópias e gravações de dados do ItemStack, a capacidade de receber tags e os canais de rede mantêm seus limites explícitos; implementar uma interface não prova que a arma emita automaticamente um pacote.

## Evidência e reprodução

O [manifesto consolidado](EXACT-GUMBALL-CONTRACTS-1.0.10.json) sela as duas fichas e seus membros do JAR, descritores JVM e instruções selecionadas. O suporte compartilhado de registro, recursos, encantamentos e emissores relaciona o equipamento e a entidade, mantendo os limites de cada ficha.

Os quatro manifestos parciais anteriores permanecem imutáveis: [impacto](EXACT-GUMBALL-IMPACT-1.0.10.json), [produtores](EXACT-GUMBALL-PRODUCERS-1.0.10.json), [estado](EXACT-GUMBALL-STATE-1.0.10.json) e [divisão/encantamentos](EXACT-GUMBALL-SPLIT-ENCHANT-1.0.10.json). Os recortes gerais de [recursos](damage-types/EXACT-RESOURCE-MANIFEST-1.0.10.json) e [factory/callers](damage-types/EXACT-CONSUMERS-1.0.10.json) também são preservados. Suas flags históricas não homologam hooks ou QA física.

```sh
python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile gumball \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-GUMBALL-CONTRACTS-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap /caminho/jdk-21/bin/javap
```

A CI confere o artefato, os hashes das fichas e dos membros e as âncoras do perfil. Os seis perfis anteriores preservam suas provas. Essas verificações não executam o modpack completo, o scheduler herdado, o transporte físico ou as políticas finais de outros mods.

**Certificação: `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. Hooks mutadores: `NOT_VERIFIED`; QA física: `NOT_TESTED`; política: `NO_MUTATION`; universo integral do provider: aberto.** Os índices promovem somente os dois contratos delimitados, sem promover Stage, integração executável ou conclusão alfabética do provider.
