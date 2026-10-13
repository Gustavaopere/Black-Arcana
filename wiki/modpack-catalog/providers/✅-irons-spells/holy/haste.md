# Haste

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:haste`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1–4
- **Raridade:** Epic → Legendary
- **Cast:** Long
- **Cast time auditado:** 30 ticks
- **Mana:** 50–80
- **Cooldown:** 80 s
- **Magical Haste atual:** 20%
- **Duração atual:** 30–45 s
- **Targeting auditado:** aliado até 32 blocos; fallback para o próprio caster

## O que faz

Aplica `HASTENED`, aumentando movimento, velocidade de ataque, mineração e Cast Time Reduction conforme a semântica atual do provider.

## Source audit 3.16.3

- spell power: base 30, +5/level;
- duração: `spellPower * 20` ticks;
- amplifier base 7, escalado pelo entity power multiplier;
- percentagem final resolvida por `HastenedEffect.getPercentForAmplifier`.

O catálogo atual resume o resultado como 20% Magical Haste por 30–45 s. A ficha preserva ambos: outcome público e implementação auditada.

## Targets / PvP / bosses / summons

- **Targeting confirmado:** aliado até 32 blocos, com fallback para o próprio caster.
- **Definição exata de aliado para players/PvP, bosses e summons:** `NÃO VERIFICADO`.
- A bridge não deve ampliar a elegibilidade nem substituir o fallback do provider.

## Obtenção, requisitos e aprendizado

- **Pipeline geral:** segue o sistema de scrolls/spellbooks do Iron's.
- **Rotas específicas de loot/trade/craft/recompensa:** `NÃO VERIFICADO`.
- **Condições/requisitos adicionais:** `NÃO VERIFICADO`.
- **Itens/focus/rituais específicos além do pipeline normal do provider:** `NÃO VERIFICADO`.

## Integrações / QA / fail-closed

- **Effect authority:** `HASTENED` / `HastenedEffect.getPercentForAmplifier`.
- **Bridge específica de aquisição/casting:** `NÃO VERIFICADO`.
- **VFX/animação/áudio final e QA client/modpack real:** `NÃO VERIFICADO`.
- Não duplicar movement/attack/mining/CTR como bônus paralelo para o mesmo cast.

## Deduplicação

Já cobre buff Holy multiatributo de haste. Perks/bridges devem operar por hooks/atributos do provider quando disponíveis e não somar um clone do mesmo buff fora do pipeline.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Source audit canônico: `wiki/modpack-catalog/providers/irons-spells/audits/source-3.16.3/spells/holy/haste.md`
- Consulta: 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`HasteSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/HasteSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:haste` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `EPIC`; maxLevel `4`; cooldown `80` segundos; cast `LONG`.
- **Campos Java:** `baseManaCost`=`50`; `manaCostPerLevel`=`10`; `baseSpellPower`=`30`; `spellPowerPerLevel`=`5`; `castTime`=`30`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `checkPreCastConditions()`, `onCast()`, `getAmplifier()`, `getDuration()`.
- **Fórmulas numéricas com retorno direto:** `getDuration = (int) (getSpellPower(spellLevel, caster) * 20)`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `TargetEntityCastData`, `MobEffectInstance`, `addEffect`, `MobEffectRegistry`.

**Contrato de perks:** escola `holy` não prova dano, cura ou imunidade universais. Inspecionar fonte de dano/cura e estado persistente do efeito nativo antes de modificar duração, alcance e alvo. Atributo provider-native e patch em entidade/efeito são integrações diferentes; requerem evento/hook real, caps e prevenção de duplicidade. Sem hook: ⚠️ condicionado/fail-closed. Iron's é autoridade do cast e mana; RPG Skill Tree, perks/Mastery/gates; Black Arcana, seu runtime mágico. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
