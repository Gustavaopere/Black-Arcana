# Soul Slice

**Dossiê documental — 24/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`; lógica `SOURCE_PINNED / SOURCE_CAUSALITY`; integração `CONTRATO_CONDICIONAL`; QA físico `PENDING`. **+0 identidades/+0 strict**: efeitos, entidades e fases derivados não são novas spells.

## Identidade e proveniência

Provider **Discerning The Eldritch**, `mod_id=discerning_the_eldritch`, JAR físico histórico **`discerning_the_eldritch-1.4.4-1.21.jar`**, SHA-1 `cf35c225aced23b705d1e0fd1bc5c62d96540e0c`; [publisher CF8816497](https://www.curseforge.com/minecraft/mc-mods/discerning-the-eldritch/files/8816497), [prova estática de identidade](../EXACT-BINARY-SPELLS-1.4.4-1.21.md). Source oficial `AceTheEldritchKing/Discerning_The_Eldritch@7bbd81f902c65a4452f47656ebd948cae8cd5833`. Build Iron’s 3.16.2/NeoForge 21.1.244/Azure 3.1.0 versus pack Iron’s 3.16.3/NeoForge 21.1.250/Azure 3.1.11; Ace 1.2.7.2 coincide na versão declarada, sem prova de ABI. Host lido Iron’s `e4056af90302d37eb1739f5ff05020b020e6e252`. Versão declarada não equipara métodos source↔JAR. Sinais MIT/PolyForm Shield conflitantes: fatos/paráfrases/permalinks, sem importar implementação/assets. [Versões][versions], [contratos comuns](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md).

Spell **`discerning_the_eldritch:soul_slice`**, escola default `irons_spellbooks:fire`, Legendary, nível default **1**; declarante `net.acetheeldritchking.discerning_the_eldritch.spells.fire.SoulSliceSpell`. [Defaults][spell]. [Guia oficial][guide], parafraseado: corte frontal de Soul Fire que pode gastar almas para reforçar dano. O texto “por cast” não substitui o consumo **por vítima** observado abaixo.

Crafting/player crafting/loot retornam false. **Lead de obtenção:** SoulFireScytheItem instala Soul Slice1 e Soul Set Ablaze1; receita smithing combina decrepit_scythe+soul_ember+timeless_slurry. Isso localiza uma rota source, sem assegurar obtenção de ingredientes, casting efetivo ou Survival PASS. [Gates][gates], [arma][scythe], [receita][recipe].

## Valores e pipeline causal

`P=(35+1(L−1))×SPELL_POWER×FIRE_SPELL_POWER×POWER_MULTIPLIER`, `W=Utils#getWeaponDamage(caster)` e **`D=P+W` HP**, ou D+2 no ramo com ≥2 stacks. W usa ATTACK_DAMAGE atual, retorno0 sem bônus sobre atributo base e Sharpness quando aplicável, não só o número do item. Neutro L1: P35, mana75, D35+W ou37+W; nível máximo default1 não autoriza extrapolação. [Dano][damage], [power][host-power], [weapon][weapon].

