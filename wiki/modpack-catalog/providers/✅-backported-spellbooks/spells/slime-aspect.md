# Slime Aspect — Backported Spellbooks

- **ID estático exato:** `backportedspellbooks:slime_aspect`
- **Classe do JAR físico:** `net.redreaper.backported_spellbooks.spells.nature.AspectOfTheSlimeSpell`
- **Registry:** `ModSpellRegistry.SLIME_ASPECT`
- **JAR certificado:** `backportedspellbooks-0.1.2.jar` (metadata embutido `0.1.0`)
- **Evidência:** ✅ `COUNTED_EXACT` para registro estático no [dossiê 0.1.2](../EXACT-BINARY-SPELLS-0.1.2.md); não é PASS de gameplay

## Comportamento documentado (fonte de referência)

Status effect Slime Aspect e interações de mobilidade (source de referência); impulse, air drag, bounce e parâmetros efetivos ainda não certificados no JAR 0.1.2 ou no jogo.

A descrição de gameplay é uma leitura limitada da fonte oficial [`@07cb65efca0c`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/tree/07cb65efca0c264762a21c2d6bce0f83e3947226), não uma garantia de bytecode funcional exato ou configuração do pack.

## Dossiê técnico para perks — source oficial de referência (18/10/2026)

**Localizador do Codex:** [`AspectOfTheSlimeSpell.java`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/blob/07cb65efca0c264762a21c2d6bce0f83e3947226/src/main/java/net/redreaper/backported_spellbooks/spells/nature/AspectOfTheSlimeSpell.java); consumidores [1]: [`SlimeAspectMobEffect.java`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/blob/07cb65efca0c264762a21c2d6bce0f83e3947226/src/main/java/net/redreaper/backported_spellbooks/effect/SlimeAspectMobEffect.java). Registry no JAR exato é o documentado no início da ficha. Método principal `onCast`; consumidores e métodos de efeito abaixo quando presentes.

- **Casting/defaults da fonte:** `INSTANT`, `castTime=0` (campo do construtor), Nature, RARE, máximo 5, cooldown declarado 90 s, `baseManaCost=35`, `manaCostPerLevel=5`, `baseSpellPower=20`, `spellPowerPerLevel=5`. Custo efetivo = **NÃO VERIFICADO**.
- **Alvo:** apenas o próprio caster em `onCast`; sem range/projétil/área declarados nesse método.
- **Efeito:** aplica `ModMobEffects.SLIME_ASPECT` por `int(getSpellPower(level,caster)*20)` **ticks**, amp `level-1`. O effect class expõe coeficientes `BOUNCE_PER_LEVEL=0.5`, `JUMP_PER_LEVEL=0.15`, `AIR_DRAG_PER_LEVEL=-0.10`; o consumidor real desses coeficientes não foi verificado nesta análise.
- **Perk axes:** duração e potência de mobilidade são **campos de cálculo provider-owned**, não hooks de mutação. Ao modelar duração, preservar a conversão float → int; não aplicar buff extra por callback de efeito.

**Classe de evidência:** `SOURCE_PINNED_RELEASE_DAY`, com ID estático `BINARY_EXACT_0.1.2`; números/fórmulas **não** certificados no bytecode 0.1.2 nem em gameplay. Os defaults do `DefaultConfig` podem ser alterados pelo host; custo/cooldown realizado e assinatura de hook para perks = **NÃO VERIFICADO / ⛔**. [Matriz comparativa](../PERK-CAUSAL-SOURCE-MATRIX-0.1.2.md).

**Authority:** Iron's conserva casting, recurso, configuração e cooldown. Backported Spellbooks conserva efeitos/entidades. RPG Skill Tree apenas progressão por boundary real, Black Arcana apenas runtime próprio. Não executar efeitos/cobranças duplicadas nem conceder Mastery por projectile, tick ou hit isolado.

## Contratos e pendências

- **Authority:** Iron's para cast, mana, cooldown; addon para efeitos/projéteis; Black Arcana não replica o settlement.
- **⚠️ Não verificados no modpack:** parâmetros finais de dano/mana/cooldown, targeting, friendly-fire/PvP, duração, rareza, nível máximo efetivo, aquisição, sincronização MP e Survival.
- **Deduplicação:** esta identidade já estava contada antes da prova; **+0** novas magias.
