# Ray Of Siphoning

- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR do pack:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Blood
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Tipo de cast:** Continuous
- **Recurso:** mana nativa do Iron's
- **Custo:** 8–17 mana
- **Cooldown:** 15 s
- **Dano:** 1–3.25 por evento/tick publicado do spell
- **Alcance:** 12 blocos
- **Cura:** 100% do dano efetivamente causado

## O que faz

Canaliza um raio necrótico que causa dano às criaturas atingidas e converte integralmente o dano entregue em cura do caster.

## Escalonamento

Dano e custo aumentam com o nível. Frequência real de aplicação/tick e modificadores de spell power serão normalizados separadamente.

## Obtenção e aprendizado

Segue o pipeline nativo de scrolls/spell books do Iron's, com equipagem via Inscription Table. Blood usa **Blood Vial** como Focus no Scroll Forge. Loot/config específicos ainda serão verificados.

## Interações / deduplicação

Ocupa drain beam contínuo com lifesteal integral. É uma referência central para impedir duplicação em Blood/Vincular.

## VFX / animação / áudio

A catalogar visualmente no runtime do pack.

## Fonte

`https://iron.wiki/spells/` · `https://iron.wiki/schools/` · `https://iron.wiki/progression/`.

## Parâmetros de implementação para perks — código auditado

- **Source exato:** [`RayOfSiphoningSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/blood/RayOfSiphoningSpell.java) (`e4056af90302d37eb1739f5ff05020b020e6e252`, versão declarada 1.21.1-3.16.3); classe `io.redspace.ironsspellbooks.spells.blood.RayOfSiphoningSpell`.
- **ID:** `irons_spellbooks:ray_of_siphoning`. **DefaultConfig:** `RARE/UNCOMMON/COMMON=COMMON` (raridade mínima), maxLevel `10`, cooldown `15` segundos, cast `CONTINUOUS`.
- **Campos Java verificados:** `baseManaCost=8`, `manaCostPerLevel=1`, `baseSpellPower=4`, `spellPowerPerLevel=1`, `castTime=100` ticks. Custo base a nível n: `(int)((baseManaCost + manaCostPerLevel*(n-1))*MANA_MULTIPLIER)`.
- **Métodos-base relevantes:** `getDefaultConfig()`, `getCastType()`, `getSpellResource()`, `onCast(...)`; consulte a classe vinculada para helpers e entidades específicas.

### Causalidade e eixos técnicos

Raycast desde a visão do caster, range fixo=12, checkForBlocks(true), bbInflation(0.15f), filtro Utils.canHitWithRaycast. getTickDamage=0.25*getSpellPower(level,caster); getDamageSource aplica lifesteal 100% e marca dano indireto. O cast contínuo tem castTime base=100 ticks, mas não é correto derivar DPS sem verificar quantas chamadas de onCast ocorrem por segundo no pipeline. Perks de alcance, chain ou sustain exigem hook real; não duplicar onCast por evento de dano.

### Limites de integração

Atributos nativos `SPELL_POWER` e poder da escola Blood podem alterar `getSpellPower`; isso **não prova** um hook genérico para modificar geometria, quantidade, efeito ou alvo. O RPG Skill Tree fornece perks/gates/Mastery; Iron's preserva a autoridade de casting/custos/cooldowns e entidades; Black Arcana só intervém através de contratos verificados. Nenhum adapter de efeitos foi implementado nesta ficha. Registro **estático/source-pinned**, não teste Survival. [Contrato transversal](../TECHNICAL-PERK-MAP.md).
