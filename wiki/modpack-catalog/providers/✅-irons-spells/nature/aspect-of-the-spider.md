# Aspect Of The Spider

- **Status:** PRESENTE — ativo
- **Spell ID real:** `irons_spellbooks:spider_aspect`
- **Classe/effect:** `SpiderAspectSpell` / `SpiderAspectEffect`
- **Provider/JAR:** Iron's Spells / `1.21.1-3.16.3`
- **Escola:** Nature
- **Níveis/raridade:** 1–8 / Rare → Legendary
- **Cast:** Instant, 0 ticks
- **Mana/cooldown:** 35–70 / 90 s
- **Bônus:** +5%–40% damage contra alvos com efeitos elegíveis
- **Duração:** 20–55 s

## Função e source audit

Aplica `SPIDER_ASPECT` ao caster por `spellPower*20` ticks, amplifier `level-1`. Spell power = 20 +5/level. O effect intercepta `LivingIncomingDamageEvent`: se o atacante possui `SPIDER_ASPECT` e o alvo possui ao menos um efeito cuja holder está na tag `ModTags.AFFECTED_BY_SPIDER_ASPECT`, multiplica o dano por `1 + 0.05*level`.

Isso é mais preciso que assumir literalmente apenas vanilla Poison: **a tag do provider é a authority da elegibilidade**.

## Authority / targets / dedup

- authority: `SPIDER_ASPECT`, `SpiderAspectEffect` e `AFFECTED_BY_SPIDER_ASPECT`;
- funciona sobre incoming damage independente de a origem ser melee/ranged/spell, desde que a source entity seja o caster afetado;
- PvP, bosses e summons seguem a tag/effect/event pipeline; exceções adicionais `NÃO VERIFICADO`;
- não aplicar um segundo multiplicador por detectar Poison manualmente.

## Verificação obrigatória

- dano próprio do cast/cura: não aplicável;
- área/range: self-buff; duração acima;
- caps além de level 8: `NÃO VERIFICADO`;
- obtenção/itens/focus/rituais: específicos `NÃO VERIFICADO`;
- som final `SPIDER_ASPECT_CAST`, animação `SELF_CAST_ANIMATION`; partículas/textura `NÃO VERIFICADO`;
- QA client-real/compat com eventos cancelados ou damage transforms posteriores: `NÃO VERIFICADO`;
- fail-closed: consultar tag/effect nativos, sem lista paralela de venenos.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- `SpiderAspectSpell.java` + `SpiderAspectEffect.java` — source 3.16.3.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`SpiderAspectSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/nature/SpiderAspectSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:spider_aspect`; o ID pode divergir do título de exibição.
- **Config:** minRarity `RARE`; maxLevel `8`; cooldown `90` segundos; cast `INSTANT`.
- **Campos Java:** `baseManaCost`=`35`; `manaCostPerLevel`=`5`; `baseSpellPower`=`20`; `spellPowerPerLevel`=`5`; `castTime`=`0`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `onCast()`, `getPercentDamage()`, `getCastStartAnimation()`.
- **Fórmulas numéricas com retorno direto:** `getPercentDamage = spellLevel * SpiderAspectEffect.DAMAGE_PER_LEVEL * 100`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `MobEffectInstance`, `addEffect`, `MobEffectRegistry`.

**Contrato de perks:** escola `nature` não implica toxicidade, dano ácido, status ou transformação automática. Verificar aplicação real por helper, entidade, efeito ou damage source. Separar atributo nativo de mudar geometria/status/quantidade; exigir contrato real, caps, segurança e dedup; sem hook ⚠️ condicionado/fail-closed. Iron's controla cast/efeitos/mana; RPG Skill Tree perks/Mastery/gates; Black Arcana seu runtime mágico. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