1. **Casting:** LONG10ticks=0.5s base; override `#getEffectiveCastTime` retorna getCastTime, **bypassando CAST_TIME_REDUCTION** neste caminho. `canBeInterrupted=false` não é imunidade a morte/removal ou toda interrupção externa. Cooldown default25s/500ticks; mana `int((75+15(L−1))×MANA_MULTIPLIER)`. Sem recast local. Admissão→SpellOnCastEvent→débito conforme origem→onCast seguem host jogador. [Tempo/gates][gates], [wrapper][host-cast].
2. **Alvos:** `SoulSliceSpell#onCast` consulta caixa **6.5×3.25×6.5 blocks** centrada em `casterPos+(0,.3×altura,0)+forward×1.9`. Exige alvo Living/alive, distância ao caster<3.25, frente pelos dot de posição e centro versus olho, e LOS. `isPickable` é testado no **caster**, não no alvo. Sem máximo/ordenação local de alvos. [Query][hit].
3. **Consumo por vítima:** lê mainhand e SOUL_FIRE_STACKS novamente a cada alvo elegível. Se ≥2, tenta helper com D+2; **só com retorno true** chama SoulFire/enchantments e escreve `stacksLidos−2`. Senão tenta D, com os mesmos efeitos após true e sem débito de stacks. N vítimas podem consumir até2N no mesmo cast; alvos posteriores podem cair para o ramo base. Spawn de partícula não consome almas. [Loop][hit].
4. **Ordem/autoria:** fonte SpellDamageSource Fire com fireTicks0 e lifesteal.10. Helper Living publica amount/cancel de SpellDamageEvent antes de resistência/friendly/hurt; pós-hit host cura causingLiving em `.10×newDamage`. Soul Fire é chamada separada `FireManager.setOnFire(target,10,SOUL_FIRE_TYPE)`, seguida de enchantments, **antes da escrita dos stacks**. Na API consultada 1.2.5, isso pede **10 segundos**, sem garantir a duração efetivamente aplicada no pack. A [API Prometheus consultada 1.2.5][prometheus], `it.crystalnest.prometheus.api.FireManager#setOnFire(Entity,float,ResourceLocation)`, linhas943–965 do sources.jar, nomeia o argumento em segundos e delega a `Entity::igniteForSeconds`. Sources.jar1016902bytes, SHA-256 `436aaa809e4162ca813e6c5bf7cce4a7ed1209ddb43b65ffcd9b3bf89006cb2a`. Isso fecha a unidade **nessa API consultada**, sem equiparar o built DTE1.1.2, o JAR físico ou a duração final em runtime. [Fonte][damage], [helper/procs][helper], [escola][school].
5. **Recurso persistente:** componente `discerning_the_eldritch:soul_fire_stacks` declara codec POSITIVE_INT/network VAR_INT; a Scythe inicializa0. O handler LivingDeathEvent incrementa1 quando causingLiving segura SoulFireScythe e target≠attacker, sem exigir esta spell. Não há cap local nesse incremento. Consumo faz read→callbacks→write; alterações reentrantes de stacks ou troca de arma pedem QA, não transação presumida. Codec/default0 e save/reload também exigem validação. [Componente][stacks], [init][scythe], [kill][kill].

## Matriz de parâmetros para perks

| Eixo | Valor / consumer / fase | Boundary real e limite | QA |
|---|---|---|---|
| Dano / power / arma | P+W, +2 com condição por vítima; source Fire. [Formula][damage], [loop][hit]. | SPELL_POWER/FIRE_SPELL_POWER **NATIVE_ATTRIBUTE**, POWER_MULTIPLIER **CONFIG_NATIVE**. SpellDamageEvent amount/cancel **HOOK_VERIFICADO**, adapter **CONDITIONAL**; W pode mudar entre vítimas. Crítico local N/A. | Q1/Q2 |
| Tipo / lifesteal / fogo | Tipo default irons_spellbooks:fire_magic, lifesteal.10, fireTicks0; SoulFire pede10s na API consultada1.2.5. [Fonte][damage], [host][source-host]. | Evento de amount não troca DamageType; SpellDamageSource setters existem por objeto, sem seam DTE pré-source para perk provada. Conversão/lifesteal/tempo SoulFire por perk **⛔ SEM_HOOK_SEGURO** sem seam DTE; API version-bounded não é mutador per-player. | Q2/Q3 |
| Range / área / targeting | Caixa6.5×3.25×6.5, forward1.9, d<3.25+frente+LOS; caster pickable. [Query][hit]. | Literais, sem cap/ordem local e sem resolver mutável localizado. Range isolado, retarget, single→AOE/resize **⛔ SEM_HOOK_SEGURO**. | Q2/Q4 |
| Projétil / visual | Slash espelhado por casting slot OFFHAND, sem entidade de dano. [VFX][vfx]. | Hitbox/speed/pierce/lifetime de projétil **N/A**; tamanho da partícula não é geometria do golpe. | Q2 |
| Tempo / cooldown | LONG10 fixo neste override,25s default; recast0 local. [Tempo][gates], [defaults][spell]. | Cooldown config/Pre event **CONFIG_NATIVE / HOOK_VERIFICADO** no [contrato comum](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md); CTR nativo não é consumido aqui. Windup independente por perk **⛔ SEM_HOOK_SEGURO**. | Q1/Q4 |
| Mana / souls / atomicidade | Mana inicial75 antes de config;2stacks só no ramo boosted com helper=true, por vítima. [Loop][hit], [host][host-cast]. | Mana setter event **HOOK_VERIFICADO** pré-débito, condicionado ao gate inicial. ItemStack#set é mecanismo real, não API transacional por perk. Sem reserva/refund/ledger RPG paralelo; desconto/cap Souls **CONTRATO_CONDICIONAL**. | Q1/Q3 |
| Summons / mundo / movimento | Sem summon/AI/bloco destruído/teleporte/knockback extra próprios. [OnCast][hit]. | Summon/geometria de movimento **N/A**; impactos do fogo, protection/claims e outros listeners continuam provider/pack. | Q2/Q4 |
| Saída / persistência | Componente persistent/network, callbacks podem mutar item; VFX após loop, super.onCast ao final. [Stacks][stacks], [vfx][vfx]. | Save/sync/relog/restart/stack0 e item trocado **PENDING**; gerar XP por hit ou kill exige correlação causal do pai, não do item apenas. | Q3/Q4 |

