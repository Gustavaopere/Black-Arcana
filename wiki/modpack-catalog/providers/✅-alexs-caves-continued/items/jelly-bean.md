# Jelly Bean

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`; provider OPEN. Não representa nova raiz mágica ou cast certificado.

**Autoridade:** Alex's Caves Continued (`alexscaves`) 1.0.10; Minecraft 1.21.1 / NeoForge 21.1.250 documental / Java 21. Modlist física sibling #019; publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`. Não houve comparação nova com dump físico instalado nem observação do runtime transformado. [Dossiê de descoberta SHA-exata](../EXACT-JELLY-KEYBIND-LIMESTONE-1.0.10.md) e [replay](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45651673635/job/139337522318): 186.937 bytes, SHA-256 `61a6010adbe0c6f41968a6ffc8f85e8c4c6e013175007f6be93280d3cf2da0ed`, duas saídas byte-idênticas, seis checks. O dossiê detalha consumidores, hashes de métodos e offsets. Replay da HEAD consolidada obrigatório.

## Identidade e descrição funcional

`alexscaves:jelly_bean`, factory `ACItemRegistry.lambda$static$198`, Code SHA `546da6af37d6cc4834693c322a2cd13c1852123744a3bd55006b0bee3fd5ed63`; [registro](../systems/item-registry.md). Owner `JellyBeanItem` (SHA-256 `9842c28cd2eff05621a23be37ce5917ca88a19bf0bd99f0da9b5a5cc62a4355f`), estende PotionItem; nove corpos próprios. É um consumível com efeitos provenientes da stack, não um efeito único universal.

## Ativação, parâmetros, custos e alvos

Construtor solicita ACFoods.JELLY_BEAN, ACFoodBuilder.food e stack máximo 16. getUseDuration retorna 16 ticks; som GENERIC_EAT. getBeanColor usa Rainbow e hue=(currentTimeMillis%4000)/4000F, saturação 1 e brilho 0,8, senão potionColor; somente apresentação.

finishUsingItem (72 instruções, Code `285ba91b3197410e4ea9e455598f972ce7a7c2be1d1febc8aa9702959b493e18`): no servidor itera potionEffects, solicita efeito instantâneo com amplificador da instância e fator 1D, ou cópia de MobEffectInstance em addEffect; descarta retorno. Player recebe estatística ITEM_USED e shrink(1) quando não instabuild; consumidor não-Player não tem shrink no corpo. Solicita EAT e critério de consumo para ServerPlayer. Não invoca explicitamente o finishUsingItem ancestral neste corpo. Alvo é o consumidor, sem projétil ou AOE ofensiva própria demonstrada. Nutrição final, componentes, tipos de efeitos, duração/amplificadores efetivos, aquisição, custo final, cooldown/mana herdados e possíveis efeitos de terceiros: NÃO VERIFICADOS.

## Consumidores, estado, integração e pendências

onUseTick solicita partícula JELLY_BEAN_EAT com vetores aleatórios e posição do consumidor, server sendParticles ou Level.addParticle; não hit. Tooltip usa dados de efeitos/amplificadores e formata modificadores percentuais para operações multiplicativas. ClientProxy.lambda$onItemColors$22 chama getBeanColor. Advancement inventory_changed usa identidade do item; Rainbow no ícone é dado de apresentação, não prova de produtor da stack.

Próximos gates: produtores de POTION_CONTENTS e Rainbow, valores de ACFoods, PotionItem/consumo/codec e liquidação efetiva de efeitos; autoridade, owner e persistência da stack. Sem hook real autorizado, não alterar componentes, multiplicar efeito, reexecutar consumo ou creditar Mastery. NO_MUTATION; universo aberto.
