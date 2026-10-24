# Otherworldly Presence

**Dossiê documental — 24/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`; lógica `SOURCE_PINNED / SOURCE_CAUSALITY`; integração `CONTRATO_CONDICIONAL`; QA físico `PENDING`. **+0 identidades / +0 strict**: efeito e callbacks pertencem à spell já contada.

## Identidade e proveniência

Provider **Discerning The Eldritch**, `mod_id=discerning_the_eldritch`; spell **`discerning_the_eldritch:otherworldly_presence`**, escola default `irons_spellbooks:eldritch`. Declarante `net.acetheeldritchking.discerning_the_eldritch.spells.eldritch.OtherworldlyPresenceSpell`; [registry][registry] e [efeito registrado][effect-registry].

JAR físico histórico **`discerning_the_eldritch-1.4.4-1.21.jar`**, SHA-1 `cf35c225aced23b705d1e0fd1bc5c62d96540e0c`, publisher [CF8816497](https://www.curseforge.com/minecraft/mc-mods/discerning-the-eldritch/files/8816497), 22098930 bytes; [prova binária de registry](../EXACT-BINARY-SPELLS-1.4.4-1.21.md). Source oficial `AceTheEldritchKing/Discerning_The_Eldritch@7bbd81f902c65a4452f47656ebd948cae8cd5833`, versão 1.4.4-1.21, build NeoForge 21.1.244/Iron’s 3.16.2/Azure 3.1.0/Ace’s 1.2.7.2; pack Minecraft 1.21.1/NeoForge 21.1.250/Iron’s 3.16.3/Azure 3.1.11. Host consultado Iron’s `e4056af90302d37eb1739f5ff05020b020e6e252`. [Versões][versions], [build efetivo][build], [contratos comuns](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md). Identidade binária não prova igualdade integral de métodos/config/runtime. Metadata `mod_license=MIT` versus `TEMPLATE_LICENSE.txt` PolyForm Shield é conflito de sinais: fatos/paráfrases/permalinks, sem importar código/assets.

[Guia oficial][guide], parafraseado: desloca o caster e concede temporariamente estado que impede causar/receber dano. O source também veta novo cast de ServerPlayer; são consumers distintos e o veto de dano foi localizado em LivingIncomingDamageEvent. Não altera noPhysics/collision do caster nesta spell. Sem override local de aquisição/crafting/loot; Survival e configuração efetiva **NÃO VERIFICADOS**. [Elegibilidade][host-acquisition].

## Teleporte, resultado e estado posterior

1. Legendary, default níveis1–3, INSTANT0ticks, cooldown10s. Sem recast próprio, precondição/target helper ou onServerPreCast override local. Wrapper Iron’s faz admissão/custo/pre-cast e executa onCast no servidor. [Spell][spell], [host][host-cast].
2. `#onCast` faz cast explícito de AdditionalCastData para **TeleportSpell.TeleportData**. Null segue fallback; objeto de outro tipo não tem instanceof guard local. Se data/destino existem, usa posição fornecida; senão chama `TeleportSpell#findTeleportLocation(level,caster,getDistance(...))`. A spell não produz esse TeleportData localmente nem demonstra quem o preenche em todos ingressos; setup externo e compatibilidade permanecem condicionados. [Fluxo][application], [data host][teleport-data].
3. Fallback host traça bloco pelo olhar sem fluid, usa largura/altura do caster, ajuste de ledge até3blocks/air/LOS e clip para baixo. Isso é solver geométrico, não prova de autorização de claims, loaded chunks, piso seguro ou troca de dimensão. Destino fornecido externamente não é limitado novamente pelo range local. [Solver][solver].
4. Em ambos caminhos chama `Utils#handleSpellTeleport`: posta SpellTeleportEvent, consome coords possivelmente alteradas e chama teleportTo se não cancelado; boolean retornado significa **canceled**. DTE ignora esse retorno. Depois stopRiding se passageiro, resetFallDistance e solicita `metaphysical_potion_effect` por200ticks/amp0, icon=true, ambient/particles=false. Buff pode ser pedido mesmo sem chegada; addEffect também tem retorno ignorado. [Aplicação][application], [helper][teleport-helper], [evento][teleport-event].
5. `ServerEvents#onPlayerCastEvent` veta SpellPreCastEvent apenas de ServerPlayer no servidor com Metaphysical, exibe feedback. Insanity é processado antes desse ramo, sem early return por cancelamento próprio. Não afirmar cancelamento de todo cast de AI/comandos ou interrupção retroativa de cast já iniciado. [Pre-cast][precast].
6. **Dano localizado:** `ServerEvents#livingIncomingDamageEvent` cancela incoming se vítima tem Metaphysical **ou source.getEntity() é Living com Metaphysical**. Usa causingEntity, não qualquer directEntity. Sem whitelist de tipo/escala/quantidade local. Fase é pós-checks de invulnerabilidade, antes de processamento/mitigação; não cobre mudanças de vida que não postem esse evento. O handler continua para outros ramos depois de cancelar, sem demonstrar ausência de todo side effect. [Veto de dano][damage-veto], [fase][incoming].
7. `MetaphysicalPotionEffect` só declara categoria BENEFICIAL; não possui tick/action/owner/cast token adicionais. Expiração/merge/remove/persistência e sync são do host/Minecraft. Não confundir com mudança de dimensão, invisibilidade ou intangibilidade geométrica. [Effect][effect].

