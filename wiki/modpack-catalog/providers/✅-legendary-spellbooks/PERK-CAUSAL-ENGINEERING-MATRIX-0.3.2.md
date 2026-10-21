# Legendary Spellbooks 0.3.2 — matriz de engenharia causal para perks

**Checkpoint 17/10/2026 · PR #825 (draft).** Esta matriz só introduz documentação. O addon preserva o runtime provider-native da Iron's Spells e da Legendary Monsters; Black Arcana é dono de seu casting/rituais e RPG Skill Tree exclusivamente de Mastery/perks/atributos/gates após contratos validados.

## Proveniência e barra de progresso

- Instalação no sibling: `legendary_spellbooks-1.21.1+neo-0.3.2.jar`, mod ID `legendary_spellbooks`, SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`; [prova exata 30/30](EXACT-BINARY-SPELLS-0.3.2.md), [Java21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179) SUCCESS no commit histórico. `COUNTED_EXACT` refere-se ao **registro estático**, não à equivalência do corpo de métodos.
- Código da release 0.3.2 [Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3](https://github.com/Higurashi34m/Legendary-Spellbooks/tree/62ced2f2b2693aa841251473cbbd726fdd928ed3); comportamentos abaixo `SOURCE_CAUSALITY`. O pin era desenvolvido com Iron's **3.16.1** e Legendary Monsters **2.1.14**; o pack possui **3.16.3** e **2.2.2**, e essa matriz não valida compatibilidade.
- **Barra por provider — identidade de spell: 30/30 = 100%**. **Barra por provider — engenharia causal source-pinned por ficha: 30/30 = 100%** neste checkpoint, com parâmetros e riscos documentados nas 30 páginas individuais. Essa cobertura é documental, sem certificação de execução, paridade binária de corpos de método ou hooks per-player. **Adapters perks homologados: 0**. Não declarar 33,33% de desenvolvimento do runtime.
- **Barra global — —%**: mínimo do checkpoint vigente **1.857 objetos semânticos / 1.855 estritos**, denominador global aberto; há documentos históricos com mínimos diferentes. **+0 novas magias** nesta tranche, nenhuma Stage promovida.

## Trinta fichas com matriz source-causal por habilidade

| Spell ID `legendary_spellbooks:*` | Ficha com engenharia | Fato causal prioritário para perks | Hook |
|---|---|---|---|
| `annihilation_resonance` | [Resonance](annihilation/annihilation-resonance.md) | Crítico de NeoForge + AABB alvo inflada 3; UI informa radius=4; `isAlliedTo(target)` usado no loop inteiro | ⚠️ evento de crítico existe, settlement/owner da explosão e alteração de raio **não** homologados |
| `annihilation_beam` | [Beam](annihilation/annihilation-beam.md) | Raycast até 30/40/50; AABB broadphase 1, target intersection inflada 0.5; dano `power + maxHP×1–3%`; explosões derivadas | ⛔ sem hook de largura, duração, HP damage e multiplicação |
| `annihilation_shockwave` | [Shockwave](annihilation/annihilation-shockwave.md) | Spawn distance 4.5..12 vs tooltip 6..13.5; 6..36 possíveis FlameStrikes e HP% `0.005×level` | ⛔ geometria e hit source de entidade externa |
| `annihilation_geyser` | [Geyser](annihilation/annihilation-geyser.md) | Gate de Curios + Spellbook, mínimo 60 ticks, busca/pull de 11 posições por cast tick e até 11 portais | ⛔ world/target, portal dimensions e processos per-tick |
| `glacier_ringburst` | [Ringburst](ice/glacier-ringburst.md) | Até 24/40/60/84 ice spikes por nível; warmups por anel; loot lvl5 versus maxLevel4 | ⛔ tamanho/range e nível 5 condicionado |
| `fossilized_fury` | [Fury](nature/fossilized-fury.md) | 1–6 summons por `spellLevel`, **não** power; `SummonManager` owns 10-min lifetime/recast | ⛔ quantidade per-caster e duplicação de lifecycle |
| `energy_beam` | [Energy Beam](lightning/energy-beam.md) | Motion Y 0.20/0.25 a cada cast tick; spawn de EnergyBeamEntity externo, duração 50/60/70 | ⛔ hitbox/target/dano não auditados no JAR da Legendary Monsters |
| `possessed_soul_blade` | [Soul Blade](blood/possessed-soul-blade.md) | Evocation lvl 1–2/Blood lvl 3–4; até 12/24/35/54 entidades; power `int` | ⛔ school double-count e fan-out |
| `flame_sector` | [Flame Sector](fire/flame-sector.md) | Até 24/54/96/150 colunas; hit a cada 5 ticks; `DamageSource` é derivado de **FLAME_EATER_SPELL** na classe da coluna | ⛔ possível inconsistência de atribuição, requer prova binária e evento efetivo |
| `cumulo_charge` | [Cumulo Charge](lightning/cumulo-charge.md) | `mobAttack` (não Spell DamageSource); AOE 4 pós-hit, STUN mesmo sem hurt true; knockback Y+0.4 no source | ⛔ não presumir dano Lightning pelo nome/school |
| `annihilation_arrow` | [annihilation arrow](annihilation/annihilation-arrow.md) | Uma flecha, dano power + HP máximo×0.25% por nível; impacto pode gerar explosão filha | ⛔ ranged/projectile/impact |
| `annihilation_bomb` | [annihilation bomb](annihilation/annihilation-bomb.md) | Bomba com AABB 2 no hit e 30/34/40/44/50/54 projéteis secundários por nível | ⛔ fan-out e damageSource por projétil |
| `summon_flameborn_knights` | [summon flameborn knights](annihilation/summon-flameborn-knights.md) | Dois summons fixos: guard e warrior, lifetime 12.000 ticks com RecastInstance | ⛔ count e lifecycle pertencem ao host |
| `release_riftwalker_predator` | [release riftwalker predator](annihilation/release-riftwalker-predator.md) | Um Annihilation Pursuer, spawn a 1 bloco atrás, 12.000 ticks e recast provider | ⛔ atributos/AI/range não homologados |
| `flameborn_drift` | [flameborn drift](annihilation/flameborn-drift.md) | Dash proporcional ao spell power, invulnerableTime=15 e FLAMEBORN_DASH_EFFECT | ⛔ movimento/i-frames/dano downstream |
| `hematite_trishula` | [hematite trishula](blood/hematite-trishula.md) | SoulTrident com power e spawn offset; hit aplica spell DamageSource; 400 ticks pode gerar SoulPillar | ⛔ hit/filhos sem contrato |
| `possessed_wing` | [possessed wing](blood/possessed-wing.md) | Self-buff 400/800 ticks; speed +10% e STEP_HEIGHT +0.25 via MobEffect | ⛔ attr/lifecycle por RPG |
| `collapsed_kingdoms_legion` | [collapsed kingdoms legion](evocation/collapsed-kingdoms-legion.md) | Três tipos de summons fixos; SummonManager owner/recast e 10 min | ⛔ AI/atributos de NPC |
| `flame_eater` | [flame eater](fire/flame-eater.md) | Target helper range 32, recast multi-target, 1 coluna por UUID em onRecastFinished | ⛔ custo/target/recast duplicados |
| `sentinel_saturation` | [sentinel saturation](fire/sentinel-saturation.md) | 3/5 DuneSentinelPhantomEntity em linha com findGround; dano externo | ⛔ count/geo e DamageType desconhecido |
| `glacier_eruption` | [glacier eruption](ice/glacier-eruption.md) | 4–10 IceSpikeEntity numa linha; warmup i+1, findGround 6/3 | ⛔ range/hitbox externa |
| `cloud_rail` | [cloud rail](lightning/cloud-rail.md) | 3–12 SpellCloudEntity; hit com AABB (1,1.5,1), dano inverso à distância | ⛔ velocidade/target/hitbox |
| `cloud_ring` | [cloud ring](lightning/cloud-ring.md) | 4/13/28/48/73 nuvens por nível; DamageSource consulta CLOUD_RAIL_SPELL | ⛔ cross-spell attribution |
| `nimbus_array` | [nimbus array](lightning/nimbus-array.md) | 2–14 LightningBoltEntity em linha; vida 25–40 ticks | ⛔ hitbox/dano Legendary Monsters |
| `triple_nimbus_array` | [triple nimbus array](lightning/triple-nimbus-array.md) | 2–10 fileiras ×3 = 6/12/18/24/30 LightningBoltEntity | ⛔ fan-out/gates |
| `thunder_fanburst` | [thunder fanburst](lightning/thunder-fanburst.md) | 3–12 ElectricityEntity em fan 70°; vida 30–75 ticks | ⛔ damage type e colisão externa |
| `tornado` | [tornado](lightning/tornado.md) | preCast helper range12 versus fallback raycast42; MISS pode não gerar Tornado | ⛔ targeting/settlement |
| `quad_tornado` | [quad tornado](lightning/quad-tornado.md) | 3–7 Tornado em círculo de raio 1.5; duração 30–70 ticks | ⛔ fanout e movimento |
| `ambush_thorns` | [ambush thorns](nature/ambush-thorns.md) | LivingDamageEvent.Pre; 50% de chance de thorns, originalDamage×0.2 + base | ⛔ evento PRE não prova dano |
| `overgrown_shockwave` | [overgrown shockwave](nature/overgrown-shockwave.md) | 36/64/100/144 entidades potenciais; return total se findGround falhar; poison sem hurt guard | ⛔ AOE/dano/stop parcial |

## Achados adicionais da auditoria de 20 fichas — 17/10/2026

- **Annihilation Bomb:** `bulletAmount=25+5×level` é parâmetro exibido, mas dois loops `i < bulletAmount/2` realizam `2×floor(bulletAmount/2)` tentativas de fragmentos. Em níveis com contagem ímpar, total real é um a menos.
- **Cloud Ring:** o `SpellCloudEntity` compartilhado usa `LSSpellRegistry.CLOUD_RAIL_SPELL` para DamageSource, mesmo quando criado por Cloud Ring. É divergência source-pinned, não bug físico validado.
- **Overgrown Shockwave:** `findGround == null` executa `return` no `onCast` inteiro; até 144 spawns seriam possíveis no lvl4 sem obstáculos. `SpellPoisonousShockwaveEntity` tenta POISON após DamageSources.applyDamage sem conferir resultado.
- **Tornado e Quad Tornado:** target helper de Tornado usa alcance 12 mas fallback raycast chega a 42; Quad cria 3..7 tornados, não sempre quatro. Não interpretar nome/tooltip como parâmetro causal.
- **Ambush Thorns:** `LivingDamageEvent.Pre` com trigger 50% e DamageSource `thorns`; dano não está liquidado nesse evento. Reação e cadeia recursiva exigem QA.
- **Summons:** `SummonFlamebornKnightsSpell` emite 2 unidades, `ReleaseRiftwalkerPredatorSpell` 1 e `CollapsedKingdomsLegionSpell` 3, independentes do spellLevel para **quantidade**; atributos e duração usam contracts do `BaseSummonSpell`.

Nenhuma destas observações autoriza hooks novos; todas são `SOURCE_CAUSALITY`, ⛔ até paridade binária/QA físico para mudanças de target, cooldown, dano, geometria, summons e Mastery.

## Contratos de engenharia e testes

1. **Tipos de dano e escola:** `spell.getDamageSource`, `damageSources().mobAttack` e source de `FLAME_EATER_SPELL` são distintos. `legendary_spellbooks:annihilation` tem escola própria. Não etiquetar como Lightning/Fire nem conceder Mastery por nome quando o `DamageSource` real divergir. Validar com handler real do modpack.
2. **Target, range e geometria:** UI de Resonance e Shockwave não substitui loop de AABB/raycast; raio visual não equivale à hitbox; anéis e feixes podem gerar dezenas/centenas de entidades. Qualquer perk que altere fan-out, alcance, hitbox ou cooldown requer seam contratual real, limites determinísticos e QA de claims/PvP.
3. **Custo:** para as trinta magias, mana, spell power, school power, cast time e cooldown passam pelo host Iron's. Campos de classe e `DefaultConfig` descrevem valores neutros; configuração instalada e multiplicadores por caster podem alterar resultados. Black Arcana não cobra mana paralela nem intercepta `SpellCastEvent` por analogia com Ars.
4. **Causalidade:** 1 cast → n projéteis/portais/colunas/summons → potenciais hits e statuses. Um evento de spawn, `CriticalHitEvent` ou `ActionActivatedEvent` não é um damage settlement. Token e idempotência do cast exigem desenho/validação com o provider.
5. **Clean room:** somente observações, identificadores, fórmulas e links permanentes públicos; não copiar implementações/assets. `CONDITIONED_ADAPTER` é possibilidade, não hook pronto.

## Aceitação e backlog

**PENDENTE:** reconciliação binária dos corpos source com JAR exato do addon e de seus helpers do Iron's 3.16.3/Legendary Monsters 2.2.2, casting com jogador conectado, server/client, cooldowns e mana reais, damage/DoT/HP% pós-evento, mouseover e claims, anti-magic, friendly fire, múltiplos targets/iframes, summon/recast, GroundRaycast, regiões não carregadas, death/logout e persistência. **Stage 06.05 continua 🟡, Stage 09 físico PENDING, PR #825 draft.** Aprofundamento documental das 30 fichas concluído neste índice; a próxima frente é paridade binária, QA e adapters condicionados. Não declarar runtime aprovado antes de confirmar os detalhes de execução.
