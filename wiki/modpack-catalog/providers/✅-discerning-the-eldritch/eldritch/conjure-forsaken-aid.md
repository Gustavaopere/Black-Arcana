# Conjure: Forsaken Aid

**Dossiê documental — 24/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`; lógica `SOURCE_PINNED / SOURCE_CAUSALITY`; mutabilidade `CONTRATO_CONDICIONAL`; QA físico `PENDING`. **+0 identidades/+0 strict**: criaturas e seus ataques são consequências desta spell.

## Identidade, descrição e ingresso

Spell **`discerning_the_eldritch:conjure_forsaken_aid`**, escola default `irons_spellbooks:eldritch`; declarante `net.acetheeldritchking.discerning_the_eldritch.spells.eldritch.ConjureForsakenAidSpell`. O nome do campo registrar `CONJURE_FORSAKE_AID` não muda o ID. [Registro][registry], [spell][spell].

Provider **Discerning The Eldritch**, `mod_id=discerning_the_eldritch`; Minecraft 1.21.1 / NeoForge no pack. JAR histórico `discerning_the_eldritch-1.4.4-1.21.jar`, SHA-1 `cf35c225aced23b705d1e0fd1bc5c62d96540e0c`, publisher [CurseForge 8816497](https://www.curseforge.com/minecraft/mc-mods/discerning-the-eldritch/files/8816497), 22098930 bytes. [Prova histórica de identidade](../EXACT-BINARY-SPELLS-1.4.4-1.21.md), sem equiparar todos os métodos ou configs ao source.

Source oficial `AceTheEldritchKing/Discerning_The_Eldritch@7bbd81f902c65a4452f47656ebd948cae8cd5833`, versão declarada 1.4.4-1.21. Build Iron’s 3.16.2 / NeoForge 21.1.244 / Azure 3.1.0 / Ace’s 1.2.7.2; pack Iron’s 3.16.3 / NeoForge 21.1.250 / Azure 3.1.11 / Ace’s 1.2.7.2. Host consultado Iron’s `e4056af90302d37eb1739f5ff05020b020e6e252`. `mod_license=MIT` versus TEMPLATE_LICENSE PolyForm Shield são sinais conflitantes: fatos/paráfrases/permalinks, sem importar implementação/assets. [Versão][versions], [contratos e proveniência comuns](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md). Config implantada, equivalência de métodos/JAR e compatibilidade física permanecem **PENDING**.

[Guia oficial][guide], parafraseado: conjura um grupo de seres Eldritch para auxiliar o caster. Legendary, níveis default 1–8. A spell não sobrescreve gates de aprendizagem/crafting/loot; o host aplica a escola Eldritch, que exige aprendizagem e tem loot genérico false, além da config. Lead específico: `BlackBookSpellbook` instala Forsaken Aid L3; a tabela do Ascended One tem um pool de um roll entre Black Book e Staff of Ascension. Isso não garante obter o livro nem fecha a rota Survival/config implantada. [Host][host-acquisition], [escola][eldritch-school], [preset][black-book], [loot][book-loot].

## Pipeline causal e parâmetros

Defina `L`=nível entregue ao `onCast`, `P=(10+5×(L−1))×SPELL_POWER×ELDRITCH_SPELL_POWER×POWER_MULTIPLIER`. `T=(int)(400P)` ticks, truncamento final; **20P segundos** nominais. Power aumenta o timer, sem reescrever HP/AttackDamage dos minions neste spell. [Defaults/cast][spell], [host][host-formulas].

| L default | Mana neutra | P neutro | Pedidos de spawn | T ticks / segundos |
|---|---|---|---|---|
| 1 | 100 | 10 | 1 | 4000 / 200 |
| 2 | 110 | 15 | 2 | 6000 / 300 |
| 3 | 120 | 20 | 3 | 8000 / 400 |
| 4 | 130 | 25 | 4 | 10000 / 500 |
| 5 | 140 | 30 | 5 | 12000 / 600 |
| 6 | 150 | 35 | 6 | 14000 / 700 |
| 7 | 160 | 40 | 7 | 16000 / 800 |
| 8 | 170 | 45 | 8 | 18000 / 900 |

1. LONG, cast base 30 ticks (1.5 s), efetivo `round(30×(2−softCap(CAST_TIME_REDUCTION)))`; cooldown default 100 s = 2000 ticks antes de modifiers. Mana `int((100+10×(L−1))×MANA_MULTIPLIER)`. No wrapper jogador, admissão/pre-cast antecedem `SpellOnCastEvent`, débito e `onCast`; recast ativo não é debitado novamente nesse wrapper. [Defaults][spell], [fórmulas][host-formulas], [ordem][host-cast].
2. Sem recast ativo, `#onCast` cria `SummonedEntitiesCastData`, resolve T e executa `i<L`: uma solicitação por iteração. Cada X/Z é eye position do caster + Gaussian×3; Y é eyeY. **3 não é raio máximo**: não há clamp das caudas, teste de chão, LOS, espaço livre, loaded chunk, claims ou distância máxima neste método. Com recast ativo, o corpo não cria outro grupo. [Cast][cast].
3. `#spawnForsakenAid` sorteia `isMaw<0.65`, `isApostle<0.25` e `isBase<0.75`, depois escolhas aninhadas. Sob draws uniformes independentes, probabilidades finais derivadas: **Maw 60.9375%, Behemoth 32.8125%, Apostle 6.25%**. Não são três chances exclusivas de 65/25/75%. Os três candidatos são construídos, mas apenas o selecionado é posicionado/postado. [Seleção][spawn].
4. Publica `SpellSummonEvent(caster,candidate,spellId,L)`, usa `getCreature()` em `addFreshEntity` e depois `SummonManager.initSummon(caster,result,T,castData)`. O boolean de spawn é ignorado. Construtores locais com argumento owner apenas delegam ao tipo; a associação real é feita pelo manager, que posta SetSummonOwnerEvent e adiciona UUID/timer/castData. [Spawn][spawn], [evento][summon-event], [manager][manager-init].
5. Cria `RecastInstance(id,L,2,T,source,castData)`: **2 casts totais**, inicial + um manual; constructor guarda remaining=1. Cast inicial não decrementa o recast recém-criado. Manual finaliza recast e o helper despawna os UUIDs resolvidos no level atual; timeout deixa o manager executar expiração. COUNTERSPELL força recast de volta; helper ainda retorna true nesse ramo. Talisman pode suprimir cooldown no TIMEOUT. `onRecastFinished` só chama super/addCooldown quando o helper retorna true. [Callback][callback], [constructor][recast], [wrapper][host-cast], [helper][manager-finish].
6. Manager testa a heap **a cada 20 ticks** e expira quando expirationServerTick **<** currentTick; T não prova instante exato de remoção. Morte/remoção, lookup entre dimensões, logout/reload e UUIDs não resolvidos são contratos do host; castData armazena UUIDs/maxHealthPool, não um novo cast por criatura. [Expiração][manager-expiry], [castData][cast-data], [persistência][manager-persist], [reload][manager-reload].

