# Wither Skull

- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR do pack:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Blood
- **Níveis:** 1–10
- **Raridade:** Uncommon → Legendary
- **Tipo de cast:** Instant
- **Recurso:** mana nativa do Iron's
- **Custo:** 20–38 mana
- **Cooldown:** 1 s
- **Dano:** 6–10.5

## O que faz

Lança um projétil em forma de wither skull que explode em pequena área ao impactar. A velocidade do projétil cresce com o nível.

## Escalonamento

Dano, custo e velocidade do projétil escalam com o nível. Raio exato da explosão ainda será normalizado.

## Obtenção e aprendizado

Segue o pipeline nativo de scrolls/spell books do Iron's, com equipagem via Inscription Table. Blood usa **Blood Vial** como Focus no Scroll Forge. Loot/config específicos ainda serão verificados.

## Interações / deduplicação

Ocupa o nicho de projétil Blood/wither explosivo de alta frequência. Também precisa ser comparado com Goety e outros providers que usam wither skulls.

## VFX / animação / áudio

A catalogar visualmente no runtime do pack.

## Fonte

`https://iron.wiki/spells/` · `https://iron.wiki/schools/` · `https://iron.wiki/progression/`.

## Parâmetros de implementação para perks — código auditado

- **Source exato:** [`WitherSkullSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/blood/WitherSkullSpell.java) (`e4056af90302d37eb1739f5ff05020b020e6e252`, versão declarada 1.21.1-3.16.3); classe `io.redspace.ironsspellbooks.spells.blood.WitherSkullSpell`.
- **ID:** `irons_spellbooks:wither_skull`. **DefaultConfig:** `RARE/UNCOMMON/COMMON=UNCOMMON` (raridade mínima), maxLevel `10`, cooldown `1` segundos, cast `INSTANT`.
- **Campos Java verificados:** `baseManaCost=20`, `manaCostPerLevel=2`, `baseSpellPower=12`, `spellPowerPerLevel=1`, `castTime=0` ticks. Custo base a nível n: `(int)((baseManaCost + manaCostPerLevel*(n-1))*MANA_MULTIPLIER)`.
- **Métodos-base relevantes:** `getDefaultConfig()`, `getCastType()`, `getSpellResource()`, `onCast(...)`; consulte a classe vinculada para helpers e entidades específicas.

### Causalidade e eixos técnicos

onCast cria WitherSkullProjectile no vetor frontal, damage=0.5*getSpellPower(level,caster), speed=(6+level)*0.08f. Raio da explosão, tipo de dano, efeitos e impacto com blocos pertencem à implementação de WitherSkullProjectile e devem ser auditados antes de perks de área/elemento. Spell power é modificador nativo para dano; speed não é necessariamente acessível por eventos genéricos.

### Limites de integração

Atributos nativos `SPELL_POWER` e poder da escola Blood podem alterar `getSpellPower`; isso **não prova** um hook genérico para modificar geometria, quantidade, efeito ou alvo. O RPG Skill Tree fornece perks/gates/Mastery; Iron's preserva a autoridade de casting/custos/cooldowns e entidades; Black Arcana só intervém através de contratos verificados. Nenhum adapter de efeitos foi implementado nesta ficha. Registro **estático/source-pinned**, não teste Survival. [Contrato transversal](../TECHNICAL-PERK-MAP.md).
