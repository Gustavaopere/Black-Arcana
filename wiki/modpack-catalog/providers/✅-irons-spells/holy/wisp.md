# Wisp

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:wisp`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Long
- **Cast time auditado:** 20 ticks
- **Mana:** 15–33
- **Cooldown:** 3 s
- **Dano atual:** 5–14
- **Target helper auditado:** 48 blocos

## O que faz

Conjura uma entidade/projétil Holy que segue o alvo e causa dano ao impactar.

## Source audit 3.16.3

- spell power: base 5, +1/level;
- com target válido, cria `WispEntity(world, caster, spellPower)`;
- associa o target e posiciona o wisp à frente do caster;
- o tooltip expõe spell power como dano.

A liquidação fina de perseguição/impacto pertence à `WispEntity`; não é reconstruída nesta ficha sem audit específico dessa entidade.

## Targets / PvP / bosses / summons

- **Target helper confirmado:** até 48 blocos; requer target válido para criar/associar a `WispEntity`.
- **Players em PvP, bosses e summons:** elegibilidade/imunidades específicas ficam `NÃO VERIFICADO`.
- **Perseguição, retarget e impacto finos:** `NÃO VERIFICADO` além da ownership confirmada pela `WispEntity`.

## Obtenção, requisitos e aprendizado

- **Pipeline geral:** segue o sistema de scrolls/spellbooks do Iron's.
- **Rotas específicas de loot/trade/craft/recompensa:** `NÃO VERIFICADO`.
- **Condições/requisitos adicionais:** `NÃO VERIFICADO`.
- **Itens/focus/rituais específicos além do pipeline normal do provider:** `NÃO VERIFICADO`.

## Integrações / QA / fail-closed

- **Entity/homing authority:** `WispEntity`.
- **Bridge específica de aquisição/casting ou retarget:** `NÃO VERIFICADO`.
- **VFX/animação/áudio final e QA client/modpack real:** `NÃO VERIFICADO`.
- Não criar uma segunda entidade/homing path nem duplicar dano no impacto.

## Deduplicação / causalidade

Já cobre orbe/wisp Holy teleguiado. Não criar segunda lógica de homing nem duplicar dano no impacto ao integrar o spell.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Source audit canônico: `wiki/modpack-catalog/providers/irons-spells/audits/source-3.16.3/spells/holy/wisp.md`
- Consulta: 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`WispSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/WispSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:wisp` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `COMMON`; maxLevel `10`; cooldown `3` segundos; cast `LONG`.
- **Campos Java:** `baseManaCost`=`15`; `manaCostPerLevel`=`2`; `baseSpellPower`=`5`; `spellPowerPerLevel`=`1`; `castTime`=`20`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `getImpactSound()`, `checkPreCastConditions()`, `onCast()`, `getDistance()`, `getDuration()`.
- **Fórmulas numéricas com retorno direto:** `getDistance = getSpellPower(spellLevel, sourceEntity) * 5`; `getDuration = ((getSpellPower(spellLevel, sourceEntity)) * 10)`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `RaycastBuilder`, `TargetEntityCastData`, `addFreshEntity`.

**Contrato de perks:** escola `holy` não prova dano, cura ou imunidade universais. Inspecionar fonte de dano/cura e estado persistente do efeito nativo antes de modificar duração, alcance e alvo. Atributo provider-native e patch em entidade/efeito são integrações diferentes; requerem evento/hook real, caps e prevenção de duplicidade. Sem hook: ⚠️ condicionado/fail-closed. Iron's é autoridade do cast e mana; RPG Skill Tree, perks/Mastery/gates; Black Arcana, seu runtime mágico. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
