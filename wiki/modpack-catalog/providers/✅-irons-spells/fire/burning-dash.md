# Burning Dash

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Fire
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Instant
- **Mana:** 20–38
- **Cooldown:** 10 s
- **Dano:** 6–15
- **I-frames durante o dash:** presentes; duração exata `NÃO VERIFICADO`

## O que faz

Lança rapidamente o caster para frente envolto em fogo, causando dano às criaturas atravessadas durante o avanço. O changelog oficial registra que o rework passou a conceder I-frames durante a execução e a causar dano nos mobs atravessados, em vez de apenas na origem do dash.

## Escalonamento

O dano listado cresce de 6 para 15. Distância, velocidade, hitbox, duração exata dos I-frames e regras finas de colisão ficam `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação / authority

Já cobre dash ofensivo de fogo com dano por atravessamento e janela defensiva nativa do provider. Uma mobilidade Black Arcana equivalente precisa de consequência/contrato distinto além de VFX; bridges não devem adicionar uma segunda janela de invulnerabilidade sobre o mesmo cast sem contrato explícito.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Changelog oficial: `https://iron.wiki/changelog/`
- Consulta: 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`BurningDashSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/fire/BurningDashSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:burning_dash` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `COMMON`; maxLevel `10`; cooldown `10` segundos; cast `INSTANT`.
- **Campos Java:** `baseManaCost`=`20`; `manaCostPerLevel`=`2`; `baseSpellPower`=`1`; `spellPowerPerLevel`=`1`; `castTime`=`0`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `onClientCast()`, `getEmptyCastData()`, `onCast()`, `getDamageSource()`, `getDamage()`, `getCastStartAnimation()`.
- **Fórmulas numéricas com retorno direto:** `getDamage = (int) (5 + getSpellPower(spellLevel, caster))`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `MobEffectInstance`, `SpellDamageSource`, `addEffect`.

**Contrato de perks:** escola `fire` não certifica que todo dano/incêndio seja fire damage; verificar fonte de dano, duração de burning e entidades de projétil. Separar atributo de spell power nativo de mutações de área/contagem/efeito, que exigem hook específico, caps e world safety. Sem contrato comprovado: ⚠️ condicionado/fail-closed. RPG Skill Tree gerencia perks, Mastery e gates; Iron's mantém cast, mana e efeitos nativos; Black Arcana mantém seu runtime e WorldEffectPolicy para efeitos próprios. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
