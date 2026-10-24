# Dimensional Adaptation

**Dossiê documental — 24/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`; lógica `SOURCE_PINNED / SOURCE_CAUSALITY`; integração `CONTRATO_CONDICIONAL`; QA físico `PENDING`. **+0 identidades**: quatro mappings default são resultados de uma spell, não quatro spells.

## Identidade e proveniência

Provider Fire's Ender Expansion (`mod_id=firesenderexpansion`), spell **`firesenderexpansion:dimensional_adaptation`**, escola default `irons_spellbooks:ender`. Declarante `net.fireofpower.firesenderexpansion.spells.DimensionalAdaptationSpell`; lookup `effect_dimension_matcher.EffectDimensionMatcher` e DTO `EffectDetails`; dados `data/firesenderexpansion/adaptable_dimensions.json`. [Registry][registry], [spell][spell], [matcher][matcher], [JSON][mapping].

MC1.21.1, JAR registrado **`firesenderexpansion-2.4.1.jar`**, SHA-1 `da87a4a0c926dd75236766584cddbae69c6aeff7`, [publisher8167304](https://www.curseforge.com/minecraft/mc-mods/fires-ender-expansion/files/8167304), [prova binária estática](../EXACT-BINARY-SPELLS-2.4.1.md). Source oficial `FireOfPower/firesenderexpansion-1.21.1@5e4067e8112316f55c9f249530ba1917a7bf6643`, build NeoForge21.1.215/Iron's3.15.6; pack registrado NeoForge21.1.250/Iron's3.16.3. Host consultado Iron's3.16.3 `e4056af90302d37eb1739f5ff05020b020e6e252`. Source↔JAR dos métodos/config/datapacks efetivos não foram equiparados. All Rights Reserved: fatos/paráfrases/permalinks, sem importar implementação/assets. [Versões][versions], [contratos comuns](../SPELL-PERK-BOUNDARIES-2.4.1.md).

[Guia oficial][description], parafraseado: conhecimento Ender concede uma adaptação às condições da dimensão atual. `#canBeCraftedBy(Player)` exige Endchiridion em inventory **ou** Curio; é condição de crafting, não gate de todo cast nem prova de exclusividade de aquisição. Scroll loot/receitas/rota Survival efetivos **NÃO VERIFICADOS**. [Gate][crafting], [host aquisição][host-acquisition].

## Ingresso e pipeline causal

1. Rare, níveis default1..6, INSTANT0ticks, self. Não há precondição específica para mapping válido nem gate Endchiridion em onCast. Wrapper jogador `AbstractSpell#attemptInitiateCast/#castSpell` possui admissão/pre-cast/evento, débito e cooldown conforme CastSource/config. Spell não possui recast. [Defaults][spell], [host][host-cast], [admissão][host-admission].
2. `DimensionalAdaptationSpell#onCast` consulta **dimensão do caster no momento do efeito**, em string namespace:path, usando `EffectDimensionMatcher#getEffectDetailsForDimension(String)`. Fallback é EffectDetails(null,200,0). Mapping ausente: para ServerPlayer, actionbar cannot_adapt e som Enderman scream (volume0.5/pitch1); sem buff. Outros Living não recebem esse feedback. Sempre segue super.onCast, sem refund/cancelamento local. [Cast][cast], [fallback][lookup].
3. Mapping presente: resolve id em BuiltInRegistries.MOB_EFFECT, wrapAsHolder, solicita **um MobEffectInstance em self** com `duration=(int)((P/10)×durationJSON)`, amplifierJSON, ambient=false/particles=false/icon=true. Não testa retorno de addEffect nem faz validação local de id/duração/amplifier. Não transporta caster nem retargeta aliados. [Cast][cast], [multiplicador][multiplier].
4. `EffectDimensionMatcher#loadFromDisk(ResourceManager)` lê **um** resource `firesenderexpansion:adaptable_dimensions.json` por getResource, não merge de todos os arquivos. Espera entries[] com dimension/id/duration/amplifier; strings e ints não recebem cap/validação semântica local. Duplicate dimension usa último Map.put. Cache é unmodifiable, mas getters de EffectDetails não são API mutadora por jogador. [Matcher][matcher], [DTO][details].
5. `#reload(...)` executa loadFromDisk no executor de preparação e altera cache dentro desse worker; barrier/game-executor posterior só registra log. Arquivo ausente ou entries ausente retorna antes de trocar cache, podendo preservar cache anterior; parse exception é capturada e depois publica cache parcial/vazio acumulado. Reload é registrado em `FiresEnderExpansion#onAddReloadListeners`. Não prometer rollback atômico ou limpeza em todo erro. [Reload/load][matcher], [registro][reload-registration].
6. Spell não observa troca posterior de dimensão nem mantém timer/estado próprio: efeito vanilla/outro provider passa a controlar ticks, merge, remoção, persistência e resultado terminal. Reload altera consultas futuras, sem reaplicar explicitamente buffs já concedidos. Comportamento físico e semântica exata de efeitos externos/vanilla **PENDING**. [Cast][cast], [matcher][matcher].

