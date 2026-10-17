# Swordmaster — velocidade de ataque por categoria e bônus de atributos

**Skill exata:** `epicfight:swordmaster` · passive/martial, `EXCLUDED` das magias · 🟡 dossiê de efeitos úteis para perks de arma.

**Autoridade e confiança:** `epicfight`, JAR físico `epic-fight-21.17.3.1-mc1.21.1-neoforge.jar`, SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`; identidade presente no registry exato de 43 skills (auditoria do artefato já catalogada). **Implementação e parâmetros abaixo vêm de fonte ADJACENTE:** `Antikythera-Studios/epicfight@a78aa24b72e90a9d09f5fd61925e4369d117abaf` / `gradle/libs.versions.toml` = **21.17.3**, não 21.17.3.1. Não declarar assinatura, valores efetivos, modpack datapack ou hook compatível com o JAR físico até inspeção comparativa. Nenhuma mudança em runtime, perk ou adapter. Conteúdo de combat/progression do RPG Skill Tree, não nova raiz de magia Black Arcana. Clean-room.

## Source e parâmetros

- [swordmaster.json](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/resources/data/epicfight/skill_parameters/swordmaster.json) define `speed_bonus=30` e **dois** attribute modifiers: `epicfight:stamina_regen` **+0.2** `add_value`, `epicfight:stamina` **+2.0** `add_value`; esses são valores dos recursos upstream 21.17.3, **não valores finais do jogador**, que podem variar por datapack/equipamento. [SwordmasterSkill.java L66–70](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/passive/SwordmasterSkill.java#L66-L70); [Skill.java L128–138](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/Skill.java#L128-L138).
- Builder usa categorias `UCHIGATANA`, `LONGSWORD`, `SWORD`, `TACHI`; verifica `CapabilityItem.isWeaponCategory(setCategory)` ao aplicar velocidade. Addons podem introduzir categorias relacionadas, mas reconhecimento efetivo e herança só podem ser assumidos após teste de capability no pack. [SwordmasterSkill.java L38–57](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/passive/SwordmasterSkill.java#L38-L57).
- `onInitiate` registra `EpicFightEventHooks.Entity.MODIFY_ATTACK_SPEED`. Quando a categoria é aceita, executa `event.setAttackSpeed(current×(1+speedBonus/100))`: default adjacente significa fator **×1.30**, não `+30` ticks, nem bônus ao dano. O mesmo método registra modificação de som de swing separada, e no cliente altera trilha VFX; esses efeitos estéticos não justificam Mastery. [SwordmasterSkill.java L73–107](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/passive/SwordmasterSkill.java#L73-L107); [EpicFightEventHooks.java L31–48](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/api/event/EpicFightEventHooks.java#L31-L48).
- `MODIFY_ATTACK_SPEED` é um `EventHook` declarado sem restrição explícita de LogicalSide nesse field, ao contrário de vários hooks de dano server-side na mesma classe. **Não presumir evento exclusivamente servidor:** a aplicação deve demonstrar onde o cálculo é consumido, prioridades, stacking e sync. [EpicFightEventHooks.java L31–48](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/api/event/EpicFightEventHooks.java#L31-L48).

## Matriz para perks

| Eixo | Valor real nesta revisão | Segurança |
|---|---|---|
| Attack speed | categoria validada ⇒ `speed×1.30` default adjacente | ⚠️ evento existe na fonte; ⛔ multiplicação adicional por perk sem dedup/teste |
| Stamina | +2 total, +0.2 regen via atributo | ⚠️ resource JSON adjacente; priorizar atributos canônicos, evitar duplicar |
| Dano/tipo | **N/A** efeito direto nessa classe; speed ≠ damage | ⛔ não somar `attack_damage` presumido |
| Hitbox/alvo | **N/A** no source desta passive | ⛔ nenhum hook de alcance/retarget |
| Mastery | não gera cast nem dano próprio | ⛔ XP por equipar buff, VFX, som ou update de atributo |

**QA:** artefato físico 21.17.3.1, datapack reload, categories de mods, WeaponCategory inheritance, mixins/EFIS, modo de combate, prioridades e stacking do `MODIFY_ATTACK_SPEED`, event server/client, recarga stamina/sync e desempenho. Sem perk/runtime implementado.
