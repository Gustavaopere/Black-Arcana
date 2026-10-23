# Asterism Arcanum 0.1.0 — código, parâmetros e boundaries para perks

**Reauditoria documental — 23/10/2026.** Base Black Arcana `a93890ed70561176ace0859f76f4e6b63170ff0f` (#877); RPG/modlist `ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc`, Enshrouded `a41dbb51aacb94b7b5db6517f1514b0b7aee3e83`, Factory `518278ae9c0d264a537cc1bc6ee4974e01270fdf`.

**11/11 mede fichas source-causais deste lote**: dez spells normais e um Gateway conditional. Não é onze spells Survival nem onze perks implementáveis; +0 identidades e +0 strict. Config implantada, JAR funcional, hooks integrados e QA físico continuam PENDING. Nenhum runtime/adapter/perk ou dependência foi alterado.

## Proveniência e universo

Source oficial `BirdieVibes/Asterism-Arcanum@f1738c7813a85d31a6da10e6c9f2dbce18d2b583` [declara](https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/gradle.properties#L9-L24) Minecraft 1.21.1, addon 1.21.1-0.1.0, NeoForge 21.1.215 e Iron’s 3.15.6. Host source consultado Iron’s 3.16.3 `e4056af90302d37eb1739f5ff05020b020e6e252`; build/dev Black Arcana NeoForge 21.1.248 versus [snapshot físico 21.1.250][modlist-loader]. Metadata **Polyform Shield** não é licença MIT do template NeoForged; só resumos factuais/paráfrases e referências, sem copiar implementação/assets.

O snapshot [#56][modlist] registra `asterismarcanum-1.21.1-0.1.0.jar`/SHA-1 `4a25ba80116168ddcc812f71467c0598127e774a`. Publisher CurseForge [8157080](https://www.curseforge.com/minecraft/mc-mods/asterism-arcanum/files/8157080), medido novamente em 23/10/2026: 987245 bytes, mesmo SHA-1 e SHA-256 `191422cf3096a79e158d3262b52ea98fb1abc745847d4eb356548a5a5f58eebc`. O original instalado não está no filesystem desta sessão; esta medição é do publisher correlacionado ao fingerprint histórico. [Prova histórica de registry](EXACT-0.1.0-BINARY-REGISTRY-AUDIT.md) sustenta 11 classes/refs; não estende igualdade aos corpos de todos os métodos source↔JAR.

[ASARSpellRegistry][registry] tem onze registrations ativos; Trailblaze permanece comentado e ausente do conjunto de Spell classes do artefato. Efeitos, tags, entidades, multipart sections, projéteis filhos e manobras da mesma raiz não aumentam o universo.

| ID real `asterismarcanum:` | Classe declarante | Ficha / consumidor relevante |
|---|---|---|
| `astral_echo` | AstralEchoSpell | [Echo](astral/astral-echo.md), teleport inicial + StarcutterEntity tagueada |
| `astral_gateway` | AstralGatewaySpell | [Gateway](astral/astral-gateway.md), foreach/transição do próprio caster; **CONDITIONAL** |
| `brightburst` | BrightburstSpell | [Brightburst](astral/brightburst.md), target.hurt direto + push |
| `celestial_tether` | CelestialTetherSpell | [Tether](astral/celestial-tether.md), montaria/contador + ServerEvents |
| `luminous_beam` | LuminousBeamSpell | [Beam](astral/luminous-beam.md), AbstractBeamProjectile/parts |
| `piercing_light` | PiercingLightSpell | [Piercing Light](astral/piercing-light.md), constructor/travel/hit |
| `silvery_barbs` | SilveryBarbsSpell | [Barbs](astral/silvery-barbs.md), Luck+tag+IncomingDamage |
| `star_swarm` | StarSwarmSpell | [Swarm](astral/star-swarm.md), gate + filhos PiercingLight |
| `starcutter` | StarcutterSpell | [Starcutter](astral/starcutter.md), clamp/área terminal/NBT |
| `starfire` | StarfireSpell | [Starfire](astral/starfire.md), ricochet/pierce/filtros |
| `summon_lunar_moths` | SummonLunarMothsSpell | [Lunar Moth](astral/summon-lunar-moth.md), SummonManager/recasts/AI |

## Nível, atributos e configuração

`n` é o nível entregue ao consumidor, não garantia de estar no intervalo default após listeners. `P=(base+porNível×(n−1))×SPELL_POWER×AstralPower×POWER_MULTIPLIER` no [AbstractSpell#getSpellPower][power]. O [getEntityPowerMultiplier][entity-power] resolve somente os três multiplicadores, sem a base linear; Echo usa esse produto em sua fórmula de distância. Atributo power pode afetar vários eixos ao mesmo tempo, não é knob isolado de dano.

Os [atributos Asterism][attributes] são `asterismarcanum:astral_spell_power` e `:astral_magic_resist`, MagicPercentAttribute default1, faixa−100..100 e sync. A [escola][school] os associa à escola Astral e ao DamageType `asterismarcanum:astral_magic`. A resistência só participa dos caminhos que realmente a consultam; registrar atributo não prova aplicação universal do helper.

[DamageType JSON][damage-json] e [bootstrap][damage-registry] distinguem tipo real de rótulo de escola/ID de spell. O resource `data/asterismarcanum/tags/item/damage_type/astral_magic.json` é um caminho de **item tag**, não prova de inclusão universal em uma tag de DamageType como `neoforge:is_magic`. Tags/datapacks efetivos continuam pendentes; não prometer classificação ou resistência por afinidade Astral.

[Config host][mana] calcula mana por `(int)((baseMana+porNível×(n−1))×MANA_MULTIPLIER)` e cooldown em ticks a partir dos segundos configurados. Defaults não são captura de `/config`/datapack do usuário. `CONFIG_NATIVE` global não é setter per-player.

## Casting, settlement e cleanup

No [wrapper jogador][cast], admissão/SpellPreCastEvent antecedem início; em castSpell, SpellOnCastEvent recebe custo do nível original → débito conforme CastSource/recast/creative → override onCast com nível do evento → recast/cooldown → pacote cliente com nível original. Mudar nível no evento não recalcula automaticamente custo inicial ou pacote. Não cobrar outra mana/XP por hit, seção, filho ou efeito. Comandos/mobs diretos podem seguir outro ingresso; o contrato não é universal a todo onCast.

[MagicManager#tick][tick] liquida CONTINUOUS em intervalos de10ticks enquanto callbacks servercasttick têm outra cadência. Cast time e lifecycle da entidade são dimensões separadas. [AbstractSpell#onServerCastComplete][complete] alcança resetCastingState do host; [MagicData reset][magic-data] chama resetAdditionalCastData e [EntityCastData#reset][entity-data] descarta a entidade guardada. Beam/Gate usam essa cadeia para cleanup normal; seus failsafes/volley budgets órfãos não são duração/budget de um cast normal. Cada ficha registra condições locais, persistência e cancelamento sem criar cleanup BA paralelo.

Os [listeners dimensionais Asterism](https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/events/ServerEvents.java#L21-L38) pedem SUCCESS no PlayerSwimEvent dentro do Astral Sea. Para não-player, EntityJoinLevelEvent liga noGravity e uma tag somente se a flag era falsa; ao chegar fora da dimensão com a tag, desliga e remove a tag. Isso também condiciona trajetórias de projéteis nessa dimensão: constructor/travel não bastam para prometer física universal. Não equivale a perk de voo nem prova compatibilidade de Expandability no JAR.

## Superfícies reais e limites por eixo

| Eixo | API / fase source-confirmada | Limite de integração |
|---|---|---|
| Nível/custo | [SpellOnCastEvent#setSpellLevel/setManaCost][cast-event], antes do débito no wrapper jogador | **HOOK_VERIFICADO** genérico, **CONTRATO_CONDICIONAL** para clamp/custo/sync/admissão. Não é setter de target, hitbox ou tipo. |
| Consulta de nível | [ModifySpellLevelEvent#setLevel][level-event] via getLevelFor | Mutação de consulta, diferente do nível já guardado no efeito/entidade. Ordenação, ambos os sides e limites precisam contrato. |
| Cooldown | [SpellCooldownAddedEvent.Pre][cooldown-event] no addCooldown do host | Mutável/cancelável na inserção suportada; não é duração do buff/projétil nem política de recast completa. |
| Dano por helper | [DamageSources.applyDamage][damage-helper] publica [SpellDamageEvent#setAmount/cancel][damage-event] só no ramo LivingEntity+SpellDamageSource, antes de resistência/friendly-fire/hurt | Bônus de amount pode ser interceptado nessa fase; não comprova HP entregue nem conversão de DamageType. Brightburst chama hurt diretamente e não passa por esse ramo. |
| Teleporte Echo inicial | [Utils.handleSpellTeleport][teleport] publica [SpellTeleportEvent][teleport-event], lê coordenadas e cancelamento | **HOOK_VERIFICADO** para destino inicial; retorno bool é canceled. Não cobre Echo anti-magic setPos ou entrada Gateway changeDimension, não revalida solver/proteção após alteração. |
| Gateway saída | [PlayerRespawnPositionEvent#setDimensionTransition/setRespawnLevel][respawn-event], publicado manualmente pelo spell ao sair | Mutador real de transition nessa fase, não cancelável. **CONDITIONAL**; não desbloqueia Survival nem garante um único teleporte por cast. |
| Summon Lunar Moth | [SpellSummonEvent#setCreature][summon-event], antes de addFreshEntity | Mutador real, não cancelável, sem setter de count/duração; tipo consumido é Moth/subtipo, com ownership já iniciado antes do evento. Replacement, null, world e cleanup exigem contrato; não trocar por criatura arbitrária. |
| Target/área/hitbox/tempo/estados | Consumidor específico nas fichas | Constante/setter/observador localizado não demonstra seam seguro per-player. Sem contrato: **⛔ SEM_HOOK_SEGURO**; N/A para eixo inexistente, nunca cast paralelo para compensar. |

NeoForge `e0e7ab5d273fdc034f23fee7bf91c61ae39d3019`: [EntityTeleportEvent][entity-teleport] e [PlayerRespawnPositionEvent][respawn-event] foram comparados byte a byte ao [sources.jar21.1.250 oficial](https://maven.neoforged.net/releases/net/neoforged/neoforge/21.1.250/neoforge-21.1.250-sources.jar), SHA-256 do artefato `a2811d794544ec67dc3fa43b900158f058ea534881ba1c160373554384311a0d`. Hashes respectivos dos arquivos: `b767390a690680a785c2da67d524b1cd511f4bd4c2a00a5688783b812473d449` e `3ee66e7d2ff8dc0b214816ff1d17ea727b7697343c7058b1f694f1f22cb6a537`. Prova limitada a esses dois arquivos, sem equivaler o tree NeoForge inteiro ou o runtime montado.

## Autoridades dos projetos e deduplicação

O [RPG IronsSpellbookProgressionEvents][rpg] exige ArcaneAccess no pre-cast HIGHEST com exceções próprias para COMMAND/FakePlayer, possui gate de inscrição e observa SpellOnCastEvent em LOWEST para Mastery. Normalização de escola externa produz `asterismarcanum/astral`, portanto chave de disciplina `irons:asterismarcanum/astral`, sem assumir `irons:astral`. [MasteryPolicies.forIron](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc/src/main/java/dev/gustavopere/rpgskilltree/core/MasteryPolicies.java#L5-L12) e [MasteryLaneCatalog.ironsDiscipline](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc/src/main/java/dev/gustavopere/rpgskilltree/core/MasteryLaneCatalog.java#L82-L84) fecham a formação da chave. Esse ingresso pré-efeito não é prova de hit, HP, summon spawn, chegada/retorno ou restauração; efeitos derivados não concedem recompensa duplicada por definição.

Asterism/Iron’s continuam donos de cast/mana/cooldown, damage/status, summons, movimento e cleanup. Black Arcana mantém seu runtime/WorldEffectPolicy, sem reaplicar dano, shield ou teleporte de terceiros. [Enshrouded MagicDamageClassifier][enshrouded] classifica DamageSource, sem converter tipo/dano ou fornecer mutador Asterism. A [Factory](https://github.com/Gustavaopere/minecraft-mod-factory/tree/518278ae9c0d264a537cc1bc6ee4974e01270fdf) permanece referência futura de tooling; nenhuma API é inferida da existência do repositório.

Preservar cast pai, caster/owner, entidade/UUID, tick/fase, target e consumerSpellID. Echo usa entidade Starcutter com tentativa0 e Swarm emite PiercingLight; isso pode separar ID de cast, ID de dano e causa pai. Estado compartilhado/tag ou efeito visual não é token causal completo. Não transformar foreach, seção de beam, DoT, summon AI ou retorno anti-magic em novo cast/mana/XP.

## Verificação e pendências

Identidade/class inventory binário é separado de fórmulas/causalidade source. A [auditoria histórica](TECHNICAL-AUDIT.md) recebe correções causais deste lote; cada ficha mantém defaults, contratos e casos de QA. Gateway continua conditional com aquisição implantada desconhecida, fora das dez identidades strict. Não promover por descrição, rarity, quality, defaults ou presença no registry.

**PENDING:** equivalência dos métodos/JAR/hosts, config/datapack implantado, Survival/cliente, multiplayer, claims/PvP/aliados, chunks/dimensões, sync, cancels/cleanup, persistência/restart e coexistência. CI/build/headless Black Arcana sem Asterism não homologa esses spells; nenhum Stage ou runtime foi promovido.

[modlist]: https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc/PROJECT-INSTRUCTIONS/modlist/modlist.md#L106
[modlist-loader]: https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc/PROJECT-INSTRUCTIONS/modlist/modlist.md#L41-L51
[registry]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/registries/ASARSpellRegistry.java#L18-L82
[attributes]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/registries/ASARAttributeRegistry.java#L19-L49
[school]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/registries/ASARSchoolRegistry.java#L44-L51
[damage-json]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/resources/data/asterismarcanum/damage_type/astral_magic.json#L1
[damage-registry]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/registries/ASARDamageTypes.java#L19-L29
[power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L211-L226
[entity-power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L234-L242
[mana]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L160-L173
[cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L338
[tick]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/MagicManager.java#L27-L90
[complete]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L411-L425
[magic-data]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/magic/MagicData.java#L107-L143
[entity-data]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/EntityCastData.java#L19-L28
[cast-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellOnCastEvent.java#L56-L70
[level-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/ModifySpellLevelEvent.java#L48-L54
[cooldown-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellCooldownAddedEvent.java#L42-L50
[damage-helper]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L64
[damage-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellDamageEvent.java#L13-L48
[teleport]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L167-L175
[teleport-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellTeleportEvent.java#L7-L18
[entity-teleport]: https://github.com/neoforged/NeoForge/blob/e0e7ab5d273fdc034f23fee7bf91c61ae39d3019/src/main/java/net/neoforged/neoforge/event/entity/EntityTeleportEvent.java#L31-L64
[respawn-event]: https://github.com/neoforged/NeoForge/blob/e0e7ab5d273fdc034f23fee7bf91c61ae39d3019/src/main/java/net/neoforged/neoforge/event/entity/player/PlayerRespawnPositionEvent.java#L29-L70
[summon-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellSummonEvent.java#L7-L27
[rpg]: https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc/src/main/java/dev/gustavopere/rpgskilltree/runtime/compat/irons/IronsSpellbookProgressionEvents.java#L26-L99
[enshrouded]: https://github.com/Gustavaopere/Enshrouded/blob/a41dbb51aacb94b7b5db6517f1514b0b7aee3e83/src/main/java/com/gustavaopere/enshrouded/api/combat/MagicDamageClassifier.java#L5-L8
