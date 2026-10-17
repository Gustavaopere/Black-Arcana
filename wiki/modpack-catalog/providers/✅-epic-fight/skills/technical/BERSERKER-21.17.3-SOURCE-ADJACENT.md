# Berserker — escala por vida perdida, velocidade e dano

**Skill ID:** `epicfight:berserker` · passive / `EXCLUDED` · 🟡 aprofundamento técnico.

**Evidência e limitação:** identidade do ID já classificada na auditoria exata Epic Fight 21.17.3.1 (SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`); observações de fórmula, método e JSON abaixo são exclusivamente `SOURCE_ADJACENT` da revisão `Antikythera-Studios/epicfight@a78aa24b72e90a9d09f5fd61925e4369d117abaf` (declara 21.17.3), ainda não prova bytecode 21.17.3.1 para esta skill. `EXCLUDED` = excluído da métrica de magia, não do universo de perks. Black Arcana não assume a execução deste combat provider; RPG Skill Tree só poderá consumir fatos/atributos via contrato real. Nenhuma perk, adapter ou teste runtime foi implementado.

## Fórmulas source-adjacent
- [berserker.json](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/resources/data/epicfight/skill_parameters/berserker.json): `speed_bonus=0.5`, `damage_bonus=0.3`, `epicfight:stamina add_value +6.0`; são defaults da revisão 21.17.3, não parâmetros de um jogador no pack.
- [BerserkerSkill.java L71–101](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/passive/BerserkerSkill.java#L71-L101): `MODIFY_ATTACK_SPEED` calcula `lost=(maxHealth-health)/maxHealth`, quantiza a duas casas **por floor(percentual perdido×100)×0.01**, e define `speed = min(5.0, currentSpeed × [1 + floor(lost×100)×0.01×speedBonus])`. Com o valor de JSON, `speedBonus=0.5`, não 50 unidades planas; o cap **5.0** é aplicado nesta passiva depois dos modificadores que já existiam quando o evento chegou.
- No mesmo método, `MODIFY_ATTACK_DAMAGE` adiciona `ValueModifier.multiplier(1 + floor(lost×100)×0.01×damageBonus)`, não chama `target.hurt`. É amplificação de cálculo do ataque, não ação mágica/cast independente.
- [BerserkerSkill.java L36–69](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/passive/BerserkerSkill.java#L36-L69): overlay vermelha e partículas locais dependem de vida atual; **VFX não é prova de dano acertado**. Não transferir fórmula visual para autoridade do servidor.

## Integração segura
- **Atributos e stacking:** stamina +6 nativa, dano e velocidade via hooks do provider; não duplicar aumento por perks nem somar Mastery por atualização do tooltip.
- **Dano e escola mágica:** não há `SpellDamageEvent` nesta classe; o registro não prova aplicação a feitiços de Iron's, Ars ou Black Arcana.
- **Hitbox, AOE, target, cast, cooldown:** não apresentados. ⛔ Nenhum setter foi demonstrado.
- **QA:** confirmar cap 5 no classfile, ordem listener e side, vitais health/max health, confronto com Swordmaster e modifiers, valor real do JSON 21.17.3.1; prever testes PvP, server e modpacks.
