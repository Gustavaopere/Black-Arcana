# Heat Surge

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Fire
- **Níveis:** 1–6
- **Raridade:** Common → Legendary
- **Cast:** Long
- **Mana:** 50–100
- **Cooldown:** 45 s
- **Redução de armor:** 15%–40%
- **Duração:** 10–20 s
- **Raio:** 6,5–9 blocos

## O que faz

Emana uma onda de magia de fogo ao redor do caster, incendiando e aplicando rend a criaturas na área; criaturas afetadas ficam com armor reduzida.

## Escalonamento

O catálogo atual confirma rend de 15%–40%, duração 10–20 s e raio 6,5–9 blocos. O changelog da linha 1.21 registra que o rend deixou de escalar com spell power e teve o valor-base reduzido para 15%; o contrato atual deve prevalecer.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação

Já cobre AOE de fogo + armor rend. Outra escola não ganha delta apenas por aplicar redução defensiva semelhante com outro VFX.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Changelog oficial: `https://iron.wiki/changelog/`
- Consulta: 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`HeatSurgeSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/fire/HeatSurgeSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:heat_surge` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `COMMON`; maxLevel `6`; cooldown `45` segundos; cast `LONG`.
- **Campos Java:** `baseManaCost`=`50`; `manaCostPerLevel`=`10`; `baseSpellPower`=`10`; `spellPowerPerLevel`=`2`; `castTime`=`20`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `onCast()`, `getRadius()`, `getDuration()`, `getRendAmplifier()`, `onServerCastComplete()`, `getCastStartAnimation()`, `getCastFinishAnimation()`.
- **Fórmulas numéricas com retorno direto:** `getRadius = 6 + spellLevel * .5f`; `getDuration = (int) (getSpellPower(spellLevel, caster) * 20)`; `getRendAmplifier = 1 + (spellLevel)`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `MobEffectInstance`, `DamageSources`, `addEffect`, `setSecondsOnFire`.

**Contrato de perks:** escola `fire` não certifica que todo dano/incêndio seja fire damage; verificar fonte de dano, duração de burning e entidades de projétil. Separar atributo de spell power nativo de mutações de área/contagem/efeito, que exigem hook específico, caps e world safety. Sem contrato comprovado: ⚠️ condicionado/fail-closed. RPG Skill Tree gerencia perks, Mastery e gates; Iron's mantém cast, mana e efeitos nativos; Black Arcana mantém seu runtime e WorldEffectPolicy para efeitos próprios. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
