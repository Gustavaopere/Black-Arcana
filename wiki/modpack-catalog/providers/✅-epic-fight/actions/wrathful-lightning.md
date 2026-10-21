# Wrathful Lightning

- Provider: **Epic Fight** (`epicfight`)
- Version: `21.17.3.1`
- Exact physical/publisher SHA-1: `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`
- Skill id: `epicfight:wrathful_lighting`
- Owner/reachability: `minecraft:trident` with vanilla **Channeling**
- Semantic type: deliberate supernatural lightning invocation
- State: `COUNTED_EXACT`

## Precedência real de grupos no registro de fases (18/10/2026)

✅ [Auditoria de bytecode #39102096383](../EXACT-TRIDENT-PHASE-OVERWRITE-RETURN-21.17.3.1.md) no JAR 21.17.3.1: a mesma `AttackAnimation.Phase` recebe `properties[0]` e depois `properties[1]`, ambos via `Phase.addProperties→Map.put`. Na chave compartilhada `MAX_STRIKES_MODIFIER`, o `setter(3)` do grupo 1 **substitui** `setter(1)` do grupo 0 nesse caminho. **Dois grupos de builder NÃO significam duas fases com limites 1/3.** Nenhuma contagem real de vítimas ou aplicação de player foi mensurada. Corrigir qualquer perk que assuma “fase 1 = 1 alvo / fase 2 = 3 alvos”; hook externo continua ⛔.

## Gate posterior — handler instalado, ainda sem hit real (18/10/2026)

✅ [Preflight NeoForge Java21 #39098101364](../EXACT-ARMOR-MIXIN-LOADED-CLASS-PREFLIGHT-21.17.3.1.md) observou o handler de absorção de armadura Epic Fight na `LivingEntity` transformada com assinatura exata em servidor sem cliente. Isso resolve a dúvida da **presença do método** nesse ambiente isolado; **não prova que Wrathful Lightning o acionou, nem o dano/negation efetivo**. ⚠️ gameplay e integração; ⛔ perks externas.

## Semântica delimitada dos modifiers após o builder (18/10/2026)

✅ [Consumidores binários Java21 #39096586191](../EXACT-ATTACK-PHASE-CONSUMERS-21.17.3.1.md): o `DAMAGE_MODIFIER.setter(8)` entra na semântica de `ValueModifier.ResultCalculator` (define a referência do valor a ser combinado; não fixa 8 HP na vítima). Os `MAX_STRIKES_MODIFIER.setter(1)` / `setter(3)` são usados por `AttackAnimation.getMaxStrikes`, não provam 1/3 acertos reais em toda situação. `ARMOR_NEGATION_MODIFIER.adder(100)` abastece `EpicFightDamageSource.calculateArmorNegation`; o mixin compilado usa `min(A×0.01,1)` antes de `CombatRules` quando a fonte é elegível. **⚠️** Mixin aplicado, ataques multi-phase e dano real não homologados; ⛔ sem perk de dano/alcance externo.

## Vínculo do registro comprovado — 18/10/2026

✅ [JAR publisher Java21 #39095049311](../EXACT-TRIDENT-REGISTRY-BOOTSTRAP-LINKAGE-21.17.3.1.md) demonstrou a sequência `String wrathful_lighting → InvokeDynamic #67 → DeferredRegister.register → WRATHFUL_LIGHTING`; o bootstrap aponta para `EpicFightSkills.lambda$static$40` (`WrathfulLightingSkill`), método que recebe os coeficientes abaixo. A relação **ID → builder** está comprovada no binário exato. ⚠️ Dano final/cast real pendentes.

## Prova posterior de propriedades compiladas (18/10/2026)

✅ [JAR 21.17.3.1, Java21 #39094435160](../EXACT-TRIDENT-ATTACK-PHASE-PROPERTIES-21.17.3.1.md): no supplier `lambda$static$40` (`WrathfulLightingSkill`), o bytecode confirma, na ordem, `MAX_STRIKES_MODIFIER setter(1)` (primeiro grupo), `DAMAGE_MODIFIER setter(8.0)`, `MAX_STRIKES_MODIFIER setter(3)`, `ARMOR_NEGATION_MODIFIER adder(100)`, `STUN_TYPE=KNOCKDOWN` e `SOURCE_TAG=WEAPON_INNATE` no segundo grupo. São **entradas de AttackPhase**, não dano final nem limite de alvos medido. `EXTRA_DAMAGE` possui chave/builder presentes, mas a composição completa não foi dataflow-validada. Assim, os valores numéricos acima não dependem mais *somente* do source adjacente. ⛔ Hook/perk externo permanece bloqueado.

## Technical parameters for perks — exact JAR vs adjacent source

✅ **Exact publisher JAR 21.17.3.1:** packaged `data/epicfight/skill_parameters/wrathful_lighting.json` declares **`consumption=50.0`**, with resource unit/real debit unverified. [Java21 #39093719405](../EXACT-TRIDENT-CAUSAL-REFERENCES-21.17.3.1.md) additionally proves that `WrathfulLightingSkill.registerPropertiesToAnimation` has **two** compiled `addProperties` callsites within the method. This confirms the registration seam, not final damage or the number of real hits.

✅ **Valores agora confirmados também no classfile 21.17.3.1 (source 21.17.3 preservado como referência histórica):** first phase-property group contains `MAX_STRIKES_MODIFIER setter(1)`; second `DAMAGE_MODIFIER setter(8.0)`, `MAX_STRIKES_MODIFIER setter(3)`, `ARMOR_NEGATION_MODIFIER adder(100)`, `STUN_TYPE KNOCKDOWN` and `SOURCE_TAG WEAPON_INNATE`. These are exact-publisher compiled builder inputs, **not** guaranteed damage, armor bypass or runtime effects in 21.17.3.1. [Source L337–349](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/registry/entries/EpicFightSkills.java#L337-L349).

**Perk axes:** target type, range, radius/AOE, projectile dimensions/speed, damage type, cast ticks, duration, cooldown and realized cost are **NÃO VERIFICADO** by this class/JSON. ⛔ Do not inject additional thunder/damage or assign RPG Mastery from uncorrelated thunder callbacks. Epic Fight owns innate attack phases, animation, hits and charges; Black Arcana retains its own runtime.

## Identity and selector

The exact `EpicFightMovesets.TRIDENT` innate selector resolves Wrathful Lightning when the trident has Channeling, after the Riptide branch and before Loyalty.

This selector closes current catalog reachability without inventing an Epic Fight-owned item: the owner surface remains the vanilla trident, while the enchantment selects the provider-owned innate.

The registry id intentionally uses `lighting`; the player-facing identity is **Wrathful Lightning**.

## Exact provider settlement

The exact skill/animation seam attaches Epic Fight's server-side `SUMMON_THUNDER` event to this skill action.

That establishes one provider-owned supernatural lightning root. The spawned lightning/event processing, particles, animation, damage and downstream hit consequences are settlement details of the same action rather than additional magic identities.

## Fallback boundary

If Riptide is present, the exact trident selector resolves Tsunami instead. Wrathful Lightning is therefore not simultaneously selected by the same innate-selector pass.

## Authority boundary

Epic Fight remains authority for battle mode, skill activation, animation, innate gauge/resource state, event execution and damage settlement. Black Arcana must not replay thunder or charge a second resource/cooldown cost.

Sources: `../EXACT-21.17.3.1-ARTIFACT-SKILL-AUDIT.md`, `../skills/SKILL-DISPOSITION-21.17.3.1.md`.

## Ficha individual para engenharia de perks — 21/10/2026

**Descrição para o jogador (resumo original):** Invocação de raio selecionada por Channeling no tridente.

### Identidade, versão e origem por campo

- **ID exato:** `epicfight:wrathful_lighting`; campo de registry `WRATHFUL_LIGHTING`. Categoria/disposição: [registro completo](../skills/SKILL-DISPOSITION-21.17.3.1.md). `COUNTED_EXACT` somente para identidade; uma das três ações mágicas já contadas.
- **Runtime físico registrado:** Epic Fight `21.17.3.1`, Minecraft `1.21.1`, NeoForge do pack `21.1.250`; arquivo `epic-fight-21.17.3.1-mc1.21.1-neoforge.jar`.
- **JAR publisher conferido nesta rodada:** SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`; SHA-256 `8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526`; 8.578.288 bytes. A equivalência é ao hash registrado na modlist; não houve leitura da instalação ao vivo.
- **Modlist consultada:** `Gustavaopere/neoforge-rpg-skilltree@ed5b65b890767b406ce41127bcb793775263c7bd`, dossiê `✅-epic-fight v21.17.3.1.md`.
- **Dados empacotados:** `data/epicfight/skill_parameters/wrathful_lighting.json`, lido diretamente do ZIP SHA-exato; config implantada NÃO VERIFICADA.
- **Implementação comparativa:** [`yesman.epicfight.skill.weaponinnate.WrathfulLightingSkill`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/weaponinnate/WrathfulLightingSkill.java); fonte `a78aa24b72e90a9d09f5fd61925e4369d117abaf` declara **21.17.3**, versão adjacente. Equivalência integral de métodos com **21.17.3.1 NÃO VERIFICADA**.
- **Registro na fonte comparativa:** [`EpicFightSkills.WRATHFUL_LIGHTING`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/registry/entries/EpicFightSkills.java#L337); identidade binária tem prova própria, não deriva apenas dessa linha.
- **Estado técnico:** ⚠️ `EXACT_PACKAGED_PARAMETERS + SOURCE_ADJACENT_CAUSALITY`; ⛔ mutação externa por perks sem contrato validado; gameplay/Survival **PENDING**. Casos binários posteriores já registrados nesta ficha/dossiê prevalecem apenas nos campos que verificam.

### Parâmetros do JAR exato

| Campo | Valor e fronteira da evidência |
|---|---|
| `consumption` | `50.0` |

**Unidades:** `consumption` é um número no recurso do provider, não automaticamente mana, stamina ou segundos. Stacks são contagens. Unidades de tempo, percentuais e geometria só são atribuídas abaixo quando o consumidor correspondente foi auditado; dados RAW não medem o valor final do jogador.

### Código e pipeline causal

- [`public WeaponInnateSkill registerPropertiesToAnimation()`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/weaponinnate/WrathfulLightingSkill.java#L26) — declaração na fonte **21.17.3 adjacente**.

**Fluxo na fonte adjacente, salvo prova binária específica já vinculada:** Preservar a cadeia e as provas binárias já descritas nesta ficha; o dossiê conjunto de tridentes detalha seleção, builder, phases e efeitos derivados. Nunca executar um segundo raio, retorno ou débito por uma perk.

**Análise detalhada:** [dossiê causal de origem](../skills/technical/TRIDENT-INNATES-21.17.3-SOURCE-ADJACENT.md). A existência de classe/método/evento ou configuração não autoriza automaticamente escrita por perk.

### Matriz de campos para integração

| Eixo | Valor, consumidor e limite conhecido | Viabilidade atual |
|---|---|---|
| Dano / tipo | Valores de AttackPhase e limites são descritos nas provas binárias acima; não são dano final medido. | `CONTRATO_CONDICIONAL`; conversão de DamageType: `SEM_HOOK_SEGURO`. |
| Alcance / LOS | Selector nativo Riptide→Tsunami, Channeling→Wrathful, Loyalty→Everlasting; alcance efetivo NÃO VERIFICADO. | `NÃO_VERIFICADO` para extensão por jogador/perk. |
| Alvo / área / máximo de alvos | Selector nativo Riptide→Tsunami, Channeling→Wrathful, Loyalty→Everlasting; alcance efetivo NÃO VERIFICADO. Seleção, dano e colisão são eixos distintos. | `SEM_HOOK_SEGURO` para single→AOE/retarget externo. |
| Projétil / hitbox / escala / velocidade | NÃO VERIFICADO para a colisão terminal; classe da skill não substitui collider/animação/entidade downstream. | `SEM_HOOK_SEGURO` para aumentar hitbox/escala externa. |
| Tempo / duração / cast / cooldown | Timing/cooldown efetivos NÃO VERIFICADOS; consumption não é medida de tempo. | `CONFIG_NATIVE` apenas para campos JSON existentes; mutação per-player não homologada. |
| Custos / recursos / refunds | WEAPON_CHARGE na fonte base WeaponInnateSkill; consumo real/config carregada pendentes. | `CONTRATO_CONDICIONAL`; respeitar CONSUME_SKILL/cancelamento/consumer. |
| Status / summons / mundo | Efeitos e estados descritos no pipeline/dossiê; alcance de bloco, claims/PvP e rollback efetivos NÃO VERIFICADOS. | Sem replay externo de efeito; proteção do provider e WorldEffectPolicy do Black Arcana preservadas. |
| Scaling / caps / causalidade | Coeficientes/stacks/limites acima pertencem aos consumidores documentados; VFX, fase, proc ou callback não criam novo root. | `SEM_HOOK_SEGURO` para award/alteração sem correlação e deduplicação. |

### Autoridades e verificação restante

- **Epic Fight:** skill/combat state, animações, stamina/gauge, target/hits e settlement. Não cobrar recurso, gerar dano ou executar ação outra vez.
- **RPG Skill Tree:** progressão, atributos, Mastery e perks/gates por contrato real; evento preflight, input, FX e simples tentativa não comprovam resultado.
- **Black Arcana:** seu casting/rituais/domains, hazards/Strain/Corruption, persistência e world safety. **Enshrouded:** seu Shroud/exposure; afinidade temática não cria bridge.
- **QA pendente:** método/ABI/campos não certificados no JAR, configuração final, order/side/cancelamento, player conectado, equip/unequip, reload/relog/respawn, multiplayer, claims/PvP e provider no modpack. Stage 06.05/09 não avança por esta ficha.
- **Provas correlatas:** [parâmetros binários](../EXACT-BINARY-PERK-PARAMETERS-21.17.3.1.md), [checkpoint técnico com QA posterior](../skills/PERK-TECHNICAL-CHECKPOINT-2026-10-16.md), [índice individual](../skills/INDIVIDUAL-SKILL-CARDS-21.17.3.1.md).
