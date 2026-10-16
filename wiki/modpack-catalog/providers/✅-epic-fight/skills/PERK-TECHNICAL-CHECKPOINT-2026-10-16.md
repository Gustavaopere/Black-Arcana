# Epic Fight — checkpoint técnico de perks (16/10/2026)

**Mod instalado (autoridade física já documentada):** `epicfight` / `epic-fight-21.17.3.1-mc1.21.1-neoforge.jar` / SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`. Ver [auditoria do artefato exato](../EXACT-21.17.3.1-ARTIFACT-SKILL-AUDIT.md) e [disposition integral](SKILL-DISPOSITION-21.17.3.1.md). O registry core foi classificado em **43/43 IDs exatos**, com **3 ações sobrenaturais** na métrica de magia e **40 skills não mágicas** úteis para pesquisa de perks. Nenhuma nova identidade semântica acrescentada neste lote.

## Barras separadas por nível de evidência

- **Global — universo de magias/rituais de todos os mods:** piso anterior **1.856 objetos semânticos mínimos / 1.854 estritos**, denominador total do pack **aberto (—%)**. Skills marciais não aumentam esse numerador.
- **Epic Fight — identidade e categoria do core (exato 21.17.3.1):** **43/43 = 100%** do registro core enumerado/dispositionado, sendo 3 `COUNTED_EXACT` e 40 `EXCLUDED` (o segundo termo é apenas exclusão da métrica de magia, não do escopo de perks).
- **Epic Fight — profundidade causal para perks (source 21.17.3 adjacente):** 🟡 **27/43 = 62,79%** do core possui aprofundamento em **24 dossiês** (21 IDs anteriores e mais 6: Adaptive Skin, Meteor Slam, Revelation, Demolition Leap, Phantom Ascent, Grasping Spire). **16/43 ainda fora desta tranche técnica de profundidade**; não confundir com ausência de classificação individual do registry. Percentual = aprofundamento de fonte, não contrato ABI nem execução segura de perks.
- **Epic Fight — parâmetros JSON e símbolos no JAR físico 21.17.3.1:** ✅ **27/43 = 62,79%** do registry passou em gate **binário estático limitado**: [GitHub Actions #38982065994](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38982065994) **SUCCESS**, SHA-1/SHA-256 do publisher confirmados, **27/27 JSONs empacotados, 31/31 classes com símbolos javap, 15/15 testes sintéticos e zero desvios**. Cinco JSONs contêm `attribute_modifiers` legados `RAW_ONLY_NOT_PROVEN_LOADED` (`adaptive_skin`, `adrenaline_fiend`, `catharsis`, `bonebreaker`, `vengeance`); os **18 limiares por entidade de Revelation** são `PACKAGED_RAW_NOT_LOADED_REGISTRY`. [Evidência e limites](../EXACT-BINARY-PERK-PARAMETERS-21.17.3.1.md). **Não** confirma instruções/callbacks runtime, valores após datapack override, parsing, dano final, reembolsos, stamina aplicada, Mastery, serviço de addon ou QA real.
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
| Passiva | [`adaptive_skin`](technical/ADAPTIVE-SKIN-21.17.3-SOURCE-ADJACENT.md) | resistência por tags de dano, stack e 300 ticks; modifier de HP **RAW LEGACY** |
| Identidade | [`meteor_slam`](technical/METEOR-SLAM-21.17.3-SOURCE-ADJACENT.md) | ataque básico aéreo, raycast de 50 blocos, distância >6; proteção de queda condicional |
| Identidade | [`revelation`](technical/REVELATION-21.17.3-SOURCE-ADJACENT.md) | stacks por parry/block/dodge, `max_revelations` 18 entidades com limites RAW |
| Mover | [`demolition_leap`](technical/DEMOLITION-LEAP-21.17.3-SOURCE-ADJACENT.md) | charge 12/40/80 ticks, stamina incremental, efeito de solo sob auditoria |
| Mover | [`phantom_ascent`](technical/PHANTOM-ASCENT-21.17.3-SOURCE-ADJACENT.md) | salto extra local, jump_power, fall protection e validação do lado servidor pendente |
| Innate marcial | [`grasping_spire`](technical/GRASPING-SPIRE-21.17.3-SOURCE-ADJACENT.md) | duas animações; `LAST_HIT_COUNT×0.4` acrescenta **impact** na segunda fase, não dano base |

**Verificações documentais:** **24 dossiês** publicados e relidos, **115 âncoras Java SHA-pinned em 32 arquivos distintos** (91 anteriores + 24 novas), com SHA e limites de linha verificados, sem referência inválida. 27 `skill_parameters/*.json` consultados no upstream pinado. **Gate binário separado:** [#38982065994](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38982065994) SUCCESS para publisher SHA-exato, 27 JSONs, 31 classes, 15 self-tests, 0 desvios. A revisão 21.17.3 do código não foi declarada equivalente à 21.17.3.1 instrução-a-instrução; QA de servidor cliente e gameplay é pendente. A falha anterior do Black Arcana CI (`blockedlandingskipsgapclosewithoutrollingbackdamage`) é independente e não foi resolvida aqui.

## Riscos prioritários e estratégia segura

1. **Discrepância de release delimitada:** o source pinado `Antikythera-Studios/epicfight@a78aa24b72e90a9d09f5fd61925e4369d117abaf` declara `mod=21.17.3`; o JAR exato do pack é `21.17.3.1`. Os **27 arquivos JSON inspecionados** tiveram os campos esperados comprovados no binário SHA-exato. Isso **não estabelece equivalência global do source nem comportamento dos métodos**. Para as seis skills recém-adicionadas, os campos empacotados e símbolos são exatos, mas a causalidade dos métodos ainda deriva do source adjacente. Os modifiers em `adaptive_skin`, `adrenaline_fiend`, `catharsis`, `bonebreaker`, `vengeance` usam schema legado `name/uuid`; **sem evidência de que `AttributeModifier.MAP_CODEC` os aceite/aplique**. Inspecionar controle e ordem real dos métodos no JAR antes de aprovar qualquer hook per-player.
2. **Evento observável ≠ setter seguro:** `Entity.MODIFY_ATTACK_SPEED` e `Player.CONSUME_SKILL` existem na fonte adjacente. Contrato de listener, fase preflight, sidedness, composição de modifiers e alteração dos recursos no JAR físico ainda condicionados.
3. **Dano guard residual:** `ImpactGuardSkill` pode cancelar incoming e invocar um novo `hurt` reduzido, com novos `DamageSource` tags. Numa bridge com Iron's, não duplicar dano/crit/Mastery nem classificar automaticamente `DamageTypes.MAGIC` como todo dano magical provider.
4. **World safety:** as três trident-innates pertencem a Epic Fight. Não emitir thunder, recall ou teleport AOE de novo por Black Arcana; categorizar cast e efeitos secundários pelo mesmo root com dedup.
5. **Mastery:** progressão do RPG sibling só por fato comprovado de acerto/defesa/cast, não packet client, FX ou tentativa cancelada. Não assumir que o progress provider terá setter nativo para stamina, hitbox, i-frames, raio de ataque ou `DamageType`.

## Falha independente do Black Arcana CI (não mascarar)

O HEAD anterior `4d42c695be4f5e365275562451b8398ed9a784be` executou `Black Arcana CI` run **38979815786**, `FAILURE` na etapa **Foundation GameTest server**: **108 GameTests / 1 required failed**, `blockedlandingskipsgapclosewithoutrollingbackdamage`: *target fixture must be visible through the server-level UUID index before Rift Blades lookup*. Build/test compilation passaram, mas não declarar CI geral verde. Esta prova Epic Fight é workflow distinto; nenhuma modificação de runtime Rift Blades, nem resolução da falha foi efetuada nesta tranche. Reproduzir e corrigir na trilha canônica apropriada antes de merge/Stage.

## Próximo bloco de auditoria

Partir do gate **27/27 JSON + 31/31 classfiles**, auditar **fluxo bytecode instrucional**, eventos server/client, parser de attributes legados e os 18 IDs `max_revelations` sob datapack efetivamente carregado. Continuar o aprofundamento das **16 identidades remanescentes**, prioritariamente weapon innates e técnicas de combate. Validar protections/regras de world em Meteor Slam/Demolition Leap, input remoto em Phantom Ascent e dedup por hits de Grasping Spire. Não ativar perks/Mastery ou promover Stage sem contratos reais e QA.

**Ownership:** Black Arcana = runtime próprio, rituals/world safety/Arcane Danger; RPG Skill Tree = progression/Mastery/perks/gates; Epic Fight = combat skills, stamina, animations/movesets e settlement; Enshrouded = Shroud/exposure próprios. Sem transferir autoridade por similaridade temática. Stage 06.05 🟡 / Stage 09 físico pendente, sem promoção.
