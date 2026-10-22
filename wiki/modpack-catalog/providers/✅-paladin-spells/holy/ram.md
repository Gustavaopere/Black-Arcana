# Ram

**Prova de identidade:** ✅ `COUNTED_EXACT` **somente para ID de registry estático** no JAR publicado, ver [auditoria binária 5/5](../EXACT-BINARY-SPELLS-1.1.1.md) e [run #38308575364](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38308575364). Os dados funcionais abaixo continuam source-pinned; efeitos reais, configurações e Survival não foram aceitos.

- **Status:** PRESENTE — released
- **ID:** `paladin_spells:ram`
- **School:** Holy
- **Levels:** 1–10
- **Min rarity:** Rare
- **Cast:** Instant / 0 ticks
- **Mana neutral:** 15–60
- **Cooldown:** 10 s
- **Spell power neutral:** 4–13
- **Role:** armor-scaling short dash + melee-like AoE hit

## Damage and movement

`damage = 1.25*armor + getSpellPower + 2*spellLevel`

With neutral spell power this simplifies to:

`damage = 1.25*armor + 3*level + 3`

so level 1 = `1.25*armor + 6`, level 10 = `1.25*armor + 33` before external armor/spell-power changes.

Dash scale:

`multiplier = getSpellPower/3`

The spell normalizes horizontal look direction, scales by that multiplier, writes `ImpulseCastData`, directly changes delta movement and creates a swept AABB by expanding the caster box toward the dash vector plus 1.5 blocks.

Every alive `LivingEntity` in that box except the caster is:

- hurt with `entity.damageSources().mobAttack(entity)`;
- knocked back at 1.5 strength.

## Authority / PvP risk

There is no ally/team/friendly-fire filter in the spell's target predicate. Therefore party/PvP behavior is `LIVE QA REQUIRED`; a global game rule may still alter damage settlement.

The spell uses **mobAttack**, not an Iron's spell damage source, which matters for perks that trigger specifically from spell-damage provenance. Do not relabel Ram damage as spell damage without an explicit bridge contract.

## Static movement quirk

When grounded, source calls `vec.add(0,0.25,0)` without assigning the returned immutable `Vec3`. The intended extra Y component may therefore be lost. The spell separately raises caster position by 1.5 blocks, so this is a source-level quirk, not proof that the dash fails in gameplay.

## Mandatory matrix

- range/duration: dash scale formula above; exact traveled blocks depend on movement/collision and are `NÃO VERIFICADO`;
- damage type/provenance: vanilla `mobAttack` confirmed;
- targets: all alive LivingEntity except caster in swept box; FF policy external `NÃO VERIFICADO`;
- acquisition/focus/ritual: specific route `NÃO VERIFICADO`;
- sound: `RAM`; VFX/animation details beyond movement `NÃO VERIFICADO`;
- dedup: occupies armor-scaling Holy charge/dash attack;
- fail-closed: do not duplicate hit scan, movement impulse, damage or knockback.

## Source

Paladin branch `1.21@31f64ccdb39d062b21cc25d434cb62d6463b486e`, `RamSpell`.


## Dossiê por campo para perks — reauditoria 22/10/2026

**Fidelidade:** `SOURCE_PARAMETERS / SOURCE_CAUSALITY` no pin abaixo; identidade `COUNTED_EXACT` histórica conforme [JAR/SHA](../EXACT-BINARY-SPELLS-1.1.1.md), sem recompilação equivalente source→JAR ou execução física nesta reauditoria. Provider `paladin_spells`, JAR `paladin_spells-1.21.1-1.1.1.jar`, SHA-1 `e4c6f4fa70989f0b9f1819e46e29f68d414ccbaf`, Minecraft 1.21.1 / NeoForge. Source declara NeoForge 21.1.200 e Iron's 3.14.7; o pack usa host 3.16.3, por isso compatibilidade não é inferida apenas do build upstream.

**Classe:** `eu.kaufko.paladin_spells.spells.RamSpell`; [RamSpell](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/RamSpell.java#L25). Registro: [PaladinSpellRegistry](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/registry/PaladinSpellRegistry.java#L12).

**Notação:** n=spellLevel, P=getSpellPower(n,caster) resolvido pelo host, A=armor do caster; valores neutros não representam config implantada. Todas as cinco magias são Rare/Holy, maxLevel default 10, INSTANT. Mana segue o host; defaults de constructor não são novo recurso Black Arcana.

| Eixo | Valor, fase e limites | Fonte no commit exato | Superfície para perk |
|---|---|---|---|
| Alcance / alvo / área | v=normalize(forward*(3,0,3))*P/3. Consulta AABB atual do caster expandTowards(v) e inflate(1,5); inclui LivingEntity viva !=caster. Sem teste explícito de equipe/LOS/limite de alvos. Consulta instantânea, não colisão acompanhando toda a trajetória futura. | [AABB chargeBox](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/RamSpell.java#L83) | SEM_HOOK_SEGURO para mudar filtros/área/alcance independentemente de P. |
| Dano / tipo | D=1,25A+P+2n health points antes do settlement. P neutro=n+3 → 1,25A+3n+3. target.hurt usa caster.damageSources().mobAttack(caster); escola Holy não muda isso para dano mágico. knockback(1,5,forward.x,forward.z) é chamado sem testar retorno booleano de hurt. | [private float getRamDamage](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/RamSpell.java#L105) | CONTRATO_CONDICIONAL para P; SEM_HOOK_SEGURO para conversão de DamageType ou dano paralelo. |
| Movimento / tempo | Cada componente recebe lerp(0,75;velocidade anterior;v). No chão setPos sobe 1,5 bloco; `vec.add(0, 0.25, 0)` sem atribuição não altera Vec3. onClientCast adiciona o impulso serializado ao deltaMovement. Cast 0 ticks, cooldown default 10 s; duração/metros efetivamente percorridos NÃO VERIFICADO. | [entity.setDeltaMovement(new Vec3](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/RamSpell.java#L76) | SEM_HOOK_SEGURO para tempo de viagem/velocidade independente; testar sincronização antes de adaptar. |
| Projétil / hitbox / summons | N/A: não há entidade de projétil. ImpulseCastData carrega impulso; consulta usa bounding box do caster +v +1,5. Não é raio visual, tamanho de projétil ou summon. | [playerMagicData.setAdditionalCastData](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/RamSpell.java#L74) | SEM_HOOK_SEGURO para redimensionamento de projétil inexistente. |
| Custos / ingresso / cooldown | Constructor e DefaultConfig definem mana e cooldown descritos acima; lançamento via pipeline Iron's. Reserva/refund, momento exato do débito, limites efetivos e obtenção Survival específica NÃO VERIFICADO nesta reauditoria. | [constructor](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/RamSpell.java#L28) / [DefaultConfig](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/RamSpell.java#L36) | CONFIG_NATIVE para defaults; não implica desconto por player nem pagamento paralelo. |

### Pipeline e consumidores downstream

onCast calcula impulso/dano, escreve ImpulseCastData, marca hurtMarked e percorre alvos da AABB uma vez, hurt seguido de knockback. Não há guard explícito level.isClientSide nem super.onCast no override; lado efetivo depende da invocação do host. onClientCast(Level,int,LivingEntity,ICastData) consome o impulso e chama super.onClientCast. RamDirectionOverrideCastData escolhe yRot(±90) se presente; a unidade desse literal segue a API Vec3 e não deve ser rotulada graus sem validação. Não deduzir hit confirmado da seleção de alvo nem emitir Mastery para cada knockback.

[ImpulseCastData](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/capabilities/magic/ImpulseCastData.java#L8).

### Contratos dos três projetos e mutabilidade

RPG Skill Tree é dono de perks/atributos/Mastery; Iron's e Paladin mantêm casting, mana, cooldown e efeito. O [boundary transversal verificado](../PERK-BOUNDARIES-1.1.1.md) aponta `IronsInvestmentAttributesRuntime#refresh(ServerPlayer,AttributeRanks)` e `IronsInvestmentCooldownEvents#onCooldownPre(SpellCooldownAddedEvent.Pre)` do RPG: eles não constituem setters de alvo, DamageType, geometria ou duração isolada deste spell. A variação de P só se aplica aos consumidores explícitos desta ficha. `SEM_HOOK_SEGURO` significa que não foi demonstrada uma API mutadora segura para o eixo neste escopo, não uma prova de impossibilidade universal.

Enshrouded continua dono de Shroud/exposure; sua interface `MagicDamageClassifier#classify(DamageSource)` classifica, sem setter de tipo/dano/alvo. Black Arcana preserva world safety/causalidade próprios e não reexecuta efeitos do provider. A Factory é referência de produção, sem criar bridge runtime automaticamente.

### Aceitação ainda necessária

Testar dano recusado/imune com knockback, aliados/jogadores, paredes, caster olhando verticalmente, chão/ar, desync e colisão; onCast versus onClientCast. Não expandir o scan por segundo hit paralelo.

**QA:** source consultado e localizadores verificados; config implantada, cliente, GameTest com provider real, Survival e modpack `PENDING`. Nenhuma perk/adapter implementada. Descrição de gameplay acima é resumo original da semântica no source, não transcrição de tooltip; [README oficial pinado](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/README.md) pode divergir do changelog. Consulta de código não autoriza copiar implementação/assets: LICENSE.txt declara CC BY-NC-SA 4.0, enquanto gradle.properties declara All Rights Reserved; preservar essa divergência e não importar source.
