# Heartstop

- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR do pack:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Blood
- **Níveis:** 1–5
- **Raridade:** Rare → Legendary
- **Tipo de cast:** Instant
- **Recurso:** mana nativa do Iron's
- **Custo:** 100–140 mana
- **Cooldown:** 120 s
- **Duração:** 10–16 s
- **Backlash:** 50% do dano acumulado durante a janela

## O que faz

Concede invulnerabilidade temporária. Enquanto Heartstop está ativo, o dano é acumulado; quando o efeito termina, 50% desse total retorna como backlash ao caster.

## Escalonamento

A duração e o custo aumentam com o nível. A proporção de backlash publicada permanece 50%.

## Obtenção e aprendizado

Segue o pipeline nativo de scrolls/spell books do Iron's, com equipagem via Inscription Table. Blood usa **Blood Vial** como Focus no Scroll Forge. Loot/config específicos ainda serão verificados.

## Interações / deduplicação

Ocupa o nicho de invulnerabilidade temporária com dívida de dano. É diferente de shield, immunity simples e Blood Price do Black Arcana.

## VFX / animação / áudio

A catalogar visualmente no runtime do pack.

## Fonte

`https://iron.wiki/spells/` · `https://iron.wiki/schools/` · `https://iron.wiki/progression/`.

## Parâmetros de implementação para perks — código auditado

- **Source exato:** [`HeartstopSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/blood/HeartstopSpell.java) (`e4056af90302d37eb1739f5ff05020b020e6e252`, versão declarada 1.21.1-3.16.3); classe `io.redspace.ironsspellbooks.spells.blood.HeartstopSpell`.
- **ID:** `irons_spellbooks:heartstop`. **DefaultConfig:** `RARE/UNCOMMON/COMMON=RARE` (raridade mínima), maxLevel `5`, cooldown `120` segundos, cast `INSTANT`.
- **Campos Java verificados:** `baseManaCost=100`, `manaCostPerLevel=10`, `baseSpellPower=200`, `spellPowerPerLevel=30`, `castTime=0` ticks. Custo base a nível n: `(int)((baseManaCost + manaCostPerLevel*(n-1))*MANA_MULTIPLIER)`.
- **Métodos-base relevantes:** `getDefaultConfig()`, `getCastType()`, `getSpellResource()`, `onCast(...)`; consulte a classe vinculada para helpers e entidades específicas.

### Causalidade e eixos técnicos

Aplica MobEffectRegistry.HEARTSTOP ao caster, por (int)getSpellPower(level,caster) ticks (200–320 antes de atributos/config). A Wiki descreve invulnerabilidade temporária e dano diferido de 50%, cuja implementação fica na classe do MobEffect, não em HeartstopSpell. Perk que altera duração/trade-off requer verificar armazenamento, remoção, logout e acúmulo, evitando evasão do custo diferido.

### Limites de integração

Atributos nativos `SPELL_POWER` e poder da escola Blood podem alterar `getSpellPower`; isso **não prova** um hook genérico para modificar geometria, quantidade, efeito ou alvo. O RPG Skill Tree fornece perks/gates/Mastery; Iron's preserva a autoridade de casting/custos/cooldowns e entidades; Black Arcana só intervém através de contratos verificados. Nenhum adapter de efeitos foi implementado nesta ficha. Registro **estático/source-pinned**, não teste Survival. [Contrato transversal](../TECHNICAL-PERK-MAP.md).
