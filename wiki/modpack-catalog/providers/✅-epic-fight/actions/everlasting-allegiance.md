# Everlasting Allegiance

- Provider: **Epic Fight** (`epicfight`)
- Version: `21.17.3.1`
- Exact physical/publisher SHA-1: `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`
- Skill id: `epicfight:everlasting_allegiance`
- Owner/reachability: `minecraft:trident` with vanilla **Loyalty**
- Semantic type: deliberate supernatural damaging trident recall
- State: `COUNTED_EXACT`

## Cinemática exata do tridente retornando (18/10/2026)

✅ [Java21 #39103337112](../EXACT-TRIDENT-RETURN-KINEMATICS-21.17.3.1.md) no classfile físico 21.17.3.1 confirmou o offset temporal `t=max(tickCount-returnTick-10,0)`, o deslocamento pedido em cada atualização `min(t²×0.0005+abs(t×0.05), min(10, distância até os olhos do proprietário))`, vetor normalizado apontando ao proprietário, zeragem de `setDeltaMovement` e `setPos` somando o vetor ao ponto atual. **Eixo para eventual perk:** velocidade/aceleração nominal está no `ThrownTridentPatch.tickEnd`; **não** é atributo comum do `AttackPhase`, nem API/hook público demonstrado. O teto calculado de 10 blocos por atualização não delimita distância máxima, target lock, tempo total ou velocidade observada. 8/8 autotestes, artifact #12127228567; Stage 09/client real ⚠️ PENDING, adapter ⛔.

## Dano do tridente retornando: patch e não fase de animação (18/10/2026)

✅ [Auditoria JAR exato #39102096383](../EXACT-TRIDENT-PHASE-OVERWRITE-RETURN-21.17.3.1.md): `EverlastingAllegiance.registerPropertiesToAnimation` consiste em `aload_0; areturn`, **sem escrita de AttackPhase nesse método**. O `ThrownTridentPatch.tickEnd` compilado cria, separadamente, `EpicFightDamageSources.trident` com `StunType.HOLD`, tag `WEAPON_INNATE`, `setBaseArmorNegation(30.0f)` e `ValueModifier.multiplier(1.4f)`. Em sua região de dano, utiliza input `8.0f`, `EnchantmentHelper.modifyDamage` e `Entity.hurt`; detecta entidades em `AABB.inflate(1,1,1)` — expansão **por eixo**, não raio circular ou alvo único. A configuração builder `ARMOR_NEGATION_MODIFIER.adder(30)` **não é a mesma operação** que `setBaseArmorNegation(30)` no source de retorno. Não inferir dano efetivo, alvo máximo, procs por tick ou ausência de i-frames. ⚠️ cliente real / ⛔ perks e Mastery.

## Gate posterior — handler instalado, ainda sem hit real (18/10/2026)

✅ [Preflight NeoForge Java21 #39098101364](../EXACT-ARMOR-MIXIN-LOADED-CLASS-PREFLIGHT-21.17.3.1.md) confirmou o handler de armadura do Epic Fight na classe `LivingEntity` transformada. Não foram executados recall do tridente, hit com `DAMAGE_MODIFIER.multiplier(1.4)` nem mitigação `ARMOR_NEGATION_MODIFIER.adder(30)` em entidade real. ⚠️ mundo/jogador/combat QA não executado; ⛔ perks/Mastery.

## Semântica delimitada do dano e armadura (18/10/2026)

✅ [Consumidores binários Java21 #39096586191](../EXACT-ATTACK-PHASE-CONSUMERS-21.17.3.1.md): `DAMAGE_MODIFIER.multiplier(1.4)` compõe o `ResultCalculator`, que avalia o acumulador segundo `((set ou base)+add)×multiply`; `calculateDamageAgainst` pode adicionar `extraDamages` depois. `ARMOR_NEGATION_MODIFIER.adder(30)` altera outro acumulador, utilizado no cálculo de absorção compilado de `MixinLivingEntity`. Portanto 1,4 é **input de fase**, não 1,4× de perda de HP demonstrada; 30 não é garantia de 30% de bypass final. Recall, quantidade de alvos/hits, dano real e `HOLD` aplicado seguem ⚠️; perks externas ⛔.

## Vínculo do registro comprovado — 18/10/2026

✅ [JAR publisher Java21 #39095049311](../EXACT-TRIDENT-REGISTRY-BOOTSTRAP-LINKAGE-21.17.3.1.md): `String everlasting_allegiance → InvokeDynamic #69 → DeferredRegister.register → EVERLASTING_ALLEGIANCE`; bootstrap `EpicFightSkills.lambda$static$43` (`EverlastingAllegiance`). Configuração `DAMAGE multiplier(1.4)` agora ligada ao ID exato por instruções compiladas; não significa HP damage medido nem recall executado.

## Prova posterior de propriedades compiladas (18/10/2026)

✅ [JAR 21.17.3.1, Java21 #39094435160](../EXACT-TRIDENT-ATTACK-PHASE-PROPERTIES-21.17.3.1.md): `EpicFightSkills.lambda$static$43` (`EverlastingAllegiance`) liga `ARMOR_NEGATION_MODIFIER adder(30)` e `DAMAGE_MODIFIER multiplier(1.4)` aos `Builder.addProperty`, além de `STUN_TYPE=HOLD` e `WEAPON_INNATE`. Há também `EXTRA_DAMAGE`, mas a composição inteira da expressão permanece fora deste gate. **Não significa 1,4× HP damage medido ou penetração efetiva de 30%.** ⛔ Sem alterações externas de recall/damage ou Mastery.

## Technical parameters for perks — exact JAR vs adjacent source

✅ **Exact publisher JAR 21.17.3.1:** `data/epicfight/skill_parameters/everlasting_allegiance.json` declares **`consumption=40.0`** (unit and actual debit not proven). [Java21 #39093719405](../EXACT-TRIDENT-CAUSAL-REFERENCES-21.17.3.1.md) verifies the compiled `checkExecuteCondition` reference to `THROWN_TRIDENT_ENTITY_ID` and a signed boundary, plus ordered references in `executeOnServer` to `recalledBySkill`, `playAnimationSynchronized`, `cancelOnServer`. This does **not** establish real trident return or damage/hit count.

✅ **Entradas numéricas e enums de fase agora compiladas no publisher 21.17.3.1, corroboradas pelo source adjacente 21.17.3:** `ARMOR_NEGATION_MODIFIER adder(30)`, `DAMAGE_MODIFIER multiplier(1.4)`, `STUN_TYPE HOLD`, `WEAPON_INNATE` tag and Sweeping Edge extra-damage object. [Source L363–371](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/registry/entries/EpicFightSkills.java#L363-L371). The 1.4 multiplier is an attack-phase input, **not** a measured final HP-damage multiplier.

**Perk axes:** target cap, hitbox/recall trajectory, projectile speed/scale, radius, range, return duration, real damage type, cooldown and cost actually settled are **NÃO VERIFICADO**. A future RPG Mastery bridge must associate all recall hits with the same provider-owned action without replaying recall or duplicating damage. ⛔ No adapter yet.

## Identity and selector

The exact `EpicFightMovesets.TRIDENT` innate selector resolves Everlasting Allegiance when Loyalty is present and neither the earlier Riptide nor Channeling selector branch is selected.

This closes owner/reachability through the exact vanilla-trident + enchantment surface.

## Exact provider settlement

The exact skill obtains the provider patch for the tracked thrown trident and invokes `recalledBySkill()`.

Exact thrown-trident behavior then performs Epic Fight's provider-owned return path and entity-hit settlement.

This differs semantically from vanilla Loyalty's automatic passive return because Epic Fight exposes an explicit player skill action and its own damaging recall lifecycle.

## Deduplication boundary

Repeated hits or movement during the returning trident lifecycle are settlement of the same recall root, not separate spell identities.

## Authority boundary

Epic Fight owns thrown-trident tracking, skill activation, return path, hit processing and resource settlement. Black Arcana must not trigger a second recall or duplicate damage.

Sources: `../EXACT-21.17.3.1-ARTIFACT-SKILL-AUDIT.md`, `../skills/SKILL-DISPOSITION-21.17.3.1.md`.

## Ficha individual para engenharia de perks — 21/10/2026

**Descrição para o jogador (resumo original):** Retorno ofensivo do tridente selecionado por Loyalty.

### Identidade, versão e origem por campo

- **ID exato:** `epicfight:everlasting_allegiance`; campo de registry `EVERLASTING_ALLEGIANCE`. Categoria/disposição: [registro completo](../skills/SKILL-DISPOSITION-21.17.3.1.md). `COUNTED_EXACT` somente para identidade; uma das três ações mágicas já contadas.
- **Runtime físico registrado:** Epic Fight `21.17.3.1`, Minecraft `1.21.1`, NeoForge do pack `21.1.250`; arquivo `epic-fight-21.17.3.1-mc1.21.1-neoforge.jar`.
- **JAR publisher conferido nesta rodada:** SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`; SHA-256 `8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526`; 8.578.288 bytes. A equivalência é ao hash registrado na modlist; não houve leitura da instalação ao vivo.
- **Modlist consultada:** `Gustavaopere/neoforge-rpg-skilltree@ed5b65b890767b406ce41127bcb793775263c7bd`, dossiê `✅-epic-fight v21.17.3.1.md`.
- **Dados empacotados:** `data/epicfight/skill_parameters/everlasting_allegiance.json`, lido diretamente do ZIP SHA-exato; config implantada NÃO VERIFICADA.
- **Implementação comparativa:** [`yesman.epicfight.skill.weaponinnate.EverlastingAllegiance`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/weaponinnate/EverlastingAllegiance.java); fonte `a78aa24b72e90a9d09f5fd61925e4369d117abaf` declara **21.17.3**, versão adjacente. Equivalência integral de métodos com **21.17.3.1 NÃO VERIFICADA**.
- **Registro na fonte comparativa:** [`EpicFightSkills.EVERLASTING_ALLEGIANCE`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/registry/entries/EpicFightSkills.java#L363); identidade binária tem prova própria, não deriva apenas dessa linha.
- **Estado técnico:** ⚠️ `EXACT_PACKAGED_PARAMETERS + SOURCE_ADJACENT_CAUSALITY`; ⛔ mutação externa por perks sem contrato validado; gameplay/Survival **PENDING**. Casos binários posteriores já registrados nesta ficha/dossiê prevalecem apenas nos campos que verificam.

### Parâmetros do JAR exato

| Campo | Valor e fronteira da evidência |
|---|---|
| `consumption` | `40.0` |

**Unidades:** `consumption` é um número no recurso do provider, não automaticamente mana, stamina ou segundos. Stacks são contagens. Unidades de tempo, percentuais e geometria só são atribuídas abaixo quando o consumidor correspondente foi auditado; dados RAW não medem o valor final do jogador.

### Código e pipeline causal

- [`public boolean checkExecuteCondition(SkillContainer container)`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/weaponinnate/EverlastingAllegiance.java#L38) — declaração na fonte **21.17.3 adjacente**.
- [`public boolean canExecute(SkillContainer container)`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/weaponinnate/EverlastingAllegiance.java#L43) — declaração na fonte **21.17.3 adjacente**.
- [`public void executeOnServer(SkillContainer container, CompoundTag arguments)`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/weaponinnate/EverlastingAllegiance.java#L48) — declaração na fonte **21.17.3 adjacente**.
- [`public void updateContainer(SkillContainer container)`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/weaponinnate/EverlastingAllegiance.java#L70) — declaração na fonte **21.17.3 adjacente**.
- [`public WeaponInnateSkill registerPropertiesToAnimation()`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/weaponinnate/EverlastingAllegiance.java#L91) — declaração na fonte **21.17.3 adjacente**.

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
