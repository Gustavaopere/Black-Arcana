# Fossilized Fury

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT` — `legendary_spellbooks:fossilized_fury`, classe `dev.higurashi.legendary_spellbooks.common.spells.nature.FossilizedFurySpell` ([Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179); [dossiê SHA-exato](../EXACT-BINARY-SPELLS-0.3.2.md)). Valores e mecânicas source-pinned; runtime/Survival ⚠️; +0 raízes.

- ID: `legendary_spellbooks:fossilized_fury`
- School: Nature
- Levels: 1–6
- Min rarity: Epic
- Cooldown: 180 s
- Cast-time field: 80 ticks
- Mana neutral: 100 / 135 / 170 / 205 / 240 / 275
- Spell power neutral: 4 / 5 / 6 / 7 / 8 / 9
- Summoned Skeloraptors: 1 / 2 / 3 / 4 / 5 / 6 — **count = spellLevel no source 0.3.2**
- Summoned HP: 25 / 30 / 35 / 40 / 45 / 50 from `20 + 5 × spellLevel`
- Summoned damage seed: provider uses spell power
- Summon lifetime: 10 minutes provider-native
- Crafting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Invoca `SummonedSkeloraptorEntity` e registra cada entidade no `BaseSummonSpell`/Iron's `SummonManager`. A quantidade é controlada pelo spell level na implementação auditada.

## Acquisition

Pool do Skeletosaurus: níveis 1–6, weight 10.

## QA obrigatório

A descrição/guide text do provider afirma que maior spell power aumenta o número de raptors, mas `FossilizedFurySpell` itera `for (i < spellLevel)`. O código do pin é a authority estática; validar se a build instalada mantém essa semântica e corrigir apenas no provider/upstream se desejado.

## Regra para o Black Arcana

Não reinterpretar spell power como summon count em bridge própria, não criar segundo summon lifecycle e não conceder progressão contínua pela permanência dos raptors.

## Source

`FossilizedFurySpell.java`, `BaseSummonSpell.java`, `SummonedSkeloraptorEntity.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Evidência:** 0.3.2 JAR ID físico `legendary_spellbooks:fossilized_fury` COUNTED_EXACT; detalhes **SOURCE_CAUSALITY** pin `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`. As entidades `SummonedSkeloraptorEntity` e ataques são downstream provider-native/Legendary Monsters; versão 2.2.2 física exige QA.

| Eixo | Cadeia e valores verificados | Política de perk |
|---|---|---|
| Admissão/stats | `DefaultConfig` nível **1–6**, cooldown **180s**, rarity EPIC, castTime **80 ticks**, mana neutra `100+35×(level−1)`, spell power neutro `4+(level−1)` antes de caster. | Iron's controla resource/cast/source; não criar outro cooldown/mana. |
| Número de summons | `getEntitiesToSummon` aloca `Entity[spellLevel]` e cria exatamente uma `SummonedSkeloraptorEntity` para cada posição; portanto **1–6 tentativas por level**, não spell power. Texto do guia upstream divergente não muda esse cálculo. | `SEM_HOOK_SEGURO` para quantidade per-player; spell power **não** autoriza multiplicar summon count. |
| Spawn e alvo | `getSpawnOffset` usa `GeometryUtils.getPointInCircle(Vec3.ZERO,2.0,totalCount,index,caster.getYRot())`, dispondo os summons em círculo nominal raio **2** perto do caster. Target AI, colisão e damage type das entidades precisam inspeção downstream. | `N/A` projectile velocity/collision na spell; controle de summon targeting ainda ⛔. |
| Atributos do summon | No `BaseSummonSpell.onCast`, para `ISummonedMob` invoca `setupAttributes(spellLevel,getSpellPower(spellLevel,caster))`; `FossilizedFurySpell.getHealth=20+5×spellLevel` (25–50) e `getDamage(power)=power`, mas o consumer final dessas helpers deve ser rastreado até `SummonedSkeloraptorEntity`. | Parâmetros condicionados à entidade real, sem assumir HP/dano aplicados sem setter físico verificado. |
| Duração/owner | `BaseSummonSpell.getSummonTime=20×60×10=12000 ticks` (10 min a 20 TPS); depois `SummonManager.initSummon(caster,entity,time,castData)` e registra `RecastInstance`, `getRecastCount=2`. Se recast existe, o bloco de novo summon não executa. | Host é owner de vida, recast, cleanup e persistência; Mastery deve deduplicar cast, spawns e ataques dos raptors. |
| Custo/resultado | `BaseSummonSpell` adiciona entidades e recast data; não expõe no corpo local um gate extra de custo ou limite de pets. Falha parcial de addFreshEntity e owner desconectado não foram testados. | `⛔` não criar summons adicionais/custos ou second summon ledger externo. |

**Âncoras:** [FossilizedFurySpell](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/nature/FossilizedFurySpell.java#L21-L66); [BaseSummonSpell / recast e SummonManager](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/api/spells/BaseSummonSpell.java#L20-L81).

**QA:** spellLevel versus spell power, recast 1/2, capacity/caps em 6 entidades, owner/summon sharing, render/spawn em áreas com claims, logout/reconnect, PvP target, atributos aplicados, relógio e mana settlement. **+0 novas magias / +0 adapter homologado.**
