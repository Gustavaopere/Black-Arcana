# Scorch

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Fire
- **Níveis:** 1–10
- **Raridade:** Uncommon → Legendary
- **Cast:** Long
- **Mana:** 50–95
- **Cooldown:** 12 s
- **Dano:** 8–17
- **Raio:** 2,5 blocos

## O que faz

Faz uma erupção localizada de magia de fogo na área alvo, causando dano e deixando um campo de fogo no local.

## Escalonamento

O dano listado cresce de 8 para 17; o raio atual é 2,5 blocos. O changelog registra que o spell foi buffado para deixar campo de fogo e que houve correção de posicionamento no recast; comportamento antigo não prevalece.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Scorch foi adicionado na linha 3.1.5; rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação / world safety

Já cobre ground-targeted burst + fire field. Uma versão Black Arcana equivalente não é gap por usar outra chama. O field permanece provider-native e não autoriza spread/mutação adicional por bridge.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Changelog oficial: `https://iron.wiki/changelog/`
- Consulta: 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`ScorchSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/fire/ScorchSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:scorch` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `UNCOMMON`; maxLevel `10`; cooldown `12` segundos; cast `LONG`.
- **Campos Java:** `baseManaCost`=`50`; `manaCostPerLevel`=`5`; `baseSpellPower`=`8`; `spellPowerPerLevel`=`1`; `castTime`=`20`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `checkPreCastConditions()`, `onCast()`, `getDamageSource()`, `getDamage()`, `getRadius()`, `getTargetingColor()`, `getCastStartAnimation()`, `getCastFinishAnimation()`.
- **Fórmulas numéricas com retorno direto:** `getDamage = getSpellPower(spellLevel, caster)`; `getRadius = 2.5f`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `RaycastBuilder`, `SpellDamageSource`, `DamageSources`, `addFreshEntity`.

**Contrato de perks:** escola `fire` não certifica que todo dano/incêndio seja fire damage; verificar fonte de dano, duração de burning e entidades de projétil. Separar atributo de spell power nativo de mutações de área/contagem/efeito, que exigem hook específico, caps e world safety. Sem contrato comprovado: ⚠️ condicionado/fail-closed. RPG Skill Tree gerencia perks, Mastery e gates; Iron's mantém cast, mana e efeitos nativos; Black Arcana mantém seu runtime e WorldEffectPolicy para efeitos próprios. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
