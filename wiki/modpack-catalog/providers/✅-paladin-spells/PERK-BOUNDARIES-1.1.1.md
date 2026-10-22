# Paladin Spells 1.1.1 — boundaries para os três projetos

Reauditoria documental de 22/10/2026 em Black Arcana base `01c42361d4c9a6fd581745b33ffdb84b4464406c`. Source Paladin `31f64ccdb39d062b21cc25d434cb62d6463b486e`; RPG `ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc`; Enshrouded `a41dbb51aacb94b7b5db6517f1514b0b7aee3e83`; Factory `518278ae9c0d264a537cc1bc6ee4974e01270fdf`. Nenhum runtime alterado.

## Medição deste lote

**5/5 fichas com matriz de campos, símbolos source-pinned e consumidores downstream reexaminados.** Isto mede a presença da reauditoria documental de todas as identidades registradas, não cinco integrações homologadas. Parâmetros ainda desconhecidos continuam explícitos. +0 identidades mágicas; mínimo global e campanha binária 38/39 preservados. Sem denominador técnico global fechado.

| Ficha | Consumidor importante | Limite para perk |
|---|---|---|
| [Taunt](holy/taunt.md) | TauntEffect#applyEffectTick força aggro por UUID | P amplia alcance e duração simultaneamente; sem segundo loop |
| [Bulwark](holy/bulwark.md) | BulwarkEffect declara modifier de armor 0.0 | amplifier/duração não comprovam armor entregue |
| [Sworn Protector](holy/sworn-protector.md) | SwornProtectorEvent#onLivingHurt | source onCast cliente; consulta AABB +64 antes do range 36–90; anti-recursão não é cast token |
| [Bedrock Skin](holy/bedrock-skin.md) | BedrockSkinEvent#onLivingDamage em LivingDamageEvent.Pre | consumidor existe; não duplicar redução; testar ordem e âncora |
| [Ram](holy/ram.md) | hurt(mobAttack), knockback e ImpulseCastData | Holy não converte mobAttack em DamageType mágico; seleção não prova dano entregue |

## RPG Skill Tree — contratos existentes, sem nova implementação

