# Technician — dodge comprovado, reembolso de stamina e VFX

**Skill ID:** `epicfight:technician` · passive / `EXCLUDED` · 🟡 pesquisa para perks.

**Evidência e limitação:** identidade do ID já classificada na auditoria exata Epic Fight 21.17.3.1 (SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`); observações de fórmula, método e JSON abaixo são exclusivamente `SOURCE_ADJACENT` da revisão `Antikythera-Studios/epicfight@a78aa24b72e90a9d09f5fd61925e4369d117abaf` (declara 21.17.3), ainda não prova bytecode 21.17.3.1 para esta skill. `EXCLUDED` = excluído da métrica de magia, não do universo de perks. Black Arcana não assume a execução deste combat provider; RPG Skill Tree só poderá consumir fatos/atributos via contrato real. Nenhuma perk, adapter ou teste runtime foi implementado.

## Causalidade
- [TechnicianSkill.java L20–33](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/passive/TechnicianSkill.java#L20-L33): o listener `EpicFightEventHooks.Entity.ON_DODGE` lê `SkillSlots.DODGE`, consulta `getConsumption()`, aplica `getModifiedStaminaConsume(...)` e restaura essa quantidade via `setStamina(current+consumption)`. O método **não demonstra clamp local**; qualquer cap precisa ser verificado no setter nativo. Não presumir que toda tentativa de Dodge receba reembolso: o gatilho é evento de dodge, não pressionamento de tecla.
- [TechnicianSkill.java L35–44](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/passive/TechnicianSkill.java#L35-L44): há outro listener em `EpicFightEventHooks.Animation.BEGIN`; quando a animação é `DodgeAnimation` e o executor não é cliente lógico, envia `TECHNICIAN_ACTIVATED` a clientes para apresentação. **Animação/packet não é evidência de dodge real**, devendo ser desconsiderado para Mastery.
- [technician.json](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/resources/data/epicfight/skill_parameters/technician.json): modificador adjacente `epicfight:stamina_regen` **add_value +0.4**, adicional ao reembolso condicional; conferir stacking e valores efetivos do JSON carregado.

## Matriz de perks
- **Custo e recuperação:** propriedade do Epic Fight; não debitar nem reembolsar segunda vez. Não presumir recurso `MANA`.
- **Condição de progressão:** estudar causalidade do `ON_DODGE` com dano efetivamente evitado e deduplicação. ⛔ XP por animation BEGIN, VFX ou pacote.
- **Hitbox/target/damage/cast:** N/A nesta passiva. ⚠️ Esta classe não documenta i-frames.
- **Validação pendente:** confirmar símbolo e fluxo no JAR 21.17.3.1, limite de stamina, SkillSlots.DODGE nulo/custom, ataque bloqueado versus dodge, modo combate, multiplayer, addons. Fail-closed sem hook de award validado.