## Ownership, concepção e pendências

DTE/Iron’s/Prometheus mantêm golpe, mana, componente, fogo, cura e callbacks; RPG progressão/Mastery, BA seu runtime/world safety e Enshrouded seus efeitos/classificação. Não manter outra contagem Souls ou reaplicar lifesteal. Dedup cast→alvo/helper→spend/item→fire/death; cada vítima não é novo cast. Assinatura ocupada: melee Fire+arma, lifesteal e souls gastos por vítima para bônus plano. Nova habilidade com orçamento atômico por cast exigiria contrato original, não descrição do comportamento atual.

- **Q1:** config/origens/Survival/receita/ingredientes, power/W/L, mana/cooldown, windup10 versus CTR/interrupções.
- **Q2:** bordas/frente/LOS, caster não-pickable/alvo não-pickable, muitos alvos/PvP/aliados/claims, cancel/zero/resist/hurtfalse e pós-ataque.
- **Q3:** Souls ausente/0/1/2/3/extremos,2N versus ordem, morte/kill increment/callback reentrante/mainhand trocado, lifesteal e API version-bounded/fogo Prometheus, codec0/save/load.
- **Q4:** dedicado/cliente/sync, death/logout/relog/restart, cancelamento e dedup/mana sem duplicação. **Todos físicos PENDING**; sem novo adapter/perk/runtime.

[versions]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/gradle.properties#L11-L48
[host-power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L160-L257
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L333
[helper]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L119
[weapon]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L787-L802
[source-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/SpellDamageSource.java#L24-L71
[spell]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/fire/SoulSliceSpell.java#L38-L77
[guide]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/assets/discerning_the_eldritch/lang/en_us.json#L209-L210
[gates]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/fire/SoulSliceSpell.java#L79-L112
[hit]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/fire/SoulSliceSpell.java#L125-L163
[vfx]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/fire/SoulSliceSpell.java#L165-L168
[damage]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/fire/SoulSliceSpell.java#L171-L185
[stacks]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/DTEDataComponentRegistry.java#L13-L21
[kill]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/events/ServerEvents.java#L405-L415
[scythe]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/items/weapons/SoulFireScytheItem.java#L36-L49
[recipe]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/data/discerning_the_eldritch/recipe/smithing/soul_fire_scythe.json#L1-L16
[school]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/registry/SchoolRegistry.java#L59-L67

[prometheus]: https://maven.crystalnest.it/it/crystalnest/prometheus-neoforge/1.21-1.2.5/prometheus-neoforge-1.21-1.2.5-sources.jar
