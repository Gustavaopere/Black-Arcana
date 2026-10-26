# Ars Nouveau — Animate Block

Status: `SOURCE-PINNED 5.13.1 / GLYPH + SUMMON LIFECYCLE AUDITED / CONFIG + PHYSICAL QA PENDING`

- Registry id: `ars_nouveau:glyph_animate_block`.
- Classe: `com.hollingsworth.arsnouveau.common.spell.effect.EffectAnimate`.
- Release **5.13.1**; escolas Manipulation e Conjuration; tier default **II**; mana default **200**.
- Augments nativos: Extend Time e Reduce Time (`glyph_duration_down`), via `getSummonAugments()` [summon-augments].

## Contrato causal: bloco, entidade e retorno

No ramo de bloco, [EffectAnimate.onResolveBlock][animate] chama `EnchantedFallingBlock.canFall`: rejeita bloco vazio, fluido não vazio, tag `RELOCATION_NOT_SUPPORTED` e block entities diferentes de `MageBlockTile`/`SkullBlockEntity`; depois consulta harvest level e `destroyRespectsClaim` [can-fall]. Não é um animador irrestrito de qualquer inventário/NBT. A posição do novo summon é `(blockX+0,5,blockY,blockZ+0,5)`; salva o blockstate e `BlockEntity.saveWithoutMetadata` quando presente. **Invoca antes** de substituir o bloco pelo estado legado do fluido e não testa os retornos de spawn/setBlock nesse caminho. Não há transação atômica de conversão comprovada.

No ramo de entidade, só converte `EnchantedFallingBlock` ainda não removido. Copia state/blockData, movimento, marca `hurtMarked`, zera fall distance e descarta a entidade anterior. Essa entrada não repete `canFall`, claims ou validação do estado original [animate]. A Form seleciona o alvo; o glyph não fornece alcance, raio, projétil ou fan-out próprios. Os tipos AnimBlock/AnimHead registrados têm largura1,0 e altura1,5 blocos e tracking10; esse tamanho de entidade não é AOE do glyph [anim-type].

`animateBlock` escolhe `AnimHeadSummon` para `AbstractSkullBlock`, senão `AnimBlockSummon`; aplica cor, posição, contador, `shooter.getLastHurtMob`, tame/aggressive e `tame(player)` quando aplicável. Chama o helper `summonLivingEntity`, **sem chamar `canSummon` ou `applySummoningSickness`**. Portanto o gate normal de jogador real/sickness de outros summons não pode ser importado para Animate [animate] [summon-helper].

## Parâmetros e consumidor combatente

`T=(int)(20*(B+E*M))` ticks, `B=60` s e `E=60` s nos defaults, `M=stats.getDurationMultiplier()`: nominal **1200+1200M**, com truncamento Java e sem clamp final local [animate-config]. Valores de config têm mínimo zero, mas o saldo de duração pode tornar T não positivo. O estado de aprendizagem/casting depende da config; não usar defaults como teto efetivo [config-helper].

[AnimBlockSummon][combat] registra velocidade **0,3**, HP **4**, ATTACK_DAMAGE **2**; `getAttributeValue(ATTACK_DAMAGE)` adiciona a destroy speed do blockstate, com fallback1 apenas se a consulta lançar exceção. Isso é atributo de ataque do mob, não dano fixo do glyph ou `IDamageEffect.attemptDamage`; a aplicação final é herdada de `TamableAnimal/Mob` e seus eventos/resistências. Não inventar uma escala Amplify que o glyph não aceita. `doHurtTarget` barra alvo aliado ao owner resolvido e reduz **400 ticks** apenas se `super.doHurtTarget` retornar true. `canAttack` também veta o próprio owner UUID e summon com mesmo UUID.

Os goals incluem ataque/leap condicionados a `CAN_WALK`, FollowOwner com distâncias10/2, defesa do owner e alerta a outros AnimBlockSummon [combat] [melee-goal] [leap-goal]. O tick servidor decrementa T, incrementa AGE e libera `CAN_WALK` somente quando **AGE>20**; isso não é um cast time adicional universal. Ao expirar vivo, converte em falling block, remove e publica `SummonEvent.Death(didExpire=true)` [anim-life].

A morte por loot path chama retorno e `onSummonDeath(...,false)`; `getBaseExperienceReward=0`. O override `getOwner()` retorna null quando `dead`, portanto o retorno de um summon morto não garante atribuição ao owner original. `onDispel` apenas seta T=0 e retorna true, deixando a conversão ao tick posterior. Spawn, evento, dano e retorno são fases distintas; não premiar cada uma como outro cast [anim-death] [anim-dispel].

## Persistência e conversão: limites reais

`AnimBlockSummon` grava `head_data`, `left`, cor, ID numérico de blockstate, AGE, CAN_WALK e dropItem; `hasConverted` não aparece nesse save. Owner usa um `OWNER_UUID` sincronizado próprio, enquanto `tame(player)` pertence à herança; os save/read locais não persistem explicitamente esse campo próprio. Não afirmar sobrevivência coerente de todas as identidades de owner após reload [anim-owner] [anim-save].

O retorno ordinário possui guard `hasConverted`, cria `EnchantedFallingBlock` com state/owner/movimento/dropItem, desativa drop para MageBlock, mas **não atribui `head_data` a `fallingBlock.blockData`**. A presença de NBT no summon não garante restauração desse NBT no bloco final [anim-life]. O override de `AnimHeadSummon` cria `EnchantedSkull` e **copia `head_data`**, condiciona servidor/dropItem/state, porém não repete o guard `hasConverted` do método ordinário [head]. São dois contratos diferentes.

