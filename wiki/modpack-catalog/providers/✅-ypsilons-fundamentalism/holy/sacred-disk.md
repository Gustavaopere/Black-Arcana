# Sacred Disk

**Revisão documental: 22/10/2026.** `technical_perk_dossier: 1`; `source_status: SOURCE_PINNED`; fidelidade `SOURCE_CAUSALITY` restrita aos pins abaixo. Catálogo ✅; runtime/perks ⚠️ condicionados. **+0 identidades mágicas.**

| Identidade e evidência | Valor / limite da prova |
|---|---|
| Provider / host / tipo | Ypsilon's Fundamentalism (Fundamental Principles); `mod_id=ypfundamentals`; host Iron's Spells 'n Spellbooks; `spell`, escola default Holy. |
| ID real / classe | `ypfundamentals:sacred_disk`; `com.ypsi.fundamentalism.spells.holy.SacredDiskSpell`; registro singleton via `ModSpells#registerSpell(AbstractSpell)` ([Registry]). Nome de exibição separado do ID. |
| Artefato físico histórico | Minecraft 1.21.1 / NeoForge; `ypfundamentals-1.1.7.1.jar`, SHA-1 `a2855c253202a8fcc2925fcf5b1bf86d64fbe4da`; [publicação CurseForge 8558503](https://www.curseforge.com/minecraft/mc-mods/fundamental-principles/files/8558503). [Auditoria histórica](../EXACT-BINARY-SPELLS-1.1.7.1.md) e [Java21 SUCCESS](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38436717443): `COUNTED_EXACT` só identidade/registry/classe/escola, sem prova de métodos ou gameplay. SHA-256: NÃO VERIFICADO. |
| Source consultado | Ypsilon `a9b8f8222fb2a800edece8c1568984bd2a764fc2`, metadados 1.1.7.1 / MIT ([Metadados]); dependência declarada Iron's **3.16.2** ([Versão]). Herança consultada separadamente em Iron's **3.16.3** `e4056af90302d37eb1739f5ff05020b020e6e252`. Não se afirma equivalência binária/source nem compatibilidade operacional 3.16.2→3.16.3. |
| Descrição oficial / resumo original | [Guia e nome no recurso de idioma][Guia]: lança um disco que retorna após um intervalo ou um bloco; o guia menciona dano na ida e volta, sem provar limite de dois hits. Nenhum asset ou implementação foi copiado. |

Os números seguintes são **defaults/fórmulas do source**, não config implantada. `n` é o nível resolvido pelo host; as listas usam nível nominal e multiplicadores neutros = 1. Gates, categorias ASM/Principles e valores efetivos exigem QA no pack. [Contrato comum de custos, eventos e compatibilidade](../SPELL-PERK-BOUNDARIES-1.1.7.1.md).

## Matriz por campo

`P_host=(3+(n−1))×spell_power×holy_spell_power×power_multiplier`, via `AbstractSpell#getSpellPower(int,Entity)` [Host valores]. `P` é o retorno efetivo: em Player, se o mixin se aplicar, `(P_host+modifier_categorias)×fatigue_ratio`; aplicação/config/categorias são condicionais [Power mixin]. Neutro, sem bônus/penalidades de Principles: **3 / 4 / 5 health points por tentativa**. Ida/volta usa a mesma entidade; o source não implementa limite de exatamente dois hits por vítima.

| Campo | Default / fórmula / unidade | Declarante, fase e boundary real | Mutabilidade / limite / teste |
|---|---|---|---|
| Nível / raridade / escola | 1–3; Common; Holy. Spell `sacred_disk`, entity type **`ypfundamentals:disk`**. | `SacredDiskSpell#defaultConfig/getSpellResource` [Spell]; `ModEntities#SACRED_DISK` [Entidade registry]. | `NATIVE/CONFIG_NATIVE`; entity não é magia adicional; Q1. |
| Mana | `10+0(n−1)` = 10 em todos os níveis, antes de mana multiplier/truncamento do host. | Construtor [Spell] + `getManaCost` [Host valores]; cobrança server antes de `onCast` [Host cast]. | `NATIVE` config; `CONDITIONAL` evento `setManaCost(int)` [Evento cast]. Retorno não custa segunda mana; Q2. |
| Cast / cooldown / recast | LONG, base 5 ticks = 0.25 s; efetivo `round(5×(2−softCap(cast_time_reduction)))`; cooldown default 1 s = 20 ticks, depois host. Recast 0; boomerang não é recast. | [Spell] [Host valores] [Host cooldown] [Softcap]. | `NATIVE` atributos/config. Não usar retorno como conclusão de cooldown adicional; Q2. |
| Spawn / seleção | Um disco com owner=caster, posição Y=`eyeHeight−AABB.height/2`, direção inicial look. Sem pré-alvo ou range próprio. | `SacredDiskSpell#onCast` [Spawn], server via host. | `SEM_HOOK_SEGURO` para multi-spawn, target→AOE ou retarget; Q3. |
| Hitbox / detecção / área | Registry **0.8×0.2 blocks**, sem override de dimensions. Host broadphase AABB expandida pelo delta+0.1; colisão final segmento com target AABB+0.3. Não há raio de AOE. | [Entidade registry] [Projectile] [Host hit] [Intersect]. | `SEM_HOOK_SEGURO` para redimensionamento. Hitbox não equivale ao raio de partículas 0.5; Q3. |
| Velocidade / trajetória | Ida inicial **1.2 blocks/tick** = 24 blocks/s a 20 TPS; noGravity=true. Retorno seta delta normalizado ×**0.7 blocks/tick** = 14 blocks/s. Sem aceleração/drag próprios. | `getSpeed`, construtor [Projectile]; `handleReturnLogic` [Retorno]. Host move antes da lógica de retorno [Host projectile]. | `SEM_HOOK_SEGURO` para velocidade independente/curva; Q3/Q4. |
| Início do retorno / alcance | `MAX_RETURN_TICKS=40` e, no server sem retorno, `tickCount%40==0` arma retorno; bloco também arma imediatamente. O próximo tick de retorno persegue owner. 48 blocks é só deslocamento ideal de 40×1.2, **não** range assegurado/limite de aquisição. | Campos [Projectile], `onHitBlock/tick` [Retorno]. | `SEM_HOOK_SEGURO` para alcance/tempo de retorno; blocos e lifecycle alteram percurso; Q4. |
| Destino / fim do retorno | Persegue **posição atual** `owner.getEyePosition()+(0,−0.5,0)`. Descarta se distância da posição corrente <0.5 blocks, owner nulo ou morto. `returnTicks++` não tem comparação de timeout. | `handleReturnLogic` [Retorno]. | `SEM_HOOK_SEGURO` para prometer timeout de 40 ticks. Owner teleportando pode prolongar; Q4/Q6. |
| Dano / tipo / filtros | `onHitEntity` server chama `applyDamage(entity,P,spell.getDamageSource(this,owner))`; tipo default **`irons_spellbooks:holy_magic`**, tags Holy/magic conforme datagen. `SacredDiskSpell#getDamageSource` só delega `super`. | [Dano] [Spawn] [Host source] [Host schools] [Host tipos] [Host tags]. Settlement [Host dano] [Host resist]. | `NATIVE_ATTRIBUTE` power genérico/Holy; `CONDITIONAL` amount antes de resist/hurt em living [Evento dano]. DamageType = ⛔ `SEM_HOOK_SEGURO` para conversão; Q5. |
| Repetição / pierce / LOS | Não descarta em hit de entidade e não guarda victims set entre ticks/ida/volta. Host ordena candidatos e deduplica por entidade **somente dentro do raycast de um tick**; iFrames/`hurt` decidem tentativas aceitas. Owner/aliados filtrados; ray usa blocos. | [Dano] [Retorno] [Host hit] [Host projectile]. Pierce/ricochet homing host não são configurados pelo cast. | `SEM_HOOK_SEGURO` para “2 hits exatos”, pierce ou multi-target adicional. Não somar segundo dano na volta; Q4/Q5. |
| Lifetime / persistência / anti-magic | Sem TTL próprio: host expira **>300 ticks** (primeiro elegível 301), nominal 15 s. Anti-magic herdado descarta. `isReturning/returnTicks` locais não são salvos pela subclasse; regra host de unload/save continua aplicável. | [Projectile] [Retorno] [Host projectile] [Host lifecycle]. | `SEM_HOOK_SEGURO` para ampliar lifecycle; retorno não evita expiração. Q6. |
| Visual / summons / mundo | Partículas radius=0.5 blocks, 8 por trail; modelo visual caixa 16×0.4×16 unidades de modelo, spin 15°/tick. Não muda AABB. Sem summon AI, explosão ou block mutation na classe. | `trailParticles` [Projectile]; `SacredDiskRenderer#createDiskLayer/render` [Render]. | `N/A` visual como colisão/summon/mundo; Q3. |

## Pipeline, obtenção e autoria

Host valida casting/mana/cooldown/aprendizado/eventos; não há pré-targeting específico [Host gates]. Ao concluir LONG: evento de cast → mana → uma entidade com owner/posição/movimento/dano → spawn → super/som → cooldown [Host cast] [Spawn]. Config e Principles podem alterar admissão/custo/fadiga/XP; valores implantados/categorias são **NÃO VERIFICADOS** [Principles]. Obtenção herda host, sem receita/chance/rota Survival demonstrada [Host obtenção].

Contato server → `SpellDamageEvent` em living → resistência/friendly fire → `hurt`; ida e volta mantêm o mesmo projectile e owner. O disco pode continuar vivo após dano recusado, e a classe não usa o retorno boolean de `applyDamage` para encerrar o voo [Dano] [Host dano]. Identidade causal por cast+entidade+hit/tick, sem segunda mana, mastery ou cast de retorno. Iron's/Ypsilon são authority de casting/dano/Principles; RPG Skill Tree de progressão/gates; Black Arcana de seu runtime/WorldEffectPolicy. A assinatura ocupada é **disco Holy com retorno ao caster e contatos repetíveis**; nenhuma perk/adapter/runtime novo.

## QA e pendências explícitas

- **Q1:** fonte/links e identidade histórica auditados; métodos do JAR/config efetiva e compatibilidade host 3.16.2→3.16.3: **PENDING**.
- **Q2:** medir um pagamento e um cooldown por lançamento, cast interrompido e Principles; muitos discos simultâneos possíveis por cooldown curto sem cap local. **PENDING**.
- **Q3:** separar AABB 0.8×0.2, raio visual 0.5, ray final+0.3, spawn/velocidades e modelo; cliente/dedicado **PENDING**.
- **Q4:** hit de bloco, retorno aos 40 ticks, mover/teleportar owner, cancelamento de impacto, paredes e múltiplos alvos; não interpretar `returnTicks` como timeout. **PENDING**.
- **Q5:** tentativas ida/volta e contatos por vários ticks, armor/resist/iFrames, PvP/team/claims e eventos; confirmar dano recebido, sem assumir exatamente duas aplicações. **PENDING**.
- **Q6:** owner morto/nulo/desconectado, timeout herdado >300, anti-magic, unload/reload com flags não persistidas; GameTest, multiplayer e Survival: **PENDING**.

[Versão]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/gradle.properties#L11-L16
[Metadados]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/gradle.properties#L30-L36
[Registry]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/ModSpells.java#L29-L58
[Guia]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/resources/assets/ypfundamentals/lang/en_us.json#L59-L73
[Spell]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/holy/SacredDiskSpell.java#L23-L64
[Spawn]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/holy/SacredDiskSpell.java#L67-L84
[Projectile]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/spells/sacredDisk/SacredDiskProjectile.java#L25-L68
[Dano]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/spells/sacredDisk/SacredDiskProjectile.java#L75-L84
[Retorno]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/spells/sacredDisk/SacredDiskProjectile.java#L86-L138
[Entidade registry]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/ModEntities.java#L54-L59
[Render]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/spells/sacredDisk/SacredDiskRenderer.java#L37-L67
[Softcap]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L177-L182
[Intersect]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L294-L308
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
