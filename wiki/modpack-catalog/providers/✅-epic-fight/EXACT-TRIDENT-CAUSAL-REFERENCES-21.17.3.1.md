# Epic Fight 21.17.3.1 — auditoria causal delimitada de três ações sobrenaturais do tridente

**Status: ✅ `EXACT_PUBLISHER_JSON_AND_COMPILED_METHOD_SEAMS` para 3/3 identidades; ⚠️ propriedades de ataque source-adjacent e execução física; ⛔ adapter de perks/Mastery.** A prova não cria novas magias nem homologa qualquer hook de runtime.

## Identidade do provider e proveniência

- Mod instalado no snapshot físico certificado: `epicfight` / `epic-fight-21.17.3.1-mc1.21.1-neoforge.jar`; posição #260; Minecraft 1.21.1, NeoForge; referência do publisher CurseForge projeto **405076** arquivo **8175609**.
- JAR publisher: **8.578.288 bytes**, SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`, SHA-256 `8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526`, ambos exigidos na etapa de download. O SHA-1 coincide com o registro histórico da modlist; nenhuma releitura do perfil local foi efetuada nesta rodada.
- [Workflow GitHub Actions #39093719405](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39093719405): job `exact_skill_parameters` **SUCCESS**, teste sintético novo **9/9** e resultado `PASS_BOUNDED_TRIDENT_CAUSAL_REFERENCES`, `deviations=[]`. O workflow reaproveita também os gates existentes de **42/42 JSONs de core**, **43/43 IDs/símbolos** e ordenação limitada de métodos.
- Artefato de evidência JSON **#12124190669**, nome `epicfight-211731-perk-binary-31b08f13a24e15e76bd9ad49b7d6cd64fd5c57d0` (compactado, 6.120 bytes, sem redistribuir o JAR).
- [Verificador read-only e fail-closed](../../../../docs/qa/epicfight_211731_trident_causal.py) e [workflow](../../../../.github/workflows/epicfight-211731-perk-binary.yml). O script exige ambos hashes, três JSONs, cinco classes e métodos com marcadores compilados em sequência. Sem bytecode de terceiros copiado ao repositório.

## Matriz por skill — identificadores e parâmetros úteis para perks

| Skill ID | Seletor no tridente vanilla | `consumption` em JSON exato | Evidência causal compilada | Dados ainda não homologados |
|---|---|---:|---|---|
| `epicfight:wrathful_lighting` | Channeling, **somente se** Riptide não venceu a precedência | `50.0` | Em `WrathfulLightingSkill.registerPropertiesToAnimation`, **duas invocações** `AttackAnimation.Phase.addProperties` no corpo do método; registro/selector com ID exato | Propriedades de fase numéricas, thunder causado, target, AOE, dano final, custo real/cooldown |
| `epicfight:tsunami` | Riptide, prioridade mais alta | `50.0` | `EpicFightSkills` possui lambda compilada com `isInWaterOrRain` e dois resultados; registro das animações `TSUNAMI` e `TSUNAMI_REINFORCED`; `ConditionalWeaponInnateSkill` seleciona e executa `playAnimationSynchronized` | Distância do dash, hitbox, armadura real, dano, efeitos de chuva sob jogador conectado |
| `epicfight:everlasting_allegiance` | Loyalty, se Riptide e Channeling não vencerem | `40.0` | `EverlastingAllegiance.checkExecuteCondition` lê `THROWN_TRIDENT_ENTITY_ID` e avalia limite assinado; `executeOnServer` referencia em ordem `recalledBySkill`, `playAnimationSynchronized`, `cancelOnServer` | Recolhimento real/entidade válida, targets, quantidade de hits, dano por recall, persistência, custo/cooldown |

**Valor `consumption`:** campo declarativo numérico no JSON exato do provider. Não é rotulado aqui como mana, stamina, ticks, segundos ou `WEAPON_CHARGE` efetivamente cobrada sem validação do settlement provider-native. O source adjacente 21.17.3 usa a categoria `Resource.WEAPON_CHARGE` para `ConditionalWeaponInnateSkill`; isso não equivale a debitar 50 unidades demonstradas no jogo 21.17.3.1.

## Propriedades de AttackPhase — atualização posterior (18/10/2026)

✅ [Java21 #39094435160](EXACT-TRIDENT-ATTACK-PHASE-PROPERTIES-21.17.3.1.md) demonstrou, no JAR publicado exato, as associações compiladas `AttackPhaseProperty` + float/enum + factory de `ValueModifier` + `Builder.addProperty` das três habilidades. As constantes `1/8/3/100` para Wrathful, `100` para Tsunami e `30/1.4` para Everlasting, mais `KNOCKDOWN/HOLD` e `WEAPON_INNATE`, agora têm prova **EXACT_PUBLISHER_COMPILED_SUPPLIER_PROPERTY_CALLSITES**. A narrativa abaixo documenta a proveniência histórica `SOURCE_ADJACENT`; ela não descreve mais a evidência máxima disponível para **esses campos específicos**. A prova não cobre formulação de dano final, runtime ou composição integral de `EXTRA_DAMAGE`.

## Proveniência histórica das propriedades (source adjacente)

A revisão upstream `Antikythera-Studios/epicfight@a78aa24b72e90a9d09f5fd61925e4369d117abaf` identifica os seguintes valores em `EpicFightSkills.java`, **versão 21.17.3**; as entradas numéricas específicas de builder abaixo foram posteriormente confirmadas no bytecode exato 21.17.3.1, conforme seção anterior:

- Wrathful Lightning: `MAX_STRIKES_MODIFIER setter(1)` no primeiro grupo; no segundo `DAMAGE_MODIFIER setter(8.0)`, `MAX_STRIKES_MODIFIER setter(3)`, `ARMOR_NEGATION_MODIFIER adder(100)`, `STUN_TYPE KNOCKDOWN` e tag `WEAPON_INNATE`.
- Tsunami: `ARMOR_NEGATION_MODIFIER adder(100)`, `STUN_TYPE KNOCKDOWN`, tag `WEAPON_INNATE`.
- Everlasting Allegiance: `ARMOR_NEGATION_MODIFIER adder(30)`, `DAMAGE_MODIFIER multiplier(1.4)`, `STUN_TYPE HOLD`, tag `WEAPON_INNATE`.

[Source primária com as três configurações, L337–371](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/registry/entries/EpicFightSkills.java#L337-L371). **Esses números não são resultados efetivos de dano, nem porcentagens de armor bypass, alcance ou raio.** O novo gate comprova o fluxo delimitado dos argumentos `AttackPhaseProperty` até `Builder.addProperty`; continua sem comprovar dano real, resultado de armadura, cadeia de `EXTRA_DAMAGE` ou ligação bootstrap completa.

## Eixos de perk, double-processing e authority

- **Target/alcance/AOE/hitbox:** nenhum dos três JSONs exatos declara alcance, AOE, velocidade, raio, número de alvos ou escala de projétil; inferir valores a partir da animação é indevido. Sem setter/hook seguro de Epic Fight 21.17.3.1 demonstrado, toda alteração externa fica **⛔ fail-closed**.
- **Tipo e valor de dano:** `DAMAGE_MODIFIER`, `ARMOR_NEGATION_MODIFIER`, `STUN_TYPE` e `SOURCE_TAG` são propriedades provider-native de fases (source adjacente). Não tratar `adder(100)` como 100% de dano/penetration nem como `DamageTypes.MAGIC` e não criar segundo `SpellDamageEvent`.
- **Cooldown/recursos:** `consumption` 50/50/40 comprovado no JSON; não existe no dossiê prova de preflight/cancelamento e transação consumida. Black Arcana não emite segunda cobrança nem concede refund.
- **Mastery:** uma intenção de innate pode produzir várias fases, raios, hits, recall e FX. Um bridge precisa de chave causal provider-owned e confirmação de execução/resultado para deduplicação; não gerar progressão por `SUMMON_THUNDER`, partículas ou callbacks isolados sem correlação.
- **Player QA:** observador Epic Fight no servidor isolado foi armado, porém registrou `connected_players=0`. `ServerPlayerPatch.initialized=true` com jogador real, skill equip/unequip e `AttributeInstance` continuam pendentes. Isso não é homologado pela presente prova.

Epic Fight conserva autoridade sobre selector, battle mode, skill, animações, gauge/stamina, projétil/dano e eventos. RPG Skill Tree apenas progressão/perks/gates via contratos reais. Black Arcana controla somente seu casting, hazards, custos próprios e `WorldEffectPolicy`, sem replay de thunder/recall.

## Contagem e gates

- ✅ **Epic Fight core 43/43** identidades dispostas, **42/42** JSONs empacotados, **3/3** ações sobrenaturais já contadas `COUNTED_EXACT` e **40** identidades core excluídas do numerador mágico mas relevantes à pesquisa de perks.
- ✅ Três fichas de ações ganham identidade, `consumption` físico e causalidade de método delimitada; **+0 raízes semânticas, +0 adapters**.
- ⚠️ Modpack completo, resposta de jogador real, parsing de addons, attack-phase dataflow, dano, cooldown, distância, escala, recursos e hooks permanecem em aberto; ⛔ não promover integração.
- Global: mínimo **1.857 objetos semânticos / 1.855 estritos**, denominador integral aberto, **—%**. Stage 06.05 🟡; Stage 09 físico PENDING. PR #825 draft sem merge.
