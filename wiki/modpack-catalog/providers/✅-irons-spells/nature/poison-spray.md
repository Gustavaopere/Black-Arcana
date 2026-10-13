# Poison Spray

- **Status:** PRESENTE — ativo
- **Nome interno histórico:** Poison Breath
- **Spell ID real:** `irons_spellbooks:poison_breath`
- **Classe:** `PoisonBreathSpell`
- **Provider/JAR:** Iron's Spells / `1.21.1-3.16.3`
- **Escola:** Nature
- **Níveis/raridade:** 1–10 / Common → Legendary
- **Cast:** Continuous
- **Cast-time field:** 100 ticks
- **Mana/cooldown:** 5–14 / 12 s
- **Dano player-facing atual:** 1–7,75

## Alias histórico

O changelog oficial registra que **Poison Breath foi renomeado para Poison Spray sem outras mudanças**. O registry ID e a classe permanecem `poison_breath` / `PoisonBreathSpell`; integrações devem usar o identificador real, não inferir `poison_spray`.

## Source audit 3.16.3

- base spell power 0, +1 por nível após o primeiro;
- damage = `1 + spellPower*0.75`;
- durante o mesmo cast, se `EntityCastData` ainda aponta para `AbstractConeProjectile`, reutiliza o cone e ativa novo settlement de dano;
- caso contrário cria `PoisonBreathProjectile`, posiciona próximo à altura dos olhos, injeta damage e salva a entity no cast data;
- loop sound `POISON_BREATH_LOOP`;
- AI stop threshold baseado em target > ~10 blocos com margem interna.

## Authority / dedup

`PoisonBreathProjectile` + `EntityCastData` são authority. Não spawnar um cone por tick, não contar cada pulse como novo cast e não reaplicar Poison por fora.

Geometry, cadence, poison duration, friendly-fire, PvP/boss/summon policy: `NÃO VERIFICADO` nesta ficha.

## Verificação obrigatória

- damage type fino: `NÃO VERIFICADO`;
- range/area/duração do cone: provider-native, números exatos `NÃO VERIFICADO`;
- scaling: `1 + 0.75*spellPower`;
- obtenção/itens/focus/rituais: específicos `NÃO VERIFICADO`;
- VFX/textura/QA client-real: `NÃO VERIFICADO` além do loop sound;
- fail-closed: preservar o cone único do provider.

## Fonte

- `https://iron.wiki/spells/` — nome atual, consulta 2026-09-06.
- changelog oficial: rename Poison Breath → Poison Spray sem mudança mecânica.
- `PoisonBreathSpell.java` — source 3.16.3.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`PoisonBreathSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/nature/PoisonBreathSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:poison_breath`; o ID pode divergir do título de exibição.
- **Config:** minRarity `COMMON`; maxLevel `10`; cooldown `12` segundos; cast `CONTINUOUS`.
- **Campos Java:** `baseManaCost`=`5`; `manaCostPerLevel`=`1`; `baseSpellPower`=`0`; `spellPowerPerLevel`=`1`; `castTime`=`100`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `onCast()`, `getDamage()`.
- **Fórmulas numéricas com retorno direto:** `getDamage = 1 + getSpellPower(spellLevel, caster) * .75f`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `addFreshEntity`.

**Contrato de perks:** escola `nature` não implica toxicidade, dano ácido, status ou transformação automática. Verificar aplicação real por helper, entidade, efeito ou damage source. Separar atributo nativo de mudar geometria/status/quantidade; exigir contrato real, caps, segurança e dedup; sem hook ⚠️ condicionado/fail-closed. Iron's controla cast/efeitos/mana; RPG Skill Tree perks/Mastery/gates; Black Arcana seu runtime mágico. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).

## Mecânica confirmada — leitura causal do código-fonte

- **ID real apesar do nome de exibição:** `irons_spellbooks:poison_breath` na classe `PoisonBreathSpell`. `CONTINUOUS` com `castTime=100` ticks nominais; `damage=1+0.75*getSpellPower(level,caster)`.
- **Causalidade do cone:** no início, `onCast` gera `PoisonBreathProjectile` e grava `EntityCastData` para rastrear a entidade; durante a conjuração ativa, encontra `AbstractConeProjectile` e chama `setDealDamageActive()`. Isso é uma máquina de estado do efeito; não gerar projétil novo a cada tick de perk.
- **Perks:** abertura do cone, duração e frequência do dano exigem inspeção de `PoisonBreathProjectile`/`AbstractConeProjectile`; o dano base pode escalar por spell power. Evitar duplicidade de tick e processamento em cascata.

**Nível de prova:** inspeção do método do spell fixado no source 3.16.3; efeitos internos da entidade/projétil, possibilidade de patch por hooks externos e runtime Survival não validados.
