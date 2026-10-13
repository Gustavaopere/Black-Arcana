# Root

- **Status:** PRESENTE — ativo
- **Spell ID:** `irons_spellbooks:root`
- **Provider/JAR:** Iron's Spells / `1.21.1-3.16.3`
- **Escola:** Nature
- **Níveis/raridade:** 1–10 / Uncommon → Legendary
- **Cast:** Long, 50 ticks
- **Mana/cooldown:** 45–72 / 35 s
- **Duração:** 5–14 s
- **Root HP:** 40 com entity-power neutro
- **Target helper:** até 32 blocos

## Função e source audit

Se houver target válido e o entity type **não** estiver em `ModTags.CANT_ROOT`, cria `RootEntity` com owner, duration, target e max health; força o target a parar de montar e então o monta na root entity, mecanismo usado para impedir movimento não-mágico.

- spell power = 5 +1 por nível após o primeiro;
- duration = spellPower*20 ticks;
- root health = `40*entityPowerMultiplier`;
- tag `CANT_ROOT` é authority de imunidade de tipo.

## Authority / targets / deduplicação

`RootEntity` + `CANT_ROOT` são authority. Não adicionar segunda immobilization, não manter blacklist paralela e não impedir teleporte/movimento mágico sem hook/provider explícito.

PvP, bosses e summons que não estejam cobertos pela tag podem ainda ter regras externas; comportamento final específico `NÃO VERIFICADO`.

## Verificação obrigatória

- dano/cura: não aplicável diretamente;
- range 32; duração 5–14s; HP 40×multiplier;
- scaling/caps: acima; hitbox/armor/root break behavior fino `NÃO VERIFICADO`;
- obtenção/focus/ritual: específicos `NÃO VERIFICADO`;
- som start `EVOKER_PREPARE_ATTACK`; finish sound vazio; VFX/textura/QA `NÃO VERIFICADO`;
- fail-closed: respeitar tag e lifecycle da entity.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- `RootSpell.java` — source 3.16.3.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`RootSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/nature/RootSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:root`; o ID pode divergir do título de exibição.
- **Config:** minRarity `UNCOMMON`; maxLevel `10`; cooldown `35` segundos; cast `LONG`.
- **Campos Java:** `baseManaCost`=`45`; `manaCostPerLevel`=`3`; `baseSpellPower`=`5`; `spellPowerPerLevel`=`1`; `castTime`=`50`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `checkPreCastConditions()`, `onCast()`, `getDuration()`, `getRootHealth()`.
- **Fórmulas numéricas com retorno direto:** `getDuration = (int) (getSpellPower(spellLevel, caster) * 20)`; `getRootHealth = 40 * getEntityPowerMultiplier(entity)`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `TargetEntityCastData`, `addFreshEntity`.

**Contrato de perks:** escola `nature` não implica toxicidade, dano ácido, status ou transformação automática. Verificar aplicação real por helper, entidade, efeito ou damage source. Separar atributo nativo de mudar geometria/status/quantidade; exigir contrato real, caps, segurança e dedup; sem hook ⚠️ condicionado/fail-closed. Iron's controla cast/efeitos/mana; RPG Skill Tree perks/Mastery/gates; Black Arcana seu runtime mágico. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
