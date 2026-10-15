# Acupuncture

- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR do pack:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Blood
- **Níveis:** 1–10
- **Raridade:** Rare → Legendary
- **Tipo de cast:** Instant
- **Recurso:** mana nativa do Iron's
- **Custo:** 25–70 mana
- **Cooldown:** 20 s
- **Dano:** 2 por projétil
- **Projéteis:** 5–14
- **Cura:** 25% do dano efetivamente causado

## O que faz

Cria um conjunto de agulhas de sangue ao redor de uma criatura-alvo e as dispara para baixo. É um ataque multihit que também converte parte do dano entregue em cura do conjurador.

## Escalonamento

O número de projéteis e o custo crescem com o nível. A fórmula interna exata por nível permanece provider-owned e só será registrada se houver fonte/config permitida e verificável.

## Obtenção e aprendizado

Segue o pipeline nativo do Iron's: scrolls podem ser obtidos pela progressão/loot do mod; spells são equipados em spell books via Inscription Table. A Blood school usa **Blood Vial** como Focus para o sistema de Scroll Forge. Particularidades exatas de loot/config desta magia ainda serão verificadas.

## Interações / deduplicação

Ocupa o nicho de projéteis hemáticos multihit + lifesteal. Black Arcana não deve criar uma magia equivalente apenas mudando nome/VFX.

## VFX / animação / áudio

A catalogar visualmente no JAR/runtime do pack.

## Fonte

Catálogo oficial atual do Iron's: `https://iron.wiki/spells/`; escola/progressão: `https://iron.wiki/schools/` e `https://iron.wiki/progression/`.

## Parâmetros de implementação para perks — código auditado

- **Source exato:** [`AcupunctureSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/blood/AcupunctureSpell.java) (`e4056af90302d37eb1739f5ff05020b020e6e252`, versão declarada 1.21.1-3.16.3); classe `io.redspace.ironsspellbooks.spells.blood.AcupunctureSpell`.
- **ID:** `irons_spellbooks:acupuncture`. **DefaultConfig:** `RARE/UNCOMMON/COMMON=RARE` (raridade mínima), maxLevel `10`, cooldown `20` segundos, cast `INSTANT`.
- **Campos Java verificados:** `baseManaCost=25`, `manaCostPerLevel=5`, `baseSpellPower=1`, `spellPowerPerLevel=0`, `castTime=0` ticks. Custo base a nível n: `(int)((baseManaCost + manaCostPerLevel*(n-1))*MANA_MULTIPLIER)`.
- **Métodos-base relevantes:** `getDefaultConfig()`, `getCastType()`, `getSpellResource()`, `onCast(...)`; consulte a classe vinculada para helpers e entidades específicas.

### Causalidade e eixos técnicos

Alvo vivo: Utils.preCastTargetHelper(...,32,0.15f); leitura de TargetEntityCastData. Fórmulas: count=(int)((4+level)*getSpellPower(level,caster)); damagePerNeedle=1+getSpellPower(level,caster). Gera count entidades BloodNeedle distribuídas ao redor do alvo (raio de spawn dependente de target.getBbWidth()+2.75), com setScale(0.4) e movimento centrípeto. ATENÇÃO: BloodNeedle.onHitEntity aplica a fonte de dano de SpellRegistry.BLOOD_NEEDLES_SPELL, cujo getDamageSource implementa lifesteal 25% e i-frames 0. Portanto o source do cast é Acupuncture, mas a damage source referencia Blood Needles. Não usar damage source sozinha para conceder Mastery/proc; necessidade de vínculo causal. Sem cap interno comprovado para count: perk de projéteis extras exige limite e orçamento de execução.

### Limites de integração

Atributos nativos `SPELL_POWER` e poder da escola Blood podem alterar `getSpellPower`; isso **não prova** um hook genérico para modificar geometria, quantidade, efeito ou alvo. O RPG Skill Tree fornece perks/gates/Mastery; Iron's preserva a autoridade de casting/custos/cooldowns e entidades; Black Arcana só intervém através de contratos verificados. Nenhum adapter de efeitos foi implementado nesta ficha. Registro **estático/source-pinned**, não teste Survival. [Contrato transversal](../TECHNICAL-PERK-MAP.md).
