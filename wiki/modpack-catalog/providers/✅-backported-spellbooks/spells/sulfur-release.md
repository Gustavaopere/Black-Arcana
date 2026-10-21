# Sulfur Release — Backported Spellbooks

- **ID estático exato:** `backportedspellbooks:sulfur_release`
- **Classe do JAR físico:** `net.redreaper.backported_spellbooks.spells.nature.SulfurReleaseSpell`
- **Registry:** `ModSpellRegistry.SULFUR_RELEASE`
- **JAR certificado:** `backportedspellbooks-0.1.2.jar` (metadata embutido `0.1.0`)
- **Evidência:** ✅ `COUNTED_EXACT` para registro estático no [dossiê 0.1.2](../EXACT-BINARY-SPELLS-0.1.2.md); não é PASS de gameplay

## Comportamento documentado (fonte de referência)

Na referência de source há comportamento radial e efeitos Sulfuric Poison; aplicação real, range e PvP não validados.

A descrição de gameplay é uma leitura limitada da fonte oficial [`@07cb65efca0c`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/tree/07cb65efca0c264762a21c2d6bce0f83e3947226), não uma garantia de bytecode funcional exato ou configuração do pack.

## Dossiê técnico para perks — source oficial de referência (18/10/2026)

**Localizador do Codex:** [`SulfurReleaseSpell.java`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/blob/07cb65efca0c264762a21c2d6bce0f83e3947226/src/main/java/net/redreaper/backported_spellbooks/spells/nature/SulfurReleaseSpell.java). Registry no JAR exato é o documentado no início da ficha. Método principal `onCast`; consumidores e métodos de efeito abaixo quando presentes.

- **Casting/defaults da fonte:** `LONG`, `castTime=24`, Nature, COMMON, máximo 5, cooldown 60 s, mana base 90, mana/nível 22, power base 6, power/nível 3.
- **Área/targeting:** explosão com centro no caster. Busca `entity.getBoundingBox().inflate(radius,4,radius)`, onde `radius=5+0.5*spellLevel`. Em seguida exige distância Euclidiana **estritamente menor** que `radius`, alvo `LivingEntity`, `!DamageSources.isFriendlyFireBetween(target,caster)` e `Utils.hasLineOfSight(...,false)`. Altura de seleção AABB ±4 não é raio esférico.
- **Resultado:** dano `getSpellPower(level,caster)` via `DamageSources.applyDamage`; aplica `SULFURIC_POISON` e `MobEffects.CONFUSION` por `int(getSpellPower*10)` ticks. Amplificador passado = `spellLevel-2`, que é **-1 no nível 1**; qualquer clamp/normalização ou comportamento efetivo precisa ser confirmado no host.
- **Perks/riscos:** separar raio de busca e filtro de distância de dano; efeitos de partículas `BlastwaveParticleOptions`/gás não são novos casts nem autoridade sobre o mundo. Limites de alvos, claims e resultado final dependem de Iron's/NeoForge.

**Classe de evidência:** `SOURCE_PINNED_RELEASE_DAY`, com ID estático `BINARY_EXACT_0.1.2`; números/fórmulas **não** certificados no bytecode 0.1.2 nem em gameplay. Os defaults do `DefaultConfig` podem ser alterados pelo host; custo/cooldown realizado e assinatura de hook para perks = **NÃO VERIFICADO / ⛔**. [Matriz comparativa](../PERK-CAUSAL-SOURCE-MATRIX-0.1.2.md).

**Authority:** Iron's conserva casting, recurso, configuração e cooldown. Backported Spellbooks conserva efeitos/entidades. RPG Skill Tree apenas progressão por boundary real, Black Arcana apenas runtime próprio. Não executar efeitos/cobranças duplicadas nem conceder Mastery por projectile, tick ou hit isolado.

## Confirmação posterior da aritmética compilada — 18/10/2026

✅ [Java21 #39131725388](../EXACT-BINARY-PERK-CONSUMERS-0.1.2.md) comprovou o corpo exato de `getWitherAmplifier(int,LivingEntity)` como `iload_1; iconst_2; isub; ireturn`, portanto a função compilada é **`spellLevel-2`**. Para argumento de nível 1, **o método devolve -1**. Isso não estabelece o amplificador efetivo após `MobEffectInstance` nem configurações do host, que seguem ⚠️. O workflow validou SHA-1 publisher, 8/8 autotestes, PASS de método e artifact **12138535465**. Não ajustar duração/efeito ou gameplay sem hook público e QA, ⛔.

## Contratos e pendências

- **Authority:** Iron's para cast, mana, cooldown; addon para efeitos/projéteis; Black Arcana não replica o settlement.
- **⚠️ Não verificados no modpack:** parâmetros finais de dano/mana/cooldown, targeting, friendly-fire/PvP, duração, rareza, nível máximo efetivo, aquisição, sincronização MP e Survival.
- **Deduplicação:** esta identidade já estava contada antes da prova; **+0** novas magias.
