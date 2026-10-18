# Sulfur Bomb — Backported Spellbooks

- **ID estático exato:** `backportedspellbooks:sulfur_bomb`
- **Classe do JAR físico:** `net.redreaper.backported_spellbooks.spells.nature.SulfurBombSPell`
- **Registry:** `ModSpellRegistry.SULFUR_BOMB`
- **JAR certificado:** `backportedspellbooks-0.1.2.jar` (metadata embutido `0.1.0`)
- **Evidência:** ✅ `COUNTED_EXACT` para registro estático no [dossiê 0.1.2](../EXACT-BINARY-SPELLS-0.1.2.md); não é PASS de gameplay

## Comportamento documentado (fonte de referência)

Projétil de Sulfur Bomb e settlement de hit/AOE pertencem ao addon; valores de dano e regras de friendly-fire não validados.

A descrição de gameplay é uma leitura limitada da fonte oficial [`@07cb65efca0c`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/tree/07cb65efca0c264762a21c2d6bce0f83e3947226), não uma garantia de bytecode funcional exato ou configuração do pack.

## Dossiê técnico para perks — source oficial de referência (18/10/2026)

**Localizador do Codex:** [`SulfurBombSPell.java`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/blob/07cb65efca0c264762a21c2d6bce0f83e3947226/src/main/java/net/redreaper/backported_spellbooks/spells/nature/SulfurBombSPell.java); consumidores [2]: [`SulfurBombProjectile.java`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/blob/07cb65efca0c264762a21c2d6bce0f83e3947226/src/main/java/net/redreaper/backported_spellbooks/entities/spell/sulfur_bomb/SulfurBombProjectile.java), [`SulfurGasCloud.java`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/blob/07cb65efca0c264762a21c2d6bce0f83e3947226/src/main/java/net/redreaper/backported_spellbooks/entities/spell/sulfur_bomb/SulfurGasCloud.java). Registry no JAR exato é o documentado no início da ficha. Método principal `onCast`; consumidores e métodos de efeito abaixo quando presentes.

- **Casting/defaults da fonte:** `LONG`, `castTime=20`, Nature, UNCOMMON, máximo 8, cooldown 12 s, mana base 30, mana por nível 5, spell power base 8, power por nível 3.
- **Geometria:** spawna um `SulfurBombProjectile` no olhar do caster com impulso vertical +0.2; entidade declara `getSpeed=1.15f` (interação com `shoot` host ainda não auditada). Raio `r=3+getEntityPowerMultiplier(caster)`; `AABB.inflate(r)` para candidatos, **filtro separado** `distanceSq<r²` e LOS para dano de impacto.
- **Dano:** valor inserido no projétil `8*getEntityPowerMultiplier(caster)`; no impacto a fonte aplica `damage*(1-distanceSq/r²)`. O caster também injeta `aoeDamage=getSpellPower(level,caster)*0.185f` no projétil; este valor é usado no `SulfurGasCloud`, **não somar como dano imediato garantido**.
- **Causalidade pós-cast:** colisão com bloco provoca bounce; `bounces>=3` descarta. Impactos/blocos criam `SulfurGasCloud` com duração declarada 200 ticks, mesmo raio e dano AoE; o cloud usa `ISSDamageTypes.POISON_CLOUD`, `target.hurt`, Wither/Confusion 120 ticks. É **efeito secundário do mesmo cast**, não uma nova identidade.
- **Risco:** caminho `onHitEntity` faz cast de `entity` para `LivingEntity` após `canHitEntity`; elegibilidade e segurança para entidades não-vivas requerem teste real. Nenhum claim/PvP safe foi inferido.

**Classe de evidência:** `SOURCE_PINNED_RELEASE_DAY`, com ID estático `BINARY_EXACT_0.1.2`; números/fórmulas **não** certificados no bytecode 0.1.2 nem em gameplay. Os defaults do `DefaultConfig` podem ser alterados pelo host; custo/cooldown realizado e assinatura de hook para perks = **NÃO VERIFICADO / ⛔**. [Matriz comparativa](../PERK-CAUSAL-SOURCE-MATRIX-0.1.2.md).

**Authority:** Iron's conserva casting, recurso, configuração e cooldown. Backported Spellbooks conserva efeitos/entidades. RPG Skill Tree apenas progressão por boundary real, Black Arcana apenas runtime próprio. Não executar efeitos/cobranças duplicadas nem conceder Mastery por projectile, tick ou hit isolado.

## Evidência física exata — perímetro do impacto e nuvem (18/10/2026)

✅ [Auditoria Java21 #39133252975](../EXACT-BINARY-BOMB-THORN-0.1.2.md) **SUCCESS**, hash publisher `747847c1f38c73250ebac05ea06b41a381187850`, 10/10 novos autotestes, `PASS_BACKPORTED_012_BOMB_THORN_BOUNDED_BYTECODE`, artifact [12138732504](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39133252975/artifacts/12138732504). Confirmados nos métodos compilados: `getRadius=3.0f+getEntityPowerMultiplier`, `getAOEDamage=getSpellPower*0.185f`, `getSpeed=1.15f`; `onHitEntity` guarda lado servidor, cria `SulfurGasCloud` antes de filtrar candidatos via AABB, distância²/`canHitEntity`/LOS, processa `damage*(1-distanceSq/radiusSq)`, `applyDamage`, Wither e Confusion com parâmetros de **200 ticks**; `onHitBlock` possui três direções de reflexão, contador `bounces` e descarte em 3; cloud recebe duração 200, dano `aoeDamage` e raio do impacto.

**Eixo de perk documentado:** raio do projétil, seleção de candidatos, multiplicador do caster, dano do impacto e dano da nuvem são **variáveis distintas**. `AABB.inflate` não significa filtro final de raio por si só; `getSpeed` não prova a velocidade física. ⚠️ Foi detectado `checkcast LivingEntity` após `applyDamage` no loop de entidades, mas não um erro funcional provado: testar candidatos não-vivos e filtros do host. **⛔** Hook de mutação seguro ainda inexistente na prova.

## Contratos e pendências

- **Authority:** Iron's para cast, mana, cooldown; addon para efeitos/projéteis; Black Arcana não replica o settlement.
- **⚠️ Não verificados no modpack:** parâmetros finais de dano/mana/cooldown, targeting, friendly-fire/PvP, duração, rareza, nível máximo efetivo, aquisição, sincronização MP e Survival.
- **Deduplicação:** esta identidade já estava contada antes da prova; **+0** novas magias.
