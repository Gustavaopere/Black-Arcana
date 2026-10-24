# Mend Flesh

**Dossiê documental — 24/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`; lógica `SOURCE_PINNED / SOURCE_CAUSALITY`; integração `CONTRATO_CONDICIONAL`; QA físico `PENDING`. **+0 identidades / +0 strict**: efeito e callbacks pertencem à spell já contada.

## Identidade e proveniência

Provider **Discerning The Eldritch**, `mod_id=discerning_the_eldritch`; spell **`discerning_the_eldritch:mend_flesh`**, escola default `irons_spellbooks:eldritch`. Declarante `net.acetheeldritchking.discerning_the_eldritch.spells.eldritch.MendFleshSpell`; [registry][registry] e [efeito registrado][effect-registry].

JAR físico histórico **`discerning_the_eldritch-1.4.4-1.21.jar`**, SHA-1 `cf35c225aced23b705d1e0fd1bc5c62d96540e0c`, publisher [CF8816497](https://www.curseforge.com/minecraft/mc-mods/discerning-the-eldritch/files/8816497), 22098930 bytes; [prova binária de registry](../EXACT-BINARY-SPELLS-1.4.4-1.21.md). Source oficial `AceTheEldritchKing/Discerning_The_Eldritch@7bbd81f902c65a4452f47656ebd948cae8cd5833`, versão 1.4.4-1.21, build NeoForge 21.1.244/Iron’s 3.16.2/Azure 3.1.0/Ace’s 1.2.7.2; pack Minecraft 1.21.1/NeoForge 21.1.250/Iron’s 3.16.3/Azure 3.1.11. Host consultado Iron’s `e4056af90302d37eb1739f5ff05020b020e6e252`. [Versões][versions], [build efetivo][build], [contratos comuns](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md). Identidade binária não prova igualdade integral de métodos/config/runtime. Metadata `mod_license=MIT` versus `TEMPLATE_LICENSE.txt` PolyForm Shield é conflito de sinais: fatos/paráfrases/permalinks, sem importar código/assets.

[Guia oficial][guide], parafraseado: cura inicial e estado temporário que permite recuperar vida por ataques e experiência. O consumer de hit usa **1.5 HP fixos**, não porcentagem do dano, e a cura XP usa o amount do evento dividido por 2. Sem override local de aquisição/crafting/loot; política de escola/host, scroll Survival e config implantada **NÃO VERIFICADOS**. [Elegibilidade][host-acquisition].

## Três caminhos de cura, sem confundir evento com mutador

1. Legendary, default níveis 1–3, INSTANT 0 ticks, cooldown 30 s. Wrapper jogador verifica ingresso/pre-cast, anuncia SpellOnCastEvent, debita conforme origem/config e executa onCast antes de cooldown. Sem recast/canal/recurso extra local. [Spell][spell], [host][host-cast].
2. `MendFleshSpell#onCast` calcula `H=P/3.5` health points, publica **SpellHealEvent(caster,caster,H,school)** e chama **entity.heal(H)** com a variável local. `SpellHealEvent` não é cancelável; healAmount é final e só tem getter. Esse evento é **observer**, não setter de heal, e o post não comprova HP restaurado. Depois solicita `mend_flesh_potion_effect` por `int(20P)` ticks/amp0 e ignora retorno; 8 partículas circulares/r0.25 são apresentação. [Aplicação/helpers][application], [evento host][heal-event].
3. `ServerEvents#livingDamageEventPost(LivingDamageEvent.Post)` resolve **source.getEntity()**, exige causingEntity Living com buff e flag mendFleshLifesteal, solicita heal(1.5F). Não exige SpellDamageSource, melee, escola, amount positivo, kill ou caster jogador. DirectEntity sozinha não substitui o causador. Handler recebe fase Post pós-HP; não reexecuta dano. Partículas e som acompanham tentativa, não confirmam cura aceita. [Consumer e guardas][hit-heal], [fase NeoForge][damage-post].
4. `ServerEvents#onExperienceGainedEvent(PlayerXpEvent.XpChange)` exige buff/flag mendFleshEXPGain e solicita heal(float(event.getAmount())/2). Não testa amount>0 ou confirmação final de XP. XpChange é cancelável/mutável; sem receiveCanceled explícito, não afirmar que recebe evento já cancelado; listeners posteriores podem mudar/cancelar XP após este handler. Não limitar o trigger a orb pickup, pois o evento corresponde a giveExperiencePoints. [XP consumer][xp-heal], [API][xp-event].
5. `MendFleshPotionEffect` apenas declara categoria BENEFICIAL; os heals reativos estão nos handlers globais. Não há tick de cura contínua, intervalo interno/cooldown por alvo/cast, heal-source token ou ledger nativo para os heals. Flags COMMON default true afetam **só caminhos reativos**; o heal inicial não testa essas flags. [Efeito][effect], [config][config], [onLoad][config-load], [registro COMMON][config-registration].

