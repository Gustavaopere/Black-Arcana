# Divine Smite

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:divine_smite`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1–5
- **Raridade:** Common → Legendary
- **Cast:** Long
- **Cast time auditado:** 16 ticks
- **Mana:** 30–90
- **Cooldown:** 15 s
- **Dano Holy base atual:** 8–20
- **Interrupção:** não interrompível pelo método do spell
- **Cast-time scaling:** deliberadamente ignorado pelo provider para preservar o timing melee

## O que faz

Executa um ataque melee em área imbuído de energia Holy.

## Source audit 3.16.3

- spell power Holy: base 8, +3/level;
- avanço/raycast curto: ~1,7 bloco;
- raio de impacto: 2,2 blocos;
- exige line of sight para cada entidade atingida;
- fórmula auditada: `damage = HolySpellPower + weaponDamage + SmiteEnchantmentContribution`;
- quando o dano confirma, aplica efeitos pós-ataque de enchantment.

VFX/animação auditados: blastwave Holy, 50 electric sparks, camera shake, sons próprios de windup/cast e `OVERHEAD_MELEE_SWING_ANIMATION`.

## Targets / PvP / bosses / summons

- **Targeting confirmado:** entidades dentro do impacto de 2,2 blocos com line of sight, após o avanço/raycast curto.
- **Elegibilidade exata de players em PvP, bosses e summons:** `NÃO VERIFICADO`; não inferir imunidades ou permissões.
- Weapon damage, Smite e post-hit enchantments permanecem sob a causalidade do provider.

## Obtenção, requisitos e aprendizado

- **Pipeline geral:** segue o sistema de scrolls/spellbooks do Iron's.
- **Rotas específicas de loot/trade/craft/recompensa:** `NÃO VERIFICADO`.
- **Condição/equipamento obrigatório além de a fórmula consumir weapon damage:** `NÃO VERIFICADO`.
- **Itens/focus/rituais específicos além do pipeline normal do provider:** `NÃO VERIFICADO`.

## Integrações / QA / fail-closed

- **Integração causal comprovada:** composição com weapon damage, Smite e efeitos pós-ataque do próprio provider.
- **Compatibilidade específica com Epic Fight/animation bridges no resultado de gameplay:** `NÃO VERIFICADO` nesta ficha.
- **QA client/modpack real:** `NÃO VERIFICADO`.
- Não reaplicar dano de arma, enchantment contribution ou post-hit effects fora do cast nativo.

## Deduplicação / causalidade

Já cobre smite Holy melee dependente da arma. Uma bridge deve preservar um único evento causal de cast/ataque; não reaplicar weapon damage, Smite contribution ou enchantment post-hit em um segundo pipeline.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Source audit canônico: `wiki/modpack-catalog/providers/irons-spells/audits/source-3.16.3/spells/holy/divine-smite.md`
- Consulta: 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`DivineSmiteSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/DivineSmiteSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:divine_smite` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `COMMON`; maxLevel `5`; cooldown `15` segundos; cast `LONG`.
- **Campos Java:** `baseManaCost`=`30`; `manaCostPerLevel`=`15`; `baseSpellPower`=`8`; `spellPowerPerLevel`=`3`; `castTime`=`16`.
- **Métodos no código:** `getUniqueInfo()`, `getEffectiveCastTime()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `onCast()`, `getDamage()`, `getAdditionalDamage()`, `getDamageText()`, `getCastStartAnimation()`, `getCastFinishAnimation()`.
- **Fórmulas numéricas com retorno direto:** `getDamage = getSpellPower(spellLevel, entity) + getAdditionalDamage(entity)`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `DamageSources`.

**Contrato de perks:** escola `holy` não prova dano, cura ou imunidade universais. Inspecionar fonte de dano/cura e estado persistente do efeito nativo antes de modificar duração, alcance e alvo. Atributo provider-native e patch em entidade/efeito são integrações diferentes; requerem evento/hook real, caps e prevenção de duplicidade. Sem hook: ⚠️ condicionado/fail-closed. Iron's é autoridade do cast e mana; RPG Skill Tree, perks/Mastery/gates; Black Arcana, seu runtime mágico. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
