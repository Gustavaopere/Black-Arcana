# Poison Splash

- **Status:** PRESENTE — ativo
- **Spell ID:** `irons_spellbooks:poison_splash`
- **Provider/JAR:** Iron's Spells / `1.21.1-3.16.3`
- **Escola:** Nature
- **Níveis/raridade:** 1–10 / Uncommon → Legendary
- **Cast:** Long, 15 ticks
- **Mana/cooldown:** 40–130 / 20 s
- **Dano:** 8–17
- **Effect length:** 7–25 s
- **Targeting:** até 32 blocos

## Função e source audit

Resolve uma entidade/posição por target helper ou raycast e cria `PoisonSplash` no local, com owner explícito, damage e effect duration.

- spell power = 8 +1 por nível após o primeiro;
- damage = spell power;
- duration = `100 + spellLevel*40` ticks = 7–25 s;
- fallback raycast = 32 blocos, com ground correction para block/miss;
- sons `POISON_SPLASH_BEGIN` / `POISON_CAST`.

## Authority / deduplicação

`PoisonSplash` é authority da wave/cloud, seleção espacial, poison e hit cadence. Não executar um segundo AoE scanner nem gerar cloud duplicada.

Friendly-fire, PvP, bosses, summons, radius exato e lifecycle da cloud: `NÃO VERIFICADO` nesta ficha.

## Verificação obrigatória

- damage type fino: `NÃO VERIFICADO`;
- alcance 32; radius `NÃO VERIFICADO`; duração 7–25 s;
- scaling: damage +1/level; duration +2s/level;
- obtenção/requisitos/focus/ritual: específicos `NÃO VERIFICADO`;
- VFX/textura/animação/QA client-real: `NÃO VERIFICADO` além dos sons;
- fail-closed: entity provider-native.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- `PoisonSplashSpell.java` — source 3.16.3.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`PoisonSplashSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/nature/PoisonSplashSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:poison_splash`; o ID pode divergir do título de exibição.
- **Config:** minRarity `UNCOMMON`; maxLevel `10`; cooldown `20` segundos; cast `LONG`.
- **Campos Java:** `baseManaCost`=`40`; `manaCostPerLevel`=`10`; `baseSpellPower`=`8`; `spellPowerPerLevel`=`1`; `castTime`=`15`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `checkPreCastConditions()`, `onCast()`, `getDamage()`, `getDuration()`.
- **Fórmulas numéricas com retorno direto:** `getDamage = this.getSpellPower(spellLevel, entity)`; `getDuration = 100 + spellLevel * 40`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `RaycastBuilder`, `TargetEntityCastData`, `addFreshEntity`.

**Contrato de perks:** escola `nature` não implica toxicidade, dano ácido, status ou transformação automática. Verificar aplicação real por helper, entidade, efeito ou damage source. Separar atributo nativo de mudar geometria/status/quantidade; exigir contrato real, caps, segurança e dedup; sem hook ⚠️ condicionado/fail-closed. Iron's controla cast/efeitos/mana; RPG Skill Tree perks/Mastery/gates; Black Arcana seu runtime mágico. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
