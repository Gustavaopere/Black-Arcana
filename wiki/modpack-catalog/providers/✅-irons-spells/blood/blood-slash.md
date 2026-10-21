# Blood Slash

- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR do pack:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Blood
- **Níveis:** 1–5
- **Raridade:** Rare → Legendary
- **Tipo de cast:** Instant
- **Recurso:** mana nativa do Iron's
- **Custo:** 25–45 mana
- **Cooldown:** 10 s
- **Dano:** 10–14
- **Cura:** 15% do dano efetivamente causado

## O que faz

Dispara à frente uma lâmina concentrada de sangue que atravessa criaturas e devolve parte do dano como cura ao caster.

## Escalonamento

Dano e custo aumentam com o nível. Fórmula interna exata permanece provider-owned até validação permitida.

## Obtenção e aprendizado

Segue o pipeline nativo de scrolls/spell books do Iron's, com equipagem via Inscription Table. A Blood school usa **Blood Vial** como Focus no Scroll Forge. Loot/config específicos ainda serão verificados.

## Interações / deduplicação

Ocupa ataque hemático linear de alto dano com sustain. Qualquer nova Blood magic semelhante precisa demonstrar delta mecânico real.

## VFX / animação / áudio

A catalogar visualmente no runtime do pack.

## Fonte

`https://iron.wiki/spells/` · `https://iron.wiki/schools/` · `https://iron.wiki/progression/`.

## Parâmetros de implementação para perks — código auditado

- **Source exato:** [`BloodSlashSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/blood/BloodSlashSpell.java) (`e4056af90302d37eb1739f5ff05020b020e6e252`, versão declarada 1.21.1-3.16.3); classe `io.redspace.ironsspellbooks.spells.blood.BloodSlashSpell`.
- **ID:** `irons_spellbooks:blood_slash`. **DefaultConfig:** `RARE/UNCOMMON/COMMON=RARE` (raridade mínima), maxLevel `5`, cooldown `10` segundos, cast `INSTANT`.
- **Campos Java verificados:** `baseManaCost=25`, `manaCostPerLevel=5`, `baseSpellPower=10`, `spellPowerPerLevel=1`, `castTime=0` ticks. Custo base a nível n: `(int)((baseManaCost + manaCostPerLevel*(n-1))*MANA_MULTIPLIER)`.
- **Métodos-base relevantes:** `getDefaultConfig()`, `getCastType()`, `getSpellResource()`, `onCast(...)`; consulte a classe vinculada para helpers e entidades específicas.

### Causalidade e eixos técnicos

onCast cria BloodSlashProjectile no olho do caster, atira na direção de olhar, setDamage(getSpellPower(level,caster)). getDamageSource: lifesteal 15%. Classificar geometria/colisões/penetração na entidade BloodSlashProjectile; a classe do spell não fornece setter de range ou width confirmado. Perks possíveis: power via atributo nativo, demais características somente por adapter comprovado.

### Limites de integração

Atributos nativos `SPELL_POWER` e poder da escola Blood podem alterar `getSpellPower`; isso **não prova** um hook genérico para modificar geometria, quantidade, efeito ou alvo. O RPG Skill Tree fornece perks/gates/Mastery; Iron's preserva a autoridade de casting/custos/cooldowns e entidades; Black Arcana só intervém através de contratos verificados. Nenhum adapter de efeitos foi implementado nesta ficha. Registro **estático/source-pinned**, não teste Survival. [Contrato transversal](../TECHNICAL-PERK-MAP.md).
