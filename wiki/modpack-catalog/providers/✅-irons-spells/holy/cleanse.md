# Cleanse

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:cleanse`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1
- **Raridade:** Epic
- **Cast:** Long
- **Cast time auditado:** 60 ticks
- **Mana:** 100
- **Cooldown:** 60 s
- **Raio:** 3 blocos

## O que faz

Purifica o caster e aliados/elegíveis próximos, removendo efeitos nocivos permitidos pelo provider.

## Source audit 3.16.3

No cast, percorre living entities na caixa 6×6×6 centrada no caster e filtra alvos por `Utils.shouldHealEntity`. Para cada alvo elegível:

1. lê efeitos ativos;
2. seleciona `MobEffectCategory.HARMFUL`;
3. preserva efeitos marcados com `ModTags.CLEANSE_IMMUNE`;
4. remove os demais efeitos nocivos elegíveis;
5. emite partículas de cleanse.

Pre-cast cria `TargetedAreaEntity` de raio 3. Animações auditadas: `CAST_KNEELING_PRAYER` no início e `SELF_CAST_TWO_HANDS` no finish.

## Targets / PvP / bosses / summons

- **Targeting confirmado:** living entities na área, filtradas por `Utils.shouldHealEntity`.
- **Players/PvP, bosses e summons:** a classificação individual dessas categorias dentro de `Utils.shouldHealEntity` fica `NÃO VERIFICADO`; a bridge não deve reconstruir essa policy.
- **Efeitos removíveis:** apenas `HARMFUL` não marcados `CLEANSE_IMMUNE`.

## Obtenção, requisitos e aprendizado

- **Pipeline geral:** segue o sistema de scrolls/spellbooks do Iron's.
- **Rotas específicas de loot/trade/craft/recompensa:** `NÃO VERIFICADO`.
- **Condições/requisitos adicionais:** `NÃO VERIFICADO`.
- **Itens/focus/rituais específicos além do pipeline normal do provider:** `NÃO VERIFICADO`.

## Integrações / QA / fail-closed

- `MobEffectCategory.HARMFUL` e `ModTags.CLEANSE_IMMUNE` são authorities comprovadas.
- **Bridge específica de aquisição/casting:** `NÃO VERIFICADO`.
- **Áudio/textura final e QA client/modpack real:** `NÃO VERIFICADO`.
- Na dúvida sobre target ou efeito removível, falhar fechado e preservar a decisão do provider.

## Deduplicação / fail-closed

Já cobre cleanse genérico de efeitos harmful. Exorcismo só representa lacuna se atuar sobre possession/demon/spirit/curse semantics específicas. Bridges não devem reconstruir a whitelist/blacklist por conta própria; respeitar `CLEANSE_IMMUNE` e a authority do provider.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Source audit canônico: `wiki/modpack-catalog/providers/irons-spells/audits/source-3.16.3/spells/holy/cleanse.md`
- Consulta: 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`CleanseSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/CleanseSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:cleanse` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `EPIC`; maxLevel `1`; cooldown `60` segundos; cast `LONG`.
- **Campos Java:** `baseManaCost`=`100`; `manaCostPerLevel`=`0`; `baseSpellPower`=`0`; `spellPowerPerLevel`=`0`; `castTime`=`60`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastFinishSound()`, `checkPreCastConditions()`, `onCast()`, `getCastStartAnimation()`, `getCastFinishAnimation()`.
- **Fórmulas numéricas com retorno direto:** não extraídas; examinar lógica e entidades auxiliares. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `MobEffectInstance`.

**Contrato de perks:** escola `holy` não prova dano, cura ou imunidade universais. Inspecionar fonte de dano/cura e estado persistente do efeito nativo antes de modificar duração, alcance e alvo. Atributo provider-native e patch em entidade/efeito são integrações diferentes; requerem evento/hook real, caps e prevenção de duplicidade. Sem hook: ⚠️ condicionado/fail-closed. Iron's é autoridade do cast e mana; RPG Skill Tree, perks/Mastery/gates; Black Arcana, seu runtime mágico. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
