# Raise Dead

- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR do pack:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Blood
- **Níveis:** 1–6
- **Raridade:** Uncommon → Legendary
- **Tipo de cast:** Long
- **Recurso:** mana nativa do Iron's
- **Custo:** 50–100 mana
- **Cooldown:** 150 s
- **Invocações:** 3–8 mortos-vivos

## O que faz

Invoca minions mortos-vivos a partir do solo. Em níveis maiores, os summons recebem equipamento melhor.

## Escalonamento

A quantidade de summons cresce de 3 a 8 e a qualidade do equipamento também escala. Vida, dano, duração e regras exatas de ownership ainda serão normalizados.

## Obtenção e aprendizado

Segue o pipeline nativo de scrolls/spell books do Iron's, com equipagem via Inscription Table. Blood usa **Blood Vial** como Focus no Scroll Forge. Loot/config específicos ainda serão verificados.

## Interações / deduplicação

É uma referência obrigatória para necromancia e Binding: o Black Arcana não deve criar um summon genérico de mortos-vivos equivalente. Goety/Eidolon também serão comparados.

## VFX / animação / áudio

A catalogar visualmente no runtime do pack.

## Fonte

`https://iron.wiki/spells/` · `https://iron.wiki/schools/` · `https://iron.wiki/progression/`.

## Parâmetros de implementação para perks — código auditado

- **Source exato:** [`RaiseDeadSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/blood/RaiseDeadSpell.java) (`e4056af90302d37eb1739f5ff05020b020e6e252`, versão declarada 1.21.1-3.16.3); classe `io.redspace.ironsspellbooks.spells.blood.RaiseDeadSpell`.
- **ID:** `irons_spellbooks:raise_dead`. **DefaultConfig:** `RARE/UNCOMMON/COMMON=UNCOMMON` (raridade mínima), maxLevel `6`, cooldown `150` segundos, cast `LONG`.
- **Campos Java verificados:** `baseManaCost=50`, `manaCostPerLevel=10`, `baseSpellPower=10`, `spellPowerPerLevel=3`, `castTime=30` ticks. Custo base a nível n: `(int)((baseManaCost + manaCostPerLevel*(n-1))*MANA_MULTIPLIER)`.
- **Métodos-base relevantes:** `getDefaultConfig()`, `getCastType()`, `getSpellResource()`, `onCast(...)`; consulte a classe vinculada para helpers e entidades específicas.

### Causalidade e eixos técnicos

getSummonCount(level,caster)=level+2; lifetime das invocações=12000 ticks; getRecastCount=2. Cast gera SummonedZombie ou SummonedSkeleton (30% de chance do último), configura equipamento proporcional a spell power, emite NeoForge.EVENT_BUS.post(new SpellSummonEvent(...)) e chama SummonManager.initSummon. Recast usa SummonedEntitiesCastData e RecastInstance. SpellSummonEvent é um ponto concreto para avaliar substituição de criatura; não prova permissão para reescrever quantidade/cooldown sem observar o restante do pipeline.

### Limites de integração

Atributos nativos `SPELL_POWER` e poder da escola Blood podem alterar `getSpellPower`; isso **não prova** um hook genérico para modificar geometria, quantidade, efeito ou alvo. O RPG Skill Tree fornece perks/gates/Mastery; Iron's preserva a autoridade de casting/custos/cooldowns e entidades; Black Arcana só intervém através de contratos verificados. Nenhum adapter de efeitos foi implementado nesta ficha. Registro **estático/source-pinned**, não teste Survival. [Contrato transversal](../TECHNICAL-PERK-MAP.md).
