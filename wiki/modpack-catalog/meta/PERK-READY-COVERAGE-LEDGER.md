# Cobertura global de dossiês técnicos para perks — base rastreável

**Acompanhamento atual:** [painel de progresso](PROGRESSO-CATALOGO-ATUAL.md). A coluna de quantidade de Markdown abaixo é uma baseline histórica de 13/10; não é um denominador de spells ou de completude técnica.

**Fonte:** árvore `Gustavaopere/Black-Arcana/main@465593694120c80db576344fc51de0d52d68d541`; auditoria estrutural de arquivos Markdown sob `wiki/modpack-catalog/providers/`, 2026-10-13.

- Diretórios com Markdown: **165**.
- Arquivos `.md` em providers: **2899**.
- **Isto não significa 2899 feitiços**: inclui índices, metadados, auditorias, arquivos de suporte, guias e objetos com classificação condicional.
- A meta é que **cada ficha real de objeto mágico** contenha o dossiê definido em [PERK-READY-TECHNICAL-STANDARD.md](PERK-READY-TECHNICAL-STANDARD.md); arquivos agregados ficam como índices ou provas.
- O Iron's base possui **110/110 fichas com anotações técnicas source-pinned integradas** pelo [PR #795](https://github.com/Gustavaopere/Black-Arcana/pull/795) em `main@c8ff878c8aab96bd546e4beb4d62ea08e94c5f94`. Isso **não** homologa 110 auditorias causais completas, hooks de perks, adapters ou QA provider-real. Os **2899** arquivos e **165** diretórios acima continuam sendo medidas históricas da baseline de 13/10, não uma nova contagem de magia.
- O Apprentice's Codex 0.9.7.1 possui 83 fichas de spells previamente source-catalogadas. Nesta branch, as **83/83 fichas receberam localizadores exatos** de classe/registro; seis tiveram rastreio causal específico (Higanbana, Blood Brand, Mist Form, Arcane Blast, Thermal Process, Echo Cast). É localização source-pinned, não prova de hooks ou runtime.
- Este inventário **não** modifica o estado de catalogação semântica vigente (mínimos 1857 global / 1855 escopo) nem a campanha de prova binária 25/39.

## Convenção de acompanhamento

A terceira coluna indica **a situação incremental nesta branch a partir da baseline da `main`**, não diz que o provider esteja ❌ não catalogado. Os registros podem já possuir valores/fórmulas validados por outras auditorias: esses dados devem ser aproveitados e os gaps calculados arquivo a arquivo. Conferência de completude por provider requer filtrar fichas de identidade semântica e validar prova por campo; uma quantidade de Markdown não substitui essa operação.

