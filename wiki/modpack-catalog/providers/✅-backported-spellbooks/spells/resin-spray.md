# Resin Spray — Backported Spellbooks

- **ID estático exato:** `backportedspellbooks:resin_spray`
- **Classe do JAR físico:** `net.redreaper.backported_spellbooks.spells.nature.ResinSpraySpell`
- **Registry:** `ModSpellRegistry.RESIN_SPRAY`
- **JAR certificado:** `backportedspellbooks-0.1.2.jar` (metadata embutido `0.1.0`)
- **Evidência:** ✅ `COUNTED_EXACT` para registro estático no [dossiê 0.1.2](../EXACT-BINARY-SPELLS-0.1.2.md); não é PASS de gameplay

## Comportamento documentado (fonte de referência)

Spell Pale Flora de casting contínuo na referência de source; estado de sessão, cancelamento e dano só podem ser integrados por contrato Iron's real.

A descrição de gameplay é uma leitura limitada da fonte oficial [`@07cb65efca0c`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/tree/07cb65efca0c264762a21c2d6bce0f83e3947226), não uma garantia de bytecode funcional exato ou configuração do pack.

## Dossiê técnico para perks — source oficial de referência (18/10/2026)

**Localizador do Codex:** [`ResinSpraySpell.java`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/blob/07cb65efca0c264762a21c2d6bce0f83e3947226/src/main/java/net/redreaper/backported_spellbooks/spells/nature/ResinSpraySpell.java); consumidores [1]: [`ResinSprayProjectile.java`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/blob/07cb65efca0c264762a21c2d6bce0f83e3947226/src/main/java/net/redreaper/backported_spellbooks/entities/spell/resin_spray/ResinSprayProjectile.java). Registry no JAR exato é o documentado no início da ficha. Método principal `onCast`; consumidores e métodos de efeito abaixo quando presentes.

- **Casting/defaults da fonte:** `CONTINUOUS`, `castTime=100`, `PALE_FLORA`, COMMON, máximo 10, cooldown 12 s, mana base 5, mana/nível 1, power base 0, power/nível 1. Tempo em ticks/consumo por ciclo: **NÃO VERIFICADO** até checar contrato Iron's.
- **Lifecycle e targeting:** em `onCast`, se `MagicData.isCasting`, spellId corrente e `additionalCastData instanceof EntityCastData` apontam para `AbstractConeProjectile`, ativa `cone.setDealDamageActive()`. Caso contrário, cria **um** `ResinSprayProjectile` na região dos olhos, define dano e armazena esse projétil em `MagicData.setAdditionalCastData`. Isso é **estado de uma sessão**, não respawn obrigatório por callback.
- **Dano/effects:** para caster presente, `5+0.4*getSpellPower(level,caster)*(0.5*NatureSpellPower+0.5*EldritchSpellPower)`; fallback caster null `getSpellPower(level,null)*0.75`. Em `ResinSprayProjectile.onHitEntity`, Resin Poison por 100 ticks/amp 1 **apenas se** `DamageSources.applyDamage` retornar true e alvo for `LivingEntity`.
- **IA e geometria:** `shouldAIStopCasting` compara `distanceToSqr(target)>120` (distância de interrupção para mob, **não** alcance de alvo humano ou raio de cone). `ResinSprayProjectile` herda `AbstractConeProjectile`; ângulo, tamanho da hitbox, intervalo de hits e persistência efetiva pertencem ao host e permanecem **NÃO VERIFICADO**.
- **Perks/causalidade:** não duplicar spawn nem `setDealDamageActive` para criar ticks adicionais; observar evento real de sessão, onHit/dano e conclusão antes de premiar Mastery.

**Classe de evidência:** `SOURCE_PINNED_RELEASE_DAY`, com ID estático `BINARY_EXACT_0.1.2`; números/fórmulas **não** certificados no bytecode 0.1.2 nem em gameplay. Os defaults do `DefaultConfig` podem ser alterados pelo host; custo/cooldown realizado e assinatura de hook para perks = **NÃO VERIFICADO / ⛔**. [Matriz comparativa](../PERK-CAUSAL-SOURCE-MATRIX-0.1.2.md).

**Authority:** Iron's conserva casting, recurso, configuração e cooldown. Backported Spellbooks conserva efeitos/entidades. RPG Skill Tree apenas progressão por boundary real, Black Arcana apenas runtime próprio. Não executar efeitos/cobranças duplicadas nem conceder Mastery por projectile, tick ou hit isolado.

## Confirmação posterior da bifurcação de casting — 18/10/2026

✅ [Java21 #39131725388](../EXACT-BINARY-PERK-CONSUMERS-0.1.2.md) verificou no método compilado `ResinSpraySpell.onCast` os callsites ordenados `MagicData.isCasting`, `getCastingSpellId`, `getAdditionalCastData` e `EntityCastData.getCastingEntity`, guardas de tipo `EntityCastData`/`AbstractConeProjectile`, além de `setDealDamageActive` e do ramo subsequente com `new ResinSprayProjectile`, `Level.addFreshEntity` e `MagicData.setAdditionalCastData`. SHA publisher confirmado, 8/8 autotestes, artefato **12138535465**. Confirma **a presença do fluxo compilado**, não a condição escolhida em cliente real, persistência, emissão de dano por tick ou API segura para perk. Não tratar reativação como novo cast; ⛔ sem boundary real.

## Contratos e pendências

- **Authority:** Iron's para cast, mana, cooldown; addon para efeitos/projéteis; Black Arcana não replica o settlement.
- **⚠️ Não verificados no modpack:** parâmetros finais de dano/mana/cooldown, targeting, friendly-fire/PvP, duração, rareza, nível máximo efetivo, aquisição, sincronização MP e Survival.
- **Deduplicação:** esta identidade já estava contada antes da prova; **+0** novas magias.
