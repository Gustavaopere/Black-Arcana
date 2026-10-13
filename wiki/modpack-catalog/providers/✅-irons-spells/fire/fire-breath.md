# Fire Breath

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Fire
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Continuous
- **Mana:** 5–14
- **Cooldown:** 12 s
- **Dano:** 1–7,75

## O que faz

Canaliza um cone de fogo à frente do caster, causando dano e incendiando criaturas e blocos atingidos.

## Escalonamento

O dano listado cresce de 1 para 7,75. Alcance, ângulo do cone, cadência e duração do fogo ficam `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação / world safety

Já cobre cone contínuo incendiário. Uma nova magia Black Arcana não é gap apenas por trocar cor/tipo de chama. Mutações de mundo adicionais continuam submetidas às políticas de world safety e não são inferidas a partir deste spell.

## Fonte / evidência

Catálogo oficial atual: `https://iron.wiki/spells/` — consulta em 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`FireBreathSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/fire/FireBreathSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:fire_breath` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `COMMON`; maxLevel `10`; cooldown `12` segundos; cast `CONTINUOUS`.
- **Campos Java:** `baseManaCost`=`5`; `manaCostPerLevel`=`1`; `baseSpellPower`=`0`; `spellPowerPerLevel`=`1`; `castTime`=`100`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastFinishSound()`, `onCast()`, `getDamage()`, `getDamageSource()`.
- **Fórmulas numéricas com retorno direto:** `getDamage = 1 + getSpellPower(spellLevel, caster) * .75f`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `SpellDamageSource`, `addFreshEntity`.

**Contrato de perks:** escola `fire` não certifica que todo dano/incêndio seja fire damage; verificar fonte de dano, duração de burning e entidades de projétil. Separar atributo de spell power nativo de mutações de área/contagem/efeito, que exigem hook específico, caps e world safety. Sem contrato comprovado: ⚠️ condicionado/fail-closed. RPG Skill Tree gerencia perks, Mastery e gates; Iron's mantém cast, mana e efeitos nativos; Black Arcana mantém seu runtime e WorldEffectPolicy para efeitos próprios. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
