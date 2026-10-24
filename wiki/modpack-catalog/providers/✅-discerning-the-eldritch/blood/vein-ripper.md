# Vein Ripper

**Dossiê documental — 24/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`; lógica `SOURCE_PINNED / SOURCE_CAUSALITY`; integração `CONTRATO_CONDICIONAL`; QA físico `PENDING`. **+0 identidades/+0 strict**: efeitos, entidades e fases derivados não são novas spells.

## Identidade e proveniência

Provider **Discerning The Eldritch**, `mod_id=discerning_the_eldritch`, JAR físico histórico **`discerning_the_eldritch-1.4.4-1.21.jar`**, SHA-1 `cf35c225aced23b705d1e0fd1bc5c62d96540e0c`; [publisher CF8816497](https://www.curseforge.com/minecraft/mc-mods/discerning-the-eldritch/files/8816497), [prova estática de identidade](../EXACT-BINARY-SPELLS-1.4.4-1.21.md). Source oficial `AceTheEldritchKing/Discerning_The_Eldritch@7bbd81f902c65a4452f47656ebd948cae8cd5833`. Build Iron’s 3.16.2/NeoForge 21.1.244/Azure 3.1.0 versus pack Iron’s 3.16.3/NeoForge 21.1.250/Azure 3.1.11; Ace 1.2.7.2 coincide na versão declarada, sem prova de ABI. Host lido Iron’s `e4056af90302d37eb1739f5ff05020b020e6e252`. Versão declarada não equipara métodos source↔JAR. Sinais MIT/PolyForm Shield conflitantes: fatos/paráfrases/permalinks, sem importar implementação/assets. [Versões][versions], [contratos comuns](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md).

Spell **`discerning_the_eldritch:vein_ripper`**, escola default `irons_spellbooks:blood`, Common, níveis 1–5; declarante `net.acetheeldritchking.discerning_the_eldritch.spells.blood.VeinRipperSpell`. [Defaults][spell]. [Guia oficial][guide], parafraseado: investida/corte de sangue com repulsão, Blood Rot e roubo de vida. Sem override local de crafting/loot/precondição/recast; elegibilidade e aprendizado seguem host/config. Rota concreta Survival **NÃO VERIFICADA**. [Host aquisição][acquisition].

## Valores e pipeline causal

Defina `L`=nível entregue ao consumer, `P=(6+2(L−1))×SPELL_POWER×BLOOD_SPELL_POWER×POWER_MULTIPLIER`, `W=Utils#getWeaponDamage(caster)` e **`D=P+W` health points** tentados por alvo. W usa ATTACK_DAMAGE atual, retorna 0 se não supera seu atributo base e pode incorporar Sharpness; não é apenas o dano nominal do item. Getter de dano é chamado por vítima, sem snapshot único da arma. [Fórmula][damage], [power][host-power], [arma][weapon].

| L default | Mana neutra | P neutro / D sem arma | Distância de seleção |
|---|---|---|---|
| 1 | 30 | 6 HP | 8 blocks |
| 2 | 45 | 8 HP | 9 blocks |
| 3 | 60 | 10 HP | 10 blocks |
| 4 | 75 | 12 HP | 11 blocks |
| 5 | 90 | 14 HP | 12 blocks |

1. **Ingresso/custo:** INSTANT 0 ticks; mana `int((30+15(L−1))×MANA_MULTIPLIER)` e cooldown default 20s=400ticks. Admissão/mana inicial precedem SpellOnCastEvent; débito antes de onCast, conforme origem/creative. Evento pré-efeito não comprova hit. [Defaults][spell], [host][host-cast].
2. **Seleção:** `VeinRipperSpell#onCast`: `d=7+L`, ray de bloco olho→forward×d (Fluid.NONE), query `caster.hitbox.expandTowards(end−eye).inflate(2)`. Candidatos Living não-spectator com dot de direção entre centros normalizados e forward ≥.85; ordena distância² e só o primeiro, se distância²<d², ancora a área. Query inicial não exige alive/LOS por candidato. [Seleção][target].
3. **Área terminal:** caixa **4.5×5.5×4.5 blocks** centrada no candidato e deslocada forward×2.25, não esfera de raio4.5. Consulta Entity: alive/pickable/LOS olho→centro → helper(D,fonte Blood). Alvos secundários não reaplicam cone/distância d; sem cap numérico local. Friendly/resist de Living são downstream. [Área][target], [helper][helper].
4. **Helper=true:** VFX, pós-ataque enchantments, impulso e Blood Rot 60ticks/amp0 em Living. Vetor do alvo=`normalize(normalize(targetPos−casterPos)+(0,.15,0))`; a chamada `kb.scale(random×resist×.1)` tem retorno descartado e não reatribui o Vec3 somado ao delta. Não apresentar esses fatores como repulsão efetivamente reduzida pela resistência. [Consequências][hit].
5. **Caster sem exigir hit:** endpoint vira média centroAoE/endpointRay se houve candidato; `rayVec=end−eye`, novo delta=`deltaAnterior×.1+rayVec/6+(0,.1,0)`, hurtMarked e FallDamageImmunity20ticks/amp0. É impulso, não teleporte seguro nem garantia de percorrer d. [Movimento][movement].
6. **Fonte/cura:** SpellDamageSource Blood, tipo default `irons_spellbooks:blood_magic`, lifesteal .15. Helper Living publica SpellDamageEvent e consome amount/cancel antes de resist/friendly/hurt. Listener host Post cura causingLiving em `.15×event.newDamage`, não .15D garantido. [Fonte][damage], [escola][school], [settlement/procs][helper].
7. **Blood Rot downstream:** atributos BloodPower/BloodResist −.25 ADD_MULTIPLIED_BASE; servidor tenta hurt **3HP** quando duração%20==0, fórmula ignora amp. Static plain DamageSource `discerning_the_eldritch:blood_rot` resolve holder pela primeira vítima e não grava autora. Não é helper/SpellDamageSource/lifesteal do corte; 60ticks não garantem três perdas de HP. [DOT][rot], [tipo][rot-type].

