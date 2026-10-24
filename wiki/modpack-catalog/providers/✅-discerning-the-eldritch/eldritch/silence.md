# Silence

**Dossiê documental — 24/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`; lógica `SOURCE_PINNED / SOURCE_CAUSALITY`; integração `CONTRATO_CONDICIONAL`; QA físico `PENDING`. **+0 identidades / +0 strict**: efeito e callbacks pertencem à spell já contada.

## Identidade e proveniência

Provider **Discerning The Eldritch**, `mod_id=discerning_the_eldritch`; spell **`discerning_the_eldritch:silence`**, escola default `irons_spellbooks:eldritch`. Declarante `net.acetheeldritchking.discerning_the_eldritch.spells.eldritch.SilenceSpell`; [registry][registry] e [efeito registrado][effect-registry].

JAR físico histórico **`discerning_the_eldritch-1.4.4-1.21.jar`**, SHA-1 `cf35c225aced23b705d1e0fd1bc5c62d96540e0c`, publisher [CF8816497](https://www.curseforge.com/minecraft/mc-mods/discerning-the-eldritch/files/8816497), 22098930 bytes; [prova binária de registry](../EXACT-BINARY-SPELLS-1.4.4-1.21.md). Source oficial `AceTheEldritchKing/Discerning_The_Eldritch@7bbd81f902c65a4452f47656ebd948cae8cd5833`, versão 1.4.4-1.21, build NeoForge 21.1.244/Iron’s 3.16.2/Azure 3.1.0/Ace’s 1.2.7.2; pack Minecraft 1.21.1/NeoForge 21.1.250/Iron’s 3.16.3/Azure 3.1.11. Host consultado Iron’s `e4056af90302d37eb1739f5ff05020b020e6e252`. [Versões][versions], [build efetivo][build], [contratos comuns](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md). Identidade binária não prova igualdade integral de métodos/config/runtime. Metadata `mod_license=MIT` versus `TEMPLATE_LICENSE.txt` PolyForm Shield é conflito de sinais: fatos/paráfrases/permalinks, sem importar código/assets.

[Guia oficial][guide], parafraseado: impede temporariamente a criatura selecionada de iniciar spells. O executor localizado cancela o pre-cast de **ServerPlayer**, não demonstra bloquear universalmente AI, comandos ou todo cast de mobs. Sem override local de crafting/loot/learning; aplica política do host/escola. Aquisição concreta de scroll e Survival **NÃO VERIFICADOS**. [Elegibilidade][host-acquisition].

## Ingresso e pipeline causal

1. Legendary, níveis default 1–5, **LONG 80 ticks** base, cooldown 200 s. Wrapper jogador valida recursos/config, chama precondição e posta SpellPreCastEvent cancelável; ao resolver, SpellOnCastEvent precede débito e onCast. Sem recast próprio. [Defaults/ingresso][spell], [host][host-cast].
2. `SilenceSpell#checkPreCastConditions` chama `Utils#preCastTargetHelper(...,32,0.15F)`: ray desde o olho pelo olhar, blocos COLLIDER/Fluid.NONE, alvo mais próximo antes do bloco, inflação 0.15 blocks. Helper resolve LivingEntity/partes e casos de montaria, guarda UUID em TargetEntityCastData. Filtros base pickable/alive/!spectator; não há política local de equipe/PvP/claims. [Helper][target-helper], [ray][ray], [filtro][ray-filter].
3. `#onCast` resolve UUID no ServerLevel atual; se existe, solicita MobEffectInstance `silence_potion_effect` com duração `int(clamp(20P,20,140))`, **amplifier 1**, ambient/particles/icon=true. Não revalida range/LOS localmente; addEffect pode falhar e seu retorno é ignorado. Alvo perdido não recebe efeito, mas super.onCast segue, sem refund local. [Aplicação/duração][application], [UUID][target-data].
4. `ServerEvents#onPlayerCastEvent` cancela SpellPreCastEvent quando a entidade é ServerPlayer no servidor com Silence; exibe tempo e som. Não interrompe por si uma spell já em andamento. O mesmo método continua após cancelar e pode incrementar Insanity se configurado; tentativa cancelada não é efeito terminal/Mastery confirmado. Amplifier não é consultado no veto. [Consumer real][precast].
5. `SilencePotionEffect#fillEffectCures` não adiciona cures; isso não impede toda remoção. `KingsEffigyCurio#curioTick` solicita remover Silence a cada tick equipado. Separadamente, `SilenceSpell#canBeInterrupted(Player)` retorna `!KINGS_EFFIGY.isEquippedBy(player)` para quem lança a spell: não confundir resistência do caster à interrupção com proteção do alvo ao debuff. [Efeito][effect], [curio][effigy], [cast][spell].

## Matriz de parâmetros e alteração por perks

`L` = nível recebido; `C` = POWER_MULTIPLIER; `P=(1+(L−1))×SPELL_POWER×eldritchPower×C`. Mana `int((100+20(L−1))×MANA_MULTIPLIER)`. Duração tem truncamento após clamp. Defaults não são config implantada. [Fórmulas/atributos][host-power], [atributos][attributes].

| L default | Mana neutra | P neutro | Duração pedida ticks / s |
|---|---|---|---|
| 1 | 100 | 1 | 20 / 1 |
| 2 | 120 | 2 | 40 / 2 |
| 3 | 140 | 3 | 60 / 3 |
| 4 | 160 | 4 | 80 / 4 |
| 5 | 180 | 5 | 100 / 5 |

