# Alex's Caves Continued 1.0.10 — índice de 51 encantamentos para perks

> **Escopo de catalogação:** inventário de identidades dos **51 recursos JSON** de `data/alexscaves/enchantment/` no artefato publisher 1.0.10. Este índice deriva do [inventário SHA-exato](INTEGRATION-SCOPE-INVENTORY-1.0.10.json) e relaciona **referências textuais nominais** em 46 manifestos técnicos `EXACT-*-1.0.10.json` da árvore atual. Referência nominal em manifesto não comprova consumer completo, registry efetiva, parâmetro de perk, hook seguro nem execução do jogo.

```text
scope=ENCHANTMENT_IDENTITY_AND_EXISTING_EVIDENCE_CROSSWALK_ONLY
mod_id=alexscaves
version=1.0.10
artifact_sha1=6960b299a39a039ac8a5eb9b07be4ad0e3e0a570
artifact_sha256=36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c
identity_resources_seen=51/51
individual_full_enchantment_dossiers=0/51
individual_partial_enchantment_dossiers=17/51
names_located_in_selected_exact_manifests=41/51
names_not_located_in_selected_exact_manifests=10/51
whole_provider_catalog_closed=false
mutating_hook=NOT_VERIFIED
physical_qa=NOT_TESTED
mutation=NO_MUTATION
perk_certification=NOT_CERTIFIED
```

**Barra de fichas individuais integralmente auditadas (escopo dos 51 encantamentos):** `░░░░░░░░░░░░░░░░░░░░ 0,0% (0/51)`.

**Barra de fichas com documentação parcial individual (não é conclusão técnica):** `██████░░░░░░░░░░░░░░ 33,3% (17/51)`.

**Barra de rastreio de referências SHA-exatas (não é conclusão):** `████████████████░░░░ 80,4% (41/51)`. As fichas individuais parciais de Arrow Inducting, Astral Transferring, Bonking, Bouncing Bolt, Bouncy Ball, Charting Call, Chomping Spirit, Crystallization, Dark Nock, Dazing Sweep, Detonating Death, Double Stab, Energy Efficiency, Enveloping Bubble, Explosive Flavor, Far Flung e Ferrous Haste entram no denominador observado após regeneração dos índices, **sem certificar contrato estático nem alterar o numerador de certificados**. Não some os 51 recursos ao denominador global sem reconciliação do universo de objetos e duplicações com ações/equipamentos existentes.

**Nova evidência Ferrous Haste:** [`EXACT-FERROUS-HASTE-1.0.10.json`](EXACT-FERROUS-HASTE-1.0.10.json) adiciona a identidade literal do recurso `ferrous_haste`, seu JSON, tag e janelas JVM de `MagneticWeaponEntity.tick`, elevando o rastreio nominal **40→41/51**, sem promover contratos ou hooks mutadores. Os símbolos JVM de `FIELD_EXTENSION` no mesmo método continuam pistas de outro encantamento, não uma nova ficha independente.

**Nova evidência exata:** [`EXACT-FAR-FLUNG-1.0.10.json`](EXACT-FAR-FLUNG-1.0.10.json) acrescenta o ID literal `far_flung` ao recorte SHA-exato e eleva o rastreio **39→40/51**. A sonda também localiza os símbolos JVM em maiúsculas `SHARP_CANE` e `STRAIGHT_HOOK` no mesmo construtor; eles são *pistas técnicas*, não substituem uma ficha individual e não foram somados como IDs literais de recursos JSON neste contador. A classificação ❌ dessas entradas continua sujeita a auditoria própria.

**Reconciliação de referência:** `dazing_sweep` já consta como recurso e consumidor no manifesto SHA-exato existente [`EXACT-EFFECT-CONTRACTS-1.0.10.json`](EXACT-EFFECT-CONTRACTS-1.0.10.json), embora o crosswalk anterior o marcasse ❌. A correção eleva somente o rastreio nominal **38→39/51**; não adiciona manifesto, raiz mágica ou certificado de perk.

## Leitura da coluna de estado

- ⚠️ **Parcial / condicionado:** nome exato encontrado em ao menos um manifesto SHA-exato do recorte; pode já existir ficha individual, mas continuam pendentes fechamento técnico integral, causalidade, targeting, custos, lifecycle, disponibilidade de hooks mutadores e QA.
- ❌ **Não catalogado individualmente:** não há referência literal ao **ID minúsculo de recurso** nos **46 manifestos selecionados**; campos simbólicos de bytecode em maiúsculas não encerram uma identidade individual. Isso **não prova** ausência de comportamento ou documentação em outros arquivos, fontes, assets ou módulos.
- ✅ **Catalogado integralmente:** nenhum desses 51 recebeu esse estado nesta revisão. Evidência de outra ação/equipamento não fecha o universo do encantamento.

