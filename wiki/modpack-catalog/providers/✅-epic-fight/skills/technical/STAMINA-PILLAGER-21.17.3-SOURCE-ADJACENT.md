# Stamina Pillager — ganho de stamina após kill

**Skill ID:** `epicfight:stamina_pillager` · passive / `EXCLUDED` · 🟡 engenharia de recurso/progressão.

**Evidência e limitação:** identidade do ID já classificada na auditoria exata Epic Fight 21.17.3.1 (SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`); observações de fórmula, método e JSON abaixo são exclusivamente `SOURCE_ADJACENT` da revisão `Antikythera-Studios/epicfight@a78aa24b72e90a9d09f5fd61925e4369d117abaf` (declara 21.17.3), ainda não prova bytecode 21.17.3.1 para esta skill. `EXCLUDED` = excluído da métrica de magia, não do universo de perks. Black Arcana não assume a execução deste combat provider; RPG Skill Tree só poderá consumir fatos/atributos via contrato real. Nenhuma perk, adapter ou teste runtime foi implementado.

## Fluxo causal
- [stamina_pillager.json](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/resources/data/epicfight/skill_parameters/stamina_pillager.json) declara `regen_rate=30`, `minecraft:generic.attack_damage add_multiplied_total +0.1` e `epicfight:stamina add_value +3.0`. Dados source 21.17.3, não buffs garantidos carregados.
- [StaminaPillagerSkill.java L27–57](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/passive/StaminaPillagerSkill.java#L27-L57): listener `EpicFightEventHooks.Entity.KILL_ENTITY`; define `missing=getMaxStamina()-getStamina()` e `newStamina=current+min(missing×regenRate×0.01,2.0)`. Com default 30 isso representa **30% do déficit com limite de +2** naquele callback. O método não checa diretamente dano de feitiço, escola mágica, entidade owner de minion ou origem de kill; o contrato do evento precisa ser confirmado antes de creditar Mastery.
- O callback reproduz áudio/partículas via pacotes `STAMINA_PILLAGER_BODY_ASHES` e `FLASH_WHITE`. Esse feedback é subsequente ao evento e não estabelece outro kill ou habilidade independente.

## Perks/limites
- **Recurso:** Epic Fight controla stamina e cap. Não criar dupla restauração num listener do RPG Skill Tree.
- **Atribuição:** `KILL_ENTITY` não basta sem verificar cause/root, attribution de summon/DoT, sequenciamento e dedup; ⛔ não dar XP automático.
- **Damage/target/area/hitbox/cast:** não definidos por esta passiva. `+0.1` aplica-se via attribute modifier, não dano secundário de entidade.
- **QA:** JAR físico 21.17.3.1, regenRate carregada, event side, kill assist/own summon, stamina full/overcap, mortes duplicadas e addon que envia kills, reentrância; nenhum teste atual confirma execução.
