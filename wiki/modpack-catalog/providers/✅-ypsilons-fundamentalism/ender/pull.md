# Pull

**Revisão documental: 22/10/2026.** `technical_perk_dossier: 1`; `source_status: SOURCE_PINNED`; fidelidade `SOURCE_CAUSALITY` restrita aos pins abaixo. Catálogo ✅; runtime/perks ⚠️ condicionados. **+0 identidades mágicas.**

| Identidade e evidência | Valor / limite da prova |
|---|---|
| Provider / host / tipo | Ypsilon's Fundamentalism (Fundamental Principles); `mod_id=ypfundamentals`; host Iron's Spells 'n Spellbooks; `spell`, escola default Ender. |
| ID real / classe | `ypfundamentals:pull_spell`; `com.ypsi.fundamentalism.spells.ender.PullSpell`; registro singleton via `ModSpells#registerSpell(AbstractSpell)` ([Registry]). Nome de exibição separado do ID. |
| Artefato físico histórico | Minecraft 1.21.1 / NeoForge; `ypfundamentals-1.1.7.1.jar`, SHA-1 `a2855c253202a8fcc2925fcf5b1bf86d64fbe4da`; [publicação CurseForge 8558503](https://www.curseforge.com/minecraft/mc-mods/fundamental-principles/files/8558503). [Auditoria histórica](../EXACT-BINARY-SPELLS-1.1.7.1.md) e [Java21 SUCCESS](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38436717443): `COUNTED_EXACT` só identidade/registry/classe/escola, sem prova de métodos ou gameplay. SHA-256: NÃO VERIFICADO. |
| Source consultado | Ypsilon `a9b8f8222fb2a800edece8c1568984bd2a764fc2`, metadados 1.1.7.1 / MIT ([Metadados]); dependência declarada Iron's **3.16.2** ([Versão]). Herança consultada separadamente em Iron's **3.16.3** `e4056af90302d37eb1739f5ff05020b020e6e252`. Não se afirma equivalência binária/source nem compatibilidade operacional 3.16.2→3.16.3. |
| Descrição oficial / resumo original | [Guia e nome no recurso de idioma][Guia]: lança uma massa que atrai entidades próximas durante o percurso. Nenhum asset ou implementação foi copiado. |

Os números seguintes são **defaults/fórmulas do source**, não config implantada. `n` é o nível resolvido pelo host; as listas usam nível nominal e multiplicadores neutros = 1. Gates, categorias ASM/Principles e valores efetivos exigem QA no pack. [Contrato comum de custos, eventos e compatibilidade](../SPELL-PERK-BOUNDARIES-1.1.7.1.md).

## Matriz por campo

`P_host=(1+2(n−1))×spell_power×ender_spell_power×power_multiplier`, conforme `AbstractSpell#getSpellPower(int,Entity)` [Host valores]. `P` é o retorno efetivo: em Player, se o mixin se aplicar, `(P_host+modifier_categorias)×fatigue_ratio`; configurações/categorias e aplicação binária são condicionais [Power mixin]. `r=min(√n+0.125P,48)` blocks após `setRadius`; neutro, sem bônus/penalidades de Principles: 1.125 / 1.7892 / 2.3571 / 2.875 blocks. Configs/atributos modificam **dano e geometria juntos**.

| Campo | Default / fórmula / unidade | Declarante, fase e boundary real | Mutabilidade / limite / teste |
|---|---|---|---|
| Nível / escola / raridade | 1–4; Ender; Rare. ID de spell **`pull_spell`**; entidade separada **`ypfundamentals:pull`**. | `PullSpell#defaultConfig/getSpellResource` [Spell]; `ModEntities#PULL_PROJECTILE` [Entidade registry]. | `NATIVE/CONFIG_NATIVE` no host; alias não cria magia nova; Q1. |
| Mana | `40+10(n−1)` = 40 / 50 / 60 / 70; host multiplica por mana multiplier e trunca `int`. | Construtor [Spell] + `getManaCost` [Host valores]; cobrança server antes de `onCast` [Host cast]. | `NATIVE` config; `CONDITIONAL` evento `setManaCost(int)` [Evento cast]. Sem refund local se spawn falhar; Q2. |
| Cast / cooldown / recast | INSTANT, 0 ticks; cooldown default 40 s = 800 ticks, depois fórmula/handler do host; recast herdado 0. | [Spell] [Host valores] [Host cooldown]. | `NATIVE` config/atributo; número/lifetime da entidade não acompanha cooldown automaticamente; Q2. |
| Origem / direção / aquisição | 1 `PullProjectile` com owner caster; spawn na posição do caster com Y=`eyeHeight−AABB.height/2`; movimento inicial pelo look. Sem alvo selecionado ou range de aquisição próprio. | `PullSpell#onCast` [Spawn]; `PullProjectile` construtores [Projectile]. Spawn é fluxo server do host. | `SEM_HOOK_SEGURO` para multi-spawn/retarget. Não duplicar entidade; Q3. |
| Dimensão / sync | Registry baseline **11×11 blocks**; override real `getDimensions(Pose)` retorna **2r×2r** escalável; `DATA_RADIUS` default 5, setado server com teto 48; sync atualiza dimensões, descarta r<0.1. | `getDimensions`, `setRadius`, `onSyncedDataUpdated`, `refreshDimensions` [Geometria]. Neutro: width/height 2.25 / 3.5784 / 4.7141 / 5.75 blocks. | Setter público não é evento seguro de perk: `CONDITIONAL`; AOE/redimensionamento = ⛔ `SEM_HOOK_SEGURO` até contrato de sync/efeitos; Q3. |
| Área de candidatos / corte | Tracker consulta `AABB.inflate(1)` a cada `max((int)(r/2),2)` ticks. Depois mede posição do candidato ao centro da AABB e usa **largura da caixa = 2r** como corte radial. A interseção com tracker limita candidatos; não é esfera pura de raio r. Sem cap explícito de entidades. | `PullProjectile#tick/updateTrackingEntities` [Tick]. O source não faz LOS nessa atração. | `SEM_HOOK_SEGURO` para prometer raio r, alcance através de walls controlado ou converter seleção. Q3/Q4. |
| Força / resistências | `diff=(center−target.position)×0.5(1−distance/(2r))×K×B`; `K=clamp(1−knockbackResistance,0.3,1)` para living, senão 1; `B=0.5` em `neoforge:bosses`, senão 1. `push(diff)` por tick; fallDistance=0. | [Tick], loop sem guard server explícito; há owner/friendly fire/spectator filter antes da força. | `SEM_HOOK_SEGURO` para intensidade/resistência independentes. Não implementar segundo ticker de atração; Q4. |
| Dano / periodicidade | A cada `tickCount%5==0`, somente com `distance<9` blocks e `canHitEntity`, tenta `P` health points por vítima. Neutro 1 / 3 / 5 / 7 **por tentativa**, não DPS garantido. | [Tick] chama `DamageSources#applyDamage(Entity,float,DamageSource)` [Host dano]; amount mutável antes de resist/hurt em living [Evento dano]. | `NATIVE_ATTRIBUTE` spell/Ender power; `CONDITIONAL` `SpellDamageEvent#setAmount(float)`. iFrames e retorno `hurt` podem rejeitar; Q4/Q5. |
| DamageType / filtros | Source default `irons_spellbooks:ender_magic`, via spell+projectile+owner; tags de datagen Ender/magic, dependentes de datapack efetivo. Host exclui owner/aliados em `canHitEntity`; settlement revalida PvP/team/friendly fire e resistência. | [Host source] [Host schools] [Host tipos] [Host tags] [Host projectile] [Host resist]. Sem crit próprio configurado na classe. | `SEM_HOOK_SEGURO` para conversão de tipo; evento amount não troca DamageType. Q5. |
| Velocidade / gravidade / colisão | Inicial 0.30 blocks/tick (6 blocks/s a 20 TPS), noGravity=true. Host raycast limita hit path por blocos, mas `travel` move pelo delta; a subclasse não descarta/para em `onHitBlock`. Tracking de força é separado do raycast e não exige LOS. | `getSpeed`, construtor e `onHitBlock` [Projectile]; [Host hit] [Host projectile]. | `SEM_HOOK_SEGURO` para velocidade/LOS/pierce sem contrato. Tamanho da AABB não é inflação exata do raycast: host usa target AABB+0.3 e broadphase+0.1; Q3/Q4. |
| Lifetime / anti-magic / save | Descarta server com `tickCount>100` (primeiro tick elegível 101), partículas finais; herança expira >300 ticks. Override `onAntiMagic(MagicData)` é **vazio**, portanto não herda discard. Save contém raio, age e dano; leitura testa Radius via `getInt` antes de `getFloat`. | [Tick] [Projectile] [Geometria] [Host lifecycle]. | `SEM_HOOK_SEGURO` para duração/antimagic; interface não prova remoção. Q6. |
| Visual / summons / mundo | Partículas em esfera de raio **2r**, renderer usa `entityScale=bbWidth×0.05` e escala adicional 0.5; VFX não define corte do dano. Sem summon com AI, explosão ou alteração de bloco nesta classe. | `trailParticles` [Projectile]; `PullRenderer#render` [Render]. | Visual `N/A` como hitbox; mundo/summon `N/A`. Q3/Q6. |

## Pipeline, obtenção e autoria

Casting do host valida mana/cooldown/aprendizado, eventos e condições; Pull não acrescenta pré-targeting [Host gates]. Na conclusão: `SpellOnCastEvent` → mana → calcular r/P → setar owner/dimensão/dano/posição/movimento → `addFreshEntity` → som/super → cooldown [Spawn] [Host cast]. Config/Principles podem cancelar admissão, alterar mana e registrar fadiga/XP [Principles]; config/categorias efetivas são **NÃO VERIFICADAS**. Loot/crafting/aprendizado herdam o host; fonte, receita e chance Survival: **NÃO VERIFICADAS** [Host obtenção].

A identidade causal é cast → **uma entidade** → múltiplos ticks/tentativas de dano com direct entity=projectile e owner=caster. Não contar cada vítima/tick/partícula como novo cast, segunda mana ou nova magia. Iron's/Ypsilon mantêm settlement e Principles; RPG Skill Tree somente progression/gates; Black Arcana permanece dono do seu runtime/WorldEffectPolicy. A assinatura já ocupada é **atração móvel em volume com dano periódico**. Não há perk, adapter ou runtime novo.

## QA e pendências explícitas

- **Q1:** identidade histórica confirmada; fórmulas/source/links auditados. Config implantada, equivalência de métodos do JAR e compatibilidade 3.16.2→3.16.3: **PENDING**.
- **Q2:** medir cobrança/cooldown uma vez por cast, interrupções e falha de spawn sob servidor+Principles. **PENDING**.
- **Q3:** níveis 1–4 e power alterado; medir AABB, sync, spawn Y, candidates, filtro 2r, raycast e VFX separadamente. Cap r=48 implica largura até 96 blocks; orçamento/performance não validado. **PENDING**.
- **Q4:** parede/LOS, owner/aliado/spectator, item/não living, bosses e resistência; comprovar fluxo client/server do loop sem guard e tentativas a cada 5 ticks. **PENDING**.
- **Q5:** dano recebido real, armor/resist/iFrames, PvP/team/claims, eventos cancelados e amount; não inferir 20 hits aceitos. **PENDING**.
- **Q6:** remoção >100 ticks, anti-magic com callback vazio, unload/reload/owner perdido e persistência Radius/age/damage; GameTest, cliente e Survival: **PENDING**.

[Versão]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/gradle.properties#L11-L16
[Metadados]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/gradle.properties#L30-L36
[Registry]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/ModSpells.java#L29-L58
[Guia]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/resources/assets/ypfundamentals/lang/en_us.json#L50-L74
[Spell]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/ender/PullSpell.java#L29-L68
[Spawn]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/ender/PullSpell.java#L75-L94
[Projectile]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/spells/pull/PullProjectile.java#L32-L129
[Geometria]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/spells/pull/PullProjectile.java#L131-L179
[Tick]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/spells/pull/PullProjectile.java#L182-L224
[Entidade registry]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/ModEntities.java#L35-L39
[Render]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/spells/pull/PullRenderer.java#L34-L61
[Host valores]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L160-L257
[Host cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L346
[Host gates]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L373-L401
[Host obtenção]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L612
[Host cooldown]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/MagicManager.java#L94-L122
[Host projectile]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L51-L214
[Host hit]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L153-L200
[Host lifecycle]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L280-L320
[Host dano]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L64
[Host resist]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L134-L173
[Host source]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/SpellDamageSource.java#L20-L51
[Host schools]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/registry/SchoolRegistry.java#L89-L107
[Host tipos]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/ISSDamageTypes.java#L16-L39
[Host tags]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/datagen/DamageTypeTagGenerator.java#L31-L95
[Evento dano]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellDamageEvent.java#L24-L50
[Evento cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellOnCastEvent.java#L20-L74
[Principles]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/event/ModEvents.java#L516-L645
[Power mixin]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/mixins/principlesMixins/PowerSpellsMixin.java#L30-L65
