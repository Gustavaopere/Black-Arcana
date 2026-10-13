# Sunbeam

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:sunbeam`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1–10
- **Raridade:** Uncommon → Legendary
- **Cast:** Instant
- **Mana:** 40–130
- **Cooldown:** 20 s
- **Dano atual:** 12–25,5
- **Targeting auditado:** até 48 blocos

## O que faz

Canaliza a energia dos céus em um ataque Holy vertical sobre o alvo/ponto resolvido.

## Source audit 3.16.3

- spell power: base 24, +3/level;
- cria `SunbeamEntity` no alvo/ponto resolvido pelo raycast;
- fórmula: `damage = getSpellPower(level, caster) * 0.5`;
- quando não há target entity, procura posição relativa ao chão;
- toca `SUNBEAM_WINDUP` na posição criada.

## Targets / PvP / bosses / summons

- **Targeting confirmado:** raycast/posição até 48 blocos; cria `SunbeamEntity`.
- **Players em PvP, bosses e summons:** elegibilidade/imunidades específicas ficam `NÃO VERIFICADO`.
- A busca de posição no chão quando não há entidade é provider-native; não substituí-la por targeting paralelo.

## Obtenção, requisitos e aprendizado

- **Pipeline geral:** segue o sistema de scrolls/spellbooks do Iron's.
- **Rotas específicas de loot/trade/craft/recompensa:** `NÃO VERIFICADO`.
- **Condições/requisitos adicionais:** `NÃO VERIFICADO`.
- **Itens/focus/rituais específicos além do pipeline normal do provider:** `NÃO VERIFICADO`.

## Integrações / QA / fail-closed

- **Entity/damage authority:** `SunbeamEntity` com `damage = spellPower * 0.5`.
- **Bridge específica de aquisição/casting:** `NÃO VERIFICADO`.
- **VFX final além do windup, animação e QA client/modpack real:** `NÃO VERIFICADO`.
- Não duplicar o beam/dano ou alterar a seleção de posição sem hook comprovado.

## Deduplicação

Já cobre “raio de luz do céu” cujo resultado é dano Holy. Uma magia Celestial futura precisa de condição/recurso/semântica distinta — Sanctum, Resonance, julgamento contextual etc. — e não apenas outro beam visual.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Source audit canônico: `wiki/modpack-catalog/providers/irons-spells/audits/source-3.16.3/spells/holy/sunbeam.md`
- Consulta: 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`SunbeamSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/SunbeamSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:sunbeam` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `UNCOMMON`; maxLevel `10`; cooldown `20` segundos; cast `INSTANT`.
- **Campos Java:** `baseManaCost`=`40`; `manaCostPerLevel`=`10`; `baseSpellPower`=`24`; `spellPowerPerLevel`=`3`; `castTime`=`0`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `checkPreCastConditions()`, `onCast()`, `getDamage()`, `getDuration()`.
- **Fórmulas numéricas com retorno direto:** `getDamage = this.getSpellPower(spellLevel, entity) * .5f`; `getDuration = 100 + spellLevel * 40`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `RaycastBuilder`, `TargetEntityCastData`, `addFreshEntity`.

**Contrato de perks:** escola `holy` não prova dano, cura ou imunidade universais. Inspecionar fonte de dano/cura e estado persistente do efeito nativo antes de modificar duração, alcance e alvo. Atributo provider-native e patch em entidade/efeito são integrações diferentes; requerem evento/hook real, caps e prevenção de duplicidade. Sem hook: ⚠️ condicionado/fail-closed. Iron's é autoridade do cast e mana; RPG Skill Tree, perks/Mastery/gates; Black Arcana, seu runtime mágico. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
