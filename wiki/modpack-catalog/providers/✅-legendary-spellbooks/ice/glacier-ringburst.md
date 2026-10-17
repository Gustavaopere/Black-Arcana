# Glacier Ringburst

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT`, `legendary_spellbooks:glacier_ringburst` / `dev.higurashi.legendary_spellbooks.common.spells.ice.GlacierRingburstSpell`; [Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179), [dossiê SHA-exato](../EXACT-BINARY-SPELLS-0.3.2.md). Números/comportamentos source-pinned; execução/Survival ⚠️; +0 magias.

- ID: `legendary_spellbooks:glacier_ringburst`
- School: Ice
- Config levels: 1–4
- Min rarity: Epic
- Cooldown: 12 s
- Cast-time field: 20 ticks
- Mana neutral: 100 / 110 / 120 / 130
- Spell power neutral: 3 / 5 / 7 / 9
- Ring count: 3 / 4 / 5 / 6
- Spikes per ring: 8 / 10 / 12 / 14 from the provider's final-ring formula
- Ring radius sequence: `1.5 + ringIndex × 1.75`
- Warmup: `ringIndex × 2` ticks
- Crafting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Cria ondas concêntricas de ice spikes, com warmup crescente por anel. A spell desabilita looting e mantém toda a resolução no provider.

## Acquisition

O loot provider do Frostbitten Golem declara `Glacier Ringburst 1–5 (w10)`, apesar de a config da classe fixar `maxLevel=4`.

## QA obrigatório

A faixa de loot até nível 5 conflita estaticamente com o max level 4 da spell. Não normalizar para 4 ou 5 por suposição; o comportamento efetivo do roll/scroll precisa de runtime QA na versão instalada.

## Regra para o Black Arcana

Fail-closed para qualquer integração que dependa de um suposto nível 5 até o runtime resolver a discrepância. Não duplicar ice spikes.

## Source

`GlacierRingburstSpell.java`, `LSSpellScrollLootProvider.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Status:** `legendary_spellbooks:glacier_ringburst` COUNTED_EXACT 0.3.2 para registry; source 0.3.2 fixo `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3` para algoritmos, **⚠️ runtime/loot 1–5 versus maxLevel 4 pendente**.

| Eixo | Implementação factual | Mutabilidade externa |
|---|---|---|
| Cast/recursos | `DefaultConfig` maxLevel **4**, cooldown **12s**, castTime **20 ticks**, mana `100+10×(level−1)`, spell power `3+2×(level−1)` antes do caster multiplier. `getSpellPower` é convertido a `int` no cast: **truncamento do valor efetivo**, não dano decimal garantido. | Iron's controla mana/bonus de escola e casts; hook per-player para conversão e target não provado. |
| Origem/área | Centro = `caster.position()`. `ringCount=min(2+level,8)` (níveis 1–4: **3,4,5,6**). Cada anel i tem raio `1.5+i×1.75` blocos; no último anel a borda fica em **5 / 6.75 / 8.5 / 10.25 blocos** respectivamente. Isto é o raio do último anel, não range de aquisição. | `SEM_HOOK_SEGURO` para ampliar/mudar concentricidade, AOE e hitboxes. |
| Número de projéteis | `spikeCount=2+ringCount×2` é fixo **para todos os anéis do mesmo cast**: 8/10/12/14. Tentativas máximas totais = `ringCount×spikeCount` = **24/40/60/84** entidades por cast, quando `findGround` retorna posição para todos os pontos. | Multiplicação de contagem cresce custo do servidor; sem perk de +X espículas enquanto não houver cap/hook oficial. |
| Timing | Cada anel i recebe warmup **i×2 ticks**, passado ao construtor `SpellIceSpikeEntity`. A entidade herda `IceSpikeEntity` de Legendary Monsters; momento exato do dano, hitbox, tipo e lifetime **não estão no método auditado**. | `⛔` não prometer tick de dano, freeze, hitbox ou DamageType sem inspecionar versão física Legendary Monsters 2.2.2. |
| Limites de mundo | Para cada ponto, chama `RaycastUtils.findGround(level, point, 6, 3)`. Se retornar null, `break` encerra somente a **fileira interna desse anel** (loop de pontos), não toda a spell. | Spawn condicionado por terreno; WorldEffectPolicy Black Arcana não protege automaticamente efeitos externos. |
| Target/dano | Geometria de anel sobre blocos, não entity target/LOS; o cast passa damage (int) e caster a cada espícula. Dano realmente recebido depende do helper/entidade externa, i-frames e equipe. | `CONFIG_NATIVE` para stats globais; `SEM_HOOK_SEGURO` para target, dano por hit e física externa. |

**Âncoras:** [source da spell, formulas, loops](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/ice/GlacierRingburstSpell.java#L23-L78); [wrapper `SpellIceSpikeEntity`](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/entities/spell/projectile/SpellIceSpikeEntity.java#L9-L23).

**QA necessário:** mínimo e máximo níveis 1–4, loot nível 5, obstáculos/ground find, chuva de 84 entidades, picos de tick e chunk, client/despawn, anti-magic, PvP/friendly, efetivo damage/type. Cada spike é filho da mesma conjuração, não cast próprio. **+0 novas raízes e adapters.**