## Matriz de parâmetros e alteração por perks

`P=(5+(L−1))×SPELL_POWER×eldritchPower×POWER_MULTIPLIER`. Mana `int((30+5(L−1))×MANA_MULTIPLIER)`. Duração trunca ao int; valores neutros pressupõem todos multiplicadores 1. [Host][host-power], [atributos][attributes], [helpers][application].

| L default | Mana neutra | P neutro | Heal inicial tentado HP | Buff ticks / s |
|---|---|---|---|---|
| 1 | 30 | 5 | 5/3.5 ≈ 1.42857 | 100 / 5 |
| 2 | 35 | 6 | 6/3.5 ≈ 1.71429 | 120 / 6 |
| 3 | 40 | 7 | 2 | 140 / 7 |

| Eixo | Valor, consumer e fase | Boundary e limite | QA |
|---|---|---|---|
| Power / heal inicial | `#getHealAmount=P/3.5`, onCast servidor solicita heal local; sem cap próprio de H, HP final é downstream. [Aplicação][application]. | spell_power/eldritch_spell_power **NATIVE_ATTRIBUTE**, POWER_MULTIPLIER **CONFIG_NATIVE**. SpellHealEvent é **HOOK_VERIFICADO SOMENTE OBSERVAÇÃO**; sem setter/cancel, **⛔ SEM_HOOK_SEGURO** de amount independente por esse evento. | Q1/Q2 |
| Duração / amp | `#getEffectDuration=int(20P)` ticks, amp0, sem periodicidade da effect class. [Aplicação][application], [efeito][effect]. | P altera H e duração ao mesmo tempo; level events host têm efeitos correlacionados. Getter privado não é API de duração. **CONTRATO_CONDICIONAL** para adapter de buff. | Q1/Q2 |
| Heal pós-dano | `#livingDamageEventPost`: causingLiving+buff+flag → heal1.5HP por Post elegível; não é 1.5×dano nem 1.5%. [Consumer][hit-heal]. | Flag COMMON **CONFIG_NATIVE** global, sem setter de 1.5/ICD por jogador. Post é observer do dano, não mutador seguro deste heal. **⛔ SEM_HOOK_SEGURO** de heal/rate independente. | Q2/Q3 |
| Heal XP | `#onExperienceGainedEvent`: amount/2HP, sem clamp positivo/ICD local. [Consumer][xp-heal], [API][xp-event]. | Flag COMMON **CONFIG_NATIVE**. XpChange#setAmount/int cancelam/alteram XP global, não só heal; não usar como setter isolado da cura. Adapter **CONDITIONAL**, **⛔ SEM_HOOK_SEGURO** deste H sem mudar recurso XP. | Q3/Q4 |
| Mana / cooldown / cast | INSTANT0, mana acima, default30s=600ticks; sem custo por proc, recast/charge/canal próprio. [Spell][spell], [host][host-cast]. | Config mana/cooldown nativa; SpellOnCastEvent#setManaCost/setSpellLevel pré-onCast **HOOK_VERIFICADO**, adapter **CONDITIONAL**. Mana inicial de admissão não recalculada por novo L. | Q1/Q2 |
| Target / range / área | Initial heal/buff self; heals posteriores no causingLiving ou player XP, sem seleção por range/LOS/área local. VFX8/r0.25 não curam vizinhos. [Aplicação][application], [consumers][hit-heal]. | Range/target remoto **N/A** no cast atual; self→grupo/retarget **⛔ SEM_HOOK_SEGURO**, sem segundo heal paralelo. | Q2/Q4 |
| Dano / tipo / projétil / summons | Spell não produz dano/DamageSource, projétil, DOT, knockback ou summon. Ataques externos só fornecem trigger. [Spell][spell], [hit][hit-heal]. | Conversão DamageType/crítico/hitbox/speed/lifetime/pierce/AI **N/A**. Não inferir lifesteal SpellDamageSource percentual ou entidade ofensiva da apresentação. | Q3/Q4 |
| Estado / mundo / persistência | Beneficial effect; nenhum bloco/teleporte/rollback ou estado serializado adicional próprio. Effect refresh/expire/remove é host-owned. [Efeito][effect], [aplicação][application]. | Sem token ligando cada heal ao cast inicial; não manter heal/XP ledger RPG paralelo. Cleanup/sync/restart **CONTRATO_CONDICIONAL**. | Q2/Q5 |

