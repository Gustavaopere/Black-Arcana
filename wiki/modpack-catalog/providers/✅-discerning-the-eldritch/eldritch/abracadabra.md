# Abracadabra

**Dossiê documental — 24/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`; lógica `SOURCE_PINNED / SOURCE_CAUSALITY`; integração `CONTRATO_CONDICIONAL`; QA físico `PENDING`. **+0 identidades / +0 strict**: efeito e callbacks pertencem à spell já contada.

## Identidade e proveniência

Provider **Discerning The Eldritch**, `mod_id=discerning_the_eldritch`; spell **`discerning_the_eldritch:abracadabra`**, escola default `irons_spellbooks:eldritch`. Declarante `net.acetheeldritchking.discerning_the_eldritch.spells.eldritch.AbracadabraSpell`; [registry][registry] e [efeito registrado][effect-registry].

JAR físico histórico **`discerning_the_eldritch-1.4.4-1.21.jar`**, SHA-1 `cf35c225aced23b705d1e0fd1bc5c62d96540e0c`, publisher [CF8816497](https://www.curseforge.com/minecraft/mc-mods/discerning-the-eldritch/files/8816497), 22098930 bytes; [prova binária de registry](../EXACT-BINARY-SPELLS-1.4.4-1.21.md). Source oficial `AceTheEldritchKing/Discerning_The_Eldritch@7bbd81f902c65a4452f47656ebd948cae8cd5833`, versão 1.4.4-1.21, build NeoForge 21.1.244/Iron’s 3.16.2/Azure 3.1.0/Ace’s 1.2.7.2; pack Minecraft 1.21.1/NeoForge 21.1.250/Iron’s 3.16.3/Azure 3.1.11. Host consultado Iron’s `e4056af90302d37eb1739f5ff05020b020e6e252`. [Versões][versions], [build efetivo][build], [contratos comuns](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md). Identidade binária não prova igualdade integral de métodos/config/runtime. Metadata `mod_license=MIT` versus `TEMPLATE_LICENSE.txt` PolyForm Shield é conflito de sinais: fatos/paráfrases/permalinks, sem importar código/assets.

[Guia oficial][guide], parafraseado: proteção própria com teto de dano por sequência recebida e prevenção de novos efeitos nocivos. Não é imunidade absoluta nem limpeza dos debuffs já instalados. Sem override local de aquisição/crafting/loot; segue política host/escola; rota Survival/config efetiva **NÃO VERIFICADAS**. [Elegibilidade][host-acquisition].

## Pipeline causal e duas defesas distintas

1. Legendary, níveis default 1–5, INSTANT 0 ticks, cooldown 75 s. Wrapper jogador: admissão/pre-cast cancelável → SpellOnCastEvent/custo → onCast → cooldown conforme origem/config. Sem recast local. `#onCast` solicita effect `abracadabra_potion_effect` em self por `int(20P)` ticks, amp `L−1`, ambient/particles=false e icon=true; ignora retorno de addEffect. [Spell][spell], [host][host-cast].
2. `AbracadabraPotionEffect#damageCapEvent(LivingDamageEvent.Pre)` exige config enableDamageCap, efeito presente e source **sem BYPASSES_INVULNERABILITY**. Lê **getOriginalDamage**, calcula `clamp(original,0,baseCap/(amp+1))`, chama setNewDamage. Não usa getNewDamage, logo não preserva automaticamente reduções ou ajustes anteriores. [Handler/helper][cap], [fase NeoForge][damage-phase].
3. Essa fase NeoForge ocorre após armor/potion reductions, antes de HP e absorption downstream; não confundir com evento SpellDamageEvent do helper Iron’s. Abracadabra reintroduz como input o valor original disponível no container. Ordem de listeners, fontes especiais e composição precisam QA; não afirmar “só reduz dano” em toda composição nem que evita qualquer morte. Tooltip converte cap a int e apresenta sinal de porcentagem, mas o cálculo usa **health points absolutos por evento**, sem divisão pela vida máxima. [Cap/tooltip][cap], [fase][damage-phase], [lang][tooltip].
4. `#preventHexes(MobEffectEvent.Applicable)` exige enableHexPrevention, Abracadabra presente e categoria HARMFUL. Sem tag bypass, seta DO_NOT_APPLY; **com tag bypass, seta APPLY**, não simplesmente DEFAULT. Isso pode sobrepor a decisão default de canBeAffected se for a última decisão; outros listeners ainda participam. Não remove status anteriores. [Handler][hex], [API/result][effect-api].
5. Tag source `discerning_the_eldritch:bypass_abracadabra` contém Silence; datapacks podem ampliar/substituir. Não há limpeza, periodicidade própria ou ledger por agressor/hit. Expiração/merge/remove do efeito é Minecraft-owned. [Tag][bypass], [efeito][cap].

