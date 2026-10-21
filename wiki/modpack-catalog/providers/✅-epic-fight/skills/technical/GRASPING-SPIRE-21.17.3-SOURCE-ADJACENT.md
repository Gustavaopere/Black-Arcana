# Grasping Spire — duas fases de weapon innate e escala de impacto por hits da primeira fase

**ID:** `epicfight:grasping_spire` · weapon innate **marcial** `EXCLUDED` do numerador de magia (três outras innates sobrenaturais já contadas) · 🟡 integração de multi-phase/impact.

**Proveniência:** `epicfight` / JAR instalado `epic-fight-21.17.3.1-mc1.21.1-neoforge.jar`, SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`, identidade incluída nos **43 IDs core já classificados**. Métodos/fórmulas abaixo = fonte adjacente oficial `Antikythera-Studios/epicfight@a78aa24b72e90a9d09f5fd61925e4369d117abaf` (**21.17.3**, não equivalência 21.17.3.1). Dados empacotados 21.17.3.1 são gate separado. `EXCLUDED` da métrica de novos feitiços; admissível à documentação de perks do RPG Skill Tree. Nenhum hook/modifier externo foi implementado.

## Source-adjacent
- [grasping_spire.json](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/resources/data/epicfight/skill_parameters/grasping_spire.json) declara `consumption=40` no JSON; a unidade/economia final é controlada por `WeaponInnateSkill`, não confirmar automaticamente `40 mana` ou `40 stamina`.
- [GraspingSpireSkill.java L19–28](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/weaponinnate/GraspingSpireSkill.java#L19-L28) tem duas animações de ataque (`GRASPING_SPIRAL_FIRST` e `GRASPING_SPIRAL_SECOND`).
- [GraspingSpireSkill.java L30–53](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/weaponinnate/GraspingSpireSkill.java#L30-L53): quando a primeira animação **termina**, guarda `LAST_HIT_COUNT` de `getCurrentlyActuallyHitEntities().size()`; em `DELIVER_DAMAGE_POST` ligado à segunda animação acrescenta `ValueModifier.adder(LAST_HIT_COUNT×0.4)` **ao impacto**, não dano bruto. `DELIVER_DAMAGE_POST` não autoriza outro `target.hurt` pelo RPG Skill Tree; o estágio de uso do modifier precisa teste.
- [GraspingSpireSkill.java L55–77](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/weaponinnate/GraspingSpireSkill.java#L55-L77) sincroniza primeira animação antes de delegar execução a super; props de phase0 e phase1 aplicadas em suas respectivas `AttackAnimation`. Collider/área/dano base não são inferidos dessa classe; dependem dos dados de animação, arma e outros modifiers.
- **Sem novo objeto mágico:** duas fases/hits continuam um root `weapon_innate` Epic Fight e Mastery não duplica por primeira animação, segundo golpe, stack `LAST_HIT_COUNT` ou FX.

## QA
QA exata bytecode 21.17.3.1, hit counting antes/depois de animação, targets persistentes, i-frames, escudo, eventos prioritários, custo/gauge, hitbox da animação, mods de arma e falha de cancelamento/latência. Nenhum adapter ou combate GameTest nesta ficha.
