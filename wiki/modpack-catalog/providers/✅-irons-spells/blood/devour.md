# Devour

- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR do pack:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Blood
- **Níveis:** 1–10
- **Raridade:** Uncommon → Legendary
- **Tipo de cast:** Instant
- **Recurso:** mana nativa do Iron's
- **Custo:** 25–61 mana
- **Cooldown:** 20 s
- **Dano:** 6–15
- **Cura:** 15% do dano efetivamente causado
- **Bônus por abate:** +2–6 Max HP temporário

## O que faz

Puxa uma criatura próxima e executa um ataque de mordida. Parte do dano retorna como cura; se o alvo morrer, o caster recebe vida máxima temporária adicional.

## Escalonamento

Dano, custo e bônus de Max HP aumentam conforme o nível. Duração do bônus temporário ainda será normalizada.

## Obtenção e aprendizado

Segue o pipeline nativo de scrolls/spell books do Iron's, com equipagem via Inscription Table. Blood usa **Blood Vial** como Focus no Scroll Forge. Loot/config específicos ainda serão verificados.

## Interações / deduplicação

Ocupa puxão + execução/bite + lifesteal + recompensa por abate. Relevante para qualquer futura magia hemática predatória.

## VFX / animação / áudio

A catalogar visualmente no runtime do pack.

## Fonte

`https://iron.wiki/spells/` · `https://iron.wiki/schools/` · `https://iron.wiki/progression/`.

## Parâmetros de implementação para perks — código auditado

- **Source exato:** [`DevourSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/blood/DevourSpell.java) (`e4056af90302d37eb1739f5ff05020b020e6e252`, versão declarada 1.21.1-3.16.3); classe `io.redspace.ironsspellbooks.spells.blood.DevourSpell`.
- **ID:** `irons_spellbooks:devour`. **DefaultConfig:** `RARE/UNCOMMON/COMMON=UNCOMMON` (raridade mínima), maxLevel `10`, cooldown `20` segundos, cast `INSTANT`.
- **Campos Java verificados:** `baseManaCost=25`, `manaCostPerLevel=4`, `baseSpellPower=6`, `spellPowerPerLevel=1`, `castTime=0` ticks. Custo base a nível n: `(int)((baseManaCost + manaCostPerLevel*(n-1))*MANA_MULTIPLIER)`.
- **Métodos-base relevantes:** `getDefaultConfig()`, `getCastType()`, `getSpellResource()`, `onCast(...)`; consulte a classe vinculada para helpers e entidades específicas.

### Causalidade e eixos técnicos

TargetEntityCastData com Utils.preCastTargetHelper(...,9,0.1f). onCast gera DevourJaw com dano getSpellPower(level,caster). hpBonus=2*(int)(getSpellPower(level,caster)*0.25f); vigorLevel=hpBonus/2-1. getDamageSource aplica lifesteal 15%. Bônus pós-abate depende da entidade DevourJaw e do efeito associado; duração/cap/acúmulo não são comprovados somente pelo spell. Perks de HP por kill exigem anti-farm e confirmação da cadeia real de morte.

### Limites de integração

Atributos nativos `SPELL_POWER` e poder da escola Blood podem alterar `getSpellPower`; isso **não prova** um hook genérico para modificar geometria, quantidade, efeito ou alvo. O RPG Skill Tree fornece perks/gates/Mastery; Iron's preserva a autoridade de casting/custos/cooldowns e entidades; Black Arcana só intervém através de contratos verificados. Nenhum adapter de efeitos foi implementado nesta ficha. Registro **estático/source-pinned**, não teste Survival. [Contrato transversal](../TECHNICAL-PERK-MAP.md).
