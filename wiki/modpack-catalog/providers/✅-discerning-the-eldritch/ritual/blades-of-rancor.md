# Blades of Rancor

**Dossiê documental — 24/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`; lógica `SOURCE_PINNED / SOURCE_CAUSALITY`; integração `CONTRATO_CONDICIONAL`; QA físico `PENDING`. **+0 identidades/+0 strict**: efeitos/entidades/impactos derivados não são novas spells.

## Identidade e proveniência

Provider Discerning The Eldritch, `mod_id=discerning_the_eldritch`, spell **`discerning_the_eldritch:blades_of_rancor`**, classe `net.acetheeldritchking.discerning_the_eldritch.spells.ritual.BladesOfRancorSpell`. Escola default **`discerning_the_eldritch:ritual`**, tipo de dano escolar **`discerning_the_eldritch:ritual_magic`**, atributos nativos `ritual_spell_power`/`ritual_magic_resist`. É spell Iron's/DTE, não RitualEngine Black Arcana. [Registry][registry], [escola][school], [atributos][attributes].

Pack MC 1.21.1: JAR histórico **`discerning_the_eldritch-1.4.4-1.21.jar`**, SHA-1 `cf35c225aced23b705d1e0fd1bc5c62d96540e0c`, [publisher 8816497](https://www.curseforge.com/minecraft/mc-mods/discerning-the-eldritch/files/8816497), [prova binária histórica de identidade](../EXACT-BINARY-SPELLS-1.4.4-1.21.md). Source oficial `7bbd81f902c65a4452f47656ebd948cae8cd5833`, declaração 1.4.4-1.21; build Iron's 3.16.2/Neo 21.1.244/Azure 3.1.0/Ace 1.2.7.2 versus pack Iron's 3.16.3/Neo 21.1.250/Azure 3.1.11/Ace 1.2.7.2. Host consultado `e4056af90302d37eb1739f5ff05020b020e6e252`. Versão/registro não provam equivalência integral dos métodos/JAR/hosts. [Versões][versions], [contratos comuns](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md). Sinais de licença conflitantes MIT/PolyForm Shield descritos ali; somente fatos/paráfrases/permalinks, sem importar código/assets.

[Guia oficial][guide], parafraseado: uma sequência de lâminas segue o ponto para o qual o caster olha. O alcance de homing e a colisão são consumidores herdados, não a descrição visual.

## Ingresso, escala e sequência

`AbstractRitualSpell` proíbe crafting, mas este override é **não complex/não super-complex**: allowLooting=true e a base não rejeita SPELLBOOK/SWORD por complexidade. Isso é elegibilidade, não scroll encontrado ou configuração implantada. Cataclysm, Devourer e Mourning Star base instalam **BladesL 6**, acima do max default 5; seus pools source em city_items têm chance 0.05 cada. Presets/loot são leads de Survival, sem homologação da rota montada ou clamp host. [Gates][ritual], [overrides][spell], [presets][preset-cataclysm], [Devourer][preset-devourer], [Mourning][preset-mourning], [loot][city].

Defina `L`=nível entregue ao onCast, `P=(5+2(L−1))×SPELL_POWER×ritualPower×POWER_MULTIPLIER`, `W=Utils.getWeaponDamage(caster)`, `D=0.45P+W` health points. W é ATTACK_DAMAGE efetivo com tratamento do base/fist e Sharpness no helper, não só o número exibido no item. P/W são resolvidos **a cada emissão**, não congelados na abertura do recast. [Defaults][spell], [dano/emissão][spawn], [power][power], [arma][weapon].

| L default | Mana neutra | P neutro | Componente 0.45 P, antes de W | Total de casts pedido |
|---|---|---|---|---|
|1|90|5|2.25 HP|1|
|2|95|7|3.15 HP|2|
|3|100|9|4.05 HP|3|
|4|105|11|4.95 HP|4|
|5|110|13|5.85 HP|5|

1. **Cast e recast:** INSTANT 0 ticks, cooldown default 20 s=400 ticks. Sem recast ativo, onCast cria RecastInstance com total=L, janela 160 ticks. Constructor guarda remaining=L−1; o cast inicial já emite. Host só considera ativo remaining>0 e ticks>0, logo L1 não concede recast extra. A entrada inativa ainda pode ficar guardada até o timeout; no host consultado, o wrapper pode adicionar cooldown inicial e o callback padrão no timeout solicitar cooldown novamente. Isso não prova o resultado temporal no pack. Recasts ativos no wrapper jogador não debitam mana novamente; decremento ocorre após onCast e renova a janela quando ainda restam usos. Spell não tem onRecastFinished próprio: conclusão/cooldown/save pertencem ao host. [Spell][spell], [constructor][recast-instance], [atividade][recasts], [wrapper][cast-host], [finish/save][recast-save].
2. **Spawn e tiro:** cria 1 BladeOfRancorProjectile(owner=caster) por cast; origem=eye+forward.normalized× 0.2−Y 0.15−YbulletHeight. Com height 1, offset vertical é−1.15 relativo ao olho. Vetor forward+(0,0.2,0) normalizado× 0.5, perturbação normalizada de magnitude 0.4, preservando módulo 0.5; host shoot multiplica getSpeed 1.0, logo velocidade inicial nominal 0.5 blocks/tick. Grava D, cursorHoming=true/noGravity=true e solicita addFreshEntity sem ler retorno. Não há refund local por spawn recusado. [Spawn][spawn], [entidade][blade], [host][projectile-host].
3. **Homing e colisão:** host cursor procura até 48 blocks com ray/blocks e bbInflation 0.5, perde tracking quando owner ausente ou projétil está a mais 48 blocks do owner; homeTowards strength 0.18 preserva velocidade corrente. Isso não é cap de alcance da trajetória. AABB registrada 1 × 1 blocks; hit detection usa swept query+inflation 0.1 e interseção 0.3, owner/aliados excluídos e hits ordenados por distância. [Tipo][entity], [cursor][homing], [hit][projectile-hit], [base][projectile-host].
4. **Terminal:** onHitEntity no servidor solicita helper D com SpellDamageSource direta=blade/causador=owner, spell Blades/iFrames 0. Em Living, tenta MalignantBurn 100 ticks/amp 0 **independente do boolean do dano**; esse effect reduz SPELL_RESIST em−0.55 ADD_MULTIPLIED_BASE, não possui DOT próprio. Host helper publica SpellDamageEvent só para Living+SpellDamageSource, aplica resistência/friendly e hurt;0 iFrames é consumido em incoming host, não prova HP garantido. [Impacto][impact], [status][malignant], [settlement][damage-host], [iFrames][damage-effects].
5. **Saída:** onHit chama super e discardHelper; com pierce/ricochet defaults 0 normalmente descarta no impacto, bloco também. Não há AOE de dano/explosion definida: blastwave 1.5 é VFX. Host expira em tickCount>300; antiMagic descarta e NBT herdado salva D/Age/homing target, mas não prova continuidade de cursor após load. onHitBlock e onHit não são segundo cast. [Impacto/discard][impact], [discard host][discard], [state][projectile-state].

## Matriz de alteração por perks

| Eixo | Valor, consumer e fase | Boundary real / limite | QA |
|---|---|---|---|
| Nível/power/dano | Max default 5; D=0.45 P+W a cada onCast. [Spell][spell], [power][power]. | SPELL_POWER/ritual_spell_power **NATIVE_ATTRIBUTE**, POWER_MULTIPLIER **CONFIG_NATIVE**; helper Living aceita SpellDamageEvent#setAmount/cancel pré-resistência/hurt. Adapter **CONTRATO_CONDICIONAL** por spell+blade+owner; não duplicar hit. |Q1/Q3|
| Tipo/iFrames | ritual_magic, owner/corpo blade, iFrames 0. [Escola][school], [fonte][spawn], [incoming][damage-effects]. | Amount não altera DamageType. **⛔ SEM_HOOK_SEGURO** para conversão; setter na fonte não é mutador terceiro do constructor desta spell. |Q3|
| Alvo/range | Cursor 48, tracking desligável além 48 do owner; ray blocks e filtros host. [Cursor][homing]. | Sem knob de range por jogador identificado. SetCursorHoming existe por instância, mas callback pré-spawn terceiro não foi fechado; retarget/single→AOE **⛔ SEM_HOOK_SEGURO**. |Q2|
| Área/targets | Sem dano AOE local; hit path host 0.3, ordenação por distância; sem cap global de entidades. [Hit][projectile-hit]. | AOE/explosionRadius visual não se substituem. Modificar geometria/budget requer contrato próprio **CONDITIONAL**, sem segundo resolver/hit. |Q2/Q3|
| Projétil |1 por cast; AABB 1 × 1, velocidade inicial 0.5 blocks/tick, inaccuracy 0.4, noGravity, lifetime host>300. [Spawn][spawn], [blade][blade], [host][projectile-host]. | SetDamage/setCursorHoming/setPierceLevel herdados são públicos por instância, não evento universal pré-spawn; getSpeed literal 1 não é setter. Resize/speed/spread **⛔ SEM_HOOK_SEGURO**. |Q2/Q4|
| Cast/cooldown | INSTANT 0;20 s default antes de modifiers; base canBeInterrupted=false. [Spell][spell], [base][ritual]. | Cooldown config/atributo host **NATIVE/CONFIG_NATIVE** e evento Pre mutável no [comum](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md). Não confundir lifetime com cooldown ou imunidade a todo cancelamento. |Q1/Q4|
| Mana/recast | `int((90+5(L−1))×MANA_MULTIPLIER)`; totalL/janela 160, custo inicial condicionado ao CastSource. [Power][power], [spawn][spawn], [wrapper][cast-host]. | Configglobal e SpellOnCastEvent#setManaCost/setSpellLevel **HOOK_VERIFICADO** nesse wrapper, adapter **CONDITIONAL**; nível novo não recalcula custo já construído. Sem setter independente do total/window local. |Q1/Q4|
| Status/mundo | MalignantBurn 100/amp 0 se Living, apesar de hurtfalse; nenhum block break/heal/summon/teleporte local. [Impacto][impact], [effect][malignant]. | Duração/status é constante do consumer; observador de dano não é setter do buff. Estado/mundo **CONDITIONAL**; summons/AI **N/A**. |Q3|
| Persistência/dedup | Recast nativo por player/spell; entidade por UUID, impacto e vítima. NBT/homing/antiMagic host. [State][projectile-state], [save][recast-save]. | Providers mantêm recurso/cleanup. Mastery Ritual e integração RPG seguem pendentes no [comum](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md), sem presumir lane. Não premiar partículas ou tentativas como HP. |Q4/Q5|

Assinatura ocupada: sequência de lâminas cursor-homing, dano weapon+Ritual, recast nativo e debuff de resistência. Uma magia original de trajetória/budget definidos exige contrato próprio; não é extensão aceita por documentar getters.

- **Q1:** config/origem/scroll e armasL 6 versus default 5, mana inicial/recasts, níveis/atributos/W a cada emissão, custo alterado e CastSource.
- **Q2:** cursor 48 versus trajetória, blocos/aliados/owner/PvP/claims, hitbox/interseção/spread, spawn recusado e quantidade viva.
- **Q3:** SpellDamageEvent veto/amount/resistência/iFrames, MalignantBurn apesar de hit recusado e merge de efeitos; impactos repetidos/pierce/ricochet externos.
- **Q4:** L1/timeout/used-all/cancel/death/logout, cooldown callbacks, antiMagic/unload/restart e cursor não persistido como garantia.
- **Q5:** dedicado/cliente/multiplayer/Survival/sync, correlação cast→blade→vítima e Mastery Ritual. **Todos PENDING**; nenhum adapter ou runtime novo.

[attributes]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/DTEAttributeRegistry.java#L19-L23
[blade]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/spells/blade_of_rancor/BladeOfRancorProjectile.java#L34-L107
[cast-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L305-L347
[city]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/data/discerning_the_eldritch/loot_table/chests/city_items.json#L21-L70
[damage-effects]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L91-L131
[damage-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L64
[discard]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L370-L406
[entity]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/DTEEntityRegistry.java#L209-L215
[guide]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/assets/discerning_the_eldritch/lang/en_us.json#L200-L201
[homing]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L221-L282
[impact]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/spells/blade_of_rancor/BladeOfRancorProjectile.java#L115-L142
[malignant]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/effects/MalignantBurnEffect.java#L9-L13
[power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L148-L257
[preset-cataclysm]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/items/weapons/CataclysmBladeItem.java#L17-L25
[preset-devourer]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/items/weapons/DevourerAxeItem.java#L19-L25
[preset-mourning]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/items/weapons/MourningStarMaceItem.java#L19-L25
[projectile-hit]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L153-L213
[projectile-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L46-L115
[projectile-state]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L301-L359
[recast-instance]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/RecastInstance.java#L27-L35
[recast-save]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/PlayerRecasts.java#L157-L212
[recasts]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/PlayerRecasts.java#L46-L131
[registry]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/SpellRegistries.java#L170-L187
[ritual]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/ritual/AbstractRitualSpell.java#L12-L59
[school]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/DTESchoolRegistry.java#L30-L40
[spawn]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/ritual/BladesOfRancorSpell.java#L89-L128
[spell]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/ritual/BladesOfRancorSpell.java#L27-L81
[versions]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/gradle.properties#L11-L27
[weapon]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L787-L801