## Índice alfabético dos recursos

| Estado | ID do recurso JSON / encantamento | Referência nominal SHA-exata já disponível |
|---|---|---|
| ⚠️ | `alexscaves:arrow_inducting` | [Ficha técnica parcial](enchantments/arrow-inducting.md) · [JAR 1.0.10 selado](EXACT-ARROW-INDUCTING-1.0.10.json) |
| ⚠️ | `alexscaves:astral_transferring` | [Ficha técnica parcial](enchantments/astral-transferring.md) · [JAR 1.0.10 selado](EXACT-ASTRAL-TRANSFERRING-1.0.10.json) · [ação Totem](actions/totem-possession-remote-control.md) |
| ⚠️ | `alexscaves:bonking` | [Ficha técnica parcial](enchantments/bonking.md) · [JAR 1.0.10 selado](EXACT-BONKING-1.0.10.json) |
| ⚠️ | `alexscaves:bouncing_bolt` | [Ficha técnica parcial](enchantments/bouncing-bolt.md) · [JAR 1.0.10 selado](EXACT-BOUNCING-BOLT-1.0.10.json) · [ação Sea Staff](actions/sea-staff-water-bolt.md) |
| ⚠️ | `alexscaves:bouncy_ball` | [Ficha técnica parcial](enchantments/bouncy-ball.md) · [JAR 1.0.10 selado](EXACT-BOUNCY-BALL-1.0.10.json) · [equipamento Shot Gum](equipment/shot-gum.md) · [dano Gumball](damage-types/gumball.md) |
| ⚠️ | `alexscaves:charting_call` | [Ficha técnica parcial](enchantments/charting-call.md) · [JAR 1.0.10 selado](EXACT-CHARTING-CALL-1.0.10.json) · [ação Magic Conch](actions/magic-conch-summon-deep-ones.md) |
| ⚠️ | `alexscaves:chomping_spirit` | [Ficha técnica parcial](enchantments/chomping-spirit.md) · [JAR 1.0.10 / consumidor](EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json) · [dano Spirit Dinosaur](damage-types/spirit-dinosaur.md) |
| ⚠️ | `alexscaves:crystallization` | [Ficha técnica parcial](enchantments/crystallization.md) · [publisher 1.0.10 e consumidor](EXACT-CRYSTALLIZATION-1.0.10.json) |
| ⚠️ | `alexscaves:dark_nock` | [Ficha técnica parcial](enchantments/dark-nock.md) · [contrato JAR 1.0.10 já selado](EXACT-DREADBOW-CONTRACTS-1.0.10.json) · [equipamento Dreadbow](equipment/dreadbow.md) |
| ⚠️ | `alexscaves:dazing_sweep` | [Ficha técnica parcial](enchantments/dazing-sweep.md) · [consumer e recurso SHA-exatos já selados](EXACT-EFFECT-CONTRACTS-1.0.10.json) · [efeito Stunned](effects/stunned.md) |
| ⚠️ | `alexscaves:detonating_death` | [Ficha técnica parcial](enchantments/detonating-death.md) · [JAR 1.0.10 e explosão já selados](EXACT-TECHNICAL-CONTRACTS-1.0.10.json) · [ação Totem of Possession](actions/totem-possession-remote-control.md) |
| ⚠️ | `alexscaves:double_stab` | [Ficha técnica parcial](enchantments/double-stab.md) · [JAR 1.0.10 e quantidade de dagas](EXACT-DESOLATE-DAGGER-CONTRACTS-1.0.10.json) · [equipamento Desolate Dagger](equipment/desolate-dagger.md) |
| ⚠️ | `alexscaves:energy_efficiency` | [Ficha técnica parcial](enchantments/energy-efficiency.md) · [referência SHA-exata do Raygun](EXACT-RAYGUN-CONTROL-1.0.10.json) · [limites de charge/rede](damage-types/raygun.md) |
| ⚠️ | `alexscaves:enveloping_bubble` | [Ficha técnica parcial](enchantments/enveloping-bubble.md) · [ação Sea Staff](actions/sea-staff-water-bolt.md) · [efeito Bubbled](effects/bubbled.md) · [manifesto SHA-exato](EXACT-TECHNICAL-CONTRACTS-1.0.10.json) |
| ⚠️ | `alexscaves:explosive_flavor` | [Ficha técnica parcial](enchantments/explosive-flavor.md) · [Shot Gum](equipment/shot-gum.md) · [Gumball](damage-types/gumball.md) · [manifesto SHA-exato](EXACT-GUMBALL-CONTRACTS-1.0.10.json) |
| ⚠️ | `alexscaves:far_flung` | [Ficha técnica parcial](enchantments/far-flung.md) · [manifesto SHA-exato 1.0.10](EXACT-FAR-FLUNG-1.0.10.json) · [sonda read-only](../../../../docs/qa/alexscaves_1010_far_flung_probe.py) |
| ⚠️ | `alexscaves:ferrous_haste` | [Ficha técnica parcial](enchantments/ferrous-haste.md) · [manifesto SHA-exato 1.0.10](EXACT-FERROUS-HASTE-1.0.10.json) · [Crystallization](enchantments/crystallization.md) |
| ❌ | `alexscaves:field_extension` | Não localizada nos 45 manifestos selecionados |
| ❌ | `alexscaves:flinging` | Não localizada nos 45 manifestos selecionados |
| ⚠️ | `alexscaves:gamma_ray` | [`EXACT-RAYGUN-CONTROL-1.0.10.json`](EXACT-RAYGUN-CONTROL-1.0.10.json) |
| ❌ | `alexscaves:heavy_slam` | Não localizada nos 45 manifestos selecionados |
| ⚠️ | `alexscaves:herd_phalanx` | [`EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json`](EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json) |
| ⚠️ | `alexscaves:humungous_hex` | [`EXACT-TECHNICAL-CONTRACTS-1.0.10.json`](EXACT-TECHNICAL-CONTRACTS-1.0.10.json) |
| ⚠️ | `alexscaves:impending_stab` | [`EXACT-DESOLATE-DAGGER-CONTRACTS-1.0.10.json`](EXACT-DESOLATE-DAGGER-CONTRACTS-1.0.10.json) |
| ⚠️ | `alexscaves:lasting_morale` | [`EXACT-TECHNICAL-CONTRACTS-1.0.10.json`](EXACT-TECHNICAL-CONTRACTS-1.0.10.json) |
| ⚠️ | `alexscaves:multiple_mint` | [`EXACT-TECHNICAL-CONTRACTS-1.0.10.json`](EXACT-TECHNICAL-CONTRACTS-1.0.10.json) |
| ⚠️ | `alexscaves:peppermint_punting` | [`EXACT-TECHNICAL-CONTRACTS-1.0.10.json`](EXACT-TECHNICAL-CONTRACTS-1.0.10.json) |
| ⚠️ | `alexscaves:plummeting_flight` | [`EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json`](EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json) |
| ⚠️ | `alexscaves:precise_volley` | [`EXACT-DREADBOW-CONTRACTS-1.0.10.json`](EXACT-DREADBOW-CONTRACTS-1.0.10.json) |
| ⚠️ | `alexscaves:rapid_possession` | [`EXACT-TECHNICAL-CONTRACTS-1.0.10.json`](EXACT-TECHNICAL-CONTRACTS-1.0.10.json) |
| ⚠️ | `alexscaves:relentless_darkness` | [`EXACT-DREADBOW-CONTRACTS-1.0.10.json`](EXACT-DREADBOW-CONTRACTS-1.0.10.json) |
| ⚠️ | `alexscaves:sated_blade` | [`EXACT-DESOLATE-DAGGER-CONTRACTS-1.0.10.json`](EXACT-DESOLATE-DAGGER-CONTRACTS-1.0.10.json) |
| ❌ | `alexscaves:sea_swing` | Não localizada nos 45 manifestos selecionados |
| ⚠️ | `alexscaves:seapairing` | [`EXACT-TECHNICAL-CONTRACTS-1.0.10.json`](EXACT-TECHNICAL-CONTRACTS-1.0.10.json) |
| ❌ | `alexscaves:second_wave` | Não localizada nos 45 manifestos selecionados |
| ⚠️ | `alexscaves:seekcandy` | [`EXACT-TECHNICAL-CONTRACTS-1.0.10.json`](EXACT-TECHNICAL-CONTRACTS-1.0.10.json) |
| ⚠️ | `alexscaves:shaded_respite` | [`EXACT-DREADBOW-CONTRACTS-1.0.10.json`](EXACT-DREADBOW-CONTRACTS-1.0.10.json) |
| ❌ | `alexscaves:sharp_cane` | Não localizada nos 45 manifestos selecionados |
| ⚠️ | `alexscaves:sightless` | [`EXACT-TECHNICAL-CONTRACTS-1.0.10.json`](EXACT-TECHNICAL-CONTRACTS-1.0.10.json) |
| ⚠️ | `alexscaves:soak_seeking` | [`EXACT-TECHNICAL-CONTRACTS-1.0.10.json`](EXACT-TECHNICAL-CONTRACTS-1.0.10.json) |
| ❌ | `alexscaves:solar` | Não localizada nos 45 manifestos selecionados |
| ⚠️ | `alexscaves:spell_lasting` | [`EXACT-TECHNICAL-CONTRACTS-1.0.10.json`](EXACT-TECHNICAL-CONTRACTS-1.0.10.json) |
| ❌ | `alexscaves:straight_hook` | Não localizada nos 45 manifestos selecionados |
| ❌ | `alexscaves:swiftwood` | Não localizada nos 45 manifestos selecionados |
| ⚠️ | `alexscaves:targeted_ricochet` | [`EXACT-GUMBALL-CONTRACTS-1.0.10.json`](EXACT-GUMBALL-CONTRACTS-1.0.10.json) |
| ⚠️ | `alexscaves:taxing_bellow` | [`EXACT-TECHNICAL-CONTRACTS-1.0.10.json`](EXACT-TECHNICAL-CONTRACTS-1.0.10.json) |
| ⚠️ | `alexscaves:triple_splash` | [`EXACT-TECHNICAL-CONTRACTS-1.0.10.json`](EXACT-TECHNICAL-CONTRACTS-1.0.10.json) |
| ⚠️ | `alexscaves:triple_split` | [`EXACT-GUMBALL-CONTRACTS-1.0.10.json`](EXACT-GUMBALL-CONTRACTS-1.0.10.json) |
| ❌ | `alexscaves:tsunami` | Não localizada nos 45 manifestos selecionados |
| ⚠️ | `alexscaves:twilight_perfection` | [`EXACT-DREADBOW-CONTRACTS-1.0.10.json`](EXACT-DREADBOW-CONTRACTS-1.0.10.json) |
| ⚠️ | `alexscaves:x_ray` | [`EXACT-RAYGUN-CONTROL-1.0.10.json`](EXACT-RAYGUN-CONTROL-1.0.10.json) |

