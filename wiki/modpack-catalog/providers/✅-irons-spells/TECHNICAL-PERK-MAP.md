# Iron's Spells — especificação de parâmetros para perks (3.16.3)

Fonte de interoperabilidade para o Codex. Minecraft 1.21.1 / NeoForge / Java 21. JAR do pack: `irons_spellbooks-1.21.1-3.16.3.jar`. Source pin: [iron431@e4056af90302d37eb1739f5ff05020b020e6e252](https://github.com/iron431/irons-spells-n-spellbooks/tree/e4056af90302d37eb1739f5ff05020b020e6e252). Base nativa: 110 spells ativos em nove escolas; este primeiro lote de auditoria mecânica profunda é Blood (10/10). **O catálogo 110/110 já existia e não deve ter sua contagem inflada por esta adição.**

## Contratos e fórmulas do provider

- `AbstractSpell.getSpellPower(level, caster)`: `(baseSpellPower + spellPowerPerLevel*(level-1)) * SPELL_POWER * schoolPower * POWER_MULTIPLIER`. Multiplicadores de atributo se aplicam quando caster é entidade viva.
- `AbstractSpell.getManaCost(level)`: `(int)((baseManaCost + manaCostPerLevel*(level-1))*MANA_MULTIPLIER)`.
- `getSpellCooldown()`: `COOLDOWN_IN_SECONDS` de config convertido para ticks (`*20`). Cooldown efetivo pós atributos requer leitura do pipeline de cast.
- `getCastTime(level)`: zero para INSTANT, caso contrário o valor da classe ou override; castTime efetivo do caster depende de redução de cast time.
- São fórmulas de source do provider para documentação, **não** código a copiar para Black Arcana.

[AbstractSpell.java — source fixado](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java).

## O que o Codex deve identificar em cada ficha

1. ID real, escola, versão, classe `*Spell` e source permalink no commit exato.
2. `DefaultConfig` e campos: maxLevel, cooldown, rarity, castType, baseManaCost, manaCostPerLevel, baseSpellPower, spellPowerPerLevel, castTime.
3. Métodos que governam targeting, geometria, efeito, entidades/projéteis e damage source; fórmulas com unidades, caps e dependências de helper/entity/effect.
4. Relação cast → projétil → aplicação de dano/cura → atribuição de Mastery, respeitando deduplicação.
5. Superfície de modificação possível, **separada** entre atributo provider-native, evento real verificado e alteração sem hook seguro (fail-closed).

## Categorias editoriais para perks (não são campos/API existentes)

`damage`, `heal`, `range`, `radius`, `cone_angle`, `projectile_count`, `projectile_speed`, `summon_count`, `effect_duration`, `status_effect`, `mana_cost`, `cooldown`, `cast_time`, `school`, `damage_type`, `world_effect`. Para cada spell, indicar N/A ou NÃO VERIFICADO quando for o caso. Uma escola Fire/Ice/Blood não comprova, sozinha, seu damage type.

## Ownership e invariantes

- Iron's é o dono do cast e da economia/mana nativos. RPG Skill Tree é dono das perks/Mastery/gates; Black Arcana é dono apenas de seu runtime mágico, hazards, domínios, rituais, world-safety e integrações seguras.
- `SpellPreCastEvent`, `SpellOnCastEvent`, `ModifySpellLevelEvent` não podem ser presumidos setters de alcance/raio/projétil. Examinar as signatures antes de afirmar comportamento compatível.
- Nenhuma perk pode provocar cast/proc recursivo, award duplo de Mastery ou ignorar custos transacionais. Todos os efeitos com alta cardinalidade exigem cap e limite de trabalho.
- Clean-room: não incorporar código/arte proprietários. O Codex usa a navegação e a descrição do comportamento para construir adapters próprios quando o contrato real permitir.
- Em particular, Acupuncture gera BloodNeedle, que aplica damage source de Blood Needles; nome de spell causador e classificação de damage source não são intercambiáveis.

## Status

✅ Iron's 110/110 fichas de identidade (pré-existentes). 🟡 Blood 10/10 com aprofundamento estático de parâmetros. ⚠️ Ainda não é QA físico, hook de reescrita comprovado nem validação de Survival ou modpack; auxiliares de effects/projectiles devem ser auditados. Sem promoção de Stage 06.05/07/08.

Fontes: [wiki oficial](https://iron.wiki/spells/), [índice do provider](README.md), [integração planejada no RPG Skill Tree](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/main/docs/integrations/irons.md), [decisões](../../../../plans/DECISIONS.md).