| Eixo | Valor, consumer e fase | Boundary e limite | QA |
|---|---|---|---|
| Nível / duração | `SilenceSpell#getEffectDuration`: int(clamp(20P,20,140)) ticks, hard bounds 1–7 s; amp 1 fixo. [Aplicação][application]. | spell_power/eldritch_spell_power **NATIVE_ATTRIBUTE**, C **CONFIG_NATIVE**. Mudar P atua até clamp; não muda range nem consumer do veto. Getter não é setter de duração. | Q1/Q2 |
| Mana / cooldown / recast | Mana acima; cooldown default 200 s = 4000 ticks antes de redução; sem recast/custo posterior. [Spell][spell], [host][host-cast]. | MANA_MULTIPLIER/cooldown **CONFIG_NATIVE**; SpellOnCastEvent#setManaCost/setSpellLevel são **HOOK_VERIFICADO** host pré-onCast, adapter **CONDITIONAL**. Admissão usa mana inicial, level alterado não recalcula custo. | Q1/Q2 |
| Cast / interrupção | LONG 80 ticks = 4 s base; host efetivo round(80×(2−softCap(CAST_TIME_REDUCTION))). Effigy impede a interrupção consultada por #canBeInterrupted. [Spell][spell], [host][host-power]. | Atributo de tempo nativo; curio é contrato existente, não boolean perk público. Outros cancelamentos/removal seguem host; não prometer imunidade total. | Q1/Q3 |
| Target / range / área | Um Living por ray 32 blocks / inflação 0.15, UUID atual; aplicação não é área. [Helper][target-helper], [UUID][target-data]. | Constantes locais sem setter de resolver/range. **⛔ SEM_HOOK_SEGURO** para alcance isolado, retarget e single→AOE; preservar claims/equipe/chunks. | Q2/Q3 |
| Status / bypass | Harmful silence, veto só no pre-cast jogador acima; amp não altera veto. Tag DTE bypass_abracadabra inclui Silence; Effigy remove por tick. [Efeito][effect], [tag][bypass], [effigy][effigy]. | MobEffect lifecycle/Applicable/remoção são downstream, não prova de aplicação aceita. **⛔ SEM_HOOK_SEGURO** para aumentar abrangência do bloqueio ou contornar cures/curio por perk. | Q2/Q4 |
| Dano / tipo / crítico / heal | A spell não chama hurt/heal nem cria DamageSource; efeito é controle. [Aplicação][application]. | Dano/DamageType/crítico/knockback **N/A**; SpellDamageEvent não é seam desta aplicação. Não criar dano extra como “mesma” spell. | Q4 |
| Projétil / summons / mundo | Sem entidade filha ofensiva, projétil, summon, mutação de bloco ou teleporte próprios. [Aplicação][application]. | Hitbox/speed/lifetime/pierce/explosão/AI/rollback **N/A**. VFX não é geometria ofensiva. | Q3/Q4 |
| Estado / autoria / cleanup | Effect no alvo, sem cast token/owner serializado próprio; TargetEntityCastData transitório host-owned. [Aplicação][application], [UUID][target-data]. | Refresh/merge/expire/cures/logout/restart dependem de Minecraft/host; **CONTRATO_CONDICIONAL**. Não manter segundo ledger anti-cast ou aplicar segunda punição/cooldown. | Q2/Q5 |

## Autoria, concepção e pendências

DTE/Minecraft possuem aplicação e lifecycle do status; Iron’s possui admissão/mana/cooldown. RPG Skill Tree deve correlacionar cast→UUID→aplicação aceita→eventos bloqueados, sem premiar cada tentativa proibida ou feedback como novo cast. BA/Enshrouded preservam suas autoridades, sem inferir bridge pelo nome Eldritch. Assinatura ocupada: controle de alvo único por debuff de anti-cast temporário; uma área original exige resolver/contrato próprios, não hook presumido desta spell.

- **Q1:** JAR/métodos/hosts/config, níveis/power negativos/extremos, clamp/truncamento, cooldown/mana/origens e tempo efetivo.
- **Q2:** miss/alvo removido/dimensão/range mudado, buff recusado/mesclado, sem refund/dupla cobrança; pre-cast cancelado com Insanity habilitado e dedupe.
- **Q3:** ray/bloco/multipart/montaria, PvP/aliados/claims, curio no caster/alvo, interrupção e cast já iniciado.
- **Q4:** Abracadabra e tag bypass, cures versus remoção Effigy, mobs/AI/comandos e caminhos que não postam pre-cast.
- **Q5:** dedicado/cliente/Survival, sync/expire/logout/morte/restart, attribution e Mastery. Todos **PENDING**, sem adapter/perk/runtime novo.

[versions]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/gradle.properties#L11-L30
[build]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/build.gradle#L175-L177
[host-power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L148-L258
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L332
[host-acquisition]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L630
[attributes]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/registry/AttributeRegistry.java#L25-L52
[precast]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/events/ServerEvents.java#L87-L191
[effect-registry]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/DTEPotionEffectRegistry.java#L11-L24
[registry]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/SpellRegistries.java#L41-L42
[guide]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/assets/discerning_the_eldritch/lang/en_us.json#L155-L156
[spell]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/eldritch/SilenceSpell.java#L29-L93
[application]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/eldritch/SilenceSpell.java#L95-L116
[effect]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/effects/SilencePotionEffect.java#L10-L18
[effigy]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/items/curios/KingsEffigyCurio.java#L27-L45
[bypass]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/data/discerning_the_eldritch/tags/mob_effect/bypass_abracadabra.json#L1-L6
[target-helper]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L665-L710
[target-data]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/TargetEntityCastData.java#L12-L39
[ray]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/RaycastBuilder.java#L20-L124
[ray-filter]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L459-L461
