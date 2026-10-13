# Firebolt

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Fire
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Instant
- **Mana:** 10–28
- **Cooldown:** 1 s
- **Dano:** 6–10,5

## O que faz

Dispara um pequeno projétil de fogo que incendeia o alvo atingido.

## Escalonamento

O dano listado cresce de 6 para 10,5. Velocidade, duração de ignite e propriedades internas ficam `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação

Já cobre bolt incendiário simples de baixo cooldown. Outra escola não ganha delta mecânico apenas trocando apresentação/elemento desse padrão.

## Fonte / evidência

Catálogo oficial atual: `https://iron.wiki/spells/` — consulta em 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`FireboltSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/fire/FireboltSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:firebolt` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `COMMON`; maxLevel `10`; cooldown `1` segundos; cast `INSTANT`.
- **Campos Java:** `baseManaCost`=`10`; `manaCostPerLevel`=`2`; `baseSpellPower`=`12`; `spellPowerPerLevel`=`1`; `castTime`=`0`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `onCast()`, `getDamageSource()`, `getDamage()`.
- **Fórmulas numéricas com retorno direto:** `getDamage = getSpellPower(spellLevel, entity) * .5f`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `SpellDamageSource`, `addFreshEntity`.

**Contrato de perks:** escola `fire` não certifica que todo dano/incêndio seja fire damage; verificar fonte de dano, duração de burning e entidades de projétil. Separar atributo de spell power nativo de mutações de área/contagem/efeito, que exigem hook específico, caps e world safety. Sem contrato comprovado: ⚠️ condicionado/fail-closed. RPG Skill Tree gerencia perks, Mastery e gates; Iron's mantém cast, mana e efeitos nativos; Black Arcana mantém seu runtime e WorldEffectPolicy para efeitos próprios. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
