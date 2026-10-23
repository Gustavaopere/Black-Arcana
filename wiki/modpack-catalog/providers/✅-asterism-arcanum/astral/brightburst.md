# Brightburst

**Dossiê documental — 23/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT` para registry/classe, lógica `SOURCE_PINNED / SOURCE_CAUSALITY`; integração `CONDITIONAL`; config efetiva/QA físico `PENDING`. **+0 identidades**, sem perk/adapter/runtime novo.

- Provider **Asterism Arcanum**, `mod_id=asterismarcanum`; spell Iron's **`asterismarcanum:brightburst`**, escola default **`asterismarcanum:astral`** ([escola][school]). Registro [ASARSpellRegistry][registry]. Entidades, VFX e impactos são filhos deste cast, não magias extras.
- Artefato histórico #56: Minecraft1.21.1/NeoForge, **`asterismarcanum-1.21.1-0.1.0.jar`**, SHA-1 **`4a25ba80116168ddcc812f71467c0598127e774a`**, [publisher8157080](https://www.curseforge.com/minecraft/mc-mods/asterism-arcanum/files/8157080). [Prova binária de identidade](../EXACT-0.1.0-BINARY-REGISTRY-AUDIT.md); não comprova equivalência dos corpos de método nem QA.
- Source oficial **`BirdieVibes/Asterism-Arcanum@f1738c7813a85d31a6da10e6c9f2dbce18d2b583`**, versão declarada `1.21.1-0.1.0`, licença **Polyform Shield**; consulta/paráfrase/referências, sem importar implementação/assets. Build usa Iron's **3.15.6**; pack registra **3.16.3** ([versões][versions]). Host examinado separadamente: **`iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`**. Compatibilidade/JAR/mixins ainda condicionados.

`L` = nível entregue ao consumidor; `P=getSpellPower(L,caster)` no source host = base linear×SPELL_POWER×poder da escola×POWER_MULTIPLIER ([host][host-power]). “Neutro” assume multiplicadores1; defaults não substituem config implantada. Poder/resistência Astral são [atributos nativos][attributes], sem demonstrar adapter RPG nem setter por jogador para cada eixo.

## Declarante, ingresso e causalidade

Classe `com.birdie.asterismarcanum.spells.BrightburstSpell`: constructor/defaultConfig, `onCast`, `getRadius`, `getDamage` e `getEmptyCastData`. Descrição para jogador, paráfrase do [guia oficial][guide]: irradia proteção que repele inimigos próximos.

A classe não sobrescreve precondição local de alvo; admissão de jogador, mana/cooldown e eventuais gates são do [wrapper Iron's][host-preflight]. Fornece `ImpulseCastData`, mas o override não lê/escreve esse objeto. No settlement do wrapper jogador, [mana/evento precedem onCast][host-cast]; ingressos diretos externos não têm necessariamente esse contrato.

`onCast` escreve o campo de instância `radius=10+2L`, cria SpellDamageSource com **directEntity=caster e causingEntity=caster**, busca LivingEntities em cubo caster.position±radius e aplica filtro esférico/facção/montaria. Para cada elegível chama **target.hurt diretamente**, ignora seu retorno, marca hasImpulse e soma movimento radial. Partículas/finish sound e `super.onCast` encerram a rotina. [Cast][cast], [fonte][host-source], [tipo][host-damage-source].

**Dano sem o helper:** embora seja SpellDamageSource, esse ramo não chama `DamageSources.applyDamage`; portanto não demonstra a publicação de SpellDamageEvent nem a aplicação de `getResist`/friendly-fire internos desse helper ([comparação][host-damage]). Minecraft/NeoForge e outros listeners continuam no hurt: não afirmar bypass universal, dano final ou compatibilidade a partir da classe da fonte. O impulso é tentado **mesmo se hurt retornar false**, sem recibo de dano nem refund próprio.

## Matriz de parâmetros e alteração por perks

| Eixo | Valor/default/fórmula e fonte | Fase, superfície e limite | QA |
|---|---|---|---|
| Nível/cast/custo | Rare, L1–6; INSTANT, cast0ticks; mana `int((25+5(L−1))×MANA_MULTIPLIER)`, neutro25/30/35/40/45/50; cooldown20s=400ticks antes de modificadores. [Defaults][defaults], [host][host-values]. | **CONFIG_NATIVE** de host; eventos de nível/custo/cooldown só nos caminhos reais. Não há recurso extra de impulso ou custo por alvo. | Config/castsource/creative/recast e settlement único. |
| Power/dano | Base1, incremento1 → P neutro1..6; `D=1+P/2`, neutro1.5/2/2.5/3/3.5/4 health points por alvo. [Constructor][defaults], [fórmula][formula]. | **NATIVE_ATTRIBUTE/CONFIG_NATIVE** para P; ele altera dano e impulso juntos. Nenhum setter isolado de D local. SpellDamageEvent não é hook comprovado desta rota direta. | Powers fracionários/negativos, resistência/absorção/imunidade e HP final. |
| Tipo/owner | Escola default Astral → DamageType `asterismarcanum:astral_magic`, scaling JSON when_caused_by_living_non_player, exhaustion0. [Escola][school], [JSON][damage-type], [fonte][host-damage-source]. | Não inferir tags is_magic/bypass só por nome ou school. Config SCHOOL/registry efetivos podem mudar fonte; conversão per-player **⛔ SEM_HOOK_SEGURO**. | Datapack efetivo, casterPlayer/mob e atribuição de mortes. |
| Centro/alcance/área | Centro em caster.position, **r=10+2L** blocks →12/14/16/18/20/22; broadphase AABB±r em X/Y/Z e condição `distanceTo(target)<=r`. Sem limite local de quantidade de alvos. [Cast][cast], [tooltip-radius][formula]. | Raio depende de L, não P; campo `radius` é estado da instância de spell, não knob por jogador. Sem setter/target resolver público; resize de área **⛔ SEM_HOOK_SEGURO**. | Borda r, altura, cantos do cubo, múltiplos casters e budget por quantidade de entidades. |
| Filtros/LOS | LivingEntity; exclui caster, `caster.isAlliedTo(target)` e `caster.isPassengerOfSameVehicle(target)`. **Não testa LOS**, linha de visão, alive, PvP/claim ou filtro simétrico de aliado no trecho. [Seleção][cast]. | Atravessar parede é possível na seleção source; proteção final do pack **NÃO VERIFICADA**. Não somar filtros do helper que não foi chamado. Retarget/filtro por perk **⛔ SEM_HOOK_SEGURO**. | Paredes, entidades aliadas só numa direção, passengers, PvP/party/claims e alvo removido. |
| Impulso/knockback | `B=2P/(d+0.01)`; `K=target.KNOCKBACK_RESISTANCE`; vetor `normalize(target.pos−caster.pos)×[B−clamp(5K,0,B)]`, somado a deltaMovement; hasImpulse=true. [Movimento][cast]. | Resistência de knockback é **NATIVE_ATTRIBUTE** realmente lida; não é dano nem garantia de deslocamento. Clamp com P negativo não recebe política adicional local. Hook de LivingKnockBackEvent não foi chamado diretamente por addDeltaMovement. | d0/d≈0, K0/alto/negativo, P negativo, hurt=false, barreiras e sincronização do movimento. |
| Projétil/tempo/estados | Sem entidade/projétil, hitbox própria, speed, pierce, summon ou DoT: **N/A**. Dano/impulso são síncronos por iteração; VFX não define novo raio. Sem recast próprio (base0). [Cast][cast], [base][host-power]. | Sem duração de buff/rollback/blocos/teleporte neste método. Não criar scheduler/segunda explosão/dano para simular ampliação. | Um processamento causal por alvo/ingresso; nenhum cast novo por partícula/impulso. |

## Integração e verificação

`getRadius/getDamage` são privados e `radius` é campo da spell; localizar números não fornece seam seguro. O [dossiê comum](../SPELL-PERK-BOUNDARIES-0.1.0.md) separa atributos/config globais, eventos pré-settlement e observação. Alterar L pode mudar raio/dano/custo em fases diferentes; o wrapper não repricing automaticamente todos os valores já calculados. Para dano, auditar o evento NeoForge efetivamente anterior ao HP e a identidade causal antes de propor adapter; não prometer SpellDamageEvent neste ramo.

Iron's/Asterism possuem casting/mana/cooldown/dano/movimento. RPG Skill Tree mantém sua progressão/perks somente por contrato; Black Arcana não repete hurt/push e Enshrouded não converte tipo por afinidade temática. A fonte carrega referência da spell, mas não um token persistente por AoE/target: distinguir cast original, alvo, dano tentado e movimento aplicado; hit, partícula e efeito não são recompensas independentes.

Obtenção source: [loot Astromancer][loot] pode sortear scroll da escola Astral com quality0.25..0.85; habilitação/crafting/receita/config efetivos e Survival continuam condicionados. Não criar nova aquisição. Assinatura ocupada: repulsão radial instantânea com dano leve e força inversa à distância, reduzida por resistência de knockback; outro VFX/nome não cria nova magia.

**PENDING:** equivalência destes métodos com JAR, config/datapack, servidor/cliente, Survival, multiplayer, proteções e os casos da matriz. Nenhuma perk/bridge implementada nem Stage promovido.

[versions]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/gradle.properties#L9-L24
[school]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/registries/ASARSchoolRegistry.java#L42-L51
[attributes]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/registries/ASARAttributeRegistry.java#L19-L49
[damage-type]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/resources/data/asterismarcanum/damage_type/astral_magic.json#L1-L5
[loot]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/resources/data/asterismarcanum/loot_table/entities/astromancer.json#L34-L54
[host-values]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L160-L174
[host-power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L211-L241
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L333
[host-preflight]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L373-L402
[host-source]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L560-L565
[host-damage-source]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/SpellDamageSource.java#L24-L51
[host-damage]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L65
[registry]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/registries/ASARSpellRegistry.java#L23-L26
[guide]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/resources/assets/asterismarcanum/lang/en_us.json#L38-L39
[defaults]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/spells/BrightburstSpell.java#L31-L74
[cast]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/spells/BrightburstSpell.java#L83-L115
[formula]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/spells/BrightburstSpell.java#L118-L124
