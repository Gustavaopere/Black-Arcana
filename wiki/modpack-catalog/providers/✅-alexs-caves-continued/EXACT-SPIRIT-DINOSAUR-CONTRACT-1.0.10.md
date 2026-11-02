# Alex's Caves Continued 1.0.10 — Spirit Dinosaur

A [ficha existente](damage-types/spirit-dinosaur.md) conclui os sete campos do contrato técnico estático: identidade, comportamento, parâmetros, targeting, custos, integração e validação. Dois consumidores diretos compartilham o DamageType; três modos de espírito preservam funções distintas. Não se acrescentam novas magias nem uma ficha para cada variante.

Autoridade: `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A fonte `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara 1.1.1 e serve apenas como orientação adjacente.

## Consumidores e emissores delimitados

O [manifesto consolidado](EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json) sela **19 classes, 12 recursos, 127 métodos e 2.493 âncoras**. Todos os membros próprios de DinosaurSpiritEntity (32), seu enum (5), ExtinctionSpearEntity (18), ExtinctionSpearItem (9) e SpearItem (12) têm todas as instruções do parser seladas. Inicializadores estáticos antes excluídos da contagem ABI não são membros novos da release.

O suporte selecionado fixa factory, helpers, registros, dados de encantamento/receita e o consumidor defensivo indireto Grotto. O levantamento de símbolos compilados localiza os três criadores diretos nas duas classes de item/lança; não exclui reflexão, outros mods ou criação indireta em runtime. A serialização UUID é um delegate nativo, sem promessa de entrega ou autorização de rede.

## Diferenças causais que uma perk precisa preservar

- Tremorsaurus solicita `(float)(3+2×nível)` e só marca dealtDamage depois de true; fading não impede novas tentativas recusadas enquanto a entidade continua sendo processada.
- A lança solicita `10+damageBonus` para vítima LivingEntity, define dealtDamage e solicita fogo antes de hurt. Enderman aceito retorna antes de efeitos posteriores/spawn; recusa ainda alcança a cauda de movimento/som.
- Subterranodon move o alvo; Grottoceratops orbita e pode ser consumido por um handler NeoForge Pre que solicita dano zero. Nenhum deles chama diretamente a factory deste DamageType em seu corpo.
- O ramo de bloco da lança chama TephraExplosion com raio 1.5 e KEEP; seu DamageSource é uma explosão nativa distinta. O selo não encerra todos os internals de blocos/exposição desse sistema adjacente.
- UUID de Player, ID volátil do alvo, dados não persistidos e clamp inclusivo do enum permanecem limites explícitos. O caminho estático de índice inválido não é um crash reproduzido no modpack.

## Reprodução e preservação

O [snapshot parcial anterior](EXACT-SPIRIT-DINOSAUR-1.0.10.json), os [recursos](damage-types/EXACT-RESOURCE-MANIFEST-1.0.10.json) e os [consumidores diretos](damage-types/EXACT-CONSUMERS-1.0.10.json) permanecem imutáveis. A certificação consolidada não reescreve seus limites históricos. Os [testes semânticos](../../../../docs/qa/alexscaves_1010_spirit_dinosaur_cards_test.py) verificam as ordens de flags/dano, produtores/custos, fronteira de explosão e consistência do inventário com o ledger.

```sh
python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile spirit_dinosaur \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap /caminho/jdk-21/bin/javap
```

**STATIC_TECHNICAL_CATALOG_ONLY / SHA_EXACT_BINARY_BEHAVIOR. Hooks NOT_VERIFIED; QA física NOT_TESTED; NO_MUTATION; universo integral do provider aberto.** Os índices refletem 9/11 contratos de dano e 28/30 fichas observadas. Raygun e Tremorzilla Beam permanecem parciais; nenhuma certificação de Stage, runtime, proteção física ou provider integral é promovida.
