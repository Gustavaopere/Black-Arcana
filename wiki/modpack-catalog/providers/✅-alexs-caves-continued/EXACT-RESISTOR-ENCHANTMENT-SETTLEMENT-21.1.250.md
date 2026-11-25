# Resistor Shield — filtro de efeitos de encantamento e liquidação de durabilidade (21.1.250)

**DISCOVERY_ONLY / NO_MUTATION.** Publisher 1.0.10, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`, 75.279.314 bytes. Modlist #019/#001, NeoForge oficial 21.1.250, Java 21, Minecraft 1.21.1. Não é runtime transformado.

## Reuso delimitado

[Dossiê codecs](EXACT-RESISTOR-CODECS-21.1.250.md), [run 45478837398/job 138746190157](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45478837398/job/138746190157): 658.305 bytes, SHA-256 `1a4dc80b88f1484d3a059ddfb3782ec7c5299452c9923cf30244a27e155c645e`. ACCompat.enchantLevel consulta a lista bruta de encantamentos da stack para Heavy Slam, mas o caminho de durabilidade usa EnchantmentHelper.runIterationOnItem, CommonHooks.resolveLookup e getAllEnchantments quando lookup disponível. processDurabilityChange usa MutableFloat, handle lambda$processDurabilityChange$0, intValue final; modifyItemFilteredCount usa getEffects/itemContext/applyEffects e o efeito de valor. A [paridade distribuída](EXACT-ENGINE-248-250-PARITY.md) fixa EventHooks class SHA-256 `f810377f87c95c04bb4de7a7ac68e8f4862f9ca33a34cc74e067e65e2a92d66b` em ambas versões. Não confundir dados de encantamento raw, efetivos e admissíveis.

## Nova coleta

A sonda `docs/qa/alexscaves_1010_resistor_enchantment_settlement_250_probe.py` usa oito hashes de classfile e sete Code hashes observados, pins exatos dos quatro artefatos oficiais e publisher. Projeta os métodos efetivamente referenciados de filtro, contexto e dispatch, e candidatos delimitados de ConditionalEffect, RemoveBinomial, LevelBasedValue, builders de loot, evento de encantamento e desgaste. Nomes candidatos não afirmam presença nem API; ausências serão registradas. Procura recurso unbreaking.json somente nas distribuições examinadas, sem pressupor sua presença ou equivalência ao registry carregado. A CI exige duas saídas idênticas. Primeiro resultado pendente.

Sem nova raiz, certificado, mutação, alteração de fichas concorrentes ou QA física.
