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
