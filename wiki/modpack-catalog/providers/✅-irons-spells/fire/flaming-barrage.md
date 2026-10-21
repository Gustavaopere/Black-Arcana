# Flaming Barrage

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Fire
- **Níveis:** 1–5
- **Raridade:** Rare → Legendary
- **Cast:** Instant
- **Mana:** 80–100
- **Cooldown:** 15 s
- **Dano:** 3–11
- **Projéteis:** 5

## O que faz

Permite casts repetidos para lançar cinco pequenas fireballs individualmente; elas fazem homing em direção ao cursor ou à criatura que ele está mirando.

## Escalonamento

O dano listado cresce de 3 para 11. Janela exata de recasts, força de homing e lifecycle dos cinco projéteis ficam `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. O spell foi adicionado na linha 3.2.0; rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação / causalidade

Já cobre sequência multi-projétil com homing. Os cinco projéteis/recasts não devem ser reinterpretados por Black Arcana como cinco casts raiz independentes para mastery/procs.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Changelog oficial: `https://iron.wiki/changelog/`
- Consulta: 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`FlamingBarrageSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/fire/FlamingBarrageSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:flaming_barrage` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `RARE`; maxLevel `5`; cooldown `15` segundos; cast `INSTANT`.
- **Campos Java:** `baseManaCost`=`80`; `manaCostPerLevel`=`5`; `baseSpellPower`=`3`; `spellPowerPerLevel`=`2`; `castTime`=`0`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getRecastCount()`, `onCast()`, `getDamage()`, `getEmptyCastData()`.
- **Fórmulas numéricas com retorno direto:** `getRecastCount = 5`; `getDamage = getSpellPower(spellLevel, caster)`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `TargetEntityCastData`, `addFreshEntity`.

**Contrato de perks:** escola `fire` não certifica que todo dano/incêndio seja fire damage; verificar fonte de dano, duração de burning e entidades de projétil. Separar atributo de spell power nativo de mutações de área/contagem/efeito, que exigem hook específico, caps e world safety. Sem contrato comprovado: ⚠️ condicionado/fail-closed. RPG Skill Tree gerencia perks, Mastery e gates; Iron's mantém cast, mana e efeitos nativos; Black Arcana mantém seu runtime e WorldEffectPolicy para efeitos próprios. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