## Matriz de parâmetros e alteração por perks

`P=(3+2(L−1))×SPELL_POWER×eldritchPower×POWER_MULTIPLIER`. Mana `int((75+15(L−1))×MANA_MULTIPLIER)`. Config **COMMON** `discerning_the_eldritch-common.toml`, apesar do nome DTEServerConfig; defaults enableDamageCap=true, baseCap=80, enableHexPrevention=true, copiados para campos em onLoad. Não são valores observados do servidor nem setters por jogador. [Fórmulas][host-power], [config][config], [carregamento][config-load], [registro][config-registration].

| L default | Mana neutra | P neutro | Duração ticks / s | Amp / teto default por evento |
|---|---|---|---|---|
| 1 | 75 | 3 | 60 / 3 | 0 / 80 HP |
| 2 | 90 | 5 | 100 / 5 | 1 / 40 HP |
| 3 | 105 | 7 | 140 / 7 | 2 / 26.666… HP |
| 4 | 120 | 9 | 180 / 9 | 3 / 20 HP |
| 5 | 135 | 11 | 220 / 11 | 4 / 16 HP |

| Eixo | Valor, consumer e fase | Boundary e limite | QA |
|---|---|---|---|
| Nível / power / duração | `AbracadabraSpell#onCast/#getEffectDuration`: int(20P) ticks; amp L−1, sem clamp próprio. [Spell][spell]. | spell_power/eldritch_spell_power **NATIVE_ATTRIBUTE**, power config **CONFIG_NATIVE**. P muda duração; L também muda teto por amp. Não existe setter independente de duração/amplificador nesta spell. | Q1/Q2 |
| Teto / dano recebido | `AbracadabraPotionEffect#getDamageCapAmount`: clamp(original,0,baseCap/(amp+1)); hard ceiling default80/L HP apenas no ramo elegível. [Cap][cap]. | Base/enable **CONFIG_NATIVE** global. LivingDamageEvent.Pre#setNewDamage é **HOOK_VERIFICADO** da fase, não hook isolado de Abracadabra; adapter/ordem **CONDITIONAL**. Não empilhar outro cap por perk sem contrato. | Q2/Q3 |
| Tipo / bypass / autoria | Source mantém DamageType/owner; BYPASSES_INVULNERABILITY exclui cap. Spell não causa dano próprio. [Cap][cap]. | Setter de amount não converte DamageType nem altera autoria. Conversão **⛔ SEM_HOOK_SEGURO**; dano ofensivo/crítico/knockback próprio **N/A**. | Q3 |
| Hex / targeting / área | Self e evento Applicable de cada effect novo/merge; HARMFUL sem tag bloqueado, tagged força APPLY. Sem área/target remoto. [Hex][hex], [API][effect-api]. | Tag/config **CONFIG_NATIVE** global; event result mutável **HOOK_VERIFICADO**, integração **CONDITIONAL** ao ordering. Não prova remover efeitos ativos nem partilhar proteção em área. Single→AOE **⛔ SEM_HOOK_SEGURO**. | Q2/Q4 |
| Mana / cooldown / cast | INSTANT 0 ticks; mana acima; default75 s=1500 ticks; sem charges/recast ou custo por hit bloqueado. [Spell][spell], [host][host-cast]. | MANA_MULTIPLIER/cooldown **CONFIG_NATIVE**; SpellOnCastEvent setters de mana/level são seams reais pré-onCast, mas level alterado não recalcula custo/admissão. Adapter **CONDITIONAL**. | Q1/Q2 |
| Projétil / summons / mundo | Nenhum projétil/summon/teleporte/mutação de bloco ou DOT próprio. [Spell][spell]. | Range ofensivo/hitbox/speed/lifetime/pierce/spread/explosão/AI/rollback **N/A**; tamanho VFX não define proteção. | Q4 |
| Estado / lifecycle / persistência | Beneficial MobEffect com amp/timer; sem cast token/ledger por dano ou estado adicional da classe. [Spell][spell], [efeito][cap]. | Merge/expire/cures/remove/logout/restart host-owned; não converter tempo de buff em budget de HP absorvido. **CONTRATO_CONDICIONAL** de persistência/sync. | Q2/Q5 |

