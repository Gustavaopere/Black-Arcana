# Volt Strike

- **Status:** PRESENTE — ativo
- **Provider/mod ID:** Iron's Spells / `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:volt_strike`
- **JAR:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Lightning
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Instant / 0 ticks
- **Mana:** 30–75
- **Cooldown:** 10 s
- **Dano:** 6–15

## O que faz

Impulsiona o caster para frente em um spin attack elétrico; o catálogo atual descreve impacto no primeiro alvo/superfície e blast residual em pequena área.

## Source audit 3.16.3

- spell power base 1 +1/level;
- damage payload = `5 + spellPower`, portanto 6–15;
- calcula dash impulse a partir do look angle e multiplier `(15+spellPower)/20`;
- se no chão, reposiciona/eleva o caster antes do dash;
- aplica `MobEffectRegistry.VOLT_STRIKE` por 10 ticks com amplifier igual ao damage payload;
- define `invulnerableTime=20`;
- define `SpinAttackType.LIGHTNING` no synced data;
- hit/blast settlement pertence ao efeito/spin pipeline do provider.

### Nota de QA source

O source chama `impulse.add(...)` sem reassinar o `Vec3` retornado em dois pontos. Como `Vec3` é imutável, o incremento adicional de Y pretendido nessas duas chamadas pode não compor o vetor final. Isto é **observação estática de source**, não confirmação de bug percebido em gameplay; QA client/runtime permanece `NÃO VERIFICADO`.

## Targets / dedup

- caster é o executor do spin;
- target/hitbox/friendly-fire/PvP/boss/summon e blast radius finos pertencem ao `VOLT_STRIKE`/spin pipeline e ficam `NÃO VERIFICADO` nesta ficha;
- não criar segundo dash, segundo hit detector ou blast paralelo.

## Matriz obrigatória

- status/provider/JAR/ID/escola/tipo: confirmado; mobility melee/spin Lightning;
- níveis/raridade: 1–10 / Common→Legendary;
- cast: Instant 0;
- mana/cooldown: 30–75 / 10 s;
- dano: payload 6–15; type fino `NÃO VERIFICADO`;
- alcance/área/duração: dash/effect 10 ticks; distância e blast radius `NÃO VERIFICADO`;
- scaling: damage=5+spellPower; dash multiplier=(15+power)/20;
- targets/PvP/boss/summon: pipeline-native, detalhes `NÃO VERIFICADO`;
- obtenção/requisitos/itens: específicos `NÃO VERIFICADO`;
- VFX/audio/animação: SpinAttackType Lightning confirmado; assets finais `NÃO VERIFICADO`;
- bugs/QA: possível immutable-Vec3 quirk acima; gameplay confirmation `NÃO VERIFICADO`.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- Source 3.16.3: `VoltStrikeSpell.java` em `e4056af90302d37eb1739f5ff05020b020e6e252`.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`VoltStrikeSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/lightning/VoltStrikeSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:volt_strike` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `COMMON`; maxLevel `10`; cooldown `10` segundos; cast `INSTANT`.
- **Campos Java:** `baseManaCost`=`30`; `manaCostPerLevel`=`5`; `baseSpellPower`=`1`; `spellPowerPerLevel`=`1`; `castTime`=`0`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `onCast()`, `getDamage()`.
- **Fórmulas numéricas com retorno direto:** `getDamage = (int) (5 + getSpellPower(spellLevel, caster))`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `MobEffectInstance`, `addEffect`.

**Contrato de perks:** escola `lightning` não prova, sozinha, dano elétrico, arcos em cadeia ou stun. Conferir classe de descarga/targeting, i-frames, limites de saltos, duração e efeitos de bloco. Atributo nativo ≠ hook para raio, count ou chain. Exigir contrato de provider, cap e anti-proc-recursivo; caso contrário ⚠️ condicionado/fail-closed. Iron's controla cast/mana/efeitos, RPG Skill Tree perks/Mastery/gates, Black Arcana runtime mágico próprio. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
