# Acid Spit

- **Status:** PRESENTE — ativo
- **Provider/mod ID:** Iron's Spells / `irons_spellbooks`
- **Spell ID real:** `irons_spellbooks:acid_orb`
- **Classe:** `AcidOrbSpell`
- **JAR:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Nature
- **Níveis/raridade:** 1–8 / Common → Legendary
- **Cast:** Long, 15 ticks
- **Mana/cooldown:** 40–110 / 15 s
- **Raio:** 3 blocos com multiplier neutro
- **Rend:** 20%–55% armor reduction
- **Duração:** 20 s com multiplier neutro

## Função e source audit 3.16.3

Spita uma orb de ácido que explode e aplica Rend. O source cria `AcidOrb`, dispara no look angle, adiciona componente vertical, injeta radius, rend amplifier e duration e então delega impacto/splash à entity.

- spell power base 1, sem scaling por nível;
- radius = `spellPower * 3`;
- rend amplifier = `level + 2`; tooltip converte `(amplifier+1)*5%`;
- duration = `spellPower * 20 * 20` ticks;
- sons `ACID_ORB_CHARGE`/`ACID_ORB_CAST`;
- animações `CHARGE_SPIT_ANIMATION`/`SPIT_FINISH_ANIMATION`;
- AI evita usar contra target com armor < 4.

## Authority / targets / deduplicação

`AcidOrb` é authority do impacto/splash; Rend effect é authority da redução de armor. Friendly-fire, PvP, boss/summon eligibility e impacto fino: `NÃO VERIFICADO`. Não criar segunda explosão nem reaplicar Rend por bridge.

## Verificação obrigatória

- recurso: mana; dano direto numérico: `NÃO VERIFICADO` na spell class;
- damage type: `NÃO VERIFICADO`;
- alcance/lifetime da orb: `NÃO VERIFICADO`;
- scaling/caps: radius/duration acima; Rend por nível; caps extras `NÃO VERIFICADO`;
- obtenção/loot/craft/trade/focus/ritual: pipeline geral scroll/spellbook; rota específica `NÃO VERIFICADO`;
- VFX/textura/QA client-real: `NÃO VERIFICADO` além de sons/animações auditados;
- fail-closed: preservar entity/effect provider-native.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- `AcidOrbSpell.java` — source 3.16.3 pinado.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`AcidOrbSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/nature/AcidOrbSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:acid_orb`; o ID pode divergir do título de exibição.
- **Config:** minRarity `COMMON`; maxLevel `8`; cooldown `15` segundos; cast `LONG`.
- **Campos Java:** `baseManaCost`=`40`; `manaCostPerLevel`=`10`; `baseSpellPower`=`1`; `spellPowerPerLevel`=`0`; `castTime`=`15`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `onCast()`, `getRadius()`, `getRendAmplifier()`, `getRendDuration()`, `getCastStartAnimation()`, `getCastFinishAnimation()`.
- **Fórmulas numéricas com retorno direto:** `getRadius = getSpellPower(spellLevel, caster) * 3`; `getRendAmplifier = spellLevel + 2`; `getRendDuration = (int) (getSpellPower(spellLevel, caster) * 20 * 20)`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `addFreshEntity`.

**Contrato de perks:** escola `nature` não implica toxicidade, dano ácido, status ou transformação automática. Verificar aplicação real por helper, entidade, efeito ou damage source. Separar atributo nativo de mudar geometria/status/quantidade; exigir contrato real, caps, segurança e dedup; sem hook ⚠️ condicionado/fail-closed. Iron's controla cast/efeitos/mana; RPG Skill Tree perks/Mastery/gates; Black Arcana seu runtime mágico. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).

## Mecânica confirmada — leitura causal do código-fonte

- **ID real apesar do nome de exibição:** `irons_spellbooks:acid_orb`, implementado por `AcidOrbSpell`. `onCast` cria `AcidOrb` e aplica `setExplosionRadius`, `setRendLevel` e `setRendDuration` antes de spawn.
- **Fórmulas:** `radius=3*getSpellPower(level,caster)`; `rendAmplifier=level+2`; `rendDurationTicks=(int)(400*getSpellPower(level,caster))`. Os campos `rend` não devem ser automaticamente classificados como veneno/dano ácido sem olhar `AcidOrb` e o efeito Rend.
- **Perks:** potencial aumento de área ou força do Rend requer adapter seguro, cap e classificação do status; modificar o atributo de spell power altera raio e duração **simultaneamente** neste feitiço.

**Nível de prova:** inspeção do método do spell fixado no source 3.16.3; efeitos internos da entidade/projétil, possibilidade de patch por hooks externos e runtime Survival não validados.