## Matriz de parâmetros e alteração por perks

`P=(10+2(L−1))×SPELL_POWER×schoolPower×POWER_MULTIPLIER` por `AbstractSpell#getSpellPower`; valores neutros pressupõem multiplicadores1. Defaults não são datapacks/config implantados. [Host][host-formulas].

| L default | Mana neutra | P neutro | Multiplicador de duração |
|---|---|---|---|
| 1 | 55 | 10 | 1.0× |
| 2 | 80 | 12 | 1.2× |
| 3 | 105 | 14 | 1.4× |
| 4 | 130 | 16 | 1.6× |
| 5 | 155 | 18 | 1.8× |
| 6 | 180 | 20 | 2.0× |

| Mapping default em JSON | Efeito real | Duração base (ticks) | Amplifier | Duração neutra pedida L1→L6 |
|---|---|---|---|---|
| minecraft:overworld | minecraft:night_vision | 400 | 0 (I) | 400→800ticks =20→40s |
| minecraft:the_nether | minecraft:fire_resistance | 400 | 0 (I) | 400→800ticks =20→40s |
| minecraft:the_end | minecraft:slow_falling | 200 | 0 (I) | 200→400ticks =10→20s |
| irons_spellbooks:pocket_dimension | minecraft:saturation | 2 | 0 (I) | 2→4ticks =0.1→0.2s |

Duração é truncada **depois** do produto: Saturation em L2 recebe2ticks, não2.4 nem3. Duração pedida não determina quantos ticks de efeito terminal realmente executam. [JSON][mapping], [cast][cast].

| Eixo | Valor / consumidor / fase | Boundary, limite e estado | QA |
|---|---|---|---|
| Nível / power / multiplicador | Max default6; `DimensionalAdaptationSpell#getDurationMultiplier(int,LivingEntity)=P/10`; sem cap extra local. Tooltip mostra multiplicador. [Defaults][spell], [getter][multiplier]. | POWER_MULTIPLIER **CONFIG_NATIVE**, spell_power/ender_spell_power nativos; eventos de nível host **HOOK_VERIFICADO**, adapter **CONDITIONAL**. Getter público não modifica instância; max default não é cap do evento. | Q1/Q2 |
| Mana / cast / cooldown | INSTANT0ticks; `int((55+25(L−1))×MANA_MULTIPLIER)`; cooldown default60s=1200ticks antes de modifiers. Caster paga no host antes do mapping; sem recast/custo de HP/stamina/item por cast local. [Defaults][spell], [host][host-formulas], [ordem][host-cast]. | Mana/cooldown **CONFIG_NATIVE**; SpellOnCastEvent#setManaCost/setSpellLevel pré-onCast reais, mas ingresso verifica mana inicial e level novo não recalcula custo. Sem refund explícito por mapping ausente/buff negado. | Q1/Q2 |
| Aquisição / gate | `#canBeCraftedBy(Player)`: Endchiridion inventory OU Curio. Sem verificação desse item em `#onCast`. [Gate][crafting], [cast][cast]. | Gate provider comprovado para crafting; runtime cast continua host-owned. **⛔ SEM_HOOK_SEGURO** para reinterpretar como consumo obrigatório/item gate universal. Loot/Survival **NÃO VERIFICADOS**. | Q1/Q2 |
| Target / alcance / área | Self na dimensão atual do caster;1 solicitação addEffect; nenhum ray/LOS/range/área/alvo múltiplo. `#onCast`. [Cast][cast]. | Mapping por dimensão não é busca espacial. Range ofensivo **N/A**; **⛔ SEM_HOOK_SEGURO** para self→aliados/AoE/teleporte. Sem cap global de casters implícito no JSON. | Q2/Q3 |
| Tipo de buff / duração / amp | `#onCast` resolve id e duração `int((P/10)×durationJSON)`, ampJSON; nenhum cap/positividade local dos ints. addEffect ignorado. [Cast][cast], [DTO][details]. | Mapping/id/duration/amplifier por resource **CONFIG_NATIVE (datapack global)**; não per-player. Buff/eventos genéricos não dão setter causal FEE confirmado. **⛔ SEM_HOOK_SEGURO** para mutação isolada por perk sem adapter. | Q2/Q3 |
| Dados / reload / cache | Resource único, cache por dimensão, duplicata last-win; ausência/entries ausente mantém cache; parse falho pode publicar parcial/vazio. `EffectDimensionMatcher#reload/#loadFromDisk`. [Matcher][matcher], [registro][reload-registration]. | Superfície nativa de datapack/reload comprovada; snapshot/ordem/concorrência e pack efetivo **CONTRATO_CONDICIONAL**. Sem setters per-caster; não mutar singleton/map como perk. | Q3/Q4 |
| Dano / heal / tipo / DOT | Spell não aplica dano/heal/SpellDamageSource; defaults delegam NightVision/FireResistance/SlowFalling/Saturation. Efeito externo configurado pode ter comportamento próprio. [Cast][cast], [JSON][mapping]. | Fórmula de dano, crit/knockback/tempo terminal **N/A** nesta spell; resultado exato downstream **NÃO VERIFICADO**. Não inferir SpellDamageEvent/conversão elemental a partir da escola. | Q3/Q5 |
| Projétil / summons / geometria | Nenhuma entidade/projétil/summon criado: AABB/radius/speed/lifetime/pierce/spread/AI/cap de summons **N/A**. [Cast][cast]. | Sem resize/contagem pertinente; VFX/som não são geometria. Não criar summon ou buff paralelo. | Q2/Q5 |
| Estado / mundo / persistência | Sem mutação de bloco/dimensão/ticket/rollback; dimensão é input no cast, não trigger contínuo. MobEffect é host/provider-owned; cache é memória, recarregada por listener. [Cast][cast], [matcher][matcher]. | Logout/morte/restart/remoção/merge/efeito ainda ativo após mudar dimensão **PENDING**. Sem ownership/token exclusivo no MobEffect demonstrado; observer não prova origem. | Q4/Q5 |