## Minions e dano downstream

| Filho nativo | Defaults de atributo / geometria | Consumer e limite |
|---|---|---|
| Sightless Maw | HP30, AttackDamage5.5, follow range45 blocks, interaction range2, movement attribute0.45; tipo0.6×1.8 blocks. | `#registerGoals` owner-hurt/copy target, follow owner, mordidas animadas; `#doHurtTarget` usa `Utils.doMeleeAttack` com source desta spell, direto=minion/causador=getSummoner. [Maw][maw], [tipo][entity-types]. |
| Untold Behemoth | HP65, AttackDamage8, knockback0.2, armor5, follow45, interaction2, movement0.25; tipo0.6×1.8. | Melee e goal com Stomp Iron’s; esses child spells têm consumers próprios, não herdam automaticamente ID/dano da raiz. [Behemoth][behemoth], [tipo][entity-types]. |
| The Apostle | HP40, AttackDamage15.5, follow45, interaction3, movement/flying0.25, SPELL_POWER1.1/SPELL_RESIST1.1; tipo0.6×1.8. | WizardAttackGoal/SpellBarrageGoal com spells Iron’s, owner targeting/follow. `finalizeSpawn` ativa noGravity, **mas o spawn da spell não chama finalizeSpawn**: voo efetivo não foi fechado por esse detalhe. [Apostle][apostle], [tipo][entity-types]. |