## Consumidores selecionados que já possuem evidência causal parcial

**`gamma_ray` e `x_ray`:** a [ficha Raygun](damage-types/raygun.md) e os manifestos [desvios de condicionais](EXACT-RAYGUN-CONDITION-BRANCHES-1.0.10.json), [consumidores de ramos](EXACT-RAYGUN-BRANCH-CONSUMERS-1.0.10.json) e [guards de radiação](EXACT-RAYGUN-RADIATION-GUARDS-1.0.10.json) documentam seleções de condições compiladas. Na região observada, `gamma_ray` seleciona dano **solicitado** 2,0f/1,5f e status `Irradiated` de 800 ticks com amplifier 4/0; `x_ray` seleciona caminhos distintos de targeting/trace. Esses fatos **não** comprovam ficha individual integral, valores finais de alcance ou dano, identidade de um hook, efeito aceito, autenticação de pacote, PvP, claims, datapacks ativos ou testagem física.

**Demais referências:** os manifestos de [ações](EXACT-TECHNICAL-CONTRACTS-1.0.10.json), [Dreadbow](EXACT-DREADBOW-CONTRACTS-1.0.10.json), [Desolate Dagger](EXACT-DESOLATE-DAGGER-CONTRACTS-1.0.10.json), [Gumball](EXACT-GUMBALL-CONTRACTS-1.0.10.json) e [Spirit Dinosaur](EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json) ajudam a localizar pontos de partida. A presença de um token em seus manifestos não foi promovida a prova de funcionamento, efeitos completos, nível/custo/slots ou comportamento de encantamento. Vários manifestos podem repetir um mesmo nome e devem ser deduplicados por ID do recurso.

## Critério de conclusão por encantamento

Para substituir ⚠️/❌ por ✅, verificar no **JAR 1.0.10**: (1) recurso JSON completo e registro/mod ID; (2) níveis, valores, custo, exclusividade e slots aplicáveis; (3) consumidor Java real com owner, descriptor, parâmetros e checkpoints; (4) aquisição, ordem causal, custos/recursos e consequências; (5) targeting, dano/tipo, alcance/área, tempo e projétil quando aplicáveis; (6) suporte real de mutação, autoria/servidor, replay/procs e coexistência; (7) QA explícita. Marcar `N/A` quando demonstrado. Sem hook verificado, **⛔ fail-closed** para perks que modificam o pipeline do provider.

A **próxima identidade em ordem alfabética** é `alexscaves:field_extension`; a continuação deve aproveitar as evidências já seladas por ação/equipamento e investigar os dados ausentes, sem repetir suas auditorias. A fila global continua no **Alex's Caves Continued**; Raygun e Tremorzilla Beam permanecem **28/30** contratos técnicos de fichas *já observadas*.