## Matriz de parâmetros e alteração por perks

Defina `B=12+4(L−1)`, `C=POWER_MULTIPLIER`, `A=SPELL_POWER×eldritchPower`, `S(x)=x` se x≤1.5, senão `2−0.25/(x−1)`. **Range fallback `R=B×C×S(C×A)` blocks**: host #getEntityPowerMultiplier inclui C e #getSpellPower(L,null) também inclui C. Não simplificar para B×S(A) quando C≠1. Nenhum clamp não-negativo/teto absoluto local de R; a assíntota de S não limita B/C ou nível externo por si. [DTE getter][application], [host power][host-power], [soft-cap][soft-cap]. Mana `int((40+10(L−1))×MANA_MULTIPLIER)`.

| L default | Mana neutra | B / range fallback neutro | Metaphysical |
|---|---|---|---|
| 1 | 40 | 12 blocks | 200 ticks /10 s, amp0 |
| 2 | 50 | 16 blocks | 200 ticks /10 s, amp0 |
| 3 | 60 | 20 blocks | 200 ticks /10 s, amp0 |

| Eixo | Valor, consumer e fase | Boundary e limite | QA |
|---|---|---|---|
| Power / range | `#getDistance` R acima, lido só no fallback; destination preexistente passa sem novo clamp local. [Aplicação][application], [solver][solver]. | spell_power/eldritch_spell_power **NATIVE_ATTRIBUTE**, C **CONFIG_NATIVE**, com soft-cap/dobro de participação de C. Não é setter de destino arbitrário; bounded adapter **CONDITIONAL**. | Q1/Q2 |
| Target / destino / área | Self→posição do TeleportData ou solver pelo olhar; sem seleção de vítima/área. [Fluxo][application]. | SpellTeleportEvent herda setTargetX/Y/Z e cancel, consumidos pré-teleport **HOOK_VERIFICADO**. Mutação exige validar claims/chunks/collision; não retarget outro Entity nem cria AOE por esse evento. **⛔ SEM_HOOK_SEGURO** de grupo/dimensão. [API][teleport-coords]. | Q2/Q3 |
| Tempo / estado | Buff literal200ticks, amp0; P não altera timer. INSTANT0, cooldown10s=200ticks são relógios independentes. [Spell][spell], [aplicação][application]. | Config/atributo cooldown nativos, timer do buff constante sem setter DTE identificado. **⛔ SEM_HOOK_SEGURO** para duração isolada/renovar por perk sem contrato de MobEffect. | Q1/Q4 |
| Dano / tipo / defesa | Não causa dano; incoming veto source-agnostic se vítima/causingLiving buffados. Cast pre-event é outro consumer. [Veto][damage-veto], [fase][incoming]. | Incoming cancelável é **HOOK_VERIFICADO** genérico, não setter exclusivo de invulnerabilidade Metaphysical. Sem nova fonte/crit/knockback; conversão DamageType **N/A** aqui. Não trocar veto por segundo dano/cura. | Q3/Q4 |
| Mana / cast / recast | Mana acima, cast instantâneo, sem cobrança por veto de dano, recast ou charge próprios. [Spell][spell], [host][host-cast]. | Config mana/cooldown **CONFIG_NATIVE**; SpellOnCastEvent setters pré-onCast **HOOK_VERIFICADO**, integração **CONDITIONAL**. Level alterado não recalcula custo nem prova chegada; sem refund por veto local. | Q1/Q2 |
| Projétil / summon / geometria | Sem projétil/summon/área ofensiva ou resize do caster; solver usa AABB existente. [Aplicação][application], [solver][solver]. | Hitbox/speed/lifetime/pierce/AI/explosion **N/A**. Nome “Metaphysical” não cria noclip/física nova. | Q3/Q4 |
| Mundo / movimento / rollback | handleSpellTeleport altera posição, depois desmonta/reseta fallDistance mesmo se cancelado. Sem bloco/ritual/rollback local. [Fluxo][application], [helper][teleport-helper]. | Coordenadas mutáveis/veto não formam transação entre chegada+buff+montaria. **CONTRATO_CONDICIONAL**, não criar retorno/fallback BA ou ponte WorldEffectPolicy presumida. | Q2/Q3 |
| Autoria / cleanup / persistência | Beneficial effect sem owner/cast ledger próprio; veto outgoing depende causingEntity atual, não root cast salvo. [Effect][effect], [veto][damage-veto]. | Dedupe cast→tentativa→posição real→effect→incoming; lifecycle host-owned e sync/restart **PENDING**. SetTargetPosition público do castdata não é callback pré-cast seguro universal. | Q4/Q5 |