Factories são ligadas em [CommonSetup][attributes-setup]; valores não são stats finais garantidos após eventos/modifiers. Melee lê AttackDamage, aplica enchantments e helper de dano; Living+SpellDamageSource publica SpellDamageEvent antes de resist/friendly/hurt. Fonte Eldritch default `irons_spellbooks:eldritch_magic`; não confundir atributo AttackDamage com dano final ou todos ataques filhos. Minions implementam IMagicSummon: owner via manager, antiMagic→onUnSummon e descarte servidor; handlers de hurt/allied e friendly-fire têm lógica própria. [Melee][melee-helper], [dano][damage-helper], [factory][host-source], [escola][eldritch-school], [interface][summon-interface].

No `DamageSources#preHitEffects` do host, em LivingIncomingDamageEvent, directEntity IMagicSummon (ou causando IMagicSummon) resolve owner: se UUID do owner coincide com a vítima, cancela; senão, owner Living multiplica o amount pelo atributo **SUMMON_DAMAGE**. Este é input nativo real adicional para o dano elegível dos minions, distinto de P/AttackDamage; não prova scaling de todo ataque filho sem seguir sua fonte. [Consumer][summon-damage].

## Matriz de alteração para perks

| Eixo | Valor / método / fase | Boundary real, limite e estado | QA |
|---|---|---|---|
| Nível / count / caps | `ConjureForsakenAidSpell#onCast`: L pedidos no cast inicial, default max8; sem cap local além do loop. [Cast][cast]. | `SpellOnCastEvent#setSpellLevel(int)` host **HOOK_VERIFICADO**, adapter **CONTRATO_CONDICIONAL**; L muda count e T juntos e não recalcula custo já calculado. Sem setter independente de count/seleção. Budget e clamp precisam contrato; não duplicar grupo. | Q1/Q2 |
| Power / duração | P e T acima; `#onCast` faz snapshot. [Cast][cast], [host][host-formulas]. | Atributos spell/eldritch power **NATIVE_ATTRIBUTE**, POWER_MULTIPLIER **CONFIG_NATIVE**; afetam timer, não stats de minion nesta classe. `SummonManager#setDuration(Entity,int)` existe, mas adiciona entrada à heap, não remove automaticamente anterior: alterar duração em runtime é **CONTRATO_CONDICIONAL**, não garantia de extensão. | Q1/Q4 |
| Mana / cooldown / tempo | LONG30, mana/cooldown acima, recast2/T. [Spell][spell], [host][host-cast]. | MANA_MULTIPLIER/cooldown **CONFIG_NATIVE**, CAST_TIME_REDUCTION nativo; `SpellOnCastEvent#setManaCost` pré-débito e cooldown Pre host reais sob contrato comum. Sem refund local por spawn recusado; não segunda mana no recast. | Q1/Q2 |
| Range / targeting / área | Spawn Gaussian×3 por eixo; AI resolve targets depois, follow45 não é alcance do cast nem um raio ofensivo. [Spawn][spawn], [AI][maw]. | Sem resolver remoto ou setter próprio de Gaussian/target/área. **⛔ SEM_HOOK_SEGURO** para retarget/perk de alcance ou single→AOE; claims/chunks/friendly precisam autoridade. | Q2/Q3 |
| HP / AI / summon replacement | Valores da tabela; `SpellSummonEvent#setCreature(K)` pré-spawn é mutável, não cancelável. [Evento][summon-event], [spawn][spawn]. | **HOOK_VERIFICADO** para candidate/atributos e replacement compatível. Publisher `#spawnForsakenAid`: getCreature offset189 → **CHECKCAST AbstractSpellCastingMob192**; LivingEntity arbitrária é incompatível. Adapter **CONTRATO_CONDICIONAL**, preservar spawn→init/timer/AI/owner. | Q2/Q4 |
| Dano / tipo / crítico / push | Melee via AttackDamage/enchantments/helper; incoming elegível multiplica por SUMMON_DAMAGE do owner Living. Demais spells de AI próprias. [Melee][melee-helper], [consumer][summon-damage], [Apostle][apostle]. | SUMMON_DAMAGE **NATIVE_ATTRIBUTE** nesse caminho; amount de SpellDamageEvent é mutável só no helper. Fonte/caster podem ser minion/owner, não caster puro. Conversão de tipo **⛔ SEM_HOOK_SEGURO**. Crítico extra local **N/A**; knockback vem do atributo/helper. | Q3/Q4 |
| Projétil / hitbox / velocidade | Raiz não lança projétil; entidades0.6×1.8, atributos de movimento não garantem blocks/tick. [Tipos][entity-types], [AI][apostle]. | Resize/spread/pierce da raiz **N/A**; mudanças de dimensão/AI/speed ou dos projéteis filhos exigem seam próprio, **⛔ SEM_HOOK_SEGURO** por analogia a AbstractMagicProjectile. | Q3/Q4 |
| Estado / persistência / mundo | CastData UUIDs/maxHealthPool e manager owner/expirations/offlineNBT; sem custo de item, mutação de bloco ou rollback local. [CastData][cast-data], [save][manager-persist]. | DTE/Iron’s são owners; owner fields/NBT locais não substituem mapas. Hooks não criam ledger RPG paralelo; cleanup/relog/restart/dimensão **PENDING**. | Q4/Q5 |

