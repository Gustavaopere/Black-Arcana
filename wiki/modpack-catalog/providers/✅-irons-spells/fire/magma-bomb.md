# Magma Bomb

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Fire
- **Níveis:** 1–8
- **Raridade:** Uncommon → Legendary
- **Cast:** Long
- **Mana:** 30–65
- **Cooldown:** 12 s
- **Dano de impacto atual:** 8
- **Dano AOE:** 1,7–3,9
- **Raio:** 4 blocos

## O que faz

Lança uma bomba de magma que explode ao impactar e deixa um campo de fogo no local.

## Escalonamento

A build atual lista impacto fixo 8, AOE 1,7–3,9 e raio 4 blocos. O changelog registra que o dano de impacto deixou de escalar com nível e que a parametrização de AOE/raio foi revisada; valores antigos não substituem os atuais.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação / world safety

Já cobre projétil de magma + explosão + campo persistente de fogo. A existência desse campo não autoriza Black Arcana a inferir vanilla fire spread, persistence ou mutação fora do provider; bridges devem observar, não duplicar, o field.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Changelog oficial: `https://iron.wiki/changelog/`
- Consulta: 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`MagmaBombSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/fire/MagmaBombSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:magma_bomb` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `UNCOMMON`; maxLevel `8`; cooldown `12` segundos; cast `LONG`.
- **Campos Java:** `baseManaCost`=`30`; `manaCostPerLevel`=`5`; `baseSpellPower`=`8`; `spellPowerPerLevel`=`3`; `castTime`=`20`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `onCast()`, `getRadius()`, `getDamage()`, `getAoeDamage()`, `getCastStartAnimation()`.
- **Fórmulas numéricas com retorno direto:** `getRadius = 3 + getEntityPowerMultiplier(caster)`; `getDamage = baseSpellPower * getEntityPowerMultiplier(caster)`; `getAoeDamage = 1 + getSpellPower(spellLevel, caster) * .1f`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `addFreshEntity`, `Explosion`.

**Contrato de perks:** escola `fire` não certifica que todo dano/incêndio seja fire damage; verificar fonte de dano, duração de burning e entidades de projétil. Separar atributo de spell power nativo de mutações de área/contagem/efeito, que exigem hook específico, caps e world safety. Sem contrato comprovado: ⚠️ condicionado/fail-closed. RPG Skill Tree gerencia perks, Mastery e gates; Iron's mantém cast, mana e efeitos nativos; Black Arcana mantém seu runtime e WorldEffectPolicy para efeitos próprios. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
