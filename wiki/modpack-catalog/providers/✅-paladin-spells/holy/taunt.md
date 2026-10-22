# Taunt

**Prova de identidade:** ✅ `COUNTED_EXACT` **somente para ID de registry estático** no JAR publicado, ver [auditoria binária 5/5](../EXACT-BINARY-SPELLS-1.1.1.md) e [run #38308575364](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38308575364). Os dados funcionais abaixo continuam source-pinned; efeitos reais, configurações e Survival não foram aceitos.

- **Status:** PRESENTE — released
- **ID:** `paladin_spells:taunt`
- **School:** Holy
- **Levels:** 1–10
- **Min rarity:** Rare
- **Cast:** Instant / 0 ticks
- **Mana neutral:** 30–120
- **Cooldown:** 20 s
- **Spell power neutral:** 10–55
- **Radius neutral:** 30–120 blocks
- **Duration neutral:** 15–60 s

## Source 1.1.1

`range = 10 + 2*getSpellPower`

`duration = 5 + getSpellPower`

The spell scans `Mob` in the inflated caster box and keeps mobs alive, within true radius and not the caster. Only mobs implementing `Enemy` receive `TAUNT_EFFECT`. The caster UUID is written to `taunt_target_uuid`.

`TauntEffect` ticks every tick server-side, resolves that UUID and repeatedly:

- `mob.setTarget(taunter)`;
- `mob.setAggressive(true)`;
- when taunter is Player, `mob.setLastHurtByPlayer(player)`.

Angry-villager particles are used as current feedback.

## Authority / gates

`TAUNT_EFFECT` + stored UUID + `TauntEffect` are the forced-aggro authority. Bridges must not run a second target-forcing loop.

- non-Mob entities: excluded;
- Mob not implementing `Enemy`: excluded by spell;
- PvP players: not targets of the taunt scan;
- bosses/summons: eligible only if they satisfy the actual Mob/Enemy/provider behavior; individual modded-class coverage `NÃO VERIFICADO`.

## Mandatory matrix

- damage/heal: none;
- range/duration: formulas above;
- scaling/caps: Holy/generic/config power can change both; additional caps absent in class;
- acquisition/focus/ritual: specific route `NÃO VERIFICADO`;
- VFX/audio: `TAUNT` sound, `TOUCH_GROUND_ANIMATION`, Angry Villager particles;
- QA: modded Enemy classification needs integration testing;
- dedup: occupies AoE hostile aggro-control signature.

## Source

Paladin branch `1.21@31f64ccdb39d062b21cc25d434cb62d6463b486e`, `TauntSpell` + `TauntEffect`.


## Dossiê por campo para perks — reauditoria 22/10/2026

**Fidelidade:** `SOURCE_PARAMETERS / SOURCE_CAUSALITY` no pin abaixo; identidade `COUNTED_EXACT` histórica conforme [JAR/SHA](../EXACT-BINARY-SPELLS-1.1.1.md), sem recompilação equivalente source→JAR ou execução física nesta reauditoria. Provider `paladin_spells`, JAR `paladin_spells-1.21.1-1.1.1.jar`, SHA-1 `e4c6f4fa70989f0b9f1819e46e29f68d414ccbaf`, Minecraft 1.21.1 / NeoForge. Source declara NeoForge 21.1.200 e Iron's 3.14.7; o pack usa host 3.16.3, por isso compatibilidade não é inferida apenas do build upstream.

**Classe:** `eu.kaufko.paladin_spells.spells.TauntSpell`; [TauntSpell](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/TauntSpell.java#L28). Registro: [PaladinSpellRegistry](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/registry/PaladinSpellRegistry.java#L12).

**Notação:** n=spellLevel, P=getSpellPower(n,caster) resolvido pelo host, A=armor do caster; valores neutros não representam config implantada. Todas as cinco magias são Rare/Holy, maxLevel default 10, INSTANT. Mana segue o host; defaults de constructor não são novo recurso Black Arcana.

| Eixo | Valor, fase e limites | Fonte no commit exato | Superfície para perk |
|---|---|---|---|
| Alcance / área / alvo | R = 10 + 2P blocos. Broad phase: AABB do caster inflada em R; narrow phase: distanceTo(caster) ≤ R. Somente Mob vivo, não morrendo, diferente do caster; aplicação exige Enemy. Não há teste de LOS, equipe ou teto de quantidade explícito nesta classe. Aumentar P amplia também o volume pesquisado. | [getRange](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/TauntSpell.java#L122) | CONTRATO_CONDICIONAL: atributo P afeta geometria; não há setter por perk para R ou filtros. |
| Tempo | D = 5 + P segundos; duração do efeito = (int)(20D) ticks; INSTANT, castTime=0, cooldown default 20 s. Não confundir truncamento em ticks com Math.round. | [getDuration](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/TauntSpell.java#L127) | CONFIG_NATIVE para default de cooldown; mutação por jogador somente pelo boundary real do host. |
| Dano / tipo | N/A: não chama hurt/heal. Aggro e setLastHurtByPlayer não são dano entregue nem prova de kill/Mastery. | [mob.addEffect](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/TauntSpell.java#L103) | SEM_HOOK_SEGURO para inventar dano ou trocar DamageType nesta ação. |
| Projétil / hitbox / summons | N/A: nenhum projétil ou summon; AABB é consulta de mobs, não hitbox de projétil nem escala visual. | [AABB aabb](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/TauntSpell.java#L86) | SEM_HOOK_SEGURO para target único→área/projétil; já é AOE nativa. |
| Custos / ingresso / cooldown | Constructor e DefaultConfig definem mana e cooldown descritos acima; lançamento via pipeline Iron's. Reserva/refund, momento exato do débito, limites efetivos e obtenção Survival específica NÃO VERIFICADO nesta reauditoria. | [constructor](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/TauntSpell.java#L42) / [DefaultConfig](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/TauntSpell.java#L51) | CONFIG_NATIVE para defaults; não implica desconto por player nem pagamento paralelo. |

### Pipeline e consumidores downstream

No servidor, onCast aplica TAUNT_EFFECT (amplifier 0) e grava taunt_target_uuid. TauntEffect#applyEffectTick(LivingEntity,int) resolve o UUID no ServerLevel e força target/aggressive a cada tick; remove UUID se a entidade não resolver como LivingEntity. Não revalida o raio original, LOS ou equipe a cada tick nesse método. shouldApplyEffectTickThisTick retorna true. Outro taunter pode sobrescrever a chave; não há token de cast único aqui. Não criar segundo loop de setTarget nem conceder progresso por cada tick. O override onCast não chama super.onCast; no ingresso jogador do host auditado, evento de cast, mana e cooldown acontecem fora de super.onCast; ver [ordem causal e Mastery](../PERK-BOUNDARIES-1.1.1.md#evento-de-cast-callbacks-e-mastery-no-host-3163). Isso não valida efeitos entregues.

[TauntEffect#applyEffectTick](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/effects/TauntEffect.java#L21) · [TauntEffect#shouldApplyEffectTickThisTick](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/effects/TauntEffect.java#L64).

### Contratos dos três projetos e mutabilidade

RPG Skill Tree é dono de perks/atributos/Mastery; Iron's e Paladin mantêm casting, mana, cooldown e efeito. O [boundary transversal verificado](../PERK-BOUNDARIES-1.1.1.md) aponta `IronsInvestmentAttributesRuntime#refresh(ServerPlayer,AttributeRanks)` e `IronsInvestmentCooldownEvents#onCooldownPre(SpellCooldownAddedEvent.Pre)` do RPG: eles não constituem setters de alvo, DamageType, geometria ou duração isolada deste spell. A variação de P só se aplica aos consumidores explícitos desta ficha. `SEM_HOOK_SEGURO` significa que não foi demonstrada uma API mutadora segura para o eixo neste escopo, não uma prova de impossibilidade universal.

Enshrouded continua dono de Shroud/exposure; sua interface `MagicDamageClassifier#classify(DamageSource)` classifica, sem setter de tipo/dano/alvo. Black Arcana preserva world safety/causalidade próprios e não reexecuta efeitos do provider. A Factory é referência de produção, sem criar bridge runtime automaticamente.

### Aceitação ainda necessária

Testar dois taunters, expiração/recarga, caster removido ou em outra dimensão, mobs Enemy customizados, bosses, alvo atrás de parede e crescimento de R. Reload/restart do UUID e resultado de aggro/Mastery permanecem NÃO VERIFICADO.

**QA:** source consultado e localizadores verificados; config implantada, cliente, GameTest com provider real, Survival e modpack `PENDING`. Nenhuma perk/adapter implementada. Descrição de gameplay acima é resumo original da semântica no source, não transcrição de tooltip; [README oficial pinado](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/README.md) pode divergir do changelog. Consulta de código não autoriza copiar implementação/assets: LICENSE.txt declara CC BY-NC-SA 4.0, enquanto gradle.properties declara All Rights Reserved; preservar essa divergência e não importar source.
