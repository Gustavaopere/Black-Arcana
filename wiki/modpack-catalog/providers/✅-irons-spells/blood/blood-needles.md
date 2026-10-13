# Blood Needles

- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR do pack:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Blood
- **Níveis:** 1–10
- **Raridade:** Uncommon → Legendary
- **Tipo de cast:** Instant
- **Recurso:** mana nativa do Iron's
- **Custo:** 25–70 mana
- **Cooldown:** 10 s
- **Dano:** 2–4.25 por projétil
- **Projéteis:** 5
- **Cura:** 25% do dano efetivamente causado

## O que faz

Forma um anel de agulhas de sangue e as lança para frente. É um ataque frontal multihit com sustain por lifesteal.

## Escalonamento

Dano e custo crescem com o nível; a contagem de projéteis publicada permanece 5.

## Obtenção e aprendizado

Pipeline nativo do Iron's: scrolls/progressão do mod, equipagem via Inscription Table; Blood usa **Blood Vial** como Focus no Scroll Forge. Loot/config específicos desta magia ainda serão verificados.

## Interações / deduplicação

Bloqueia duplicatas de “agulhas hemáticas frontais” com lifesteal.

## VFX / animação / áudio

A catalogar visualmente no runtime do pack.

## Fonte

`https://iron.wiki/spells/` · `https://iron.wiki/schools/` · `https://iron.wiki/progression/`.

## Parâmetros de implementação para perks — código auditado

- **Source exato:** [`BloodNeedlesSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/blood/BloodNeedlesSpell.java) (`e4056af90302d37eb1739f5ff05020b020e6e252`, versão declarada 1.21.1-3.16.3); classe `io.redspace.ironsspellbooks.spells.blood.BloodNeedlesSpell`.
- **ID:** `irons_spellbooks:blood_needles`. **DefaultConfig:** `RARE/UNCOMMON/COMMON=UNCOMMON` (raridade mínima), maxLevel `10`, cooldown `10` segundos, cast `INSTANT`.
- **Campos Java verificados:** `baseManaCost=25`, `manaCostPerLevel=5`, `baseSpellPower=8`, `spellPowerPerLevel=1`, `castTime=0` ticks. Custo base a nível n: `(int)((baseManaCost + manaCostPerLevel*(n-1))*MANA_MULTIPLIER)`.
- **Métodos-base relevantes:** `getDefaultConfig()`, `getCastType()`, `getSpellResource()`, `onCast(...)`; consulte a classe vinculada para helpers e entidades específicas.

### Causalidade e eixos técnicos

Anel frontal com 5 projéteis BloodNeedle constantes; raycast de 32 blocos com colisão com blocos. Fórmula: damagePerNeedle=0.25*getSpellPower(level,caster). getDamageSource aplica lifesteal 25% e i-frames 0; a mesma fonte é usada pelas agulhas de Acupuncture. Count não escala com level neste código; extensão de contagem, ângulo e trajetória depende de interceptação comprovada do spawn, não de um setter genérico da API.

### Limites de integração

Atributos nativos `SPELL_POWER` e poder da escola Blood podem alterar `getSpellPower`; isso **não prova** um hook genérico para modificar geometria, quantidade, efeito ou alvo. O RPG Skill Tree fornece perks/gates/Mastery; Iron's preserva a autoridade de casting/custos/cooldowns e entidades; Black Arcana só intervém através de contratos verificados. Nenhum adapter de efeitos foi implementado nesta ficha. Registro **estático/source-pinned**, não teste Survival. [Contrato transversal](../TECHNICAL-PERK-MAP.md).