A prova estreita de CHECKCAST usa JDK21 `javap -c -p` na classe publisher do fingerprint acima; não equipara o método inteiro ao source nem homologa integração física.

## Autoria, concepção e QA

Correlacionar cast pai→recast/castData→UUID minion→ataque/child spell→vítima/resultado, sem Mastery por cada spawn/tick/ataque como nova spell. RPG Skill Tree possui progressão/perks; Black Arcana seu runtime/world safety; Enshrouded mantém seus efeitos. DTE/Iron’s continuam donos de AI, mana, cooldown, stats e cleanup.

Assinatura ocupada: grupo aleatório de minions com AI distinta e janela de dispensa por recast. Uma nova magia original pode propor seleção explícita/budget por papéis, mas não é mutador já disponível desta spell.

- **Q1:** config física, L1–8/evento fora de faixa, power/tempo/truncamento, mana/cooldown/CastSource e aprendizagem.
- **Q2:** recast manual/timeout/counterspell/talisman, spawn negado/parcial, replacement compatível/incompatível, gaussianas/chão/parede/loaded chunk e sem segunda cobrança.
- **Q3:** AI/targets/aliados/PvP/claims, melee versus spells filhos, owner/tipo/dano real, follow e voo do Apostle sem finalizeSpawn.
- **Q4:** timer/heap duplicada, owner alterado, minion morto/unloaded/dimensão/relog, castData removido/serializado e cleanup/atribuição.
- **Q5:** dedicado/cliente, aquisição Black Book/loot, multiplayer/orçamento de entidades, restart/sync e dedupe. **Todos PENDING**; sem adapter/perk/runtime novo.

[versions]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/gradle.properties#L10-L25
[host-formulas]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L148-L257
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L305-L347
[host-acquisition]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L612
[host-source]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L560-L565
[eldritch-school]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/registry/SchoolRegistry.java#L138-L148
[summon-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellSummonEvent.java#L7-L39
[manager-init]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/SummonManager.java#L63-L135
[manager-finish]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/SummonManager.java#L142-L179
[manager-expiry]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/SummonManager.java#L294-L320
[manager-persist]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/SummonManager.java#L239-L290
[manager-reload]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/SummonManager.java#L330-L377
[cast-data]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/SummonedEntitiesCastData.java#L18-L84
[recast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/RecastInstance.java#L27-L35
[melee-helper]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L475-L497
[damage-helper]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L64
[summon-interface]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/mobs/IMagicSummon.java#L22-L85
[attributes-setup]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/events/CommonSetup.java#L25-L37
[registry]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/SpellRegistries.java#L41-L53
[spell]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/eldritch/ConjureForsakenAidSpell.java#L23-L59
[cast]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/eldritch/ConjureForsakenAidSpell.java#L74-L98
[spawn]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/eldritch/ConjureForsakenAidSpell.java#L100-L123
[callback]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/eldritch/ConjureForsakenAidSpell.java#L62-L72
[guide]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/assets/discerning_the_eldritch/lang/en_us.json#L173-L174
[black-book]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/items/spellbooks/BlackBookSpellbook.java#L11-L25
[book-loot]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/data/discerning_the_eldritch/loot_table/entities/ascended_one.json#L121-L132
[maw]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/mobs/sightless_maw/SightlessMawEntity.java#L91-L160
[behemoth]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/mobs/untold_behemoth/UntoldBehemothEntity.java#L54-L145
[apostle]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/mobs/eldritch_caster/TheApostleEntity.java#L80-L180
[entity-types]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/DTEEntityRegistry.java#L78-L103
[summon-damage]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L114-L130
