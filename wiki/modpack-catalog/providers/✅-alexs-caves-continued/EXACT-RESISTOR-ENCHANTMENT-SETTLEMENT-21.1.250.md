# Resistor Shield — filtro de efeitos de encantamento e liquidação de durabilidade (21.1.250)

**DISCOVERY_ONLY / NO_MUTATION.** Publisher 1.0.10, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`, 75.279.314 bytes. Modlist #019/#001, NeoForge oficial 21.1.250, Java 21, Minecraft 1.21.1. Não é runtime transformado.

## Reuso delimitado

[Dossiê codecs](EXACT-RESISTOR-CODECS-21.1.250.md), [run 45478837398/job 138746190157](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45478837398/job/138746190157): 658.305 bytes, SHA-256 `1a4dc80b88f1484d3a059ddfb3782ec7c5299452c9923cf30244a27e155c645e`. ACCompat.enchantLevel consulta a lista bruta de encantamentos da stack para Heavy Slam, mas o caminho de durabilidade usa EnchantmentHelper.runIterationOnItem, CommonHooks.resolveLookup e getAllEnchantments quando lookup disponível. processDurabilityChange usa MutableFloat, handle lambda$processDurabilityChange$0, intValue final; modifyItemFilteredCount usa getEffects/itemContext/applyEffects e o efeito de valor. A [paridade distribuída](EXACT-ENGINE-248-250-PARITY.md) fixa EventHooks class SHA-256 `f810377f87c95c04bb4de7a7ac68e8f4862f9ca33a34cc74e067e65e2a92d66b` em ambas versões. Não confundir dados de encantamento raw, efetivos e admissíveis.

## Nova coleta

A sonda `docs/qa/alexscaves_1010_resistor_enchantment_settlement_250_probe.py` usa oito hashes de classfile e sete Code hashes observados, pins exatos dos quatro artefatos oficiais e publisher. Projeta os métodos efetivamente referenciados de filtro, contexto e dispatch, e candidatos delimitados de ConditionalEffect, RemoveBinomial, LevelBasedValue, builders de loot, evento de encantamento e desgaste. Nomes candidatos não afirmam presença nem API; ausências serão registradas. Procura recurso unbreaking.json somente nas distribuições examinadas, sem pressupor sua presença ou equivalência ao registry carregado. A CI exige duas saídas idênticas. Primeiro resultado reproduzido abaixo.

Sem nova raiz, certificado, mutação, alteração de fichas concorrentes ou QA física.

## Resultado reproduzido

[Run 45528205575, job 138916697852](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45528205575/job/138916697852), HEAD `38ced08c51c3edcfe84671cb93070198e8fe1136`: cinco verificações, duas saídas byte-idênticas, **337.346 bytes**, SHA-256 `366175b90c9e16b9093454c5da5a996af07b9b33b3ecd4482db74e38b529090c`. 17 owners presentes, 51 declarações distintas (50 Code, uma abstrata); LootItemCondition presente sem corpo selecionado. GetEnchantmentLevelEvent$EnchantmentLevel, candidato da seleção, ausente. Ausência de `data/minecraft/enchantment/unbreaking.json` nos arquivos pesquisados não demonstra ausência no registry carregado; nenhum valor de probabilidade de Unbreaking foi atribuído ao escudo. Replay na HEAD final obrigatório.

| Método / Code SHA-256 | Contrato estático observado |
|---|---|
| ACCompat.enchantLevel / `7bfacebb8312d2d52f34a61ed657b575e62cb2cc9155b6b8f33a63bbd571e940` | ItemStack.getEnchantments @1, Holder.is @42, nível correspondente ou 0. |
| ItemStack.getEnchantments / `1bdcf0941ca353fb52143f02833aacff0d846a9092bb0c9639643dbbaacbbfab` | ENCHANTMENTS ou EMPTY; getTagEnchantments delega. Heavy Slam não consulta evento de nível efetivo nesse caminho. |
| EventHooks.getEnchantmentLevelSpecific / `c67d3683fc9d1cf603d62ec30e3ed861d250ee1f0ade4f4dac910c1d11447137` | Holder.unwrapLookup @1; sem lookup, retorna nível original; com lookup, Mutable, evento específico @46, post @56, getLevel @65. |
| EventHooks.getAllEnchantmentLevels / `a020597332d1a562dbaa124c15ab692454db4fc37d2ab269fe903aebc79de80c` | Copia conjunto em Mutable @5; evento @17, post @27, toImmutable @34; não grava componente da stack nesses corpos. |
| GetEnchantmentLevelEvent.getEnchantments / `d0cf9f922ab010f8c80625ee6685ff3cb0a085a2217bde1a5d580997c5014bcb` | Retorna campo Mutable. Não prova listener instalado ou autorização de Black Arcana. |
| EnchantmentHelper.lambda$processDurabilityChange$0 / `a169532c6ca9127aa164463941239eee0d8304f8d781b8e9300568ecde0768c9` | Holder.value e modifyDurabilityChange @14. |
| Enchantment.getEffects / `2c296bd6347539c84cff062e5f7eb04944c4fc701aabc0724e8143348283c037` | Component map getOrDefault com lista vazia @8. |
| Enchantment.itemContext / `5b1a6f56d581fe1507e28426825d2496982f33b13f3a6cfb2ff5b2da5591c6ad` | TOOL=stack, ENCHANTMENT_LEVEL, ENCHANTED_ITEM paramset e Optional.empty na criação de LootContext. Não há argumento Player neste corpo. |
| Enchantment.applyEffects / `3cad78a362c0c545f0f117159e58ca9b9559c2ef61a19de7249db852cc8e16e4` | Itera lista; matches @30, guarda @33; efeito aceito pelo filtro passa ao consumer @42. |
| ConditionalEffect.matches / `6e8faa68c1252179071f68595e530f0e8b137573a2f225132db7c1c14d1f419e` | requirements ausente implica true; se presente, predicate.test(context). |
| LevelBasedValue$Constant.calculate / `12430ca46cff070647d25b61db34e6a7b04ed9bc22ef98aa827acc34c2c799cb` | Retorna valor constante. |
| LevelBasedValue$Linear.calculate / `9aac6b452c131ac541a9e4bad525dad6ad7875ab1ac11d7e5442b2276e9eb679` | base + perLevelAboveFirst × (level − 1). |
| RemoveBinomial.process / `be66dad3386c45aea502d0b5dbebdcc2d1d55fe3053f95f3a59147f0f810c31d` | Calcula p por nível, para índice i enquanto float(i)<entrada, incrementa removidos se nextFloat()<p, retorna entrada−removidos; sem clamp local. |

A composição do desgaste segue efeitos condicionais em sequência, cada process recebe nível, RandomSource do ServerLevel e o valor anterior do MutableFloat. O valor final é convertido por intValue no helper. Para uma entrada inteira não negativa pequena D, p em [0,1] e um único RemoveBinomial com sorteios uniformes independentes, a esperança matemática condicional é D(1−p), variância Dp(1−p). Isso descreve o operador isolado, não a receita efetiva de Unbreaking nem o desgaste real do Resistor Shield. Entradas fracionárias, outras transformações, ordem de efeitos, registries/datapacks, hooks, guarda de criatividade, damageItem e conversão final impedem uma previsão universal. Não se deve usar esse modelo como orçamento de durabilidade ou reaplicar dano.

**Limite:** permanece descoberta estática delimitada, sem certificação do item, do registry efetivo, do uso transformado ou do hook. NO_MUTATION.