## Autoria, concepção e pendências

FEE/Iron's possuem cast/recursos e lookup; provider do MobEffect possui efeito terminal. RPG Skill Tree/Black Arcana devem correlacionar cast→dimensão/mapping efetivo→pedido/resultado de addEffect, sem reaplicar buff ou premiar reload/tick como novo cast. Enshrouded mantém Shroud/exposure e seus gates: adicionar uma dimensão/id ao JSON não comprova bridge de progressão, classificação ou segurança ambiental.

Assinatura ocupada: auto-buff escolhido por dimensão via datapack. Uma adaptação original por exposição acumulada seria contrato diferente e exigiria authority explícita do owner; não é comportamento desta spell nem perk disponível automaticamente.

- **Q1:** fingerprint/config/datapack efetivos, níveis/power/mana/cooldown, item em inventory/Curio/ausente e aquisição Survival por canais distintos.
- **Q2:** mapping presente/ausente com jogador/NPC, débito sem buff/refund, cancelamentos, level/custo alterados, buff recusado/refresh/merge.
- **Q3:** quatro defaults/IDs externos inválidos, namespace/duplicatas, duração0/negativa/extrema/amp inválido, truncamento Saturation; resultado downstream e nenhum AoE.
- **Q4:** resource prioridade única, reload válido→ausente→sem entries→malformado parcial/vazio, casts concorrentes e cache anterior; troca de dimensão com buff ativo.
- **Q5:** efeito terminal/ticks/save/remoção/morte/logout/restart, dedicado/cliente/Survival e autoria/Mastery. Todos **PENDING**; sem adapter/perk/runtime novo.

[registry]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/registries/SpellRegistries.java#L13-L27
[versions]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/gradle.properties#L15-L50
[description]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/resources/assets/firesenderexpansion/lang/en_us.json#L53-L55
[spell]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/spells/DimensionalAdaptationSpell.java#L33-L56
[cast]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/spells/DimensionalAdaptationSpell.java#L59-L75
[multiplier]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/spells/DimensionalAdaptationSpell.java#L77-L79
[crafting]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/spells/DimensionalAdaptationSpell.java#L91-L111
[matcher]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/effect_dimension_matcher/EffectDimensionMatcher.java#L21-L91
[lookup]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/effect_dimension_matcher/EffectDimensionMatcher.java#L86-L90
[details]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/effect_dimension_matcher/EffectDetails.java#L3-L22
[reload-registration]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/FiresEnderExpansion.java#L75-L82
[mapping]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/resources/data/firesenderexpansion/adaptable_dimensions.json#L1-L28
[host-formulas]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L148-L241
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L332
[host-admission]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L373-L401
[host-acquisition]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L612
