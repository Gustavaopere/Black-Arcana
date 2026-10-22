# Epic Fight — 21.17.3.1

**Fichas individuais (21/10/2026):** [43/43 IDs core em caminhos dedicados](skills/INDIVIDUAL-SKILL-CARDS-21.17.3.1.md), incluindo 42 skills jogáveis e uma sentinela. Parâmetros do JAR exato separados da causalidade source-adjacent; hooks/QA continuam condicionados. [Progresso geral e por mod](../../meta/PROGRESSO-CATALOGO-ATUAL.md).

## Cinemática binária do retorno de Everlasting Allegiance — 18/10/2026

✅ [Java21 #39103337112](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39103337112) **SUCCESS**, JAR publisher exato SHA-1/SHA-256, novo verificador de sequência de movimento **8/8 autotestes**, `PASS_EXACT_TRIDENT_RETURN_KINEMATICS_BOUNDED` e JSON artefato **12127228567**. [Dossiê de movimento do tridente](EXACT-TRIDENT-RETURN-KINEMATICS-21.17.3.1.md): `t=max(tickCount-returnTick-10,0)`; deslocamento solicitado `min(t²*0.0005+abs(t*0.05), min(10, distância aos olhos do proprietário))` na direção normalizada; `setDeltaMovement(0,0,0)` e `setPos`. **O teto de 10 é por execução do movimento, não limite de alcance, e o offset 10 não é cooldown nem duração garantida.** Sem player/anim real, hook de perks, medição de dano/colisão ou adapter autorizado; +0 spells.


## Wrathful: sobreposição por mapa; Everlasting: dano no patch do projétil (18/10/2026)

✅ [Java21 #39102096383](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39102096383) **SUCCESS** no JAR exato SHA-1/SHA-256 e `PASS_BOUNDED_TRIDENT_PHASE_PRECEDENCE_AND_RETURN_PATH` (9/9 autotestes do gate original; artefato **12127086820**). [Dossiê de precedência e retorno](EXACT-TRIDENT-PHASE-OVERWRITE-RETURN-21.17.3.1.md): `WrathfulLightingSkill.registerPropertiesToAnimation` aplica grupos 0 e 1 **à mesma Phase**, com `Phase.addProperties→Map.put`: o segundo `MAX_STRIKES.setter(3)` sobrescreve o primeiro `setter(1)` nesse caminho de registro. `EverlastingAllegiance.registerPropertiesToAnimation` é um retorno direto, enquanto `ThrownTridentPatch.tickEnd` constrói `EpicFightDamageSource.trident` próprio com `HOLD`, `WEAPON_INNATE`, `baseArmorNegation=30`, `damage multiplier=1.4`, input `8.0f` e varredura de AABB expandida **1 por eixo**. Não extrapolar para 3 alvos/raio esférico/dano final ou player QA. +0 roots, +0 adapters.


## Nova instrumentação de dano provider-native para Stage 09 — 18/10/2026

✅ [QA servidor sem cliente #39098965924](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39098965924) **SUCCESS**, Java21/NeoForge 21.1.250/Epic Fight 21.17.3.1 publisher SHA-1/SHA-256; observer separado da produção compilado, servidor iniciado e `AWAIT_NATIVE_PLAYER_ATTACK` armado sem falsa amostra de jogador. JSON artefato **12126200760**. [Contrato e matriz de aceitação](NATIVE-PLAYER-DAMAGE-TELEMETRY-QA-21.17.3.1.md): `LivingIncomingDamageEvent` e `LivingDamageEvent.Post` são observados passivamente **somente** com fonte `EpicFightDamageSource` e atacante `ServerPlayer` conectado; coletam dano original/efetivo e reductions ARMOR/ABSORPTION, sem IDs, no máximo 12 samples/fase. **Não há correlação causal automática entre os eventos, ataque real observado nem chamada de handler comprovada**. ⚠️ Stage09 client/combate; ⛔ mudanças externas e Mastery. +0 magias/adapters.


## Mixin de armadura observado na classe transformada — 18/10/2026

✅ [QA servidor dedicado #39098101364](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39098101364) **SUCCESS**, Java21/NeoForge 21.1.250 e publisher Epic Fight 21.17.3.1 SHA-1/SHA-256 fixados. [Dossiê de preflight runtime](EXACT-ARMOR-MIXIN-LOADED-CLASS-PREFLIGHT-21.17.3.1.md): observer QA opt-in identificou **exatamente um** handler de `epicfight$getDamageAfterArmorAbsorb` com assinatura `DamageSource, float, CallbackInfoReturnable` no `LivingEntity.class` carregado pelo servidor (`TRANSFORMED_HANDLER_PRESENT`). Compilação e isolamento QA/produção confirmados, JSON artefato **12125471763**. A primeira execução #39097863144 falhou por regex de verificação duplicadamente escapado; os controles positivo e negativo passaram após correção. **Ainda nenhum handler invocado por dano real, jogador conectado, dano final ou perk/Mastery validada**; ⚠️ Stage 09 e ⛔ adapters permanecem.


## Consumidores compilados de dano, strikes e armadura — 18/10/2026

✅ [Java21 #39096586191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39096586191) **SUCCESS**, SHA-1/SHA-256 publisher exatos, 8/8 novos autotestes e `PASS_BOUNDED_EPICFIGHT_ATTACK_PHASE_CONSUMERS` (JSON #12124059084). [Dossiê de consumo real de propriedades nos métodos compilados](EXACT-ATTACK-PHASE-CONSUMERS-21.17.3.1.md): `ValueModifier.ResultCalculator` recebe `Setter/Adder/Multiplier` (ordem set → soma → multiplica); `AttackAnimation` busca propriedades da fase; `EpicFightDamageSource` mantém acumuladores distintos e processa `extraDamages` após o modificador; o bytecode de `MixinLivingEntity` contempla `calculateArmorNegation*0.01`, `Math.min(...,1)` e `CombatRules.getDamageAfterAbsorb`. **Métodos presentes não provam Mixin aplicado, player/hit/HP real, proc de Mastery ou hook seguro.** 43/43 skills core e 3/3 tridente intactas, +0 identidades.


## Fechamento de linkage compilado das três habilidades (18/10/2026)

✅ [Java21 #39095049311](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39095049311) **SUCCESS**, publisher SHA-1/SHA-256 verificados, 10/10 autotestes de `<clinit>` + `BootstrapMethods`, `PASS_BOUNDED_TRIDENT_REGISTRY_BOOTSTRAP_LINKAGE`. [Dossiê do vínculo ID → supplier → propriedades](EXACT-TRIDENT-REGISTRY-BOOTSTRAP-LINKAGE-21.17.3.1.md): `wrathful_lighting→InvokeDynamic #67→lambda$static$40`, `tsunami→#68→$42`, `everlasting_allegiance→#69→$43`, com `DeferredRegister.register` e holders corretos. Essa prova completa a associação compilada das **configurações de AttackPhase aos IDs exatos**, sem demonstrar execução da skill, dano final, custo real, target/range, callback para perk ou jogador conectado. +0 magias e +0 adapters.


## Novo gate exato de AttackPhase — 18/10/2026

✅ [Java21 #39094435160](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39094435160) **SUCCESS**, SHA-1/SHA-256 verificados, 11/11 autotestes adicionais e `PASS_BOUNDED_TRIDENT_ATTACK_PHASE_PROPERTIES`, artifact JSON **12124346492**. [Dossiê exato do JAR](EXACT-TRIDENT-ATTACK-PHASE-PROPERTIES-21.17.3.1.md): `EpicFightSkills.lambda$static$40/42/43` possui as propriedades de fases, constantes float, `ValueModifier.setter/adder/multiplier` e `Builder.addProperty` que correspondem a Wrathful Lightning/Tsunami/Everlasting Allegiance. A prova agora cobre os *argumentos de construção* exatos para `MAX_STRIKES`, `DAMAGE`, `ARMOR_NEGATION`, `STUN_TYPE` e `WEAPON_INNATE`. **Não prova resultado final de combate, linkage de bootstrap completo, custo realizado, escala de projétil, target/range, nem player/adapter.** 3/3 magic actions, +0 roots.


## Three supernatural trident actions — exact compiled causal proof (18/10/2026)

✅ [Java21 #39093719405](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39093719405) **SUCCESS** on publisher SHA-1/SHA-256 exact, **9/9** synthetic fail-closed checks and `PASS_BOUNDED_TRIDENT_CAUSAL_REFERENCES`; artifact JSON **12124190669**. [Dossiê causal](EXACT-TRIDENT-CAUSAL-REFERENCES-21.17.3.1.md): 3/3 JSONs exact-current `consumption` **50 / 50 / 40** (unit not presumed); trident selector Riptide → Channeling → Loyalty; Tsunami water/rain two animations; Wrathful two phase property callsites; Everlasting condition on thrown-trident ID and server recall/animation/cancel references. Este checkpoint #39093719405 foi anterior ao novo gate #39094435160: nele as propriedades ainda eram source-adjacent; **os valores de builder agora têm confirmação binária exata**, documentada na seção superior, sem prova de dano final. No gameplay or hook authorization, +0 spells. Epic Fight 43/43 IDs, 42/42 packaged JSONs, 3 magical roots / 40 nonmagical identities usable for perk research; ⛔ Mastery/adapters without real player provider QA.


## Stage 09 — observer de jogador conectado armado, sem cliente (17/10/2026)

✅ [QA #39027854991](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39027854991) **SUCCESS**, artifact **12099685054**: compilação Java21 / NeoForge físico **21.1.250** do observer read-only de `PlayerLoggedInEvent`, `PlayerRespawnEvent`, logout e server tick. O Epic Fight exato `21.17.3.1` foi carregado, mas **nenhum jogador conectou-se**; o run comprovou somente `AWAIT_CONNECTED_PLAYER`, `connected_players=0`, `has_proven_join_patch=false`, `equip_invoked=false`, `attribute_mutated=false`. [Protocolo, fonte e limites](EXACT-CONNECTED-PLAYER-LIFECYCLE-OBSERVER-PREFLIGHT-21.17.3.1.md).

⚠️ **Não promover** lifecycle de `ServerPlayerPatch` com cliente, `SkillContainer.setSkill`, `AttributeInstance` aplicado nem Stage 09 com base no no-client smoke. É obrigatório observar um `ServerPlayer` real com `initialized=true` após login/respawn, sem `FakePlayer` ou `onJoinWorld` forçado. ⛔ Integração perks/Mastery ainda sem contrato físico seguro.

## Gate de elegibilidade do PlayerPatch — 17/10/2026

✅ [QA físico #39003200555](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39003200555) **SUCCESS**, com JSON artifact **12090146205**: servidor NeoForge 21.1.250 com Epic Fight exato 21.17.3.1 e FakePlayer do NeoForge. A attachment provider-native criou **ServerPlayerPatch** para o FakePlayer, com max-health base **20.0**, mas **EntityPatch.initialized=false**. Status **PATCH_ATTACHED_UNINITIALIZED_REQUIRES_JOIN_LIFECYCLE**. [Dossiê e próximo gate de jogador real](EXACT-FAKE-PLAYER-PATCH-LIFECYCLE-ELIGIBILITY-21.17.3.1.md).

⛔ Portanto não se chamou SkillContainer.setSkill, onInitiate ou onRemoved artificialmente. A prova anterior **0→8→0** em cinco skills diz respeito exclusivamente ao mapa de modifiers de Skill.attributes; AttributeInstance de jogador conectado, ciclo equip/unequip, persistência, sincronização e integração de perks permanecem **pendentes**, sem promoção de Stage.

## Cobertura causal ampliada: oito modifiers e cinco skills no provider carregado (17/10/2026)

✅ [CI de oito modificadores #39001996512](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39001996512) **SUCCESS**, com JSON de QA efetivamente publicado como artefato **12089431494**. Servidor Java21 / NeoForge físico **21.1.250**, JAR do Epic Fight **21.17.3.1** verificado por dois hashes. Cinco datapacks de substituição temporária escritos **somente no runner**, usando campos modernos e oito IDs QA distintos: `adaptive_skin 0→1→0`, `adrenaline_fiend 0→2→0`, `catharsis 0→2→0`, `bonebreaker 0→1→0`, `vengeance 0→2→0`; controles modernos `swordmaster/forbidden_strength/technician` estáveis **2/2/1** em três fases. Inclui `epicfight:stamina_regen`, aceito na coleção carregada. [Relatório e escopo](EXACT-ALL-FIVE-LEGACY-MODIFIER-OVERRIDE-RESTORE-21.17.3.1.md).

⚠️ Evidência de **mapa do provider**, não de atributos efetivos de jogador; sem `SkillContainer.setSkill`, equip/unequip, client ou modpack completo. Nenhum artefato QA foi transferido à produção; ⛔ hooks de perks e Mastery ainda sem contrato homologado. Core catalogado ✅ 43/43, **+0** magia.

## Gate causal de datapack original e restauração — 17/10/2026

✅ [Actions #38999302329](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38999302329) **SUCCESS**: em servidor NeoForge 21.1.250 com Epic Fight físico 21.17.3.1, o datapack descartável original de QA substituiu `data/epicfight/skill_parameters/adaptive_skin.json` por um modifier moderno `id=black_arcana_epicfight_qa:adaptive_skin_control`, `operation=add_value`. Após reload, a coleção `Skill.attributes` de `adaptive_skin` mudou **0→1**; após remover o datapack e novo reload, voltou **1→0**. As outras sete skills controladas permaneceram **0/0/0/0 (legadas)** e **2/2/1 (modernas)**. [Prova de três fases e limites](EXACT-TEMPORARY-DATAPACK-OVERRIDE-RESTORE-21.17.3.1.md).

⚠️ Prova causal **somente do mapa carregado da skill** no servidor isolado. Não prova `AttributeInstance` aplicado no jogador, equip/unequip ou modpack completo de 587 entradas. Nenhum datapack de override de QA foi incluído no produto; nenhum adapter de perks/Mastery foi implementado. O gate anterior de reload sem override permanece válido como evidência histórica separada.

## Gate de reload real no provider carregado — 17/10/2026

✅ [CI #38998283536](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38998283536), **SUCCESS**: no servidor dedicado Java21 / NeoForge **21.1.250**, com Epic Fight físico 21.17.3.1 carregado, o QA registrou o mapa `Skill.attributes` das **cinco skills legadas (0/0/0/0/0)** e dos **três controles modernos (2/2/1)**, acionou o **reload real de recursos do MinecraftServer** e reobservou as **oito identidades** após a conclusão do future, sem desvios. [Dossiê de reload e limites](EXACT-SERVER-RELOAD-ATTRIBUTE-CARDINALITY-21.17.3.1.md).

⚠️ Não houve override de datapack nem equip/unequip em jogador, nem modpack com todos os addons. Resultado limitado à **estabilidade de cardinalidade após reload**, não à aplicação de atributos em `AttributeInstance`, execução de `SkillReloadListener.apply` com nova entrada, nem hook seguro de perks/Mastery.

## Checkpoint mais recente — Epic Fight carregado no servidor exato (16/10/2026)

- ✅ [Provider-loaded QA #38990309407](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38990309407) **SUCCESS**: JAR 21.17.3.1 SHA-fixado iniciado como mod em servidor NeoForge **21.1.250**. Cinco skills com JSON `name/uuid` legados apresentaram **0/0/0/0/0** entradas em `Skill.attributes`; três controles positivos de JSONs modernos (`swordmaster`, `forbidden_strength`, `technician`) apresentaram **2/2/1**, provando carregamento seletivo em vez de loader inteiramente vazio. [Dossiê provider-loaded e limites](EXACT-LOADED-REGISTRY-LEGACY-ATTRIBUTE-PROOF-21.17.3.1.md).
- ⚠️ **Status atualizado:** `PROVIDER_LOADED_REGISTRY_EMPTY_ISOLATED_SERVER` para **cinco atributos de skill**, no servidor isolado testado; **não** `PLAYER_ATTRIBUTE_INSTANCE_VALIDATED`, não modpack completo, não equip/unequip, não datapack reload. Todas as observações anteriores `RAW_ONLY_NOT_PROVEN_LOADED` abaixo são **marcos históricos dos gates anteriores**, superados **somente** quanto à existência/contagem da coleção no provider carregado, e **não** quanto à aplicação em jogador. ⛔ Integração de perks/Mastery sem hook homologado.

## Perks — cobertura integral do registro core (16/10/2026)

- **Identidades exatas do registro:** ✅ **43/43** classificadas no JAR `21.17.3.1`, três ações sobrenaturais `COUNTED_EXACT` já contadas no catálogo mágico e quarenta `EXCLUDED` do numerador mágico. **Nenhuma magia nova neste lote.**
- **Dossiês técnico-causais source-adjacent:** 🟡 **43/43 = 100% das identidades core cobertas em 28 dossiês**, baseados no upstream `21.17.3` pinado. Isso é cobertura de pesquisa, **não equivalência de bytecode ou perks implementadas**.
- **Prova física estática exata:** ✅ [GitHub Actions #38982933095](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38982933095) SUCCESS — **42/42 JSONs empacotados**, mais sentinel `epicfight:empty` não configurado, **43/43 literais de IDs de registry compilados**, **43 classfiles com símbolos exigidos**, **21/21 self-tests** e zero desvios, hashes SHA-1/SHA-256 correspondentes ao JAR físico. [Relatório e limites](EXACT-BINARY-PERK-PARAMETERS-21.17.3.1.md). O sentinel `empty` não é cast nem objeto mágico extra.
- **Novo gate instrucional limitado (JAR exato):** ✅ [Actions #38983851582](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38983851582) confirmou **5/5 métodos** quanto à ordem de referências `javap`, **8/8 testes sintéticos específicos**, sem desvio, após checagem SHA. [Relatório da ordem de invocações](EXACT-BYTECODE-INVOCATION-ORDER-21.17.3.1.md). **Não é CFG, execução de branch, parsing de NBT ou contrato seguro para perks.**
- **Ampliação do gate compilado:** ✅ [Java21 #38985378708](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38985378708), **7/7 métodos** com ordem de invocações limitada, incluindo agora o ciclo `Skill.onInitiate`/`onRemoved`, **10/10 self-tests**, zero desvio. [Relatório de métodos](EXACT-BYTECODE-INVOCATION-ORDER-21.17.3.1.md). Ordem textual não demonstra branch efetivo nem modifier carregado.
- **Atributos legados — teste real do codec Minecraft:** ⚠️ [CI #38984538266](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38984538266) **SUCCESS**, incluindo os 3 asserts `AttributeModifier.MAP_CODEC`/`NbtOps`: os dois formatos representativos `name/uuid/addition` e `name/uuid/multiply_total` não decodificam; o controle moderno `id/add_value` decodifica. Cinco skills (`adaptive_skin`, `adrenaline_fiend`, `catharsis`, `bonebreaker`, `vengeance`) seguem **`RAW_ONLY_NOT_PROVEN_LOADED`** na execução Epic Fight. [Dossiê do codec e limites](EXACT-LEGACY-ATTRIBUTE-CODEC-REVIEW-21.17.3.1.md). A CI testou Minecraft 1.21.1 com NeoForge 21.1.248, não a montagem real do modpack NeoForge 21.1.250. Os 18 entity limits de Revelation seguem apenas RAW.
- **JAR publisher real + NeoForge físico 21.1.250, sem provider carregado:** ✅ [Actions #38987519161](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38987519161) **SUCCESS** — publisher SHA-1/SHA-256 verificados, **5/5 JSONs exatos** lidos diretamente do JAR, **8/8 linhas legadas** submetidas ao codec Minecraft, controles modernos individuais e de lista aceitos, **2/2 testes Java realmente executados**, zero desvios. [Dossiê com resultado e gate ainda faltante](EXACT-PUBLISHER-JSON-PACK-NEOFORGE-CODEC-21.17.3.1.md). O Epic Fight foi fonte de arquivos ZIP e **não** mod inicializado: modifiers seguem ⚠️ `RAW_ONLY_NOT_PROVEN_LOADED` na engine.
- **Oito registros de modifiers legados, não só exemplos:** ⚠️ [Black Arcana CI #38985688067](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38985688067) mostrou **`Unit tests` e build `SUCCESS`** para a ampliação Java: **8/8 rows sem parse completo**, incompatibilidades independentes de `id` e `operation`, controles positivos individuais e de lista, listas legada/mista sem resultado completo. Workflow global **cancelado** antes de GameTests devido a commit posterior; não declarar CI geral verde a partir dele. [Detalhamento e bloqueios](EXACT-LEGACY-ATTRIBUTE-CODEC-REVIEW-21.17.3.1.md). O Epic Fight físico ainda não foi carregado nesse gate.

[Checkpoint completo das 43 identidades](skills/PERK-TECHNICAL-CHECKPOINT-2026-10-16.md) · [Empty, Combo e Wakeup](skills/technical/CORE-SENTINEL-COMBO-WAKEUP-21.17.3-SOURCE-ADJACENT.md) · [Innates marciais simples](skills/technical/SIMPLE-WEAPON-INNATES-21.17.3-SOURCE-ADJACENT.md) · [Innates complexas](skills/technical/COMPLEX-WEAPON-INNATES-21.17.3-SOURCE-ADJACENT.md) · [Battojutsu Passive](skills/technical/BATTOJUTSU-PASSIVE-21.17.3-SOURCE-ADJACENT.md).

**Black Arcana permanece authority do seu casting e WorldEffectPolicy.** Epic Fight mantém skills, weapon gauge/stamina, fases de ataque, dano e animações. RPG Skill Tree fornece progressão/Mastery/perks/gates somente por contratos reais. Falta análise **completa** de bytecode/controle de fluxo, provider-loaded QA, parser real para schema legado e eventual interface segura de progresso. A ordem de invocações foi verificada somente em cinco métodos. Sem adapter implementado, Stage 06.05 🟡, Stage 09 físico pendente, PR draft, sem merge.

**Global mágico inalterado:** piso 1.856 objetos semânticos identificados / 1.854 estritos; denominador global desconhecido, +0 magia.
Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / 43-SKILL REGISTRY FULLY DISPOSITIONED / 3 COUNTED_EXACT SUPERNATURAL TRIDENT INNATES / RUNTIME QA SEPARATE`

## Current physical identity

Current sibling physical authority identifies:

- physical row: **#260**;
- JAR: `epic-fight-21.17.3.1-mc1.21.1-neoforge.jar`;
- mod id: `epicfight`;
- runtime: `21.17.3.1`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`.

Epic Fight is primarily the pack's action-RPG combat framework. It owns battle mode, stamina, stun, weapon capabilities, movesets, skills and special attacks. Only a narrow subset of its exact core skill registry qualifies for the Black Arcana semantic-magic metric.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#562** audits CurseForge project/file `405076 / 8175609` and hard-gates the publisher artifact against the physical pack fingerprint.

Final exact evidence checkpoint:

- audit HEAD: `3b8e5ccd58e72bc99fdeeaac84b10d8f25538ca0`;
- exact-artifact run: `37170317148` — **SUCCESS**;
- evidence artifact: `11291375884`;
- evidence digest: `sha256:88fbb713615e5f996a40c609facb03792df812c4a762e47247bb3e1d6466821b`;
- publisher SHA-1: `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`;
- publisher SHA-256: `8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526`;
- bytes: `8,578,288`.

The publisher SHA-1 exactly equals the physical sibling SHA-1.

The exact artifact contains **3,213 archive entries / 1,530 classes / 1,683 non-class resources / 117 skill-like classes / 280 skill-like resources / 174 provider-data paths**.

See [`EXACT-21.17.3.1-ARTIFACT-SKILL-AUDIT.md`](EXACT-21.17.3.1-ARTIFACT-SKILL-AUDIT.md).

## Exact core skill registry — 43 IDs

Direct exact-artifact inspection closes **43 unique Epic Fight core skill IDs**:

- 2 technical/core skill slots;
- 3 dodge/wakeup movement skills;
- 3 guard skills;
- 14 passive skills;
- 2 identity skills;
- 2 mover skills;
- 16 weapon-innate skills;
- 1 weapon-passive skill.

All 43 IDs are dispositioned in [`skills/SKILL-DISPOSITION-21.17.3.1.md`](skills/SKILL-DISPOSITION-21.17.3.1.md).

## Semantic-magic result — 3 exact roots

Epic Fight 21.17.3.1 contributes exactly **3 provider-owned supernatural player-action identities** under the current semantic metric:

1. `epicfight:wrathful_lighting` — **Wrathful Lightning**;
2. `epicfight:tsunami` — **Tsunami**;
3. `epicfight:everlasting_allegiance` — **Everlasting Allegiance**.

All three are weapon-innate actions on the provider's exact trident moveset and are selected by normal vanilla trident enchantments:

- **Riptide** -> `epicfight:tsunami`;
- **Channeling** -> `epicfight:wrathful_lighting`;
- **Loyalty** -> `epicfight:everlasting_allegiance`;
- otherwise -> `epicfight:grasping_spire`.

This exact selector closes current catalog reachability without inventing a separate Epic Fight item-acquisition path: the owner remains `minecraft:trident`, while the vanilla enchantment parameter selects the provider-owned Epic Fight innate.

Object cards:

- aggregate: [`actions/SUPERNATURAL-ACTION-CARDS.md`](actions/SUPERNATURAL-ACTION-CARDS.md);
- [Wrathful Lightning](actions/wrathful-lightning.md);
- [Tsunami](actions/tsunami.md);
- [Everlasting Allegiance](actions/everlasting-allegiance.md).

Individual-card checkpoint: [`INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md`](INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md).

## Why the three count

### Wrathful Lightning

The exact animation/control seam attaches the provider server-side `SUMMON_THUNDER` event to the skill action. The provider therefore owns a discrete player-triggered lightning invocation rather than merely a martial swing animation.

### Tsunami

The exact trident innate selector resolves Tsunami for Riptide. Exact Tsunami resources and control flow provide provider-specific tide/water behavior, strengthened use while the player is in water or rain, Tsunami particles and a dedicated skill settlement. This is a discrete supernatural movement/attack action rather than ordinary trident use.

### Everlasting Allegiance

The exact selector resolves Everlasting Allegiance for Loyalty. The provider tracks the thrown trident and invokes its own `recalledBySkill()` lifecycle, returning the trident through a damaging recall path. That deliberate supernatural recall is a distinct Epic Fight action, not merely vanilla Loyalty's passive return.

## Why the other 40 IDs do not count

The semantic-magic ledger does not count every Epic Fight skill. The remaining 40 exact IDs are excluded because they are technical slots, dodge/wakeup, guard/parry, passive/reactive combat behavior, locomotion, combat identities or conventional weapon techniques.

Important boundary examples:

- `forbidden_strength` remains excluded despite magical wording: exact implementation is a passive stamina/health substitution skill, not an independent cast/action;
- `meteor_slam`, `demolition_leap` and `phantom_ascent` are combat movement/mobility;
- `revelation` is a combat identity/counter-weakpoint mechanic;
- `grasping_spire`, `heartpiercer`, `battojutsu`, `blade_rush`, `eviscerate` and the other ordinary weapon innates remain martial special attacks;
- `battojutsu_passive` is a weapon-passive support skill.

## Skillbook and acquisition boundary

The exact artifact packages Epic Fight's skillbook loot system, but the three counted roots are **weapon innates selected by the trident moveset**, not ordinary skillbook-unlock entries. Their catalog reachability therefore comes from the exact trident + enchantment selector above.

Skillbook loot, stamina, innate gauge/resource state, animation timing, damage and downstream particles/lightning/trident hits remain provider-owned settlement details and do not create extra semantic identities.

## Authority boundary

Epic Fight remains authority for:

- battle mode and player/entity patches;
- stamina, stun and skill state;
- weapon capabilities and movesets;
- trident innate selection;
- skill execution, animation and resource settlement;
- provider damage/hit/event processing.

Black Arcana catalogs the three supernatural identities but must not replay Epic Fight skills, apply a second stamina/cooldown/resource charge, duplicate thunder/trident damage, or treat downstream particles/events as separate spells.

## Runtime QA remains separate

Catalog closure is not an assembled-pack runtime PASS. Battle-mode state, multiplayer settlement, skill-slot conflicts, addon precedence, weapon-capability datapacks, Werewolves compatibility, EFIS/Iron's casting coexistence, controller/input and render compatibility remain runtime QA.

## Result

**✅ Cataloged — exact current 43-ID skill denominator closed and fully dispositioned.**

Current Epic Fight core semantic inventory: **3 exact-current supernatural player actions + 40 excluded non-magic skill identities**.

Strict semantic delta: **+3 `COUNTED_EXACT`**.
