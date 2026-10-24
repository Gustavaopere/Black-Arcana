# Esoteric Edge

**Dossiê documental — 24/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`, lógica `SOURCE_PINNED / SOURCE_CAUSALITY`, integração `CONTRATO_CONDICIONAL`, QA físico `PENDING`. **+0 identidades/+0 strict**: entidade de corte, contatos, status e partículas são filhos desta spell.

## Identidade, descrição e ingresso

Provider Discerning The Eldritch (`mod_id=discerning_the_eldritch`), spell **`discerning_the_eldritch:esoteric_edge`**, escola default `irons_spellbooks:eldritch`. Declarante `net.acetheeldritchking.discerning_the_eldritch.spells.eldritch.EsotericEdgeSpell`; consumer `entity.spells.esoteric_edge.EsotericEdge#tick/#damageEntity`, filho registrado `discerning_the_eldritch:esoteric_edge`. [Registry][registry], [entidade][entity-registry].

JAR físico histórico **`discerning_the_eldritch-1.4.4-1.21.jar`**, SHA-1 `cf35c225aced23b705d1e0fd1bc5c62d96540e0c`, publisher [CurseForge8816497](https://www.curseforge.com/minecraft/mc-mods/discerning-the-eldritch/files/8816497), 22098930 bytes segundo a [prova binária anterior](../EXACT-BINARY-SPELLS-1.4.4-1.21.md). Source oficial `AceTheEldritchKing/Discerning_The_Eldritch@7bbd81f902c65a4452f47656ebd948cae8cd5833`, versão declarada1.4.4-1.21. Build Iron’s3.16.2/NeoForge21.1.244/Azure3.1.0/Ace1.2.7.2; pack registrado Iron’s3.16.3/NeoForge21.1.250/Azure3.1.11/Ace1.2.7.2. Host consultado Iron’s3.16.3 `e4056af90302d37eb1739f5ff05020b020e6e252`. [Versões][versions], [contratos comuns](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md). Não se equiparam todos os métodos source/JAR nem a composição de hosts. Metadata MIT versus template PolyForm Shield permanece conflito de sinais de licença; somente fatos/paráfrases/permalinks, sem importar implementação/assets.

[Guia oficial][guide], parafraseado: emite um corte de energia Eldritch e aplica escuridão ao impacto. A descrição não garante um único hit ou que o raycast seja o executor do dano. Sem overrides locais de crafting/loot/learning: herda escola Eldritch com requiresLearning=true e allowLooting=false; crafting depende de aprendizado/config host. Não é prova de creative-only; rota concreta Survival/config implantada **NÃO VERIFICADAS**. [Escola][school], [aquisição][acquisition].

## Pipeline, geometria e settlement

1. Legendary, níveis default1–5, **INSTANT0ticks**, cooldown default25s. O wrapper Iron’s verifica admissão, mana/cooldown/aprendizado e SpellPreCastEvent antes do início; depois SpellOnCastEvent antecede débito/onCast. Nenhum precheck próprio de alvo nesta classe. [Defaults][spell], [wrapper][cast].
2. `EsotericEdgeSpell#onCast` cria **1** EsotericEdge com owner=caster, posição no caster com Y=eyeHeight−metade da altura da entidade; `shootFromRotation` usa pitch/headYaw, speed1.2 e parâmetro de imprecisão1. Grava D antes de solicitar addFreshEntity; retorno do spawn não é examinado. D é snapshot deste disparo, sem segundo pagamento por contato. [Spawn][spawn], [constructor][entity].
3. Tipo registrado **5×1blocks** (AABB nominal5×1×5), tracking64. Não há seleção remota/range máximo próprio; viaja segundo deltaMovement com noGravity=true. Trails a±4blocks são VFX, não hitbox. No servidor, `#tick` faz ray de movimento para blocos e, separadamente, consulta **sobreposição ao AABB atual**; filtros canHitEntity herdados excluem owner/alianças nos dois sentidos. Não há LOS/cap/ordenação de vítimas adicional nesse contato. [Registro][entity-registry], [tick][tick], [host filtros][projectile].
4. **Executor ativo é `#damageEntity`**: primeira tentativa applyDamage para todo Entity ainda ausente da lista. Para Living, pede Darkness60ticks/amp0 e disableShield se Player **sem depender do primeiro retorno**, depois faz **segunda tentativa applyDamage de D**; só o retorno da segunda controla doPostAttackEffects. ShieldPart/AbstractShieldEntity recebe kill independentemente do retorno do helper. Ao fim registra a vítima mesmo se dano foi vetado/falhou. Isso são duas tentativas em Living, não promessa de2D de HP final. O onHitEntity semelhante no arquivo está comentado. [Terminal][terminal].
5. Fonte é SpellDamageSource da própria Esoteric Edge, direta=projétil, causador=owner; default Eldritch → `irons_spellbooks:eldritch_magic`. Para Living, helper publica SpellDamageEvent antes da resistência/friendly/hurt em **cada tentativa**; demais Entity seguem hurt direto. Cancelar dano não desfaz Darkness/shield disable/kill ou a entrada no ledger local. [Fonte][damage-source], [escola][school], [helper][damage-helper].
6. AABB local não publica ProjectileImpactEvent; o evento no raycast **herdado** não é veto universal do contato anterior. Host super.tick ainda executa homing, detecção, travel e expiry>300; callbacks de bloco são encaminhados ao pai, sem conversão local de blocos ou discardHelper ativo nesse filho. Não inferir perfuração garantida, bloqueio por impacto ou hit por ray do código comentado. [Tick][tick], [host hit][host-hit], [callbacks][callbacks].
7. `lifetimeInTicks` começa300 e é decrementado antes do scan; quando≤0 solicita discard, mas não retorna imediatamente. É limite local nominal15s, não um orçamento garantido de distância/acertos. `#onAntiMagic` está vazio, sobrepondo o discard padrão do host. Ledger/lifetime próprios não têm save/load; host salva Damage/Age e exclui save em UNLOADED_TO_CHUNK. Spawn data extra do host transmite owner/homing, não prova sync de D/ledger/contador local. [Lifecycle][tick], [callbacks][callbacks], [NBT][host-nbt], [spawn sync][host-spawn].

## Matriz de parâmetros para perks

`P=(20+5(L−1))×SPELL_POWER×schoolPower×C`, `C=POWER_MULTIPLIER`; **`D=0.77P+W` health points por tentativa**, `W=Utils.getWeaponDamage(caster)`. No host, W retorna0 se ATTACK_DAMAGE atual≤base; senão usa o ATTACK_DAMAGE atual e pode somar processamento de Sharpness da arma, não apenas um literal do item. Não acrescentar outra contribuição de arma por perk. [Fórmula][formula], [power][power], [arma][weapon].

| L default | Mana neutra | P neutro | Componente0.77P, antes de W |
|---|---|---|---|
|1|70|20|15.4HP|
|2|85|25|19.25HP|
|3|100|30|23.1HP|
|4|115|35|26.95HP|
|5|130|40|30.8HP|

| Eixo | Valor / consumer / fase | Boundary real e limite para perks | QA |
|---|---|---|---|
| Dano / escala / crit | D snapshot em `EsotericEdgeSpell#getDamage`, consumido até2tentativas em Living no contato. Sem crítico local declarado. [Fórmula][formula], [terminal][terminal]. | Power/atributos **NATIVE_ATTRIBUTE**, POWER_MULTIPLIER **CONFIG_NATIVE**; SpellDamageEvent#setAmount/cancel **HOOK_VERIFICADO** por tentativa pré-resistência/hurt, adapter **CONDITIONAL**. Não multiplica o HP final nem desfaz side effects. | Q1/Q3 |
| Tipo / autoria | SpellDamageSource, direta=EsotericEdge, owner=caster, default eldritch_magic. [Fonte][damage-source], [escola][school]. | Amount não é setter de DamageType; conversão elemental **⛔ SEM_HOOK_SEGURO** nesse consumer. Defaults/tags/datapack podem mudar settlement. | Q3 |
| Targeting / alcance / área | Sem target resolver; contato AABB5×1×5, owner/aliados filtrados pelo host, sem LOS/cap local; ray de voo separado. [Tick][tick], [filtros][projectile]. | Sem mutador seguro de alvo/área/range DTE; **⛔ SEM_HOOK_SEGURO** para retarget/single→AOE. ProjectileImpactEvent do ray não governa sozinho o scan local. | Q2/Q3 |
| Projétil / trajetória |1 entidade; speed1.2blocks/tick, shootFromRotation imprecisão1, noGravity=true; tracking64 não é alcance ofensivo. [Spawn][spawn], [entity][entity], [speed][speed], [registro][entity-registry]. | setDamage público real por instância; getters/literais não são setters de speed/resize. Homing/pierce herdados não recebem configuração local. Callback terceiro pré-spawn **NÃO VERIFICADO**; resize/spread/count **⛔ fail-closed**. | Q2/Q4 |
| Tempo / cooldown | INSTANT0; cooldown default25s=500ticks; contador local300, host expiry>300, discard sem return no tick local. [Spell][spell], [tick][tick], [host][projectile]. | Config de cooldown e evento Pre documentados no [contrato comum](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md); modificar lifetime requer consumer próprio, sem setter local. **CONDITIONAL**; não escalar contador por analogia com cast time. | Q1/Q4 |
| Mana / level / recast | `int((70+15(L−1))×MANA_MULTIPLIER)`; sem recast/charge próprio. [Spell][spell], [power][power], [cast][cast]. | Mana **CONFIG_NATIVE** e SpellOnCastEvent#setManaCost/setSpellLevel reais pré-onCast; custo inicial já usado na admissão, nível alterado não recalcula mana. Sem pagamento por contato/bullet extra RPG. | Q1 |
| Estados / shields | Darkness60ticks/amp0, Player.disableShield, shield Entity.kill, ledger após tentativa; sem teste de retorno de addEffect. [Terminal][terminal]. | Sem setter de duration/amp/kill nesse trecho. **⛔ SEM_HOOK_SEGURO** para trocar status/ignorar proteção via perk. Cancelamento de SpellDamageEvent sozinho não cancela esses pedidos. | Q3 |
| Persistência / antiMagic | Ledger e lifetime locais sem NBT; onAntiMagic vazio; Damage/Age e owner têm parte herdada. [Callbacks][callbacks], [NBT][host-nbt], [sync][host-spawn]. | Cleanup/load/sync **CONTRATO_CONDICIONAL**; não assumir retomada com ledger intacto. Sem ledger paralelo de hits/owner no RPG. | Q4/Q5 |
| Summons / mundo / custos extras | Projétil filho, não summon AI; sem mutação de bloco/teleporte/combustível/custoHP próprios. [Spawn][spawn], [callbacks][callbacks]. | Summon cap/AI **N/A**. Kill de shields é efeito Entity, não autorização a WorldEffectPolicy/claims. | Q2/Q5 |

## Autoria, concepção e pendências

DTE/Iron’s possuem cast, snapshots de arma/power, projétil e settlement; RPG Skill Tree possui progressão/Mastery/perks, BA seus casts/world safety, Enshrouded sua classificação/Shroud. Dedup precisa cast pai→UUID da entidade→vítima→tentativa1/2→resultado; uma vítima no ledger não confirma dano. Não premiar novamente por partículas, shield kill ou cada tentativa. Assinatura ocupada: onda de arma+poder Eldritch que aplica escuridão, desarma defesa e marca vítimas por projétil; uma magia original deve definir contrato próprio, não copiar implementação/VFX.

- **Q1:** aprendizado/config/origens Survival, L/power/W com arma/vazio/Sharpness e changes de atributo, mana/cooldown/eventlevel e spawn negado.
- **Q2:** AABB versus ray/cantos/swept path/velocidade/blocos, imprecisão, owner/aliados/PvP/claims, ProjectileImpactEvent cancelado e shields.
- **Q3:** tentativas1/2 com cancel/resistência/iFrames/HP, Darkness/shield após falha, post-enchant e procs downstream, atribuição/tipo e dedup.
- **Q4:** tick final300/host300, antiMagic vazio, unload/save/load, lifetime e ledger não persistidos, owner removido e budgets de projéteis/alvos.
- **Q5:** dedicado/cliente/Survival/multiplayer, sync e restart/logout/morte. **Todos PENDING**; sem adapter/perk/runtime novo ou promoção de Stage.

[versions]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/gradle.properties#L11-L25
[power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L148-L241
[cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L347
[school]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/registry/SchoolRegistry.java#L138-L148
[acquisition]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L630
[damage-source]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L560-L565
[damage-helper]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L64
[damage-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellDamageEvent.java#L24-L51
[registry]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/SpellRegistries.java#L41-L48
[guide]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/assets/discerning_the_eldritch/lang/en_us.json#L164-L165
[spell]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/eldritch/EsotericEdgeSpell.java#L23-L63
[spawn]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/eldritch/EsotericEdgeSpell.java#L80-L93
[formula]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/eldritch/EsotericEdgeSpell.java#L95-L120
[entity-registry]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/DTEEntityRegistry.java#L46-L52
[entity]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/spells/esoteric_edge/EsotericEdge.java#L36-L67
[tick]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/spells/esoteric_edge/EsotericEdge.java#L69-L101
[speed]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/spells/esoteric_edge/EsotericEdge.java#L103-L139
[terminal]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/spells/esoteric_edge/EsotericEdge.java#L173-L200
[callbacks]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/spells/esoteric_edge/EsotericEdge.java#L202-L234
[projectile]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L46-L114
[host-hit]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L153-L213
[host-nbt]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L289-L358
[host-spawn]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L534-L553
[weapon]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L787-L803
