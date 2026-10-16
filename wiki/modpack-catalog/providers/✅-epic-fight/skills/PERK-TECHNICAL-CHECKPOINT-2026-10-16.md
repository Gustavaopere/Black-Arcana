# Epic Fight — checkpoint técnico de perks (16/10/2026)

**Mod instalado (autoridade física já documentada):** `epicfight` / `epic-fight-21.17.3.1-mc1.21.1-neoforge.jar` / SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`. Ver [auditoria do artefato exato](../EXACT-21.17.3.1-ARTIFACT-SKILL-AUDIT.md) e [disposition integral](SKILL-DISPOSITION-21.17.3.1.md). O registry core foi classificado em **43/43 IDs exatos**, com **3 ações sobrenaturais** na métrica de magia e **40 skills não mágicas** úteis para pesquisa de perks. Nenhuma nova identidade semântica acrescentada neste lote.

## Barras separadas por nível de evidência

- **Global — universo de magias/rituais de todos os mods:** piso anterior **1.856 objetos semânticos mínimos / 1.854 estritos**, denominador total do pack **aberto (—%)**. Skills marciais não aumentam esse numerador.
- **Epic Fight — identidade e categoria do core (exato 21.17.3.1):** **43/43 = 100%** do registro core enumerado/dispositionado, sendo 3 `COUNTED_EXACT` e 40 `EXCLUDED` (o segundo termo é apenas exclusão da métrica de magia, não do escopo de perks).
- **Epic Fight — matriz de parâmetros para perks nesta tranche (source 21.17.3 adjacente):** **21/43 = 48,84%** do registro recebeu aprofundamento source-adjacent, via **18 dossiês** (13 IDs anteriores + 8 IDs novos: Guard, Endurance, HyperVitality, Adrenaline Fiend, Catharsis, Emergency Escape, Bonebreaker e Vengeance). **22/43 ainda fora destas tranches técnicas de profundidade**; não presumir que não tenham outra documentação histórica. O percentual mede **cobertura documental de causalidade em código adjacente**; a confirmação física **de parâmetros/identidade de símbolos**, agora igualmente 21/43, é uma barra separada e não prova execução segura de perks.
- **Epic Fight — parâmetros JSON e presença de símbolos no JAR exato 21.17.3.1:** ✅ **21/43 = 48,84%** das skills do core passaram em um **gate binário estático limitado**: [run 38981181742](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38981181742) SUCCESS, SHA-1/SHA-256 iguais ao físico, **21 JSONs empacotados, 25 classes via javap, 11/11 testes sintéticos e zero divergências**. Quatro JSONs têm `attribute_modifiers` **legacy-shaped: RAW_ONLY_NOT_PROVEN_LOADED**, portanto seus bônus ainda são condicionados, apesar de a presença e os campos terem sido verificados. [Prova e limites](../EXACT-BINARY-PERK-PARAMETERS-21.17.3.1.md). **Ainda não é** contrato hook/ABI/causalidade instrução-a-instrução, datapack aplicado, execução real, Mastery ou adapter. As oito novas skills têm agora **JSONs e símbolos compilados exatos**; suas **fórmulas, ordem de eventos, acceptance de modifiers e settlement** permanecem `SOURCE_ADJACENT`/condicionados até auditoria causal de bytecode, parsing de attributes e gameplay.

## Objetos aprofundados

| Grupo | IDs exatos do registro | Conteúdo auditado na revisão 21.17.3 (condicionado) |
|---|---|---|
| Defesa | [`parrying`](technical/PARRYING-21.17.3-SOURCE-ADJACENT.md) | janela8t, direção do ataque, `penalty×impact`, guard/parry e stamina |
| Defesa | [`impact_guard`](technical/IMPACT-GUARD-21.17.3-SOURCE-ADJACENT.md) | tipo de dano, `damage_reducer=.2`, tentativa de hurt residual e tags |
| Passiva | [`swordmaster`](technical/SWORDMASTER-21.17.3-SOURCE-ADJACENT.md) | `MODIFY_ATTACK_SPEED`, categorias de arma, `speed_bonus=30`, stamina/regen |
| Passiva | [`forbidden_strength`](technical/FORBIDDEN-STRENGTH-21.17.3-SOURCE-ADJACENT.md) | `CONSUME_SKILL`, fallback STAMINA→HEALTH e modifiers próprios |
| Dodge | [`roll` + `step`](technical/DODGE-ROLL-STEP-21.17.3-SOURCE-ADJACENT.md) | custo4/3 defaults, input cliente, execução server, animações/movesets e estado |
| Trident innate | [`wrathful_lighting`, `tsunami`, `everlasting_allegiance`](technical/TRIDENT-INNATES-21.17.3-SOURCE-ADJACENT.md) | `consumption` 50/50/40 (sem Resource confirmado), properties de attack phase e selector Riptide/Channeling/Loyalty |
| Passiva | [`technician`](technical/TECHNICIAN-21.17.3-SOURCE-ADJACENT.md) | `ON_DODGE` restitui stamina modificada; feedback por animation é separado; stamina regen +0.4 |
| Passiva | [`berserker`](technical/BERSERKER-21.17.3-SOURCE-ADJACENT.md) | health perdido, bônus por floor percentual, attack speed com cap 5.0, damage modifier e stamina +6 |
| Passiva | [`stamina_pillager`](technical/STAMINA-PILLAGER-21.17.3-SOURCE-ADJACENT.md) | `KILL_ENTITY` restaura 30% do déficit de stamina com teto de +2 por callback |
| Passiva | [`death_harvest`](technical/DEATH-HARVEST-21.17.3-SOURCE-ADJACENT.md) | `KILL_ENTITY` weapon-innate gera orb de recuperação de gauge, NÃO projétil ofensivo independente |
| Defesa | [`guard`](technical/GUARD-21.17.3-SOURCE-ADJACENT.md) | `TAKE_DAMAGE_INCOME` frontal, stamina `penalty×impact`, `GUARD_BREAK` |
| Passiva | [`endurance`](technical/ENDURANCE-21.17.3-SOURCE-ADJACENT.md) | `TAKE_DAMAGE_PRE` com cooldown e `max(currentStamina×0.3,1.5)` de stamina para stun shield |
| Passiva | [`hypervitality`](technical/HYPERVITALITY-21.17.3-SOURCE-ADJACENT.md) | `CONSUME_SKILL` de weapon innate; fallback de stamina e consumo de stack |
| Passiva | [`adrenaline_fiend`](technical/ADRENALINE-FIEND-21.17.3-SOURCE-ADJACENT.md) | `KILL_ENTITY` redefine espera de stamina regen; modifiers **RAW LEGACY** |
| Passiva | [`catharsis`](technical/CATHARSIS-21.17.3-SOURCE-ADJACENT.md) | `ON_DODGE` aumenta gauge da weapon innate; modifiers **RAW LEGACY** |
| Passiva | [`emergency_escape`](technical/EMERGENCY-ESCAPE-21.17.3-SOURCE-ADJACENT.md) | `CAST_SKILL` e `CONSUME_SKILL` do Dodge; cooldown, stamina e state preflight |
| Passiva | [`bonebreaker`](technical/BONEBREAKER-21.17.3-SOURCE-ADJACENT.md) | `DELIVER_DAMAGE_PRE`: dano escalado por stack mesmo alvo; modifier **RAW LEGACY** |
| Passiva | [`vengeance`](technical/VENGEANCE-21.17.3-SOURCE-ADJACENT.md) | lock do agressor, bônus contextual e kill callback; modifiers **RAW LEGACY** |

**Verificações documentais:** 18 dossiês publicados e relidos; **91 âncoras source SHA-pinned em 26 arquivos Java distintos** (52 âncoras anteriores + **39** neste lote, todas com bounds/SHA e path checados), sem intervalo inválido. Vinte e um nomes de `skill_parameters/*.json` upstream consultados. **Prova binária adicional e separada:** [run 38981181742](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38981181742) SUCCESS no publisher JAR SHA-exato, com **21 JSONs empacotados, 25 classfiles e 11/11 self-tests**, expandindo o [run anterior 38979547368](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38979547368) de 13 JSON/17 classes/8 self-tests; o run inicial [38978906335](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38978906335) falhou por inspeção incorreta da classe externa `EpicFightEventHooks` e foi corrigido para as internas `$Entity` e `$Player`, mantendo os checks. Isso **não é QA visual, runtime, GameTest ou aceite físico do modpack montado**.

## Riscos prioritários e estratégia segura

1. **Discrepância de release delimitada:** o source pinado `Antikythera-Studios/epicfight@a78aa24b72e90a9d09f5fd61925e4369d117abaf` declara `mod=21.17.3`; o JAR exato do pack é `21.17.3.1`. Os **21 arquivos JSON inspecionados** tiveram os campos esperados comprovados no binário SHA-exato. Isso **não estabelece equivalência global do source nem comportamento dos métodos**. Para as oito skills novas, os campos empacotados e símbolos são exatos, mas a causalidade dos métodos ainda deriva do source adjacente. Os modifiers em `adrenaline_fiend`, `catharsis`, `bonebreaker`, `vengeance` usam schema legado `name/uuid`; **sem evidência de que `AttributeModifier.MAP_CODEC` os aceite/aplique**. Inspecionar controle e ordem real dos métodos no JAR antes de aprovar qualquer hook per-player.
2. **Evento observável ≠ setter seguro:** `Entity.MODIFY_ATTACK_SPEED` e `Player.CONSUME_SKILL` existem na fonte adjacente. Contrato de listener, fase preflight, sidedness, composição de modifiers e alteração dos recursos no JAR físico ainda condicionados.
3. **Dano guard residual:** `ImpactGuardSkill` pode cancelar incoming e invocar um novo `hurt` reduzido, com novos `DamageSource` tags. Numa bridge com Iron's, não duplicar dano/crit/Mastery nem classificar automaticamente `DamageTypes.MAGIC` como todo dano magical provider.
4. **World safety:** as três trident-innates pertencem a Epic Fight. Não emitir thunder, recall ou teleport AOE de novo por Black Arcana; categorizar cast e efeitos secundários pelo mesmo root com dedup.
5. **Mastery:** progressão do RPG sibling só por fato comprovado de acerto/defesa/cast, não packet client, FX ou tentativa cancelada. Não assumir que o progress provider terá setter nativo para stamina, hitbox, i-frames, raio de ataque ou `DamageType`.

## Falha independente do Black Arcana CI (não mascarar)

O HEAD anterior `4d42c695be4f5e365275562451b8398ed9a784be` executou `Black Arcana CI` run **38979815786**, `FAILURE` na etapa **Foundation GameTest server**: **108 GameTests / 1 required failed**, `blockedlandingskipsgapclosewithoutrollingbackdamage`: *target fixture must be visible through the server-level UUID index before Rift Blades lookup*. Build/test compilation passaram, mas não declarar CI geral verde. Esta prova Epic Fight é workflow distinto; nenhuma modificação de runtime Rift Blades, nem resolução da falha foi efetuada nesta tranche. Reproduzir e corrigir na trilha canônica apropriada antes de merge/Stage.

## Próximo bloco de auditoria

A partir do gate **21/21 JSON + 25/25 classfiles** exatos, auditar **as instruções, event phase, ordem causal e parsing dos quatro JSONs legados** (não apenas existência de símbolos), conferir parâmetros sob datapack carregado e avançar para as **22 skills core restantes**, especialmente outras passivas, identidade, movesets e weapon innates. Fazer fichas de eixos individuais apenas para valores provados; `NÃO_VERIFICADO` nos demais. Revisar overlap com PR #795 e preservar branch `#825` draft enquanto QA/aceite não estiver fechado.

**Ownership:** Black Arcana = runtime próprio, rituals/world safety/Arcane Danger; RPG Skill Tree = progression/Mastery/perks/gates; Epic Fight = combat skills, stamina, animations/movesets e settlement; Enshrouded = Shroud/exposure próprios. Sem transferir autoridade por similaridade temática. Stage 06.05 🟡 / Stage 09 físico pendente, sem promoção.
