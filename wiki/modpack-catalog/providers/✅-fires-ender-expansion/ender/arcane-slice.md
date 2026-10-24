# Arcane Slice

**Dossiê documental — 24/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`; lógica `SOURCE_PINNED / SOURCE_CAUSALITY`; integração `CONTRATO_CONDICIONAL`; QA físico `PENDING`. **+0 identidades**: partículas e fator de mana pertencem ao mesmo hit.

## Identidade e proveniência

Provider Fire's Ender Expansion, `mod_id=firesenderexpansion`, spell **`firesenderexpansion:arcane_slice`**, escola default `irons_spellbooks:ender`. Declarante `net.fireofpower.firesenderexpansion.spells.ArcaneSliceSpell`; registro `SpellRegistries#registerSpell(new ArcaneSliceSpell())`. [Registry][registry], [defaults][defaults].

MC1.21.1, JAR registrado **`firesenderexpansion-2.4.1.jar`**, SHA-1 `da87a4a0c926dd75236766584cddbae69c6aeff7`, [publisher8167304](https://www.curseforge.com/minecraft/mc-mods/fires-ender-expansion/files/8167304), [prova binária estática](../EXACT-BINARY-SPELLS-2.4.1.md). Source oficial `FireOfPower/firesenderexpansion-1.21.1@5e4067e8112316f55c9f249530ba1917a7bf6643`, build NeoForge21.1.215/Iron's3.15.6; pack registrado NeoForge21.1.250/Iron's3.16.3. Host consultado `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252` (3.16.3). Identidade exata não prova equivalência integral dos métodos source↔JAR nem config efetiva. All Rights Reserved: fatos/paráfrases/permalinks, sem importar código/assets. [Versões][versions], [contratos comuns](../SPELL-PERK-BOUNDARIES-2.4.1.md).

[Guia oficial][description], parafraseado: corte Ender concentrado contra uma criatura, mais eficaz contra jogador com pouca mana. A implementação aplica dano direto; não executa teleporte/desmembramento. Aquisição usa elegibilidade do host, sem override local de loot/crafting; distribuição real de scrolls e rota Survival **NÃO VERIFICADAS**. [Spell][cast], [elegibilidade host][host-acquisition].

## Ingresso e pipeline causal

1. Rare, níveis default1..3, INSTANT0ticks. Wrapper jogador `AbstractSpell#attemptInitiateCast` valida aprendizado/mana/cooldown conforme CastSource, executa precondição e evento cancelável SpellPreCastEvent antes de iniciar. `#castSpell` posta SpellOnCastEvent antes do débito/onCast; cooldown ocorre depois, conforme source/config. Não há recast próprio. [Defaults][defaults], [admissão][host-admission], [cast host][host-cast].
2. `ArcaneSliceSpell#checkPreCastConditions(Level,int,LivingEntity,MagicData)` retorna `Utils#preCastTargetHelper(...,32,0.15F)`. Helper resolve ray do eye pelo olhar, clip COLLIDER/Fluid.NONE, nearest hit antes do bloco; filtro inicial pickable/alive/!spectator. Guarda LivingEntity por UUID, incluindo tratamentos host para PreventDismount/PartEntity. Miss falha a admissão. [Precondição][precast], [helper][target-helper], [ray][ray], [filtro][ray-filter].
3. `#onCast` lê TargetEntityCastData e resolve UUID no ServerLevel atual. Alvo não null recebe40 partículas de uma linha inclinada e **uma** chamada `DamageSources#applyDamage`. Sem nova validação local de range/LOS. Alvo ausente gera zero tentativas de dano, seguido de super.onCast; sem refund local. [Cast][cast], [UUID][target-data].
4. Privado `#getDamage(int,LivingEntity,LivingEntity)`: base `D=0.77P`; apenas alvo **ServerPlayer e MAX_MANA>0** usa `D=0.77P×(1.5−(manaAtual/MAX_MANA)/2)`. Não drena mana nem faz clamp da razão. Extremos base..1.5×base pressupõem mana0..MAX_MANA; tooltip usa overload sem alvo, só0.77P. [Dano][damage].
5. `AbstractSpell#getDamageSource(caster)` passa caster como entidade direta/causadora e spell como referência. SpellDamageSource usa tipo da escola default `irons_spellbooks:ender_magic`, fallback genericKill se holder ausente. Helper posta SpellDamageEvent antes da resistência, friendly-fire e hurt. Amount tentado não é HP entregue; retorno é ignorado pela spell. Não há DOT, child-cast, ledger persistente ou entidade própria. [Factory][host-source-factory], [source][host-source], [escola][school], [terminal][damage-helper].

## Matriz de parâmetros e alteração por perks

`L`=nível recebido; `P=(12+5(L−1))×SPELL_POWER×schoolPower×POWER_MULTIPLIER`, por `AbstractSpell#getSpellPower`. Valores neutros pressupõem multiplicadores1; defaults não são config implantada. Dano em health points. [Fórmulas host][host-formulas].

| L default | Mana neutra | P neutro | D base aproximado | D com alvo em0mana aproximado |
|---|---|---|---|---|
| 1 | 75 | 12 | 9.24 | 13.86 |
| 2 | 90 | 17 | 13.09 | 19.635 |
| 3 | 105 | 22 | 16.94 | 25.41 |

| Eixo | Valor / consumidor / fase | Boundary, limite e estado | QA |
|---|---|---|---|
| Nível / power | Max default3; P acima, servidor em `ArcaneSliceSpell#getDamage`; tooltip pode consultar client. [Defaults][defaults], [dano][damage], [host][host-formulas]. | POWER_MULTIPLIER **CONFIG_NATIVE**, atributos spell_power/ender_spell_power nativos; ModifySpellLevelEvent e SpellOnCastEvent#setSpellLevel(int) são seams host condicionados ao adapter comum. Sem clamp adicional de P/D; max default não é cap do evento. | Q1/Q2 |
| Mana / compromisso | `int((75+15(L−1))×MANA_MULTIPLIER)`; caster paga antes do efeito conforme CastSource/creative. Sem roubo de mana da vítima. [Defaults][defaults], [host][host-formulas], [ordem][host-cast]. | **CONFIG_NATIVE** global; SpellOnCastEvent#setManaCost(int) **HOOK_VERIFICADO** pré-débito. Ingresso exige mana original; mudar level não recalcula custo. Integração **CONDITIONAL**, sem refund local por alvo perdido/dano negado. | Q1/Q2 |
| Tempo / cooldown / recast | INSTANT0ticks; default35s=700ticks antes de config/reduction; getRecastCount host0 e nenhum recast local. [Defaults][defaults], [host][host-formulas], [cast][host-cast]. | Cooldown **CONFIG_NATIVE**; cooldown_reduction conforme contrato comum. Redução de cast não cria wind-up em INSTANT. Duração/DOT/charges **N/A**. | Q1/Q2 |
| Aquisição / alcance / alvo | Um alvo Living por ray32blocks, inflation0.15blocks, nearest hit/block clip; UUID resolve no mundo atual. `#checkPreCastConditions/#onCast`. [Helper][target-helper], [ray][ray], [UUID][target-data]. | Constantes locais, sem setter de range/retarget. **⛔ SEM_HOOK_SEGURO** para ampliar range, trocar filtros ou single→AOE; preservar claims/PvP/chunks. Inflation não é raio ofensivo. | Q2/Q3 |
| Dano / mana da vítima | `#getDamage`:0.77P ou fator1.5−ratio/2 acima; uma chamada servidor. [Dano][damage], [cast][cast]. | SpellDamageEvent#setAmount(float), cancelável **HOOK_VERIFICADO** antes de resist/FF/hurt; adapter **CONDITIONAL**, filtrar spell/caster/alvo e valor finito/bounded. Não reaplicar fator de baixa mana. Sem clamp local do ratio. [Evento][damage-event]. | Q2/Q4 |
| Tipo / resist / crítico / knockback | `AbstractSpell#getDamageSource` → SpellDamageSource Ender; resistência host genérica×escolar; sem crit/knockback extra local. [Source][host-source], [escola][school], [terminal/resist][damage-resist]. | Evento de amount não altera DamageType/tags/alvo. **⛔ SEM_HOOK_SEGURO** para conversão elemental; tags/resolução efetivas e knockback vanilla **NÃO VERIFICADOS** no pack. | Q4 |
| Área / partículas / projétil | `#onCast`:i−20..19, offset i×0.1blocks;40 VFX, um alvo/um hit. Sem projétil: AABB/speed/lifetime/pierce/spread/explosão **N/A**. [Cast][cast]. | Visual não determina colisão/área. **⛔ SEM_HOOK_SEGURO** para AoE; resize de projétil **N/A**. | Q3/Q4 |
| Estados / summons / mundo / cleanup | Sem buff/summon/teleporte/mudança de bloco/tick posterior/persistência próprios. Target data transitório é host-owned; `#onCast` sempre chama super. [Cast][cast], [UUID][target-data]. | Summon count/AI/rollback **N/A**; não reproduzir efeito por fallback. Cleanup/sync de cast dependem do host. | Q2/Q5 |

## Autoria, concepção e pendências

FEE/Iron's possuem cast, mana, cooldown e dano. RPG Skill Tree observa progressão na lane `irons:ender` sob contrato comum; cast admitido não prova hit. Black Arcana deve correlacionar raiz/caster/UUID do alvo/settlement sem segundo dano/custo. Proc Shulker, quando ativo, é derivado; partículas não geram prática. Enshrouded não ganha bridge de Shroud ou conversão de tipo pela escola Ender.

Assinatura ocupada: hit direto de alvo único com fator inverso de mana do jogador atingido. Lacuna conceitual possível: troca explícita de recurso por controle, com identidade/runtime originais; não constitui hook desta spell.

- **Q1:** fingerprint/source↔métodos, configs, L/power/atributos, mana/cooldown por CastSource; level/custo alterados e mana inicialmente insuficiente.
- **Q2:** miss, alvo perdido/removido/trocado de dimensão, UUID/concorrência, cancelamento pre-cast/damage, nenhum refund/segunda cobrança/recast.
- **Q3:** ray32/bordas0.15, bloco/multipart/montaria, aliado/PvP/claims, movimento entre aquisição/resolução,40 VFX versus uma tentativa.
- **Q4:** ServerPlayer mana0/max/acima/abaixo, MAX_MANA0 e não-player; resistência/tags/hurt recusado/proc Shulker/autoria/HP real.
- **Q5:** dedicado/cliente/Survival/sync, logout/morte/restart e dedupe Mastery. Todos **PENDING**; documentação não implementa perk/adapter nem aprova gameplay.

[registry]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/registries/SpellRegistries.java#L13-L27
[versions]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/gradle.properties#L15-L50
[defaults]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/spells/ArcaneSliceSpell.java#L29-L78
[description]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/resources/assets/firesenderexpansion/lang/en_us.json#L43-L44
[precast]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/spells/ArcaneSliceSpell.java#L81-L83
[cast]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/spells/ArcaneSliceSpell.java#L85-L110
[damage]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/spells/ArcaneSliceSpell.java#L112-L125
[host-formulas]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L148-L241
[host-admission]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L373-L401
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L332
[host-acquisition]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L612
[target-helper]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L665-L710
[target-data]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/TargetEntityCastData.java#L12-L39
[ray]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/RaycastBuilder.java#L20-L124
[ray-filter]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L459-L461
[host-source-factory]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L560-L565
[host-source]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/SpellDamageSource.java#L24-L51
[school]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/registry/SchoolRegistry.java#L99-L106
[damage-helper]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L64
[damage-resist]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L134-L174
[damage-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellDamageEvent.java#L24-L50
