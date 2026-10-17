# Legendary Spellbooks 0.3.2 — matriz de engenharia causal para perks

**Checkpoint 17/10/2026 · PR #825 (draft).** Esta matriz só introduz documentação. O addon preserva o runtime provider-native da Iron's Spells e da Legendary Monsters; Black Arcana é dono de seu casting/rituais e RPG Skill Tree exclusivamente de Mastery/perks/atributos/gates após contratos validados.

## Proveniência e barra de progresso

- Instalação no sibling: `legendary_spellbooks-1.21.1+neo-0.3.2.jar`, mod ID `legendary_spellbooks`, SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`; [prova exata 30/30](EXACT-BINARY-SPELLS-0.3.2.md), [Java21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179) SUCCESS no commit histórico. `COUNTED_EXACT` refere-se ao **registro estático**, não à equivalência do corpo de métodos.
- Código da release 0.3.2 [Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3](https://github.com/Higurashi34m/Legendary-Spellbooks/tree/62ced2f2b2693aa841251473cbbd726fdd928ed3); comportamentos abaixo `SOURCE_CAUSALITY`. O pin era desenvolvido com Iron's **3.16.1** e Legendary Monsters **2.1.14**; o pack possui **3.16.3** e **2.2.2**, e essa matriz não valida compatibilidade.
- **Barra por provider — identidade de spell: 30/30 = 100%**. **Barra por provider — engenharia causal por ficha na tranche: 10/30 = 33,33%**, restam **20** fichas no padrão aprofundado deste checkpoint. As outras 20 já têm páginas descritivas, porém ainda não receberam esta verificação focada de parâmetros, helpers, efeitos e hooks. **Adapters perks homologados: 0**. Não declarar 33,33% de desenvolvimento do runtime.
- **Barra global — —%**: mínimo do checkpoint vigente **1.856 objetos semânticos / 1.854 estritos**, denominador global aberto; há documentos históricos com mínimos diferentes. **+0 novas magias** nesta tranche, nenhuma Stage promovida.

## Dez fichas com matriz source-causal por habilidade

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

## Contratos de engenharia e testes

1. **Tipos de dano e escola:** `spell.getDamageSource`, `damageSources().mobAttack` e source de `FLAME_EATER_SPELL` são distintos. `legendary_spellbooks:annihilation` tem escola própria. Não etiquetar como Lightning/Fire nem conceder Mastery por nome quando o `DamageSource` real divergir. Validar com handler real do modpack.
2. **Target, range e geometria:** UI de Resonance e Shockwave não substitui loop de AABB/raycast; raio visual não equivale à hitbox; anéis e feixes podem gerar dezenas/centenas de entidades. Qualquer perk que altere fan-out, alcance, hitbox ou cooldown requer seam contratual real, limites determinísticos e QA de claims/PvP.
3. **Custo:** para as dez magias, mana, spell power, school power, cast time e cooldown passam pelo host Iron's. Campos de classe e `DefaultConfig` descrevem valores neutros; configuração instalada e multiplicadores por caster podem alterar resultados. Black Arcana não cobra mana paralela nem intercepta `SpellCastEvent` por analogia com Ars.
4. **Causalidade:** 1 cast → n projéteis/portais/colunas/summons → potenciais hits e statuses. Um evento de spawn, `CriticalHitEvent` ou `ActionActivatedEvent` não é um damage settlement. Token e idempotência do cast exigem desenho/validação com o provider.
5. **Clean room:** somente observações, identificadores, fórmulas e links permanentes públicos; não copiar implementações/assets. `CONDITIONED_ADAPTER` é possibilidade, não hook pronto.

## Aceitação e backlog

**PENDENTE:** reconciliação binária dos corpos source com JAR exato do addon e de seus helpers do Iron's 3.16.3/Legendary Monsters 2.2.2, casting com jogador conectado, server/client, cooldowns e mana reais, damage/DoT/HP% pós-evento, mouseover e claims, anti-magic, friendly fire, múltiplos targets/iframes, summon/recast, GroundRaycast, regiões não carregadas, death/logout e persistência. **Stage 06.05 continua 🟡, Stage 09 físico PENDING, PR #825 draft.** Próximas 20 fichas em [README](README.md), sem declarar auditoria concluída antes de confirmar os detalhes de cada uma.