## Matriz de parâmetros para perks

| Eixo | Valor / consumer / fase | Boundary real e limite | QA |
|---|---|---|---|
| Dano / power / arma | D=P+W no loop onCast. [Damage][damage], [weapon][weapon]. | SPELL_POWER/BLOOD_SPELL_POWER **NATIVE_ATTRIBUTE**, POWER_MULTIPLIER **CONFIG_NATIVE**; SpellDamageEvent amount/cancel **HOOK_VERIFICADO** para helper Living, adapter **CONDITIONAL**. Crítico local N/A. | Q1/Q2 |
| Tipo / cura / DOT | Blood +lifesteal .15; BloodRot plain3HP separado. [Fonte][damage], [DOT][rot]. | Amount não é setter de DamageType. Conversão, lifesteal independente e autoria do DOT por perk **⛔ SEM_HOOK_SEGURO**; não repetir cura/DOT. | Q2/Q3 |
| Range / targeting | 7+L/cone≥.85 inicial; mais próximo ancora caixa. [Seleção][target]. | Nível é input host condicionado, não setter isolado de range/resolver; retarget/single→AOE **⛔ SEM_HOOK_SEGURO**. | Q1/Q2 |
| Área / budgets | Caixa4.5×5.5×4.5 deslocada2.25, secundários Entity alive/pickable/LOS. [Área][target]. | Literais sem cap de targets/config local; resize/budget **⛔ SEM_HOOK_SEGURO** antes de adapter pré-query verificado. | Q2/Q4 |
| Projétil / visual | Não spawna projétil de dano; slash/trace são partículas. [VFX][vfx]. | Hitbox/speed/lifetime/pierce de projétil **N/A**. Tamanho visual não controla a query. | Q2 |
| Tempo / custo / cooldown | INSTANT0, mana30+15(L−1) antes de config, cooldown20s, recast local0. [Defaults][spell], [host][host-power]. | Config mana/cooldown **CONFIG_NATIVE**; SpellOnCastEvent setters/cooldownPre **HOOK_VERIFICADO** genérico no [contrato comum](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md), adapter **CONDITIONAL**; nível alterado não recalcula custo. | Q1/Q4 |
| Movimento / repulsão | Impulso no alvo só após helper=true; impulso caster mesmo sem hit. [Hit][hit], [caster][movement]. | Sem seam DTE pré-vetor localizado; observer de dano não modifica automaticamente ambos. Dash/knockback independente **⛔ SEM_HOOK_SEGURO**. | Q2/Q4 |
| Estados / mundo / saída | Rot60/FallImmunity20; DOT static sem autora. Sem bloco destruído/teleporte/summon/AI/custo extra próprio. [Rot][rot], [movimento][movement]. | Summon knobs **N/A**; merge/refresh/save/load host-owned. Claims/cleanup/atribuição depois de restart **PENDING**; sem ledger RPG paralelo. | Q3/Q4 |

## Ownership, concepção e pendências

DTE/Iron’s possuem corte, mana, movimento, DOT e cura; RPG progressão/Mastery; BA seu casting/world safety; Enshrouded classificação/Shroud próprios. Dedup caster/cast→vítima/helper→DOT/fase: partículas, impulso, DOT e cura não são casts extras. Assinatura ocupada: investida com seleção frontal/caixa deslocada, Blood+arma, lifesteal e DOT que enfraquece Blood. Nova magia exige contrato original de movimento/autoria.

- **Q1:** config/origens/Survival, L1–5/extrapolação/power/W, mana inicial/evento, cooldown e cast recusado.
- **Q2:** candidato morto/parede, bordas cone/ray/caixa, aliados/PvP/claims, amount0/cancel/resist/hurtfalse, repulsão real e impulso sem hit.
- **Q3:** DOT refresh/ordem, autoria/kill credit, atributos/amplifier, lifesteal com mitigação e MendFlesh coexistindo.
- **Q4:** dedicado/cliente/sync, muitos alvos, colisão/quedas, morte/logout/unload/restart e cobrança/dedup. **Todos físicos PENDING**; sem novo adapter/perk/runtime.

[versions]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/gradle.properties#L11-L48
[host-power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L160-L257
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L333
[helper]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L119
[weapon]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L787-L802
[source-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/SpellDamageSource.java#L24-L71
[spell]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/blood/VeinRipperSpell.java#L39-L78
[guide]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/assets/discerning_the_eldritch/lang/en_us.json#L218-L219
[acquisition]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L612
[target]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/blood/VeinRipperSpell.java#L98-L122
[hit]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/blood/VeinRipperSpell.java#L122-L138
[movement]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/blood/VeinRipperSpell.java#L141-L146
[vfx]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/blood/VeinRipperSpell.java#L148-L174
[damage]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/blood/VeinRipperSpell.java#L177-L184
[rot]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/effects/BloodRotPotionEffect.java#L17-L58
[rot-type]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/DTEDamageTypes.java#L11-L27
[school]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/registry/SchoolRegistry.java#L109-L117