## Autoria, concepção e pendências

DTE possui essas duas defesas; Minecraft/NeoForge possui applicability/damage container e lifecycle. RPG Skill Tree só modifica por seam real antes do resultado, sem novo listener que replique defesa ou ledger de “dano salvo” inferido do tooltip. BA/Enshrouded não recebem autoridade de tipo, Shroud ou proteção por afinidade temática. Correlacionar cast→instância de buff→sequência de dano/applicability, sem premiar cada cap/hex rejeitado como novo cast. Assinatura ocupada: teto absoluto por dano recebido + veto a efeitos nocivos; proteção compartilhada é concepção original pendente de resolver próprio.

- **Q1:** JAR/hosts/config COMMON efetiva, L/power/amplificador externos, duração truncada, mana/cooldown/CastSource.
- **Q2:** addEffect recusado/mesclado, expire/remove, eventos de cast e custos/dedupe, vários danos no mesmo tick.
- **Q3:** original versus newDamage com armor/potions/resist/listeners, absorption, dano zero/negativo/extremo, bypass/kill/fonte direta, teto exato e HP final.
- **Q4:** harmful/beneficial, Silence tag, APPLY versus DEFAULT, debuff anterior, datapacks e ordem de listeners; sem cleanses/AOE inferidos.
- **Q5:** cliente/dedicado/Survival/multiplayer/claims, reload/logout/morte/restart/sync e Mastery. Todos **PENDING**, sem runtime/perk/adapter novo.

[versions]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/gradle.properties#L11-L30
[build]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/build.gradle#L175-L177
[host-power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L148-L258
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L332
[host-acquisition]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L630
[attributes]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/registry/AttributeRegistry.java#L25-L52
[precast]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/events/ServerEvents.java#L87-L191
[effect-registry]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/DTEPotionEffectRegistry.java#L11-L24
[registry]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/SpellRegistries.java#L71-L72
[guide]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/assets/discerning_the_eldritch/lang/en_us.json#L191-L192
[spell]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/eldritch/AbracadabraSpell.java#L22-L79
[cap]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/effects/AbracadabraPotionEffect.java#L21-L71
[hex]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/effects/AbracadabraPotionEffect.java#L73-L95
[bypass]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/data/discerning_the_eldritch/tags/mob_effect/bypass_abracadabra.json#L1-L6
[tooltip]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/assets/discerning_the_eldritch/lang/en_us.json#L236
[config]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/utils/DTEServerConfig.java#L37-L51
[config-load]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/utils/DTEServerConfig.java#L134-L145
[config-registration]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/DiscerningTheEldritch.java#L84-L85
[damage-phase]: https://github.com/neoforged/NeoForge/blob/e0e7ab5d273fdc034f23fee7bf91c61ae39d3019/src/main/java/net/neoforged/neoforge/event/entity/living/LivingDamageEvent.java#L34-L83
[effect-api]: https://github.com/neoforged/NeoForge/blob/e0e7ab5d273fdc034f23fee7bf91c61ae39d3019/src/main/java/net/neoforged/neoforge/event/entity/living/MobEffectEvent.java#L100-L162
