# Blood Step

- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR do pack:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Blood
- **Níveis:** 1–5
- **Raridade:** Uncommon → Legendary
- **Tipo de cast:** Instant
- **Recurso:** mana nativa do Iron's
- **Custo:** 30–70 mana
- **Cooldown:** 12 s
- **Alcance:** 8–12 blocos
- **Dano:** 0 direto listado

## O que faz

Teleporta instantaneamente o caster para o ponto mirado ou diretamente para trás de uma criatura-alvo. Ao chegar, concede uma curta janela de invisibilidade verdadeira.

## Escalonamento

O alcance e o custo variam com o nível. A duração exata da invisibilidade ainda será normalizada.

## Obtenção e aprendizado

Segue o pipeline nativo de scrolls/spell books do Iron's, com equipagem via Inscription Table. Blood usa **Blood Vial** como Focus no Scroll Forge. Loot/config específicos desta magia ainda serão verificados.

## Interações / deduplicação

Ocupa mobilidade hemática de curto alcance + reposition atrás de alvo + invisibilidade. É relevante para deduplicar futuros teleports de Blood/Chaos.

## VFX / animação / áudio

A catalogar visualmente no runtime do pack.

## Fonte

`https://iron.wiki/spells/` · `https://iron.wiki/schools/` · `https://iron.wiki/progression/`.

## Parâmetros de implementação para perks — código auditado

- **Source exato:** [`BloodStepSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/blood/BloodStepSpell.java) (`e4056af90302d37eb1739f5ff05020b020e6e252`, versão declarada 1.21.1-3.16.3); classe `io.redspace.ironsspellbooks.spells.blood.BloodStepSpell`.
- **ID:** `irons_spellbooks:blood_step`. **DefaultConfig:** `RARE/UNCOMMON/COMMON=UNCOMMON` (raridade mínima), maxLevel `5`, cooldown `12` segundos, cast `INSTANT`.
- **Campos Java verificados:** `baseManaCost=30`, `manaCostPerLevel=10`, `baseSpellPower=8`, `spellPowerPerLevel=1`, `castTime=0` ticks. Custo base a nível n: `(int)((baseManaCost + manaCostPerLevel*(n-1))*MANA_MULTIPLIER)`.
- **Métodos-base relevantes:** `getDefaultConfig()`, `getCastType()`, `getSpellResource()`, `onCast(...)`; consulte a classe vinculada para helpers e entidades específicas.

### Causalidade e eixos técnicos

Distância: Utils.softCapFormula(getEntityPowerMultiplier(caster))*getSpellPower(level,null). Raycast e seleção de destino; para alvo vivo testa até 8 posições angulares atrás dele; teleporte executado por Utils.handleSpellTeleport. Aplica TRUE_INVISIBILITY por 100 ticks, zera fall distance. Range pode mudar pela potência, mas respeita soft cap. Perks de invisibilidade/segurança exigem inspecionar helper, proteção contra teleporte inválido e regressão Survival/PvP.

### Limites de integração

Atributos nativos `SPELL_POWER` e poder da escola Blood podem alterar `getSpellPower`; isso **não prova** um hook genérico para modificar geometria, quantidade, efeito ou alvo. O RPG Skill Tree fornece perks/gates/Mastery; Iron's preserva a autoridade de casting/custos/cooldowns e entidades; Black Arcana só intervém através de contratos verificados. Nenhum adapter de efeitos foi implementado nesta ficha. Registro **estático/source-pinned**, não teste Survival. [Contrato transversal](../TECHNICAL-PERK-MAP.md).
