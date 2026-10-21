# Firefly Swarm

- **Status:** PRESENTE — ativo
- **Spell ID:** `irons_spellbooks:firefly_swarm`
- **Provider/JAR:** Iron's Spells / `1.21.1-3.16.3`
- **Escola:** Nature
- **Níveis/raridade:** 1–10 / Uncommon → Legendary
- **Cast:** Long, 30 ticks
- **Mana/cooldown:** 40–130 / 20 s
- **AoE damage:** 2–5
- **Raio público:** 2 blocos
- **Targeting:** até 32 blocos

## Source audit

Pre-cast usa target helper 32. O cast resolve target/position do `TargetEntityCastData` ou faz raycast 32; para block/miss corrige a posição em relação ao chão. Cria `FireflySwarmProjectile(level, owner, target, damage)` e move a swarm para a posição resolvida.

- spell power = 6 +1/level;
- damage = spellPower/3;
- radius mostrado vem de `FireflySwarmProjectile.radius`;
- o catálogo atual confirma que a swarm acompanha o alvo e, se o alvo inicial morrer, passa ao último creature harmed; esse lifecycle pertence ao projectile.

## Authority / dedup

`FireflySwarmProjectile` é authority de follow/retarget/AoE ticks. Não criar scheduler ou retarget paralelo. Friendly-fire, PvP/boss/summon eligibility, tick cadence e lifetime: `NÃO VERIFICADO` nesta ficha.

## Verificação obrigatória

- damage type fino: `NÃO VERIFICADO`;
- range 32, radius público 2; duration/lifetime `NÃO VERIFICADO`;
- scaling damage = power/3;
- obtenção/focus/ritual: específicos `NÃO VERIFICADO`;
- prepare sound `FIREFLY_SPELL_PREPARE`; VFX/finish sound/QA `NÃO VERIFICADO`;
- fail-closed: projectile provider-native.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- `FireflySwarmSpell.java` — source 3.16.3.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`FireflySwarmSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/nature/FireflySwarmSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:firefly_swarm`; o ID pode divergir do título de exibição.
- **Config:** minRarity `UNCOMMON`; maxLevel `10`; cooldown `20` segundos; cast `LONG`.
- **Campos Java:** `baseManaCost`=`40`; `manaCostPerLevel`=`10`; `baseSpellPower`=`6`; `spellPowerPerLevel`=`1`; `castTime`=`30`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `checkPreCastConditions()`, `onCast()`, `getDamage()`.
- **Fórmulas numéricas com retorno direto:** `getDamage = this.getSpellPower(spellLevel, entity) / 3f`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `RaycastBuilder`, `TargetEntityCastData`, `addFreshEntity`.

**Contrato de perks:** escola `nature` não implica toxicidade, dano ácido, status ou transformação automática. Verificar aplicação real por helper, entidade, efeito ou damage source. Separar atributo nativo de mudar geometria/status/quantidade; exigir contrato real, caps, segurança e dedup; sem hook ⚠️ condicionado/fail-closed. Iron's controla cast/efeitos/mana; RPG Skill Tree perks/Mastery/gates; Black Arcana seu runtime mágico. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
