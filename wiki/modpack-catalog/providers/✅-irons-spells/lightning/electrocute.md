# Electrocute

- **Status:** PRESENTE — ativo
- **Provider/mod ID:** Iron's Spells / `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:electrocute`
- **JAR:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Lightning
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Continuous
- **Cast time field source:** 100 ticks
- **Mana:** 3–12
- **Cooldown:** 12 s
- **Dano:** 1,75–8,5

## O que faz

Mantém um cone de energia elétrica à frente do caster e causa dano às criaturas alcançadas durante o channel.

## Source audit 3.16.3

- damage = `1 + getSpellPower * 0.75`, com spell power base 1 +1/level;
- se o caster já estiver no mesmo cast e o `EntityCastData` apontar para um `AbstractConeProjectile`, reutiliza a entity e marca o próximo settlement de dano ativo;
- caso contrário cria `ElectrocuteProjectile`, posiciona próximo à altura dos olhos, injeta damage e guarda a entity no cast data;
- cast finish sound: `ELECTROCUTE_LOOP`;
- AI stop casting quando distância ao target excede o threshold interno da spell.

## Authority / targets / dedup

- **Cone authority:** `ElectrocuteProjectile` + `EntityCastData`.
- Não spawnar um cone por tick nem tratar cada pulse como novo cast raiz.
- Hit cadence, alcance geométrico, friendly-fire, PvP/boss/summon policy: `NÃO VERIFICADO` nesta ficha.

## Matriz obrigatória

- status/provider/JAR/ID/escola/tipo: confirmado; continuous cone;
- níveis/raridade: 1–10 / Common→Legendary;
- cast/channel: Continuous; field `castTime=100` ticks; semântica de duração/interrupção adicional `NÃO VERIFICADO`;
- mana/cooldown: 3–12 / 12 s;
- dano: 1,75–8,5; type fino `NÃO VERIFICADO`;
- alcance/área: cone provider-native; números exatos `NÃO VERIFICADO`;
- scaling: `1 + 0.75*spellPower`;
- targets/PvP/boss/summon: `NÃO VERIFICADO`;
- obtenção/requisitos/itens: específicos `NÃO VERIFICADO`;
- VFX/áudio: loop sound confirmado; assets finos `NÃO VERIFICADO`;
- bridge/QA: projectile authority, fail-closed.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- Source 3.16.3: `ElectrocuteSpell.java` em `e4056af90302d37eb1739f5ff05020b020e6e252`.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`ElectrocuteSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/lightning/ElectrocuteSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:electrocute` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `COMMON`; maxLevel `10`; cooldown `12` segundos; cast `CONTINUOUS`.
- **Campos Java:** `baseManaCost`=`3`; `manaCostPerLevel`=`1`; `baseSpellPower`=`1`; `spellPowerPerLevel`=`1`; `castTime`=`100`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `onCast()`, `getDamage()`.
- **Fórmulas numéricas com retorno direto:** `getDamage = 1 + getSpellPower(spellLevel, caster) * .75f`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `addFreshEntity`.

**Contrato de perks:** escola `lightning` não prova, sozinha, dano elétrico, arcos em cadeia ou stun. Conferir classe de descarga/targeting, i-frames, limites de saltos, duração e efeitos de bloco. Atributo nativo ≠ hook para raio, count ou chain. Exigir contrato de provider, cap e anti-proc-recursivo; caso contrário ⚠️ condicionado/fail-closed. Iron's controla cast/mana/efeitos, RPG Skill Tree perks/Mastery/gates, Black Arcana runtime mágico próprio. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