## Autoria, concepção e pendências

DTE possui buff/vetos, Iron’s possui castdata/helper/custo e Minecraft posição/effect lifecycle. RPG Skill Tree não deve creditar chegada por evento pré-teleport nem tratar cada hit cancelado como Mastery. BA/Enshrouded preservam suas autoridades sem duplicar transação de movimento ou defesa. Assinatura ocupada: teleporte próprio + janela neutra de dano/anti-cast; transporte de grupo com confirmação atômica é concepção distinta que exige runtime próprio.

- **Q1:** JAR/métodos/hosts/config, L/C/A/soft-cap extremos, range fallback versus tooltip, cooldown/mana e CastSource.
- **Q2:** null/data incorreto/data externo, destino bloqueado/chunk/dimensão, cancel/coords alteradas, posição real/buff após veto, sem refund/dupla execução.
- **Q3:** ledges/air/LOS/AABB, montaria/fallDistance, claims/PvP/aliados, eventos que mudam/cancelam e nenhuma intangibilidade inferida.
- **Q4:** effect recusado/mesclado/expirado/removido, pre-cast ServerPlayer versus AI, fonte sem causingLiving/projétil órfão, tipo bypass e caminhos fora de incoming; zero side effects não presumido.
- **Q5:** Survival/cliente/dedicado/multiplayer, sync/logout/morte/restart/persistência e dedupe. Todos **PENDING**, sem adapter/perk/runtime novo.

[versions]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/gradle.properties#L11-L30
[build]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/build.gradle#L175-L177
[host-power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L148-L258
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L332
[host-acquisition]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L630
[attributes]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/registry/AttributeRegistry.java#L25-L52
[precast]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/events/ServerEvents.java#L87-L191
[effect-registry]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/DTEPotionEffectRegistry.java#L11-L24
[registry]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/SpellRegistries.java#L57-L58
[guide]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/assets/discerning_the_eldritch/lang/en_us.json#L167-L168
[spell]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/eldritch/OtherworldlyPresenceSpell.java#L21-L58
[application]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/eldritch/OtherworldlyPresenceSpell.java#L60-L96
[effect]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/effects/MetaphysicalPotionEffect.java#L6-L10
[damage-veto]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/events/ServerEvents.java#L419-L441
[incoming]: https://github.com/neoforged/NeoForge/blob/e0e7ab5d273fdc034f23fee7bf91c61ae39d3019/src/main/java/net/neoforged/neoforge/event/entity/living/LivingIncomingDamageEvent.java#L15-L28
[teleport-data]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/TeleportSpell.java#L153-L172
[solver]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/TeleportSpell.java#L109-L130
[teleport-helper]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L167-L174
[teleport-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellTeleportEvent.java#L7-L18
[teleport-coords]: https://github.com/neoforged/NeoForge/blob/e0e7ab5d273fdc034f23fee7bf91c61ae39d3019/src/main/java/net/neoforged/neoforge/event/entity/EntityTeleportEvent.java#L31-L65
[soft-cap]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L177-L185
