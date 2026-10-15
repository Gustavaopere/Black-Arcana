# Earthquake

- **Status:** PRESENTE — ativo
- **Spell ID:** `irons_spellbooks:earthquake`
- **Provider/JAR:** Iron's Spells / `1.21.1-3.16.3`
- **Escola:** Nature
- **Níveis/raridade:** 1–10 / Uncommon → Legendary
- **Cast:** Long, 40 ticks
- **Mana/cooldown:** 50–140 / 16 s
- **AoE damage:** 2–4.25
- **Slowness:** I–III
- **Raio:** 8 com entity-power neutro
- **Duração source da AoE:** 12 s

## Source audit

Pre-cast tenta target helper até 32 blocos sem exigir sucesso. Se não houver target, raycast 32 e ground correction até 6. Cria `EarthquakeAoe`, owner explícito, circular, com radius, duração, damage e slowness amplifier.

- spell power = 8 +1/level;
- damage = `spellPower*0.25`;
- radius = `4 + 4*entityPowerMultiplier`;
- duration fixa na spell class = `20*12` ticks;
- slowness amplifier = clamp(`floor(damage)-2`, 0, 2).

## Authority / dedup

`EarthquakeAoe` possui tick/hit/slow settlement. Não criar segundo scan por tick ou segunda aplicação de Slowness. Friendly-fire, PvP/boss/summon policy e cadence fina da AoE: `NÃO VERIFICADO`.

## Verificação obrigatória

- damage type: `NÃO VERIFICADO` na spell class;
- targeting 32; radius/duration acima;
- scaling/caps: fórmulas acima;
- obtenção/requisitos/itens: específicos `NÃO VERIFICADO`;
- sons `EARTHQUAKE_LOOP`/`EARTHQUAKE_CAST`; VFX finais `NÃO VERIFICADO`;
- QA real: `NÃO VERIFICADO`, fail-closed por `EarthquakeAoe`.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- `EarthquakeSpell.java` — source 3.16.3.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`EarthquakeSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/nature/EarthquakeSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:earthquake`; o ID pode divergir do título de exibição.
- **Config:** minRarity `UNCOMMON`; maxLevel `10`; cooldown `16` segundos; cast `LONG`.
- **Campos Java:** `baseManaCost`=`50`; `manaCostPerLevel`=`10`; `baseSpellPower`=`8`; `spellPowerPerLevel`=`1`; `castTime`=`40`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `checkPreCastConditions()`, `onCast()`, `getDamage()`, `getRadius()`, `getSlownessAmplifier()`.
- **Fórmulas numéricas com retorno direto:** `getDamage = getSpellPower(spellLevel, caster) * .25f`; `getRadius = 4 + 4 * getEntityPowerMultiplier(caster)`; `getSlownessAmplifier = Math.clamp((int) getDamage(spellLevel, caster) - 2, 0, 2)`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `RaycastBuilder`, `TargetEntityCastData`, `addFreshEntity`.

**Contrato de perks:** escola `nature` não implica toxicidade, dano ácido, status ou transformação automática. Verificar aplicação real por helper, entidade, efeito ou damage source. Separar atributo nativo de mudar geometria/status/quantidade; exigir contrato real, caps, segurança e dedup; sem hook ⚠️ condicionado/fail-closed. Iron's controla cast/efeitos/mana; RPG Skill Tree perks/Mastery/gates; Black Arcana seu runtime mágico. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
