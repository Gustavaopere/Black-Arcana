# Pale Thorn — Backported Spellbooks

- **ID estático exato:** `backportedspellbooks:pale_thorn`
- **Classe do JAR físico:** `net.redreaper.backported_spellbooks.spells.nature.PaleThornSpell`
- **Registry:** `ModSpellRegistry.PALE_THORN`
- **JAR certificado:** `backportedspellbooks-0.1.2.jar` (metadata embutido `0.1.0`)
- **Evidência:** ✅ `COUNTED_EXACT` para registro estático no [dossiê 0.1.2](../EXACT-BINARY-SPELLS-0.1.2.md); não é PASS de gameplay

## Comportamento documentado (fonte de referência)

Spell Pale Flora cuja cadeia física passa por AbstractPaleSpells → AbstractSpell; efeitos e comportamento de targeting necessitam QA.

A descrição de gameplay é uma leitura limitada da fonte oficial [`@07cb65efca0c`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/tree/07cb65efca0c264762a21c2d6bce0f83e3947226), não uma garantia de bytecode funcional exato ou configuração do pack.

## Dossiê técnico para perks — source oficial de referência (18/10/2026)

**Localizador do Codex:** [`PaleThornSpell.java`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/blob/07cb65efca0c264762a21c2d6bce0f83e3947226/src/main/java/net/redreaper/backported_spellbooks/spells/nature/PaleThornSpell.java); consumidores [1]: [`PaleThornVisualEntity.java`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/blob/07cb65efca0c264762a21c2d6bce0f83e3947226/src/main/java/net/redreaper/backported_spellbooks/entities/spell/pale_thorn/PaleThornVisualEntity.java). Registry no JAR exato é o documentado no início da ficha. Método principal `onCast`; consumidores e métodos de efeito abaixo quando presentes.

- **Casting/defaults da fonte:** `INSTANT`, `castTime=0`, `PALE_FLORA`, COMMON, máximo 5, cooldown 10 s, mana base 25, mana/nível 15, power base 6, power/nível 1.
- **Targeting:** `Utils.raycastForEntity(level,caster,15,false,0.15f)`, com **15 blocos** retornados por `getRange`, constante e não escalada pelo spellLevel nessa fonte; hit ENTITY causa dano, hit BLOCK somente VFX. Cria `PaleThornVisualEntity` entre olho e hit (lifetime declarado `30` ticks), que é visual e não uma segunda fonte de dano.
- **Dano:** para caster presente, `5 + 0.4*getSpellPower(level,caster)*(0.5*NatureSpellPower + 0.5*EldritchSpellPower)`. Fallback quando caster null: `getSpellPower(level,null)*1.5`. O nome de variável da fonte (`firePower`/`bloodPower`) **não altera** os atributos efetivamente referenciados.
- **Status:** acertando `LivingEntity`, adiciona `PARANOIA` por `int(getSpellPower*100)` ticks, amp 1. O método não mostra um segundo filtro manual de friendly fire além da política dos utilitários de raycast/dano (não auditados).
- **Perks:** alcance, atributos e duração são pontos de **leitura matemática**, não setters externos comprovados. Duração de VFX (30) é distinta da duração do status.

**Classe de evidência:** `SOURCE_PINNED_RELEASE_DAY`, com ID estático `BINARY_EXACT_0.1.2`; números/fórmulas **não** certificados no bytecode 0.1.2 nem em gameplay. Os defaults do `DefaultConfig` podem ser alterados pelo host; custo/cooldown realizado e assinatura de hook para perks = **NÃO VERIFICADO / ⛔**. [Matriz comparativa](../PERK-CAUSAL-SOURCE-MATRIX-0.1.2.md).

**Authority:** Iron's conserva casting, recurso, configuração e cooldown. Backported Spellbooks conserva efeitos/entidades. RPG Skill Tree apenas progressão por boundary real, Black Arcana apenas runtime próprio. Não executar efeitos/cobranças duplicadas nem conceder Mastery por projectile, tick ou hit isolado.

## Evidência física exata — raycast, VFX e status (18/10/2026)

✅ [Auditoria Java21 #39133252975](../EXACT-BINARY-BOMB-THORN-0.1.2.md) **SUCCESS**, hash publisher verificado e 10/10 autotestes; artifact [12138732504](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39133252975/artifacts/12138732504). O JAR 0.1.2 contém `getRange=15.0f`, `getDuration=int(getSpellPower*100f)`, o branch nulo `getSpellPower*1.5f` e os parâmetros de dano com `NATURE_SPELL_POWER`, `ELDRITCH_SPELL_POWER`, `5.0`, `0.4f` e duas ponderações `0.5`. No `onCast`, o raycast recebe `getRange`, `false` e `0.15f`; cria `PaleThornVisualEntity` e registra no Level antes da separação `ENTITY`/`BLOCK`. No ramo ENTITY, há um `DamageSources.applyDamage` e um `MobEffectInstance(PARANOIA)`. A VFX descarta após o limiar `tickCount>30`, **separado da duração do status**.

**Eixo de perk documentado:** alcance de busca e tolerância de raycast, dano por atributos, duração de Paranoia e lifetime visual são superfícies diferentes. Não foi observado callsite direto de `isFriendlyFireBetween` no próprio `onCast`, mas os utilitários Iron's podem filtrar PvP/claims; ⚠️ runtime não verificado. **⛔** Nenhum setter público de alcance/targeting ou duração foi homologado.

## Contratos e pendências

- **Authority:** Iron's para cast, mana, cooldown; addon para efeitos/projéteis; Black Arcana não replica o settlement.
- **⚠️ Não verificados no modpack:** parâmetros finais de dano/mana/cooldown, targeting, friendly-fire/PvP, duração, rareza, nível máximo efetivo, aquisição, sincronização MP e Survival.
- **Deduplicação:** esta identidade já estava contada antes da prova; **+0** novas magias.
