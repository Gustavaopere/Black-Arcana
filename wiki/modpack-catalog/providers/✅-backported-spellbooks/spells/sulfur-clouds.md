# Sulfur Clouds — Backported Spellbooks

- **ID estático exato:** `backportedspellbooks:sulfur_clouds`
- **Classe do JAR físico:** `net.redreaper.backported_spellbooks.spells.nature.SulfurCloudSpell`
- **Registry:** `ModSpellRegistry.SULFUR_CLOUD`
- **JAR certificado:** `backportedspellbooks-0.1.2.jar` (metadata embutido `0.1.0`)
- **Evidência:** ✅ `COUNTED_EXACT` para registro estático no [dossiê 0.1.2](../EXACT-BINARY-SPELLS-0.1.2.md); não é PASS de gameplay

## Comportamento documentado (fonte de referência)

Na referência de source há criação de projéteis/nuvens de sulfur; a quantidade emitida, duração e regras de colisão permanecem sujeitas à validação binária funcional.

A descrição de gameplay é uma leitura limitada da fonte oficial [`@07cb65efca0c`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/tree/07cb65efca0c264762a21c2d6bce0f83e3947226), não uma garantia de bytecode funcional exato ou configuração do pack.

## Dossiê técnico para perks — source oficial de referência (18/10/2026)

**Localizador do Codex:** [`SulfurCloudSpell.java`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/blob/07cb65efca0c264762a21c2d6bce0f83e3947226/src/main/java/net/redreaper/backported_spellbooks/spells/nature/SulfurCloudSpell.java); consumidores [1]: [`SulfurCloudProjectile.java`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/blob/07cb65efca0c264762a21c2d6bce0f83e3947226/src/main/java/net/redreaper/backported_spellbooks/entities/spell/sulfur_clouds/SulfurCloudProjectile.java). Registry no JAR exato é o documentado no início da ficha. Método principal `onCast`; consumidores e métodos de efeito abaixo quando presentes.

- **Casting/defaults da fonte:** `LONG`, `castTime=45`, Nature, RARE, máximo 10, cooldown 16 s, mana base 50, mana/nível 5, power base 15, power/nível 1.
- **Quantidade e targeting:** com `!world.isClientSide`, gera **3 entidades** `SulfurCloudProjectile` nos ângulos `0°,-15°,+15°` (rotação Y do olhar) com `shoot(...,1.25f,0)`. A classe do projétil também retorna `getSpeed=0.5f`; o resultado da combinação no host é **NÃO VERIFICADO**, sem alcance/LOS fixados.
- **Dano e efeitos:** dano configurado `getSpellPower(level,caster)`. Em `onHitEntity`, só aplica uma vez por entidade registrada em `victims`, Sulfuric Poison e Confusion de `5*20=100` ticks, amp 1.
- **Lifecyle de entidades:** `lifetime=100` (ticks de entidade), `hitsPerTick<5` no ramo de piercing, `getPierceLevel()!=0`. O source invoca `super.tick()` **duas vezes por chamada** do próprio `tick`: potencial multiplicação de processamento, **não** prova de 2x dano ou 2x vida útil no JAR instalado.
- **Causalidade:** 3 projéteis pertencem a **uma** execução; não conceder três casts de Mastery. Limites reais de vítimas e duplicidade sob colisão/projétil atravessando mundo continuam ⚠️.

**Classe de evidência:** `SOURCE_PINNED_RELEASE_DAY`, com ID estático `BINARY_EXACT_0.1.2`; números/fórmulas **não** certificados no bytecode 0.1.2 nem em gameplay. Os defaults do `DefaultConfig` podem ser alterados pelo host; custo/cooldown realizado e assinatura de hook para perks = **NÃO VERIFICADO / ⛔**. [Matriz comparativa](../PERK-CAUSAL-SOURCE-MATRIX-0.1.2.md).

**Authority:** Iron's conserva casting, recurso, configuração e cooldown. Backported Spellbooks conserva efeitos/entidades. RPG Skill Tree apenas progressão por boundary real, Black Arcana apenas runtime próprio. Não executar efeitos/cobranças duplicadas nem conceder Mastery por projectile, tick ou hit isolado.

## Confirmação posterior no bytecode do JAR 0.1.2 — 18/10/2026

✅ [Java21 #39131725388](../EXACT-BINARY-PERK-CONSUMERS-0.1.2.md) comprovou **duas** instruções `invokespecial ...tick()` com o mesmo proprietário no método compilado `SulfurCloudProjectile.tick()`, ambas anteriores a `createParticleSphere()`. Verificador 8/8 autotestes, SHA-1 publisher físico confirmado, artefato **12138535465**. Isso eleva **a presença das duas chamadas** de SOURCE_PINNED a BINARY_EXACT. A frequência efetiva de atualizações, processamento do host, dano por tick, lifetime e problemas causais em jogo **não** foram medidos. Perks que modificam velocidade/cadência ou concedem Mastery continuam ⛔ sem contrato.

## Contratos e pendências

- **Authority:** Iron's para cast, mana, cooldown; addon para efeitos/projéteis; Black Arcana não replica o settlement.
- **⚠️ Não verificados no modpack:** parâmetros finais de dano/mana/cooldown, targeting, friendly-fire/PvP, duração, rareza, nível máximo efetivo, aquisição, sincronização MP e Survival.
- **Deduplicação:** esta identidade já estava contada antes da prova; **+0** novas magias.
