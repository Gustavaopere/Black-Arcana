# Sacrifice

- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR do pack:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Blood
- **Níveis:** 1–5
- **Raridade:** Rare → Legendary
- **Tipo de cast:** Instant
- **Recurso:** mana nativa do Iron's
- **Custo:** 25–45 mana
- **Cooldown:** 1 s
- **Dano base:** 12–16
- **Raio base listado:** 3 blocos

## O que faz

Seleciona uma invocação mágica do próprio caster, mata o summon e o converte numa explosão ofensiva. A vida restante da criatura aumenta o dano e o raio da explosão.

## Escalonamento

O dano base e o custo aumentam com o nível. A fórmula exata que converte HP restante do summon em dano/raio ainda será normalizada.

## Obtenção e aprendizado

Segue o pipeline nativo de scrolls/spell books do Iron's, com equipagem via Inscription Table. Blood usa **Blood Vial** como Focus no Scroll Forge. Loot/config específicos ainda serão verificados.

## Interações / deduplicação

É uma referência crítica para qualquer sistema futuro de sacrifício de familiar/servo. Arcana Vincular não deve recriar esta mecânica sem delta causal/resource-routing claro.

## VFX / animação / áudio

A catalogar visualmente no runtime do pack.

## Fonte

`https://iron.wiki/spells/` · `https://iron.wiki/schools/` · `https://iron.wiki/progression/`.

## Parâmetros de implementação para perks — código auditado

- **Source exato:** [`SacrificeSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/blood/SacrificeSpell.java) (`e4056af90302d37eb1739f5ff05020b020e6e252`, versão declarada 1.21.1-3.16.3); classe `io.redspace.ironsspellbooks.spells.blood.SacrificeSpell`.
- **ID:** `irons_spellbooks:sacrifice`. **DefaultConfig:** `RARE/UNCOMMON/COMMON=RARE` (raridade mínima), maxLevel `5`, cooldown `1` segundos, cast `INSTANT`.
- **Campos Java verificados:** `baseManaCost=25`, `manaCostPerLevel=5`, `baseSpellPower=2`, `spellPowerPerLevel=1`, `castTime=0` ticks. Custo base a nível n: `(int)((baseManaCost + manaCostPerLevel*(n-1))*MANA_MULTIPLIER)`.
- **Métodos-base relevantes:** `getDefaultConfig()`, `getCastType()`, `getSpellResource()`, `onCast(...)`; consulte a classe vinculada para helpers e entidades específicas.

### Causalidade e eixos técnicos

Raycast até 25 blocos, bbInflation=0.25, somente IMagicSummon pertencente ao caster; onCast revalida owner UUID. getDamage=(10+getSpellPower(level,caster))*atributo SUMMON_DAMAGE; dano na detonação acrescenta 0.5*healthAtualDaInvocacao. getRadius=3*(1+0.5*healthAtual/maxHealth). doSacrificeExplosion usa AABB.ofSize(pos,radius,radius,radius), LOS e filtro de distância; a AABB pode limitar a cobertura efetiva mesmo quando o raio nominal é maior. A criatura é removida. Perks de raio/dano requerem limites, ownership, friendly fire e processamento único.

### Limites de integração

Atributos nativos `SPELL_POWER` e poder da escola Blood podem alterar `getSpellPower`; isso **não prova** um hook genérico para modificar geometria, quantidade, efeito ou alvo. O RPG Skill Tree fornece perks/gates/Mastery; Iron's preserva a autoridade de casting/custos/cooldowns e entidades; Black Arcana só intervém através de contratos verificados. Nenhum adapter de efeitos foi implementado nesta ficha. Registro **estático/source-pinned**, não teste Survival. [Contrato transversal](../TECHNICAL-PERK-MAP.md).