| Diretório do provider | Arquivos `.md` na `main` baseline | Gaps de dossiê técnico |
|---|---:|---|
| `✅-a-good-place` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-aces-spell-utils` | 5 | ✅ [Catálogo da versão-fonte 1.2.7.2](../providers/✅-aces-spell-utils/SOURCE-CATALOG-CLOSURE-1.2.7.2.md): 118 fichas / 132 Java / 245 arquivos rastreados, manifesto com hashes; 0 spells standalone. ⚠️ Certificação individual 0/118, paridade de métodos do JAR, Iron's 3.16.3, hooks e QA física pendentes. A coluna 5 é a baseline histórica, não o total atual. |
| `✅-acolyte` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-aeromancy-additions` | 16 | ✅ 10/10 spells com fichas source-pinned, [matriz de parâmetros, targeting e WORLD SAFETY](../providers/✅-aeromancy-additions/PERK-CAUSAL-ENGINEERING-MATRIX-1.2.8.md); ⚠️ JAR publisher comprovado, **SHA do instalado inválido**, host/config/Survival/QA pendentes; ⛔ perks/adapters não homologadas |
| `✅-alexs-caves-continued` | 13 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-alexs-mobs-continued` | 8 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-alshanex-familiars` | 20 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-apokinetics` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-apotheosis` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-apotheotic-creation` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-apothic-attributes` | 7 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-apothic-compat` | 4 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-apothic-compats` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-apothic-enchanting` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-apothic-spawners` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-apprentice-codex` | 101 | ✅ 83/83 source-catalogadas + 83/83 callsites de registry confirmados no JAR exato; 🟡 83/83 dossiês causais documentados; ⚠️ método/config/Survival/5 casos provider-real PENDING; ⛔ RPG perk adapter |
| `✅-ars-additions` | 48 | ✅ 5/5 magias/rituais (3 glyphs, 2 rituals) com cadeia e source exato; ⚠️ compatibilidade host/config/QA; ⛔ adapter RPG |
| `✅-ars-controle` | 25 | ✅ 9/9 glyphs com source 1.6.16 causal exato; ⚠️ runtime/concurrency/scheduler; ⛔ perk adapter RPG |
| `✅-ars-creo` | 14 | ✅ 7/7 sistemas de Create↔Ars com [matriz causal e fichas técnicas](../providers/✅-ars-creo/PERK-CAUSAL-ENGINEERING-MATRIX-5.4.0.md); 0 glyphs; ⚠️ Source, FakePlayer/OTHER, teleport, ritual mockado, fill/drain Create e compat dos hosts sujeitos a QA; ⛔ 0 adapters homologados e nenhuma nova raiz mágica |
| `✅-ars-elemancy` | 11 | ✅ 7/7 famílias foci/bangles/essences/armaduras com [fichas causais source-pinned](../providers/✅-ars-elemancy/PERK-CAUSAL-EQUIPMENT-MATRIX-1.18.3.md), registro de 105 items e **0 glyph/perks próprias**; ⚠️ Ars Nouveau 5.13.1/Ars Elemental 0.7.10.1, Curios/atributos e full-pack QA pendentes; ⛔ nenhum adapter RPG homologado |
| `✅-ars-elemental` | 59 | ✅ 47/47 objetos core (23 effects, 2 methods, 2 propagators, 12 filtros, 8 rituais) com dossiês source-located; ⚠️ config/QA; ⛔ adapter RPG |
| `✅-ars-hex` | 10 | ✅ [dataflow binário limitado #39093013655](../providers/✅-ars-hex/EXACT-BINARY-PERK-SCYTHE-DATAFLOW-5.0.4b.md) (3 perks + laço de desconto, 48 autotestes, publisher SHA fixado; gameplay QA PENDING); ✅ [operandos numéricos #39089774180](../providers/✅-ars-hex/EXACT-PUBLISHER-NUMERIC-OPERANDS-5.0.4b.md) confirmados por hash + 12/12 autotestes (presença de constantes, não def-use/QA); ✅ [JAR publisher/perks/foice Java21 #39087382649](../providers/✅-ars-hex/EXACT-PUBLISHER-PERK-SCYTHE-REFERENCES-5.0.4b.md) 13/13 + 6 classes compiladas (referências, não dataflow/QA); ✅ glyph único Soul Shatter `1/1` (registro binário); ✅ **3/3 threads/perks e 1/1 equipamento com ficha individual SOURCE_CAUSALITY** e [matriz de parâmetros/ingressos](../providers/✅-ars-hex/PERK-CAUSAL-ENGINEERING-MATRIX-5.0.4b.md); ⚠️ JAR de perk/foice, equip real, Malum/Ars/Lodestone, stack e mana/boomerang QA pendentes; ⛔ adapter perks/Mastery |
| `✅-ars-morph` | 7 | ✅ glifo Morph 1/1, 7/7 habilidades Identity2 e 11/11 atribuições JSON; ✅ [publisher 2.2.4 JAR #39077751784](../providers/✅-ars-morph/IDENTITY2-ABILITY-COOLDOWN-SOURCE-BRACKET-2.2.4.md) hash/assinaturas do alvo morph e método direct NBT restore `PASS_DIRECT_RESTORE_BOUNDED`, [matriz de ingressos/QA](../providers/✅-ars-morph/IDENTITY2-MORPH-INGRESS-RESTORE-QA-2.2.4.md); ⚠️ JAR instalado, aplicação real do mixin e revogação via respec/relog/respawn pendentes; ⛔ cooldown per-caster/Mastery não homologados |
| `✅-ars-n-spells` | 15 | ✅ 5/5 rituais com IDs binários 3.3.4 e métodos source 3.3.3; ⚠️ semântica método/JAR 3.3.4; ⛔ adapter RPG |
| `✅-ars-nouveau` | 149 | ✅ 85/85 glyph parts (5 Forms, 67 Effects, 13 Augments) + 24/24 rituais com dossiê source-located; ⚠️ runtime/hooks/QA e ⛔ adapter RPG não validados; eventos públicos reais source-pinned, adapter RPG e QA pendentes |
| `✅-ars-polymorphia` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ars-sable` | 4 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ars-sophisticated-compat` | 4 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ars-technica` | 8 | ✅ 11/11 objetos (10 effects + 1 augment) em 11 fichas novas com source 2.7.6; ⚠️ Ars/Create host/QA; ⛔ perk adapter RPG |
| `✅-ars-two-way-portals` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ars-zero` | 24 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-arsdelight` | 6 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-artifacts` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-asterism-arcanum` | 18 | [11/11 fichas com parâmetros e consumidores source-causais](../providers/✅-asterism-arcanum/SPELL-PERK-BOUNDARIES-0.1.0.md); 10 normais + Gateway conditional separado. Mutadores/config/JAR/QA PENDING; +0 strict |
| `✅-backported-spellbooks` | 12 | ✅ [post-Mixin exported handler invokes #39180390922](../providers/✅-backported-spellbooks/EXACT-RUNTIME-VANILLABACKPORT-POSTMIXIN-CALLLINK-1.1.7.10.md) (7/7 exatos, 3 `Entity.move`, 2 `LivingEntity.travel`, 1 `createLivingAttributes`, 1 `RangedAttribute.<init>`; jogador/modpack ⚠️ e perk adapter ⛔); ✅ [minimal NeoForge runtime + loader Mixin #39178310071](../providers/✅-backported-spellbooks/EXACT-RUNTIME-VANILLABACKPORT-MINIMAL-SERVER-1.1.7.10.md) (10/10, `Done`, Platform 1.3.3/VB 1.1.7.10 hashes pinados, 3 target-mixing reports 1× cada; pós-transform/cliente/modpack ⚠️ e perks ⛔); ✅ [NeoForge 21.1.250 patched server #39176290939](../providers/✅-backported-spellbooks/EXACT-NEOFORGE-211250-MIXIN-TARGETS.md) (7/7, official installer SHA, patched server `Entity.move` 1+1 calls, `LivingEntity.travel` 1+4 calls, ordinal 3 PC1314; modpack-applied mixins ⚠️, perk adapter ⛔); ✅ [Mojang 1.21.1 vanilla callsite #39170808679](../providers/✅-backported-spellbooks/EXACT-MOJANG-1211-VANILLA-CLIENT-CALLSITES.md) (16/16 regressões, SHA hash oficial, 4 `setDeltaMovement(DDD)` em `LivingEntity.travel`; quarta PC1240/ordinal3 **vanilla**, NeoForge/mixin aplicado ⚠️); ✅ [Mojang vanilla 1.21.1 methods #39170006472](../providers/✅-backported-spellbooks/EXACT-MOJANG-1211-MIXIN-TARGET-SIGNATURES.md) (7/7 métodos nomeados client+server, 8/8 testes, mapping hash oficial, `ordinal=3`/aplicação Mixin ❌ não demonstrados; runtime ⚠️ e perks ⛔); ✅ [classfile mixin injectors #39169078531](../providers/✅-backported-spellbooks/EXACT-BINARY-VANILLABACKPORT-MIXIN-INJECTION-SELECTORS-1.1.7.10.md) (7/7 handlers do escopo, 12/12 regressões, @ModifyArg index=1 e @WrapOperation ordinal=3; transformação em host ⚠️, perks ⛔); ✅ [NeoForge/mixins publisher gate #39164766070](../providers/✅-backported-spellbooks/EXACT-BINARY-VANILLABACKPORT-MIXIN-DECLARATION-1.1.7.10.md) (12/12 manifesto + 10/10 consumer, config JSON e três classes em lista comum; deps NeoForge/Minecraft/Platform 1.3.3, **aplicação física/mixin runtime ⚠️**, adapter ⛔); ✅ [host Vanilla Backport 1.1.7.10 SHA publisher #39156441117](../providers/✅-backported-spellbooks/EXACT-BINARY-VANILLABACKPORT-MOBILITY-HOST-1.1.7.10.md) (10/10, bounciness default0/teto1, drag/friction default1/range0–2048, mixins físicos apenas compilados; host instância e perk QA ⚠️/⛔); ✅ [Slime Boots/Fall gate #39153448024](../providers/✅-backported-spellbooks/EXACT-BINARY-SLIME-BOOTS-FALL-0.1.2.md) (11/11, quatro modifiers, slot FEET→cancelamento, **item não counted como magia**, runtime ⚠️/hook ⛔); ✅ [6/6 spells com pelo menos 1 método compilado delimitado](../providers/✅-backported-spellbooks/EXACT-BINARY-SLIME-ASPECT-0.1.2.md) (gate Slime Aspect #39149742796, SHA-1 do publisher igual ao físico, 9/9 regressões, três modifiers BOUNCINESS/JUMP_STRENGTH/AIR_DRAG + cast self, complementa Bomb/Thorn #39133252975 e os três anteriores; **100% só desse critério**, não QA/perks; runtime ⚠️, integração ⛔); ✅ [tranche histórica 3/6 com métodos de consumidor binário publisher 0.1.2 #39131725388](../providers/✅-backported-spellbooks/EXACT-BINARY-PERK-CONSUMERS-0.1.2.md) (2 super.tick do SulfurCloud, getWitherAmplifier=level-2, sessão de ResinSpray; 8/8 autotestes; runtime ⚠️; adapter ⛔); ✅ 6/6 fichas com [matriz causal source-pinned release-day](../providers/✅-backported-spellbooks/PERK-CAUSAL-SOURCE-MATRIX-0.1.2.md) e parâmetros por spell (6 registros físicos no JAR 0.1.2 já comprovados); ⚠️ fórmulas/efeitos binários e configurações Iron's/Survival não validados; ⛔ adapters/perks sem hook |
| `✅-betterend` | 53 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-betternether` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-bloodlines` | 39 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-born-in-chaos` | 21 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-bosses-of-mass-destruction` | 9 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-bosses-rise` | 12 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-cataclysm` | 31 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-cataclysm-spellbooks` | 67 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-cold-sweat` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-companions` | 13 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-corail-tombstone` | 30 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-chromatic-return` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-cold-sweat` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-deep-dark` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-dragons-plus` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-dreams-n-desires` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-enchantable-machinery` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-enchantment-industry` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-enchantment-industry-plus` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-ender-transmission` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-fantasizing-again` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-mechanical-companion` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-mechanical-spawner` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-mobile-packages` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-more-automation` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-more-features` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-teleporters-remastered` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-wizardry` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-creating-space` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-crystal-chronicles` | 5 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-deeper-and-darker` | 17 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-deeper-and-darker-spellbooks` | 8 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-dimensional-sable` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-dis-enchanting-table` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-discerning-the-eldritch` | 32 | **22/22 fichas documentais** com parâmetros/consumidores e [contratos condicionais](../providers/✅-discerning-the-eldritch/SPELL-PERK-BOUNDARIES-1.4.4-1.21.md); hosts/config/Mastery Ritual/Survival/QA PENDING; +0 strict |
| `✅-dragon-care` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-dreamless-spells` | 10 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-dungeons-delight` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-dynamic-rpg-resource-bars` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-efiscompat` | 4 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-eidolon-repraised` | 7 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-emf-compat-iron-spells` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-enchantment-descriptions` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-enders-spells-and-stuff-requiem` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-epic-fight` | 8 | ✅ **43/43** core skill IDs e **42/42** JSONs catalogados e verificados no JAR físico/publisher 21.17.3.1; ✅ [movimento exato de tridente de retorno #39103337112](../providers/✅-epic-fight/EXACT-TRIDENT-RETURN-KINEMATICS-21.17.3.1.md) (8/8 testes; tempo relativo, fatores 0.0005/0.05 e teto por tick de 10 no método; não alcance/duração real nem API de perk); ✅ [precedência de fases e source do tridente de retorno #39102096383](../providers/✅-epic-fight/EXACT-TRIDENT-PHASE-OVERWRITE-RETURN-21.17.3.1.md) (Wrathful grupos 0→1 na mesma Phase, sobrescrita por Map.put; Everlasting registra no-op e ThrownTridentPatch usa source independente, AABB inflate por eixo; gameplay não medido); ✅ [QA observação de dano de jogador #39098965924](../providers/✅-epic-fight/NATIVE-PLAYER-DAMAGE-TELEMETRY-QA-21.17.3.1.md) (observer nativo compilado/armado sem cliente, zero amostras; ataque real e correlação PENDING); ✅ [handler Mixin de armadura observado em LivingEntity transformada #39098101364](../providers/✅-epic-fight/EXACT-ARMOR-MIXIN-LOADED-CLASS-PREFLIGHT-21.17.3.1.md) (NeoForge 21.1.250, 1 handler com assinatura exata, **sem** cliente/hit/dano; QA isolado, artefato 12125471763); ✅ [consumo compilado de AttackPhase #39096586191](../providers/✅-epic-fight/EXACT-ATTACK-PHASE-CONSUMERS-21.17.3.1.md) (8/8 testes; ResultCalculator, source, mixin e armor path; runtime PENDING); ✅ [ID → LambdaMetafactory bootstrap #39095049311](../providers/✅-epic-fight/EXACT-TRIDENT-REGISTRY-BOOTSTRAP-LINKAGE-21.17.3.1.md) (3/3, 10/10 testes, sem gameplay); ✅ [AttackPhase compilada do tridente #39094435160](../providers/✅-epic-fight/EXACT-TRIDENT-ATTACK-PHASE-PROPERTIES-21.17.3.1.md) (constantes/enums ligados aos builders exatos, 11/11 testes; **não** dano final ou runtime); ✅ **3/3** ações sobrenaturais individuais `COUNTED_EXACT` (Trident: Riptide/Tsunami, Channeling/Wrathful Lightning, Loyalty/Everlasting Allegiance), **40/43** habilidades marciais/passivas excluídas apenas do numerador mágico; ✅ [43/43 fichas individuais core](../providers/✅-epic-fight/skills/INDIVIDUAL-SKILL-CARDS-21.17.3.1.md) (42 jogáveis + uma sentinela), apoiadas nos 28 dossiês source-adjacent; ✅ 5 skills de modifiers legados sob override temporário com cardinalidade 0→8→0 no provider isolado; ⚠️ `ServerPlayerPatch.initialized=true` ainda não observado com jogador conectado e `AttributeInstance` efetivo não validado; [contratos de STAMINA e progressão já presentes na main RPG](../providers/✅-epic-fight/skills/RPG-SIBLING-BOUNDARIES-ed5b65b.md) documentados separadamente; ⛔ novos mutadores de alcance/área/tipo/hitbox sem contrato. [Evidência e limites](../providers/✅-epic-fight/README.md) · [índice técnico](../providers/✅-epic-fight/skills/PERK-TECHNICAL-CHECKPOINT-2026-10-16.md) |
| `✅-familiarslib` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-fantasy-armor` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-farmers-spell` | 12 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-fires-ender-expansion` | 15 | [11/11 fichas com parâmetros e consumidores source-causais](../providers/✅-fires-ender-expansion/SPELL-PERK-BOUNDARIES-2.4.1.md); config/hosts/mutadores/Survival/QA PENDING; +0 strict |
| `✅-gaze` | 34 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-goety` | 375 | ⚠️ 2 Focuses com boundary técnico e bloqueio explícito; código exato pendente |
| `✅-goety-cataclysm` | 60 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-goety-iron` | 23 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-grapplemod-skybound` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-gtbcs-geomancy-plus` | 4 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-gtbcs-spelllib` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-hazen-n-stuff` | 41 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-hazentouvelib` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-hexalia` | 53 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ice-and-fire-ce` | 16 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ice-and-fire-dread-land` | 5 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ignis-soulfires` | 12 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ignis-soulfires-spellbooks` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-immersive-portal-irons-spells-addon` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-immersive-portals-true-immersion` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-integrated-villages` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-irons-apothic` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-irons-gems-n-jewelry` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-irons-lib` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-irons-spellbooks-kubejs` | 5 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-irons-spells` | 150 | ✅ 110/110 fichas source-pinned (#795) e 110/110 dossiês source-causais (#825) integrados; ⚠️ equivalência binária por campo, hooks mutadores e gameplay/QA seguem condicionados. [Checkpoint pós-merge](CHECKPOINT-POS-PR825-2026-10-21.md) |
| `✅-irons-spells-recolor` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ironsable` | 13 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ironsable-x-winds-spellbooks` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-iss-magic-from-the-east` | 27 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-kubejs-ars-nouveau` | 4 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-legendary-monsters` | 26 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-legendary-spellbooks` | 33 | ✅ 30/30 spells com IDs compilados no JAR 0.3.2 e fichas de engenharia causal source-pinned ([matriz](../providers/✅-legendary-spellbooks/PERK-CAUSAL-ENGINEERING-MATRIX-0.3.2.md)); ⚠️ métodos/dependências e gameplay pendentes; ⛔ nenhum adapter Mastery/perks homologado |
| `✅-leyline-spellbooks` | 21 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-malum` | 5 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-mobstein` | 78 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-monsters-spellbooks` | 6 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-more-relics` | 65 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-mowzies-cataclysm` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-mowzies-mobs` | 17 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-northstar-redux` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-not-enough-glyphs` | 49 | ✅ 40/40 fichas source-located (39 source-enabled condicionais + Momentum disabled); ⚠️ config SERVER/bytecode/QA; ⛔ RPG perk adapter |
| `✅-ozymandias-sundries` | 6 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-paladin-spells` | 9 | [5/5 fichas com matriz e consumidores source-pinned reauditados](../providers/✅-paladin-spells/PERK-BOUNDARIES-1.1.1.md); contagem 9 preserva a fotografia histórica de documentos, não identidades. Hooks/runtime PENDING |
| `✅-photon` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-pickable-orbs` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-portable-hole` | 5 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-protection-pixel` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-pufferfishs-attributes` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-pufferfishs-skills` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-pufferfishs-unofficial-additions` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-relics` | 45 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-reliquified-ars-nouveau` | 21 | ✅ 19/19 habilidades com dossiês source-located 0.8.1 e identidades estáticas físico-exatas; ⚠️ config/bytecode de métodos/QA; ⛔ RPG perk adapter |
| `✅-reliquified-artifacts` | 55 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-reliquified-irons-spells-n-spellbooks` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-reliquified-l-enders-cataclysm` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-reliquified-lenders-cataclysm-new-relics-fix` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-runiclib` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-shadowsz` | 16 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-simply-more` | 28 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-simply-swords` | 71 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-simply-swords-cataclysm` | 9 | [4/4 fichas de habilidades com parâmetros e consumidores source-causais](../providers/✅-simply-swords-cataclysm/IMPLEMENTATION-PERK-BOUNDARIES-1.0.2.md); config STARTUP/host/ativação/mutadores/QA PENDING; +0 strict |
| `✅-sky-aesthetics` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-snow-real-magic` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-somake-spells` | 178 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-soul-fire-d` | 4 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-spell-actionbar` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-spell-codex-specs` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-starbunclemania` | 5 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-toxony` | 7 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-traveloptics` | 61 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-tunes-n-tomes` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-vampire-spells-addon` | 4 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-vampiric-ageing` | 24 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-vampirism` | 8 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-vampirism-integrations` | 4 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-waystones` | 9 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-weapons-of-miracles` | 18 | ✅ [64/64 fichas individuais por ID](../providers/✅-weapons-of-miracles/skills/INDIVIDUAL-SKILL-CARDS-2.0.178.md) (51 novas + 13 enriquecidas; 58 JSONs e seis ausências); ✅ JAR hash-exato, 64 vínculos ID→bootstrap/supplier/holder, 64 recursos de builder, 370 descritores/915 referências e dez casos de operandos delimitados; ⚠️ downstream, montantes negativos/ordem de listeners, atributos de player e gameplay PENDING; [contrato RPG genérico já existente](../providers/✅-epic-fight/skills/RPG-SIBLING-BOUNDARIES-ed5b65b.md) preservado, ⛔ novos mutadores sem hook; sem delta mágico (12 strict + 1 Nova condicional). [Provas e limites](../providers/✅-weapons-of-miracles/skills/EXACT-TECHNICAL-BOUNDARIES-2.0.178.md) |
| `✅-werewolves` | 8 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-winds-spellbooks` | 11 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-woodwalkers-spellbooks` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ypsilons-fundamentalism` | 26 | [15/15 fichas de spells com parâmetros e consumidores source-causais](../providers/✅-ypsilons-fundamentalism/SPELL-PERK-BOUNDARIES-1.1.7.1.md); [13/13 Principles](../providers/✅-ypsilons-fundamentalism/principles/README.md) em métrica separada. Hooks/versões/config/QA PENDING; +0 magias |
| `✅-yungs-better-end-island` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-yungs-better-witch-huts` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `README.md` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |

## Ars Nouveau — checkpoint 2026-10-13

**85/85 Glyph Parts** e **24/24 rituais** com mapeamento de perks/cadeia causal source-pinned nesta branch; sendo 5 Forms, 67 Effects, 13 Augments e 24 rituais. [Matriz técnica Ars 5.13.1](../providers/✅-ars-nouveau/PERK-ENGINEERING-MATRIX-5.13.1.md) com métodos, fórmulas, provas auxiliares e bloqueios. [Eventos reais do Ars 5.13.1](../providers/✅-ars-nouveau/VERIFIED-EVENT-SURFACES-5.13.1.md) foram localizados, mas não constituem adapter implementado. A cobertura semântica de identidade preexistente é diferente da profundidade técnica para perks. **✅ source-located** nesta branch não implica **✅ adapter implementado**, **✅ QA**, **✅ hooks em todos os efeitos** ou merge na main.

## Continuação — Ars Additions e Ars Elemental 2026-10-13

- ✅ [Ars Additions 21.3.0](../providers/✅-ars-additions/PERK-ENGINEERING-MATRIX-21.3.0.md): 5/5 objetos de magias/rituais com métodos source-pinned, fórmulas e limites de perks. Fonte é 21.3.0; build baseline publica Ars 5.11.2, pack usa host 5.13.1 — compatibilidade ⚠️.
- ✅ [Ars Elemental 0.7.10.1](../providers/✅-ars-elemental/PERK-ENGINEERING-MATRIX-0.7.10.1.md): 47/47 objetos (39 Glyph Parts + 8 Rituals) com classes source-pinned e dossiês por ficha. ID no JAR físico foi comprovado anteriormente; igualdade entre implementação do source pin e JAR não foi provada.
- Este lote é +0 no denominador semântico; mantém mínimos 1857 global / 1855 escopo e 25/39 providers com prova binária. Nenhum teste de runtime/CI/Survival, adapter RPG, merge ou promoção de Stage por este lote.

## Continuação — Ars Controle e Ars Technica (2026-10-13)

- ✅ [Ars Controle 1.6.16](../providers/✅-ars-controle/PERK-ENGINEERING-MATRIX-1.6.16.md): 9/9 glifos existentes receberam source pin da release e detalhes de parser, efeitos de Delay, fórmulas de Random, operadores booleanos, validação e risco de estado singleton. IDs físicos anteriormente comprovados.
- ✅ [Ars Technica 2.7.6](../providers/✅-ars-technica/PERK-ENGINEERING-MATRIX-2.7.6.md): os 11 objetos **já contados no catálogo** foram materializados pela primeira vez em 11 novos `glyphs/*.md` individuais com receitas Create, mana default, compatibilidade, cadeia causal e riscos de conservação. **+11 arquivos `.md`**, **+0 novas identidades de magia**.
- As quantidades de `.md` na tabela e o total de 2899 são a contagem de arquivos que já existiam na main baseline. A branch draft adicionou fichas/matrizes, portanto seus números de arquivo são maiores; não atualizar o denominador semântico para refletir documentação nova.
- Nenhum adapter Java, CI, GameTest, Survival ou Stage foi promovido. Testes de equivalência método↔JAR, config real, concorrência, claims e integração Create/Ars permanecem ⚠️ e adaptações de perks RPG ⛔.

## Continuação — Ars 'n' Spells e Ars Morph (2026-10-13)

- ✅ [Ars 'n' Spells 3.3.4](../providers/✅-ars-n-spells/PERK-ENGINEERING-MATRIX-3.3.4.md): cinco rituais com IDs e gates estáticos comprovados no JAR 3.3.4; cinco fichas ampliadas com source público exato **3.3.3**, preflight, receipt/settlement, configuração e boundary da bridge. **⚠️ sem prova de corpo de método exato da release instalada 3.3.4**.
- ✅ [Ars Morph 2.0.0](../providers/✅-ars-morph/PERK-ENGINEERING-MATRIX-2.0.0.md): uma ficha nova individual `glyphs/morph.md` com seleção de target/form, Max HP, Identity2 e condições de sucesso. Release-aligned source não equivale a bytecode físico nem a teste da versão atual Identity2.
- +0 identidades semânticas. O ledger de provider `.md` da main baseline (2899) não é métrica de cobertura de perks desta branch. Sem alterações runtime, adapters, CI, GameTests, QA/Survival ou promoção do Stage 06.05.

## Priorização para próximos lotes

1. Spells do Apprentice's Codex (`apprenticecodex`), 83 identidades source-pinned; depois validar as classes de entidades/helpers e a versão binária instalada.
2. Ars Nouveau 5.13.1, Ars Elemental 0.7.10.1 e Ars Additions 21.3.0: objetos source-located no PR draft; aprofundar auxiliares/eventos/versões e QA, sem repetir fichas.
3. Goety 3.1.4, cujo catálogo dos 123 Focuses é exact-binary, mas muitos arquivos não comprovam método, custo, raio e hook.
4. Outros 162 diretórios conforme relevância de spells, glifos, rituais, habilidades e riscos/capacidade de implementação, sempre preservando as fontes instaladas.

**Não usar este ledger como contagem de spells** e não marcar implementação nem CI como completos.

## Continuação NEG 4.6.2 — 2026-10-13

- **8/40** fichas aprofundadas, com links Java e causalidade no novo `PERK-ENGINEERING-MATRIX-4.6.2.md`. IDs completos `glyph_` confirmados por `CompatRL`.
- Defaults retificados: Plow **0** (antes 5), Flatten **30** (antes 100), Echoing Trail **200, Tier III** (antes 50, Tier II). Os 40 registros incluem Momentum **source-disabled**, não 40 spells ativas.
- Perks e Mastery **⛔** fail-closed até hooks, custo/debit real e deduplicação. O source 4.6.2 e a estrutura da modlist são provas documentais, **não** execução de bytecode/GameTest/Survival. Delta semântico **+0**.

## Continuação Not Enough Glyphs — contingências/filtros, 2026-10-13

- **+22 fichas** individuais de engenharia (7 contingências e 15 filtros), cobertura de **8/40 a 30/40**; permanecem 10 perfis. Nova `PERK-ENGINEERING-MATRIX-FILTERS-CONTINGENCIES-4.6.2.md` e READMEs vinculados.
- Source pin `45604dd18d9d2e3e7ca80a2c616b3309f42aca77`, `Events.java` para handlers de `LivingHealEvent`, `LivingDeathEvent`, `LivingUseTotemEvent`, `EntityTeleportEvent`; `ContingencyTriggers` para fall/fire/health; expiry pertence a Sauce. Semântica do cast armazenado e custos ainda exigem auditoria da dependência real.
- Retificações: `FilterLight` usa SKY e `FilterDark` usa BLOCK, limiar `8+ampMultiplier` (`>=` versus `<`); `EntityDummy` é incluído como player; `FilterSelf.onResolve` possui predicado local incompleto para exclusão de outros alvos (hipótese source-level, não falha física confirmada). Todas as identidades ganharam ID completo `glyph_` e links Java.
- Mantêm-se ⚠️ config ativa, bytecode instalado, GameTest/Survival e ⛔ hooks/adapters RPG. **+0 identidades semânticas**.

## Fechamento documental Not Enough Glyphs 4.6.2 — 2026-10-13

- **+10 fichas finais** atualizadas a partir do source público 4.6.2: Ride, Feed, Chaining, Reverse Direction, Resize, Propagate Missile/Overhead/Projectile/Self e Overhead form. A cobertura de engenharia chega a **40/40 (39 source-enabled condicionais; 1 source-disabled Momentum)** com três matrizes de controle.
- Observações: `EffectFeed` demanda custo item-side/explosão Crush e cuidado com eventos `Pre`; `EffectChaining` cria child resolvers e defaults 16 blocos/8 entidades; `EffectResize` exige auditoria de unidades `IPotionEffect`; `PropagateMissile` menciona Extract mas a lista de augments parece não incluí-lo na fonte.
- **+0** no denominador mágico global. Todos os 40 registros já existiam. Nenhum adapter, dano, mundo, receita, core Java, GameTest ou validação física foi implementado. Config ativa e equivalência source/binário ficam ⚠️; hooks de perks e Mastery permanecem ⛔.

## Dossiês Reliquified Ars Nouveau 0.8.1 — source 2026-10-13

- 3/19 `AbilityTemplate` roots aprofundadas em `PERK-ENGINEERING-MATRIX-0.8.1.md`; source declarado 0.8.1 `Octo-Studios/reliquified_ars_nouveau@125e1e3a723d8bc7050026e0670f8ac49535c8bc`. **19/19 identidades estáticas já eram COUNTED_EXACT** no JAR hash-matched. +0 raízes semânticas.
- Archmage Glove: `SpellCastEvent` primário + `AugmentMulticast` posicional, filhos a cada 5 ticks, tag de custo 0 de filhos, chance de refund condicionada a resolução.
- Mana Ring: max mana/regeneration Ars, heal-to-mana, custo `SpellCostCalcEvent.Pre` com dívida `MANA_RING_DEBT`, repagamento pelo tick.
- Last Will: intercepta `LivingIncomingDamageEvent`, enfileira `RewindEvent` 60 ticks, cancela dano, registra cooldown, vingança por UUID e synergy dummy/vanishing.
- Implementação física exata de métodos / config atual / GameTests/Survival ⚠️; Black Arcana/RPG perk adapter ⛔.

## Fechamento documental Reliquified Ars Nouveau 0.8.1 — 2026-10-13

- Na continuação do PR #797, **+16 fichas** aprofundadas sobre as **3 prévias**, atingindo **19/19** em `PERK-ENGINEERING-MATRIX-0.8.1.md`. **+0 identidades**; as 19 roots já integravam a métrica global (mínimos mantidos).
- Bytecode/JAR físico verificado para registro `AbilityTemplate.builder` (Java 21 #38461801129), enquanto a engenharia de handlers/callbacks usa apenas source `Octo-Studios/reliquified_ars_nouveau@125e1e3a723d8bc7050026e0670f8ac49535c8bc`. NÃO promover corpos compilados, config efetiva ou QA/Survival a PASS.
- Riscos mais importantes: `RingOfThrift` Pre/Post com free-cast token e refunds, `QuantumBubble` owner e lifecycle de projéteis, `ArchitectsStaff` MageBlock placement, `SpectralWalker` IntangibleAir e claims, `HornOfWildHunter` UUIDs de wolves, `IllusionistsMantle` death swap e `LastWill` rewind simultâneos.
- Interoperabilidade RPG **⛔** sem hook seguro; world/resource authority externa preservada. Stage 06.05 não avançou.

## Apprentice's Codex 0.9.7.1 — incremento de engenharia 2026-10-13

- `main` de partida `a6ccf7fd1d4ea6a18e5ff697f4e5abc82a197248`; versão física do sibling modlist `0.9.7.1`, JAR `apprentice_codex-0.9.7.1+mc1.21.1.jar`, SHA-1 `b514315add32b93b0049c8673075627d7ef812e0`, mod ID `apprenticecodex`.
- **+8** dossiês causais profundos: [matriz técnica](../providers/✅-apprentice-codex/PERK-ENGINEERING-MATRIX-HIGH-RISK-0.9.7.1.md), elevando **6/83→14/83**. **83/83** identidades permanecem catalogadas; **69/83** pendentes da mesma profundidade; **+0** ao denominador global.
- Auditoria source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` em eventos, auxiliares, managers e entidades; corpos do JAR/config/QA não provados. O provider/Iron's preserva ownership do cast/mana e world mutations; BA só do próprio runtime.
- **Perks/Mastery ⛔** sem contrato real; **Stage 06.05** não promovido. Alterações exclusivas em Markdown; sem GameTest físico de conteúdo Apprentice's Codex.

## Apprentice's Codex — entidades/jobs: +10 dossiês, 2026-10-13

- `main` de partida: `61696cd5ec7589c5f42a461d6c5ef4c2599e88c0`. Modlist sibling `main@f5d31633186a004ada41557220dcafa94a75546e` confirma `apprentice_codex-0.9.7.1+mc1.21.1.jar`, `apprenticecodex`, SHA-1 `b514315add32b93b0049c8673075627d7ef812e0`.
- Source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`; **+10** dossiês em Auto Turret, Companion Trunk, Call Broom, Bound Sword, Bound Bow, Archer Multiple, Search Beacon, Tamer's Pocket, Personal Shelf e Tiny Lumberjack. [Matriz técnica lifecycle](../providers/✅-apprentice-codex/PERK-ENGINEERING-MATRIX-LIFECYCLE-0.9.7.1.md).
- Cobertura de **engenharia causal** progride **14/83 → 24/83**, restam **59/83** sem a mesma profundidade. **Identidades catalogadas 83/83, +0 ao denominador semântico global**. Arquivos Markdown podem crescer, mas não são novas magias.
- Riscos ⚠️: cobrança de restock, cleanup varrendo níveis, item inventory/cursor, UUID e NBT de pets, item reservation/refund, transferência via item handler e jobs sem cap agregado neste manager. Bytecode exato do JAR, pack config e QA físico não provados.
- **Black Arcana e RPG Skill Tree:** nenhum adapter, cast replay, segunda liquidação, reward, claim policy ou world effect externo implementado; RPG perks/Mastery ⛔. Stage 06.05 permanece sem promoção.


## Apprentice's Codex 0.9.7.1 — persistência, combate e mundo (+10), 2026-10-14

- Baseline `Black-Arcana/main@504e00b83c1f4a09d4f265042af93369736d7a28`. Sibling modlist `main@82d7b7a8d15ab96ed7c59cc0c3e870edfe02cf4d` mantém `apprentice_codex-0.9.7.1+mc1.21.1.jar`, `apprenticecodex`, SHA-1 `b514315add32b93b0049c8673075627d7ef812e0`.
- Source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`; **10 dossiês**: Assist Wings, Manifestation Grimoire, Bullet Stream, Healing Bloom, Heavenly Fist, Edge Dancer, World Flatter, Divine Possession, Otherworld Lens e Totem of Permafrost. [Matriz de alta fidelidade source-located](../providers/✅-apprentice-codex/PERK-ENGINEERING-MATRIX-PERSISTENT-0.9.7.1.md).
- Cobertura profunda avança **24/83→34/83**, restam **49/83**. **83/83 identidades já catalogadas, +0 raiz semântica**. Os eventos de entidades, visualização, timers e limpeza não ampliam o inventário de magias.
- **⚠️** Source não certifica bytecode do JAR nem execução de addon físico, configuração, world claim checks, Survival, client/dedicated, NBT ou incompatibilidade com outros mods. **⛔** nenhum adapter RPG perks/Mastery implementado e homologado. Sem código runtime BA ou Stage 06.05 promotion.


## Apprentice's Codex — ofensiva/movimento/detecção (+10), 2026-10-14

- Baseline `Black-Arcana/main@94f19f9ecf2959cb30fc6fa3195d3a71ca27bf9c`; source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`; sibling modlist `main@63a41587ed91e6768a6b863e74dfaf44b9eb3a46`.
- ✅ 83/83 catalogadas; 🟡 74/83 com engenharia causal, 9 pendentes; +10 dossiês anexados a fichas existentes, [matriz](../providers/✅-apprentice-codex/PERK-ENGINEERING-MATRIX-OFFENSE-MOVEMENT-0.9.7.1.md), +0 raízes semânticas.
- Achado de auditoria: `ArcaneBeamEntity.tick` tem condição de frequência distinta do comentário. `MantisLeapMovementEvent` preserva fallback de pouso ao destino se os offsets falham; `SenseEvil` não apresenta cap explícito no coletor de highlights.
- ⚠️ QA do JAR/config, claims/PvP, dedicated, client e packets pendente. ⛔ RPG adapter sem contrato; Black Arcana não alterou pipeline mágico nem promoveu Stage.


## Apprentice's Codex — nove dossiês finais de source-level, 2026-10-14

- Dependência base `Black-Arcana catalog/apprentice-codex-offense-motion-sensing-20261014@e44a2aab5a6ff1b56b2aad36246f471d35cdf8cc` (PR #804); modlist sibling `main@63a41587ed91e6768a6b863e74dfaf44b9eb3a46`; source declarado `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`.
- ✅ 83/83 identidades + 🟡 **83/83 dossiês causais** com class/method tracing source-level, +9 sobre os 74 de #804, zero magias novas. [Matriz final](../providers/✅-apprentice-codex/PERK-ENGINEERING-MATRIX-FINAL-NINE-0.9.7.1.md).
- Riscos estáticos: `UniteLunaMoonEntity.explodeByAntiMagic` com multiplicador 3×; `PaletteShiftReceptionEvent.onSpellPreCast` cancela magia receptora; `ManaMendingCastData.matchesTarget` exige mesma instância de ItemStack; listener `DeepSensor` limita display a 8.
- ⚠️ Leitura source concluída **não** equivale a QA binário/Survival/dedicated/claims/PvP/config; ⛔ perks/Mastery ainda não implementáveis sem contrato homologado com RPG Skill Tree. Nenhuma promoção Stage 06.05.


## Apprentice's Codex — prova dos 83 registros no JAR exato, 2026-10-14

- [CI binária #38576975705](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38576975705): SHA-1 e SHA-256 do JAR oficial 0.9.7.1 coincidem com a modlist sibling; `SpellRegistry` contém **83/83** pares `ID → Supplier → reg() → DeferredHolder`, sem faltas, extras ou duplicações. [Relatório técnico](../providers/✅-apprentice-codex/README.md) e [evidência QA](../../../docs/qa/apprentice-codex-registry-binary-2026-10-14.md).
- **✅** igualdade documental/callsite de registro; **⚠️** não confirma registry carregado, classes de todos os spells em runtime, disponibilidade em Survival, configs nem comportamento real. `AC-P01–AC-P05` ainda **PENDING**. **⛔** nenhuma integração Mastery/perks sem contrato real RPG Skill Tree. Stage 06.05 inalterado.