- [IronsInvestmentAttributePolicy](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc/src/main/java/dev/gustavopere/rpgskilltree/runtime/compat/irons/IronsInvestmentAttributePolicy.java#L15): exige Iron's `1.21.1-3.16.3` exato. Targets: `max_mana`, `mana_regen`, `spell_power` no namespace Iron's.
- [IronsInvestmentAttributesRuntime](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc/src/main/java/dev/gustavopere/rpgskilltree/runtime/compat/irons/IronsInvestmentAttributesRuntime.java#L34): `public static void refresh(ServerPlayer player, AttributeRanks ranks)`. Servidor; remove modifier estável antes de reaplicar. MAX_MANA usa ADD_VALUE; mana regen/spell power usam ADD_MULTIPLIED_TOTAL. Não seta fields de spells nem cobra mana.
- [IronsInvestmentCooldownEvents](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc/src/main/java/dev/gustavopere/rpgskilltree/runtime/compat/irons/IronsInvestmentCooldownEvents.java#L21): `public static void onCooldownPre(SpellCooldownAddedEvent.Pre event)`, LOWEST. Exige evento não cancelado, ServerPlayer elegível, não FakePlayer/creative/spectator, CastSource que respeita cooldown, versão exata e Determination investida ≥10; chama setEffectiveCooldown conforme policy. Não é hook de cast time, duração de buff ou cooldown de outro provider.
- [IronMasterySourcePolicy](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc/src/main/java/dev/gustavopere/rpgskilltree/runtime/compat/irons/IronMasterySourcePolicy.java#L5): `counts(boolean creative, boolean spectator, boolean fakePlayer, String castSource)` é package-private e limita fonte a SPELLBOOK/SCROLL após exclusões. Não chamar por adapter externo como API pública nem tratar cast elegível como acerto/kill.

Esses símbolos provam boundaries no source atual do RPG. Não foi executado teste RPG+Paladin nesta sessão; inscrição efetiva dos listeners e comportamento no modpack não são promovidos a PASS. Perks específicas só podem usar seam compatível com o campo e com a autoridade do provider. Alterar spell power pode mudar mais de um parâmetro; não chamar isso bônus puro de dano/raio.

## Evento de cast, callbacks e Mastery no host 3.16.3

Source Iron's `e4056af90302d37eb1739f5ff05020b020e6e252`, sem alegação de equivalência integral source→JAR. No ingresso de jogador via [`AbstractSpell#castSpell`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L305), a ordem é: construir/postar `SpellOnCastEvent` → debitar mana conforme fonte/recast/creative usando o custo do evento → invocar override `onCast` com **nível do evento** → tratar recast/cooldown → enviar `OnClientCastPacket` com **nível original do argumento**. Custo/cooldown não ficam sob responsabilidade de `super.onCast`.

[`AbstractSpell#onCast`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L362) base contém debug e `playSound(getCastFinishSound(), entity)`. Logo a ausência de chamada ao super nos overrides Taunt/Bulwark/Bedrock/Ram não suprime o evento, débito ou cooldown daquele ingresso. Não compensar esses passos em outro adapter. Para INSTANT, [`MagicManager#tick`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/MagicManager.java#L55) chama `castSpell`, tenta remover scroll quando aplicável e chama `onServerCastComplete` depois; isso também independe de `super.onCast`. Ingressos alternativos de entidades/adapters não foram homologados por essa análise do caminho de jogador.

O RPG [`IronsSpellbookProgressionEvents#onSpellCast`](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc/src/main/java/dev/gustavopere/rpgskilltree/runtime/compat/irons/IronsSpellbookProgressionEvents.java#L79) escuta esse evento em LOWEST, filtra fonte/jogador e chama `awardMastery`. Portanto ele observa a prática de cast **antes do efeito**: não prova dano entregue, alvo encontrado ou ativação server de Sworn Protector. Não conceder uma segunda recompensa como se esse evento representasse acerto. Interferência de outros listeners e comportamento no pack continuam QA.

A API [`SpellOnCastEvent#setSpellLevel(int)`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellOnCastEvent.java#L56) e [`setManaCost(int)`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellOnCastEvent.java#L68) é uma superfície mutadora source-confirmada antes do débito/efeito nesse ingresso. Não é setter isolado de raio, DamageType, alvo ou hitbox. O evento nasce com custo do nível original; alterar nível não recalcula automaticamente esse custo, e o pacote cliente continua com o nível original. Qualquer perk nesses setters exige clamp, política de custo e teste de sincronização; nenhum adapter foi implementado aqui.

Não generalizar esse wrapper para comandos ou mobs: [`CastCommand`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/command/CastCommand.java#L62) e [`AbstractSpellCastingMob`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/mobs/abstract_spell_casting_mob/AbstractSpellCastingMob.java#L282) têm caminhos que chamam `onCast` diretamente. Evento de jogador e seus gates/recompensas não são universais para todo efeito com a mesma identidade de spell.

## Enshrouded e Factory

[MagicDamageClassifier](https://github.com/Gustavaopere/Enshrouded/blob/a41dbb51aacb94b7b5db6517f1514b0b7aee3e83/src/main/java/com/gustavaopere/enshrouded/api/combat/MagicDamageClassifier.java) declara `MagicDamageClassification classify(DamageSource source)`. É classificação, não API mutadora. Não há bridge de Paladin comprovada por essa interface. Ram usa mobAttack; atribuição mágica, exposure, progresso e procs precisam de prova causal antes de integração.

A [Factory](https://github.com/Gustavaopere/minecraft-mod-factory/tree/518278ae9c0d264a537cc1bc6ee4974e01270fdf) permanece authority de ferramentas reutilizáveis; [VERSION-AUTHORITY](https://github.com/Gustavaopere/minecraft-mod-factory/blob/518278ae9c0d264a537cc1bc6ee4974e01270fdf/skills/VERSION-AUTHORITY.md) prioriza runtime, modlist/JAR e source exato. Nenhuma modificação ou migração de infraestrutura é necessária para este lote documental.

## Correção e proveniência

O README, TECHNICAL-AUDIT e a ficha Bedrock Skin afirmavam ausência de consumidor de redução. `events/BedrockSkinEvent.java` no próprio pin lê a constante de BedrockSkinEffect, o que invalida a afirmação de consumidor ausente. O [catálogo agregado anterior](../../../../docs/catalog/PALADIN-SPELLS-1.1.1.md) já descrevia o consumidor corretamente. Corrigir a documentação não valida ordem de listeners nem dano final no JAR instalado.

Source upstream declara NeoForge 21.1.200/Iron's 3.14.7; alvo Black Arcana é NeoForge 21.1.248/Iron's 3.16.3. Identidade dos cinco IDs no JAR foi comprovada historicamente, sem prova de igualdade integral source→classfiles. LICENSE.txt é CC BY-NC-SA 4.0 e gradle.properties declara All Rights Reserved: divergência preservada, sem copiar código/arte. As fichas usam resumos de semântica e símbolos para consulta.

## QA pendente

JAR runtime, configuração implantada, Survival/scrolls, server/client, ordem de eventos, equip/unequip, reload/restart, geometria/LOS/PvP e coexistência permanecem PENDING. Stage e campanhas físicas não avançam. Usar as matrizes de cada ficha como roteiro; não emular silenciosamente efeitos faltantes.
