# Guardian's Gaze

**Dossiê documental — 24/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`; lógica `SOURCE_PINNED / SOURCE_CAUSALITY`; integração `CONTRATO_CONDICIONAL`; QA físico `PENDING`. **+0 identidades/+0 strict**: beam visual e Mining Fatigue são filhos desta spell.

## Identidade e proveniência

Provider **Discerning The Eldritch**, `mod_id=discerning_the_eldritch`; spell **`discerning_the_eldritch:guardians_gaze`**, escola default `irons_spellbooks:evocation`. Classe `net.acetheeldritchking.discerning_the_eldritch.spells.evocation.GuardiansGazeSpell`, registro `SpellRegistries#registerSpell(new GuardiansGazeSpell())`; terminal `#onCast/#getDamage`. [Registro][registry], [defaults][spell].

Pack MC 1.21.1/NeoForge, JAR histórico **`discerning_the_eldritch-1.4.4-1.21.jar`**, SHA-1 `cf35c225aced23b705d1e0fd1bc5c62d96540e0c`, publisher [CF8816497](https://www.curseforge.com/minecraft/mc-mods/discerning-the-eldritch/files/8816497), 22098930 bytes; [prova binária](../EXACT-BINARY-SPELLS-1.4.4-1.21.md). Source `AceTheEldritchKing/Discerning_The_Eldritch@7bbd81f902c65a4452f47656ebd948cae8cd5833`, versão 1.4.4-1.21, build Iron's 3.16.2/NeoForge 21.1.244/Azure 3.1.0/Ace's 1.2.7.2 versus pack Iron's 3.16.3/NeoForge 21.1.250/Azure 3.1.11/Ace's 1.2.7.2. Host Iron's 3.16.3 `e4056af90302d37eb1739f5ff05020b020e6e252`; igualdade integral de métodos/JAR/hosts não provada. `mod_license=MIT` versus TEMPLATE_LICENSE PolyForm Shield é conflito: só fatos/paráfrases/permalinks. [Versões][versions], [contratos comuns](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md).

[Guia oficial][guide], parafraseado: variante de raio que causa fadiga de mineração. Escola **Evocation**: reusar Ray of Frost visual não comprova dano Ice/freeze. `#canBeCraftedBy=false`, `#allowLooting=false`; não demonstra creative-only. `GuardianGuidebookSpellbook` instala Gaze nível1 em livro de9slots, MAX_MANA+200 ADD_VALUE e EVOCATION_SPELL_POWER+0.10 ADD_MULTIPLIED_BASE. É pista de ingresso por item; obtenção concreta/Survival **NÃO VERIFICADA**. [Gates][spell], [livro][guidebook].

## Pipeline causal e resultados

1. **Ingresso/custo:** Epic, nível default1, INSTANT0ticks, mana `int(50×MANA_MULTIPLIER)`, cooldown default10s=200ticks antes de modifiers. Sem override de checkPreCastConditions/recast. Wrapper jogador: admissão/pre-cast → SpellOnCastEvent/débito → onCast; miss sem refund local. **P=(10+(L−1))×SPELL_POWER×EVOCATION_SPELL_POWER×POWER_MULTIPLIER**, **D=2P** tentado; neutro L1:P10/D20 health points. Max default1 não é clamp interno de fórmula. [Defaults][spell], [fórmulas][formulas], [wrapper][host-cast].
2. **Ray no onCast:** `Utils.raycastForEntity(level,caster,30,true,0.15)` parte do olho/look, termina em COLLIDER/sem fluidos. RaycastBuilder consulta AABB expandida ao longo do ray, filtra pickable/alive/não spectator e interseção com inflação0.15; escolhe primeiro hit por distância. Máximo um Entity, não cilindro que danifica tudo. Sem filtro DTE extra de aliado/PvP/claims. [Cast][cast], [utils][ray-call], [ray][ray], [filtro][filter].
3. **Visual primeiro:** solicita spawn de RayOfFrostVisualEntity entre olho e hitLocation mesmo em block/miss, sem conferir retorno. Host registra `irons_spellbooks:ray_of_frost`1×1blocks/tracking64; posição start−0.75Y, distance/rotação armazenadas; **não há hurt/impacto de dano nessa classe visual**. Dano do onCast independe da aceitação do spawn. [Cast][cast], [visual][visual], [registro visual][visual-registry].
4. **Dano:** somente ENTITY chama `DamageSources.applyDamage(target,2P,GUARDIANS_GAZE.getDamageSource(caster))`. Factory host dá direta=caster/causador=caster; default Evocation mapeia `irons_spellbooks:evocation_magic` quando o holder existe; a factory usa genericKill se ele estiver ausente. [Factory concreta][source-factory]. Living+SpellDamageSource publica SpellDamageEvent cancelável, consome amount, aplica resistência escolar/friendly e hurt; Entity não Living segue outro ramo. Gaze ignora retorno. [Cast][cast], [fonte][damage-source], [escola][school], [helper][damage-helper].
5. **Status independente:** em Living tenta DIG_SLOWDOWN60ticks=3s, amplifier1 (Mining Fatigue II), ambient/particles/icon=true **mesmo se applyDamage retornou false/cancelado**. addEffect também tem retorno ignorado. Sem freeze/Chilled/knockback próprio nesse executor. [Cast][cast].
6. **Saída/lifecycle:** else-if BLOCK dentro de ENTITY é inalcançável; partículas genéricas permanecem no ramo ENTITY, com adicionais em Living. Não prometer ramo especial de bloco. super.onCast encerra o método. Visual usa pré-incremento em tick e discard quando contador>15, shouldBeSaved=false, NBT vazio; spawn envia int(distance×10), recebe÷10. Contador de apresentação não é15ticks de dano nem alcance ofensivo. [Cast][cast], [visual][visual].

## Matriz para perks

| Eixo | Valor / consumidor / fase | Boundary real / limite | QA |
|---|---|---|---|
| Dano / power / tipo | D=2P em `#getDamage` privado; school Evocation, direta/causador=caster. [Cast][cast], [source][damage-source], [escola][school]. | Power/EVOCATION_SPELL_POWER **NATIVE_ATTRIBUTE**, POWER_MULTIPLIER **CONFIG_NATIVE**; [`SpellDamageEvent#setAmount/cancel`][damage-event] **HOOK_VERIFICADO** para Living antes de resistência/hurt. Source sem setter de tipo: conversão **⛔ SEM_HOOK_SEGURO**. Amount não confirma HP final. | Q1/Q3 |
| Range / targeting |30blocks literal, inflação0.15, ray no onCast, primeiro Entity. [Cast][cast], [ray][ray]. | Não lê P/range config. Nível altera D, não30. Sem evento mutável de resolver: alcance/retarget/single→AOE **⛔ SEM_HOOK_SEGURO**. | Q2/Q3 |
| Área / projétil / geometria | Ray é query; visual1×1/tracking64 não é dano por hitbox. Sem AOE/speed ofensivo/spread/pierce/gravidade/explosão local. [Cast][cast], [visual][visual], [registro][visual-registry]. | Eixos de projectile ofensivo **N/A**; resize visual não muda ray. Uma segunda vítima exige contrato novo, não largura de render. | Q2/Q4 |
| Tempo / cooldown | INSTANT0, cooldown default10s; visual contador>15, status60ticks. [Spell][spell], [visual][visual]. | Cooldown config/atributo nativo e evento pré-inserção no contrato comum; não é spell duration. Duração do status **⛔ SEM_HOOK_SEGURO** local. | Q1/Q4 |
| Mana / nível / recast | Mana50×config/int final, default nível1; sem recast local. [Spell][spell], [host][formulas]. | `SpellOnCastEvent#setManaCost/setSpellLevel` **HOOK_VERIFICADO** pré-onCast; nível não recalcula custo sozinho. Adapter/clamps/sync **CONTRATO_CONDICIONAL**; sem segunda mana por VFX/status. | Q1/Q4 |
| Status / cura / DOT | Mining Fatigue amp1/60ticks tentada depois do helper sem testar retorno. Heal/DOT/crit locais ausentes. [Cast][cast]. | addEffect não garante aceitação/merge. Cura/DOT **N/A**, duração/amplificador **⛔ SEM_HOOK_SEGURO**; observer do dano não é knob desse status. | Q3/Q4 |
| Summons / owner / mundo | Sem summon AI, fuel/vida/stamina/bloco/teleporte. Visual recebe caster no constructor mas não grava campo owner local. [Cast][cast], [visual][visual]. | Summon cap/AI **N/A**; visual não é entidade de dano atribuível. Claims/PvP downstream e WorldEffectPolicy precisam contratos. | Q2/Q3 |
| Persistência / cleanup / sync | Visual shouldBeSaved=false, NBT vazio, distance quantizada0.1block no spawn; buff usa lifecycle MobEffect. [Visual][visual]. | Sem ledger de vítimas/token persistente local. Sync/dedicado/cliente/remoção **PENDING**; não reemitir dano ao reconstruir visual. | Q4 |

## Ownership, dedup e verificação

DTE/Iron's possuem ray, dano, status, mana e visual. RPG Skill Tree precisa correlacionar cast→ray→tentativa→HP/status; BA não soma “beam ticks” como novos hits. Enshrouded mantém classificação/Shroud. Assinatura ocupada: ray Evocation instantâneo com Mining Fatigue; magia persistente precisaria contrato/identidade próprios, não resize do visual.

- **Q1:** livro/scroll/config efetiva/Survival, mana/cooldown/origens/creative, power/resist e níveis fora default1, nenhuma dupla cobrança/Mastery.
- **Q2:** miss/bloco/fluido/entidade fina/AABB0.15, primeiro alvo/partes, aliado/PvP/claims, direção/posição onCast e quantização visual.
- **Q3:** dano cancel/amount/hurtfalse/friendly com Mining Fatigue ainda tentada, efeito recusado/mesclado, DamageType/tags/kill credit/listeners.
- **Q4:** spawn visual recusado versus dano, dedicado/cliente/multiplayer, contador/descarte/sync, logout/restart/status; **todos PENDING**, sem adapter/runtime novo.

[registry]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/SpellRegistries.java#L121-L125
[spell]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/evocation/GuardiansGazeSpell.java#L28-L69
[versions]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/gradle.properties#L11-L30
[guide]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/assets/discerning_the_eldritch/lang/en_us.json#L161-L162
[guidebook]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/items/spellbooks/GuardianGuidebookSpellbook.java#L10-L18
[cast]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/evocation/GuardiansGazeSpell.java#L77-L105
[formulas]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L160-L257
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L346
[ray-call]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L330-L339
[ray]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/RaycastBuilder.java#L20-L124
[filter]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L459-L461
[visual]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/ray_of_frost/RayOfFrostVisualEntity.java#L18-L76
[visual-registry]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/registries/EntityRegistry.java#L485-L489
[damage-source]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L560-L565
[school]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/registry/SchoolRegistry.java#L118-L125
[damage-helper]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L64

[source-factory]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/SpellDamageSource.java#L24-L51
[damage-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellDamageEvent.java#L24-L50
