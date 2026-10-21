# Shockwave

- **Status:** PRESENTE — ativo
- **Provider/mod ID:** Iron's Spells / `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:shockwave`
- **JAR:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Lightning
- **Níveis:** 1–8
- **Raridade:** Common → Legendary
- **Cast:** Long
- **Cast time:** 16 ticks
- **Mana:** 70–105
- **Cooldown:** 30 s
- **Dano:** 10–15,25
- **Raio:** 9–16 blocos

## O que faz

Libera uma explosão elétrica radial em torno do caster, atingindo criaturas expostas no raio.

## Source audit 3.16.3

- `baseSpellPower=8`, +1/level;
- `radius = 8 + spellLevel`;
- `damage = 4 + spellPower*0.75`;
- enumera entidades no bounding box inflado e filtra `!DamageSources.isFriendlyFireBetween(target, caster)` + line of sight;
- só atinge LivingEntity válida dentro do raio real;
- usa `DamageSources.applyDamage`;
- Creepers recebem `thunderHit` em dummy visual-only lightning;
- VFX: múltiplos `BlastwaveParticleOptions`, 80 electricity particles, zaps por alvo e camera shake;
- sons prepare/cast; animações `PREPARE_CROSS_ARMS` e `CAST_T_POSE`.

## Targets / authority

- friendly-fire e LOS gates estão explicitamente no spell source;
- PvP/boss/summon behavior além desses gates: `NÃO VERIFICADO`;
- spell class é authority do AoE settlement; não executar segundo scan radial.

## Matriz obrigatória

- status/provider/JAR/ID/escola/tipo: confirmado; radial AoE;
- níveis/raridade: 1–8 / Common→Legendary;
- cast: Long 16 ticks;
- mana/cooldown: 70–105 / 30 s;
- dano/range: 10–15,25 / 9–16;
- damage type fino: `NÃO VERIFICADO`;
- scaling: radius 8+level; damage 4+0.75*power;
- targets: FF+LOS source gates; PvP/boss/summon específico `NÃO VERIFICADO`;
- obtenção/requisitos/itens: específicos `NÃO VERIFICADO`;
- VFX/audio/animação: source-auditados acima;
- QA client-real: `NÃO VERIFICADO`;
- dedup: um scan/settlement provider-native.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- Source 3.16.3: `ShockwaveSpell.java` em `e4056af90302d37eb1739f5ff05020b020e6e252`.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`ShockwaveSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/lightning/ShockwaveSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:shockwave` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `COMMON`; maxLevel `8`; cooldown `30` segundos; cast `LONG`.
- **Campos Java:** `baseManaCost`=`70`; `manaCostPerLevel`=`5`; `baseSpellPower`=`8`; `spellPowerPerLevel`=`1`; `castTime`=`16`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `onCast()`, `getRadius()`, `getDamage()`, `getCastStartAnimation()`, `getCastFinishAnimation()`.
- **Fórmulas numéricas com retorno direto:** `getRadius = 8 + spellLevel`; `getDamage = 4 + (getSpellPower(spellLevel, caster) * .75f)`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `DamageSources`, `LightningBolt`.

**Contrato de perks:** escola `lightning` não prova, sozinha, dano elétrico, arcos em cadeia ou stun. Conferir classe de descarga/targeting, i-frames, limites de saltos, duração e efeitos de bloco. Atributo nativo ≠ hook para raio, count ou chain. Exigir contrato de provider, cap e anti-proc-recursivo; caso contrário ⚠️ condicionado/fail-closed. Iron's controla cast/mana/efeitos, RPG Skill Tree perks/Mastery/gates, Black Arcana runtime mágico próprio. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