## Autoria, concepção e pendências

DTE decide os três heals; Minecraft decide a aplicação final à vida; Iron’s possui admissão/mana/cooldown e anúncio de heal inicial. RPG Skill Tree deve diferenciar cast inicial, Post externo e XPChange, sem dar crédito por partículas ou evento anterior à aceitação da cura. BA/Enshrouded preservam suas autoridades sem segunda cura/progressão. Assinatura ocupada: heal inicial + sustain fixo no hit e proporcional à alteração de XP durante um buff. Uma cura transacional com budget explícito é lacuna de concepção, não API disponível aqui.

- **Q1:** JAR/hosts/config COMMON, L/power/H/duração truncada, CastSource/mana/cooldown e heal em vida máxima.
- **Q2:** heal/buff cancelado/recusado/mesclado por terceiros, healing modifiers/HP real, cast→buff→proc e dedupe sem dupla cobrança/XP.
- **Q3:** melee/spell/projétil, causing versus directEntity, dano zero/mitigado/kill e múltiplos Post no tick; sem assumir um heal por ataque visual.
- **Q4:** XP positivo/zero/negativo/extremo, mudanças/cancelamentos posteriores, giveExperiencePoints sem orb e config flags on/off sem afetar heal inicial.
- **Q5:** dedicado/cliente/Survival/multiplayer, sync/expire/morte/logout/restart/cleanup e attribution. Todos **PENDING**; sem perk/adapter/runtime novo.

[versions]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/gradle.properties#L11-L30
[build]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/build.gradle#L175-L177
[host-power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L148-L258
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L332
[host-acquisition]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L630
[attributes]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/registry/AttributeRegistry.java#L25-L52
[precast]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/events/ServerEvents.java#L87-L191
[effect-registry]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/DTEPotionEffectRegistry.java#L11-L24
[registry]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/SpellRegistries.java#L60-L61
[guide]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/assets/discerning_the_eldritch/lang/en_us.json#L179-L180
[spell]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/eldritch/MendFleshSpell.java#L28-L76
[application]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/eldritch/MendFleshSpell.java#L79-L104
[effect]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/effects/MendFleshPotionEffect.java#L6-L10
[heal-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellHealEvent.java#L18-L40
[hit-heal]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/events/ServerEvents.java#L207-L265
[xp-heal]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/events/ServerEvents.java#L525-L546
[config]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/utils/DTEServerConfig.java#L17-L24
[config-load]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/utils/DTEServerConfig.java#L134-L145
[config-registration]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/DiscerningTheEldritch.java#L84-L85
[damage-post]: https://github.com/neoforged/NeoForge/blob/e0e7ab5d273fdc034f23fee7bf91c61ae39d3019/src/main/java/net/neoforged/neoforge/event/entity/living/LivingDamageEvent.java#L86-L131
[xp-event]: https://github.com/neoforged/NeoForge/blob/e0e7ab5d273fdc034f23fee7bf91c61ae39d3019/src/main/java/net/neoforged/neoforge/event/entity/player/PlayerXpEvent.java#L42-L60
