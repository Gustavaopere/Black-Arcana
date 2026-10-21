# Tsunami

- Provider: **Epic Fight** (`epicfight`)
- Version: `21.17.3.1`
- Exact physical/publisher SHA-1: `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`
- Skill id: `epicfight:tsunami`
- Owner/reachability: `minecraft:trident` with vanilla **Riptide**
- Semantic type: deliberate supernatural tide/mobility attack
- State: `COUNTED_EXACT`

## Gate posterior — handler instalado, ainda sem hit real (18/10/2026)

✅ [Preflight NeoForge Java21 #39098101364](../EXACT-ARMOR-MIXIN-LOADED-CLASS-PREFLIGHT-21.17.3.1.md) observou no `LivingEntity` carregado exatamente um handler Epic Fight de absorção de armadura. **Não houve ataque Tsunami, ativação da variante água/chuva ou passagem de `EpicFightDamageSource` por esse método em runtime.** ⚠️ alcance/dano/AA e cliente pendentes; ⛔ adapter.

## Semântica delimitada de armadura e stun (18/10/2026)

✅ [Consumidores binários Java21 #39096586191](../EXACT-ATTACK-PHASE-CONSUMERS-21.17.3.1.md): `ARMOR_NEGATION_MODIFIER.adder(100)` alimenta o acumulador de negação de `EpicFightDamageSource`. O ramo compilado de `MixinLivingEntity` aplica `min(A×0.01,1)` e calcula no `CombatRules` apenas o dano restante, **se** a fonte satisfizer as guardas. `KNOCKDOWN` permanece `STUN_TYPE` de fase, não dano mágico automaticamente. Distância do avanço, área, alvos, efeito de água/chuva e dano líquido em jogo continuam **NÃO VERIFICADO**; sem adapter.

## Vínculo do registro comprovado — 18/10/2026

✅ [JAR publisher Java21 #39095049311](../EXACT-TRIDENT-REGISTRY-BOOTSTRAP-LINKAGE-21.17.3.1.md): `String tsunami → InvokeDynamic #68 → DeferredRegister.register → TSUNAMI`; `BootstrapMethods` associa ao método `EpicFightSkills.lambda$static$42` (`ConditionalWeaponInnateSkill`). **ID → builder** comprovado para as propriedades abaixo, sem provar alcance/dash ou hit em runtime.

## Prova posterior de propriedades compiladas (18/10/2026)

✅ [JAR 21.17.3.1, Java21 #39094435160](../EXACT-TRIDENT-ATTACK-PHASE-PROPERTIES-21.17.3.1.md): `EpicFightSkills.lambda$static$42` para `ConditionalWeaponInnateSkill` passa `ARMOR_NEGATION_MODIFIER adder(100)`, `STUN_TYPE=KNOCKDOWN`, tag `WEAPON_INNATE`, e vincula `setAnimations`. Prova da **entrada de fase**, não do impacto no HP, área, dash ou acerto. O registro exato normal/reforçado em água/chuva segue em auditoria separada. ⛔ Perks e mudança de targeting sem hook real.

## Technical parameters for perks — exact JAR vs adjacent source

✅ **Exact publisher JAR 21.17.3.1:** packaged `data/epicfight/skill_parameters/tsunami.json` declares **`consumption=50.0`**, unit/charge settlement unverified. The [bounded Java21 proof #39093719405](../EXACT-TRIDENT-CAUSAL-REFERENCES-21.17.3.1.md) confirms `isInWaterOrRain` with two compiled results in `EpicFightSkills` and both animations `TSUNAMI` / `TSUNAMI_REINFORCED`. `ConditionalWeaponInnateSkill` selects an animation and invokes `playAnimationSynchronized`. This establishes an environmental selection seam, not measured dash distance/damage.

✅ **Valores de builder confirmados no binário exato 21.17.3.1; source 21.17.3 é referência independente:** `ARMOR_NEGATION_MODIFIER adder(100)`, `STUN_TYPE KNOCKDOWN`, and tag `WEAPON_INNATE` in its configured attack phase. [Source L352–360](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/registry/entries/EpicFightSkills.java#L352-L360). The constant 100 is not proof of a 100% HP-damage bonus or full armor bypass.

**Perk axes:** target, range, dash length, AOE radius, hitbox, projectile velocity/scale, real damage type, cast duration, cooldown and settled cost remain **NÃO VERIFICADO**. A perk may not permanently apply the rain variant or duplicate water particles as casts; both animations belong to one Tsunami root. ⛔ External retarget/range manipulation without safe provider hook.

## Identity and selector

The exact `EpicFightMovesets.TRIDENT` innate selector resolves Tsunami when the trident has Riptide.

Because Riptide is the first selector branch, this path takes precedence over the Channeling and Loyalty branches in the same exact selector.

## Exact provider behavior

The exact artifact packages dedicated Tsunami animation resources and provider Tsunami particle paths. Exact control flow also chooses a strengthened action variant when the server player is in water or rain.

Water/rain state modifies this same Tsunami identity. It does not create a second semantic root.

## Deduplication boundary

Dash/movement, particles, animation, hits, damage and the strengthened environmental variant are parameters or consequences of the one provider-owned action.

## Authority boundary

Epic Fight remains authority for movement, resource state, animation, target/hit processing and all settlement. Black Arcana catalogs the action but must not duplicate it.

Sources: `../EXACT-21.17.3.1-ARTIFACT-SKILL-AUDIT.md`, `../skills/SKILL-DISPOSITION-21.17.3.1.md`.

## Ficha individual para engenharia de perks — 21/10/2026

**Descrição para o jogador (resumo original):** Ataque de tridente selecionado por Riptide, condicionado por água/chuva.

### Identidade, versão e origem por campo

- **ID exato:** `epicfight:tsunami`; campo de registry `TSUNAMI`. Categoria/disposição: [registro completo](../skills/SKILL-DISPOSITION-21.17.3.1.md). `COUNTED_EXACT` somente para identidade; uma das três ações mágicas já contadas.
- **Runtime físico registrado:** Epic Fight `21.17.3.1`, Minecraft `1.21.1`, NeoForge do pack `21.1.250`; arquivo `epic-fight-21.17.3.1-mc1.21.1-neoforge.jar`.
- **JAR publisher conferido nesta rodada:** SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`; SHA-256 `8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526`; 8.578.288 bytes. A equivalência é ao hash registrado na modlist; não houve leitura da instalação ao vivo.
- **Modlist consultada:** `Gustavaopere/neoforge-rpg-skilltree@ed5b65b890767b406ce41127bcb793775263c7bd`, dossiê `✅-epic-fight v21.17.3.1.md`.
- **Dados empacotados:** `data/epicfight/skill_parameters/tsunami.json`, lido diretamente do ZIP SHA-exato; config implantada NÃO VERIFICADA.
- **Implementação comparativa:** [`yesman.epicfight.skill.weaponinnate.ConditionalWeaponInnateSkill`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/weaponinnate/ConditionalWeaponInnateSkill.java); fonte `a78aa24b72e90a9d09f5fd61925e4369d117abaf` declara **21.17.3**, versão adjacente. Equivalência integral de métodos com **21.17.3.1 NÃO VERIFICADA**.
- **Registro na fonte comparativa:** [`EpicFightSkills.TSUNAMI`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/registry/entries/EpicFightSkills.java#L352); identidade binária tem prova própria, não deriva apenas dessa linha.
- **Estado técnico:** ⚠️ `EXACT_PACKAGED_PARAMETERS + SOURCE_ADJACENT_CAUSALITY`; ⛔ mutação externa por perks sem contrato validado; gameplay/Survival **PENDING**. Casos binários posteriores já registrados nesta ficha/dossiê prevalecem apenas nos campos que verificam.

### Parâmetros do JAR exato

| Campo | Valor e fronteira da evidência |
|---|---|
| `consumption` | `50.0` |

**Unidades:** `consumption` é um número no recurso do provider, não automaticamente mana, stamina ou segundos. Stacks são contagens. Unidades de tempo, percentuais e geometria só são atribuídas abaixo quando o consumidor correspondente foi auditado; dados RAW não medem o valor final do jogador.

### Código e pipeline causal

- [`public WeaponInnateSkill registerPropertiesToAnimation()`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/weaponinnate/ConditionalWeaponInnateSkill.java#L66) — declaração na fonte **21.17.3 adjacente**.
- [`public void executeOnServer(SkillContainer containter, CompoundTag arguments)`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/weaponinnate/ConditionalWeaponInnateSkill.java#L79) — declaração na fonte **21.17.3 adjacente**.

**Fluxo na fonte adjacente, salvo prova binária específica já vinculada:** Preservar a cadeia e as provas binárias já descritas nesta ficha; o dossiê conjunto de tridentes detalha seleção, builder, phases e efeitos derivados. Nunca executar um segundo raio, retorno ou débito por uma perk.

**Análise detalhada:** [dossiê causal de origem](../skills/technical/TRIDENT-INNATES-21.17.3-SOURCE-ADJACENT.md). A existência de classe/método/evento ou configuração não autoriza automaticamente escrita por perk.

**Contratos existentes no sibling:** [RPG Skill Tree `main@ed5b65b`](../skills/RPG-SIBLING-BOUNDARIES-ed5b65b.md) já contém modificação de custo via `CONSUME_SKILL`/`setAmount` quando o recurso do evento é `STAMINA`, além de observadores de dodge e damage para progressão. Pendências desta ficha referem-se a novos mutadores/validação por campo e não negam esse runtime já presente. Não duplicar desconto, débito ou Mastery.

### Matriz de campos para integração

| Eixo | Valor, consumidor e limite conhecido | Viabilidade atual |
|---|---|---|
| Dano / tipo | Valores de AttackPhase e limites são descritos nas provas binárias acima; não são dano final medido. | `CONTRATO_CONDICIONAL`; conversão de DamageType: `SEM_HOOK_SEGURO`. |
| Alcance / LOS | Selector nativo Riptide→Tsunami, Channeling→Wrathful, Loyalty→Everlasting; alcance efetivo NÃO VERIFICADO. | `NÃO_VERIFICADO` para extensão por jogador/perk. |
| Alvo / área / máximo de alvos | Selector nativo Riptide→Tsunami, Channeling→Wrathful, Loyalty→Everlasting; alcance efetivo NÃO VERIFICADO. Seleção, dano e colisão são eixos distintos. | `SEM_HOOK_SEGURO` para single→AOE/retarget externo. |
| Projétil / hitbox / escala / velocidade | NÃO VERIFICADO para a colisão terminal; classe da skill não substitui collider/animação/entidade downstream. | `SEM_HOOK_SEGURO` para aumentar hitbox/escala externa. |
| Tempo / duração / cast / cooldown | Timing/cooldown efetivos NÃO VERIFICADOS; consumption não é medida de tempo. | `CONFIG_NATIVE` apenas para campos JSON existentes; mutação per-player não homologada. |
| Custos / recursos / refunds | WEAPON_CHARGE na fonte base WeaponInnateSkill; consumo real/config carregada pendentes. | [`HOOK_VERIFICADO` no código sibling](../skills/RPG-SIBLING-BOUNDARIES-ed5b65b.md) somente para evento com `Resource.STAMINA`; demais recursos e composição final condicionados. Respeitar cancelamento/consumer. |
| Status / summons / mundo | Efeitos e estados descritos no pipeline/dossiê; alcance de bloco, claims/PvP e rollback efetivos NÃO VERIFICADOS. | Sem replay externo de efeito; proteção do provider e WorldEffectPolicy do Black Arcana preservadas. |
| Scaling / caps / causalidade | Coeficientes/stacks/limites acima pertencem aos consumidores documentados; VFX, fase, proc ou callback não criam novo root. | `SEM_HOOK_SEGURO` para award/alteração sem correlação e deduplicação. |

### Autoridades e verificação restante

- **Epic Fight:** skill/combat state, animações, stamina/gauge, target/hits e settlement. Não cobrar recurso, gerar dano ou executar ação outra vez.
- **RPG Skill Tree:** progressão, atributos, Mastery e perks/gates por contrato real; evento preflight, input, FX e simples tentativa não comprovam resultado.
- **Black Arcana:** seu casting/rituais/domains, hazards/Strain/Corruption, persistência e world safety. **Enshrouded:** seu Shroud/exposure; afinidade temática não cria bridge.
- **QA pendente:** método/ABI/campos não certificados no JAR, configuração final, order/side/cancelamento, player conectado, equip/unequip, reload/relog/respawn, multiplayer, claims/PvP e provider no modpack. Stage 06.05/09 não avança por esta ficha.
- **Provas correlatas:** [parâmetros binários](../EXACT-BINARY-PERK-PARAMETERS-21.17.3.1.md), [checkpoint técnico com QA posterior](../skills/PERK-TECHNICAL-CHECKPOINT-2026-10-16.md), [índice individual](../skills/INDIVIDUAL-SKILL-CARDS-21.17.3.1.md).