A entidade de queda tenta assentar conforme colisão/suporte, pode virar drop conforme gamerule/falha e só carrega blockData em block entity se a colocação tiver sucesso. Possui TTL de queda próprio (`time>600`, ou `>100` fora da altura), gravidade −0,04/tick e drag0,98; não é restauração garantida da posição original. A conversão de Animate passa resolver null e não estabelece o contexto de Rewind/Shaper nesse retorno [fall-life] [fall-place].

[SummoningFocus][focus] pode dobrar o contador e aplicar Strength500ticks/amplifier2 e Speed500ticks/amplifier1 **se** o listener resolver owner com esse Curio; o helper pode executar a receita restante num child context cujo caster é o summon. A correlação de owner e a execução de child não provam spawn aceito nem novo débito de mana [summon-helper].

## Aquisição e custos

Receita: `ars_nouveau:conjuration_essence` + `#c:obsidians` ×3 [recipe]. TierII/**55XP** de receita [xp], starter default **não** [starter]. [Aquisição85/85](../../ACQUISITION.md). Mana200 é default do componente; config, composição, descontos, admissão e pagamento permanecem Ars-owned [part] [resolve]. Duração, redução por ataque e tempo de queda não são cooldown.

## Certificação estática individual — 25/10/2026

| Campo | Contrato e limites |
|---|---|
| Identidade e versão | `ars_nouveau:glyph_animate_block`, EffectAnimate, Ars5.13.1; Manipulation/Conjuration, tierII. |
| Comportamento e causalidade | Bloco ou EnchantedFallingBlock → AnimBlock/AnimHeadSummon → combate/ticks → falling block; sem canSummon/sickness no glyph. |
| Parâmetros e caps | T=(int)(20*(60+60M)) default; ataques aceitos−400ticks; HP4/speed0,3/attack2+destroySpeed; sem clamp final de T. |
| Targeting e resultado | Um bloco elegível ou falling entity; claims no ingresso de bloco; sem área/range/dano instantâneo; owner/AI e retorno downstream. |
| Custos e aprendizagem | Mana200, tierII,55XP, conjuration essence+obsidian×3, starternão; custo efetivo da composição e config separados. |
| Integração e autoridade | Builder/eventos existem; duração, AI, owner, NBT e restauração exigem consumidores distintos; sem adapter RPG/Black Arcana validado, sem duplicar bloco/summon/Mastery. |
| Evidência e validação | Source pinado e109IDs/classes SHA-exatos; NOT_VERIFIED/NOT_TESTED; NBT salvo não equivale a restore/ownership provados em jogo. |

## Evidência, API e autoridade

**✅ `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Grau `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`: source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. A [auditoria compilada](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) comprova ID/classe, não equivalência integral dos métodos Java/bytecode, config instalada ou gameplay.

[SpellStats.Builder.build][builder] publica `SpellModifierEvent` depois dos augments/itens e devolve os stats do builder original; mutação *in-place* tem superfície pública real. Reatribuir `event.builder` não troca o objeto retornado. [EffectResolveEvent.Pre][event] permite veto; [o resolver][resolve] consulta cancelamento, mas não relê substituições de payload `spellStats`, `rayTraceResult`, `resolveEffect` ou `context` como novos locais. `Post` pode ser publicado em `STOP_ALL`/skip; não confirma captura, dano, spawn ou restauração bem-sucedidos.

Ars mantém casting, mana de jogador, aprendizagem e entidades/estados nativos. Source de mundo não é mana do jogador. RPG Skill Tree fornece progressão apenas por contrato comprovado; Black Arcana conserva seu próprio casting, Corruption, Strain, WorldEffectPolicy e causalidade; Enshrouded conserva seus efeitos ambientais. Nenhum tick, passageiro, alvo adicional, callback de morte ou contexto derivado é automaticamente outro cast pago ou crédito de Mastery. Adapter seguro, custos/caps configurados, listeners, claims/PvP, save/reload, multiplayer e QA físico continuam pendentes. Mudança de JAR, source, configuração ou consumidores exige reauditoria. Nenhum hook executável foi implementado nesta ficha.

[builder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L152
[resolve]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L220-L279
[event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/EffectResolveEvent.java#L11-L50
[part]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L127-L150
[starter]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L307-L310
[xp]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L142-L157
[animate]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectAnimate.java#L26-L68
[animate-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectAnimate.java#L70-L105
[can-fall]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EnchantedFallingBlock.java#L130-L139
[anim-type]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/ModEntities.java#L283-L293
[combat]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/AnimBlockSummon.java#L80-L139
[anim-life]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/AnimBlockSummon.java#L141-L172
[anim-death]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/AnimBlockSummon.java#L192-L233
[anim-owner]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/AnimBlockSummon.java#L174-L189
[anim-owner-api]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/AnimBlockSummon.java#L235-L244
[anim-save]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/AnimBlockSummon.java#L299-L333
[anim-dispel]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/AnimBlockSummon.java#L342-L361
[head]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/AnimHeadSummon.java#L23-L53
[fall-life]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EnchantedFallingBlock.java#L188-L232
[fall-place]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EnchantedFallingBlock.java#L235-L319
[summon-helper]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractEffect.java#L69-L89
[summon-augments]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractEffect.java#L225-L231
[focus]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/curios/SummoningFocus.java#L66-L98
[melee-goal]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/goal/ConditionalMeleeGoal.java#L8-L19
[leap-goal]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/goal/ConditionalLeapGoal.java#L8-L19
[config-helper]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractEffect.java#L162-L176
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L120-L121
