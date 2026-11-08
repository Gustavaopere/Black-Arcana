# Alex's Caves Continued 1.0.10 — índice de 51 encantamentos para perks

> Identidades dos 51 JSONs publisher e dossiers individuais são contagens diferentes. A conclusão abaixo é do **contrato técnico estático**, independente de hook mutador e QA física. Referências históricas a nomes/símbolos em outros manifestos permanecem úteis, mas não bastam para concluir outro encantamento.

```text
scope=INDIVIDUAL_STATIC_ENCHANTMENT_CATALOG_AND_HISTORICAL_CROSSWALK
mod_id=alexscaves
version=1.0.10
artifact_sha1=6960b299a39a039ac8a5eb9b07be4ad0e3e0a570
artifact_sha256=36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c
identity_resources_seen=51/51
individual_full_enchantment_dossiers=19/51
individual_partial_enchantment_dossiers=20/51
individual_existing_enchantment_dossiers=39/51
whole_provider_catalog_closed=false
mutating_hook=NOT_VERIFIED
physical_qa=NOT_TESTED
mutation=NO_MUTATION
executable_perk_certification=NOT_CERTIFIED
```

**Barra dos contratos técnicos estáticos dos 51 encantamentos:** `███████░░░░░░░░░░░░░ 37.3% (19/51)`.

**Barra de dossiers individuais existentes, completos ou parciais:** `███████████████░░░░░ 76.5% (39/51)`; destes, vinte permanecem parciais, enquanto Heavy Slam, Herd Phalanx, Humungous Hex, Impending Stab, Lasting Morale, Multiple Mint, Peppermint Punting, Plummeting Flight, Precise Volley, Rapid Possession, Relentless Darkness, Sated Blade, Sea Swing, Seapairing, Second Wave, Seekcandy, Shaded Respite, Sharp Cane e Sightless possuem contratos estáticos individuais certificados.

**Sea Swing (✅ contrato estático):** [ficha individual](enchantments/sea-swing.md), [manifesto exato](EXACT-SEA-SWING-STATIC-1.0.10.json) e [prova de métodos e NBT](EXACT-SEA-SWING-STATIC-1.0.10.md) comprovam produtor Ortholance e 20 métodos completos + dois construtores nativos, incluindo owner, parâmetros, alvo, dano solicitado e descarte. Hook mutador e QA física continuam **NOT_VERIFIED/NOT_TESTED**; fonte 1.1.1 é corroboração sem paridade alegada.

**Sharp Cane:** [ficha estática](enchantments/sharp-cane.md) e [prova reproduzível](EXACT-SHARP-CANE-CONTRACT-1.0.10.md) distinguem snapshot `3F×L`, busca de alvo no tick, atribuição de UUID e pedido de dano com retorno descartado. `onHitEntity` não chama hurt nesse corpo; tick integral, persistência herdada e engine conservam fronteiras próprias. Não homologa hook ou QA física.

**Shaded Respite:** [ficha estática](enchantments/shaded-respite.md) e [prova reproduzível](EXACT-SHADED-RESPITE-CONTRACT-1.0.10.md) distinguem luz calculada abaixo de 11, desgaste dispensado e isenção de munição somente para `Items.ARROW`. O início de uso ainda exige munição ou creative; release e callback Relentless têm custos próprios. Não homologa factories externas, hook ou QA física.

**Soak Seeking:** [ficha estática](enchantments/soak-seeking.md) e [prova individual SHA-exata](EXACT-SOAK-SEEKING-STATIC-1.0.10.md) fixam `seekAmount=0.3F+0.2F×L`, guardas server-side e homing; a comparação `(double)0.3F > 0.3D` é verdadeira mesmo no baseline, e o bolt filho de ricochete não herda o parâmetro. Não homologa alcance final, dano efetivo, hook mutador ou QA física.

**Seapairing:** [ficha estática](enchantments/seapairing.md) e [prova reproduzível](EXACT-SEAPAIRING-CONTRACT-1.0.10.md) documentam selected ignorado, igualdade da stack em uso, RNG antes de água/chuva/bolhas e pedido literal `min(0,D−1)`. O setter da engine e o reparo aplicado permanecem fronteiras externas; não homologa hook ou QA física.

**Sated Blade:** [ficha estática](enchantments/sated-blade.md) e [prova reproduzível](EXACT-SATED-BLADE-CONTRACT-1.0.10.md) delimitam hurt aceito, fonte Player, saturação anterior<5 e pedido +0,1×L; a ausência de binding no produtor impede presumir benefício ao atacante. Não homologa heal, hook ou QA física.

**Relentless Darkness:** [ficha estática](enchantments/relentless-darkness.md) e [prova reproduzível](EXACT-RELENTLESS-DARKNESS-CONTRACT-1.0.10.md) distinguem `%3` do timer restante, M5/incremento3 visual, 1/2 tentativas de flechas e custos por callback; não homologam DPS, inserção, hook ou QA física.

**Rapid Possession:** [ficha técnica estática](enchantments/rapid-possession.md) e [selo SHA-exato](EXACT-RAPID-POSSESSION-CONTRACT-1.0.10.md) verificam o fator `1,25+0,35×L` no movimento do Totem; navegação Mob, aceleração não-Mob e raio `32×ramp` são superfícies separadas. Custos, binding e ataques permanecem provider-native. Não homologa velocidade física, hook mutador ou multiplayer.

**Precise Volley:** [ficha técnica estática](enchantments/precise-volley.md) e [selo SHA-exato](EXACT-PRECISE-VOLLEY-CONTRACT-1.0.10.md) fixam que `L>0` zera a imprecisão do disparo e seleciona `shadowArrowDamage=2F` em vez de 3F para Dark Arrows; quantidade, caixa de spawn, mira e custos seguem nativos. Não homologa hit, altura, dano efetivo ou perk mutadora.

**Plummeting Flight:** [ficha técnica estática](enchantments/plummeting-flight.md) e [selo exato individual](EXACT-PLUMMETING-FLIGHT-CONTRACT-1.0.10.md) documentam `0,03+0,005×L` no delta vertical do espírito e limite `duration<40+5L` para transporte, mas não homologam altura final, dano novo, física ou hook mutador. Reutiliza Spirit Dinosaur sem acrescentar raiz mágica.

**Peppermint Punting:** [ficha técnica estática](enchantments/peppermint-punting.md) e [prova compacta SHA-exata](EXACT-PEPPERMINT-PUNTING-CONTRACT-1.0.10.md) mostram que o nível positivo seleciona `Straight`, yaw inicial e cooldown 20, com overrides de Seekcandy e tick independentes; não multiplica o dano 3F, não altera o número de peppermints e não homologa hook ou QA física.

**Multiple Mint:** [ficha estática](enchantments/multiple-mint.md) e [prova reproduzível](EXACT-MULTIPLE-MINT-CONTRACT-1.0.10.md) documentam `3+L` como quantidade solicitada e denominador angular, sem promover tentativas de spawn a inserções aceitas, dano proporcional ou hook seguro.

**Lasting Morale:** [ficha estática](enchantments/lasting-morale.md) e [prova reproduzível](EXACT-LASTING-MORALE-CONTRACT-1.0.10.md) documentam a variável `1200+400L` compartilhada entre contador dos summons e cooldown por Item; fade, aceitação de spawn e NBT condicionado ao UUID são fronteiras separadas.

**Impending Stab:** [ficha individual estática](enchantments/impending-stab.md) e [selo/reprodução](EXACT-IMPENDING-STAB-CONTRACT-1.0.10.md) reaproveitam a cadeia Desolate Dagger. A espera inicial é 40–49 para qualquer nível positivo, enquanto o stab relê a stack e solicita 2+2L; autoria, exclusividade, descarte e persistência conservam fronteiras próprias.

**Humungous Hex:** [ficha técnica estática](enchantments/humungous-hex.md), [selo exato 1.0.10](EXACT-HUMUNGOUS-HEX-CONTRACT-1.0.10.json) e [resumo de reprodução](EXACT-HUMUNGOUS-HEX-CONTRACT-1.0.10.md). A escala `1+0,25×L` modifica a largura da Hex (4/5/6 nos níveis 0/I/II), mas o consumidor conserva o limite independente `distanceTo<=4` além da AABB. Renderer cliente, dano 1F/6F e duração Spell Lasting são ramos distintos; hook e QA física não foram homologados. O número de fichas parciais não muda.

**Herd Phalanx:** [ficha individual completa no escopo estático](enchantments/herd-phalanx.md) e [prova reaproveitando Spirit Dinosaur](EXACT-HERD-PHALANX-CONTRACT-1.0.10.md). O nível altera 3+L tentativas de Grotto; consumo, órbita, cleanup e pedido de dano zero no Pre conservam seus guards. A entrada não certifica outros espíritos nem reduz os vinte dossiers parciais anteriores.

**Heavy Slam:** [ficha completa no escopo estático](enchantments/heavy-slam.md) e [prova reproduzível](EXACT-HEAVY-SLAM-CONTRACT-1.0.10.md). JSON, níveis, custos, slots, aquisição, consumidor, dano, área, cadência, movimento e estado estão documentados; hooks e QA física continuam pendentes. Gamma Ray e as dezenove fichas parciais anteriores são preservadas.

## Leitura dos estados

- ✅ **Contrato técnico estático concluído:** Heavy Slam, Herd Phalanx, Humungous Hex, Impending Stab, Lasting Morale, Multiple Mint, Peppermint Punting, Plummeting Flight, Precise Volley, Rapid Possession, Relentless Darkness, Sated Blade, Sea Swing, Seapairing, Second Wave, Seekcandy, Shaded Respite, Sharp Cane e Sightless, sustentados por certificados individuais, hashes e auditoria do JAR. Não significa integração mutadora ou teste físico aprovado.
- ⚠️ **Referência histórica/parcial:** o objeto tem evidências nominais ou consumidor em outro recorte; vários ainda não têm ficha própria. Não promover conclusão por associação a outro equipamento/ação.
- ❌ **Sem ficha individual no checkpoint histórico:** preserva a pendência existente; não prova inexistência do recurso, ausência de referências ou comportamento.

Os percentuais antigos de rastreio nominal eram checkpoints de recortes selecionados e misturavam IDs minúsculos e campos JVM. Eles não são recontados como certificação nesta entrega. As barras atuais usam apenas o inventário publisher de 51 IDs, os ficheiros individuais existentes e o ledger de certificados. A relação nominal abaixo é histórica fora das linhas com certificado individual; não é uma nova varredura integral dos consumidores de todos os encantamentos.

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
| ⚠️ | `alexscaves:field_extension` | [Ficha técnica parcial](enchantments/field-extension.md) · [manifesto SHA-exato 1.0.10](EXACT-FIELD-EXTENSION-1.0.10.json) · [Ferrous Haste](enchantments/ferrous-haste.md) |
| ⚠️ | `alexscaves:flinging` | [Ficha técnica parcial](enchantments/flinging.md) · [manifesto SHA-exato 1.0.10](EXACT-FLINGING-1.0.10.json) |
| ⚠️ | `alexscaves:gamma_ray` | [Ficha técnica parcial](enchantments/gamma-ray.md) · [Raygun 1.0.10](EXACT-RAYGUN-CONTROL-1.0.10.json) · [branches Gamma](EXACT-RAYGUN-CONDITION-BRANCHES-1.0.10.json) · [consumidores](EXACT-RAYGUN-BRANCH-CONSUMERS-1.0.10.json) |
| ✅ | `alexscaves:heavy_slam` | [Contrato técnico estático](enchantments/heavy-slam.md) · [JSON/consumidor selados](EXACT-HEAVY-SLAM-CONTRACT-1.0.10.json) · hooks e QA física pendentes |
| ✅ | `alexscaves:herd_phalanx` | [Contrato técnico estático](enchantments/herd-phalanx.md) · [selo individual](EXACT-HERD-PHALANX-CONTRACT-1.0.10.json) · [consumidor Spirit Dinosaur](EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json) · hooks e QA física pendentes |
| ✅ | `alexscaves:humungous_hex` | [Contrato técnico estático](enchantments/humungous-hex.md) · [JSON/classes/renderer SHA-exatos](EXACT-HUMUNGOUS-HEX-CONTRACT-1.0.10.json) · hooks e QA física pendentes |
| ✅ | `alexscaves:impending_stab` | [Contrato técnico estático](enchantments/impending-stab.md) · [selo individual](EXACT-IMPENDING-STAB-CONTRACT-1.0.10.json) · [consumidores Desolate Dagger](EXACT-DESOLATE-DAGGER-CONTRACTS-1.0.10.json) · hooks e QA física pendentes |
| ✅ | `alexscaves:lasting_morale` | [Contrato técnico estático](enchantments/lasting-morale.md) · [selo individual](EXACT-LASTING-MORALE-CONTRACT-1.0.10.json) · tempo/cooldown compartilhados; hooks e QA física pendentes |
| ✅ | `alexscaves:multiple_mint` | [Contrato técnico estático](enchantments/multiple-mint.md) · [selo individual](EXACT-MULTIPLE-MINT-CONTRACT-1.0.10.json) · quantidade/ângulo compartilhados; hooks e QA física pendentes |
| ✅ | `alexscaves:peppermint_punting` | [Contrato técnico estático](enchantments/peppermint-punting.md) · [selo reutilizando Multiple Mint](EXACT-PEPPERMINT-PUNTING-CONTRACT-1.0.10.json) · hooks e QA física pendentes |
| ✅ | `alexscaves:plummeting_flight` | [Contrato estático](enchantments/plummeting-flight.md) · [selo individual SHA-exato](EXACT-PLUMMETING-FLIGHT-CONTRACT-1.0.10.json) · [Spirit Dinosaur](EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json) · hook/QA física pendentes |
| ✅ | `alexscaves:precise_volley` | [Contrato técnico estático](enchantments/precise-volley.md) · [selo individual SHA-exato](EXACT-PRECISE-VOLLEY-CONTRACT-1.0.10.json) · [Dreadbow/Dark Arrow](EXACT-DREADBOW-CONTRACTS-1.0.10.json) · hook/QA física pendentes |
| ✅ | `alexscaves:rapid_possession` | [Contrato técnico estático](enchantments/rapid-possession.md) · [selo SHA-exato](EXACT-RAPID-POSSESSION-CONTRACT-1.0.10.json) · [Totem de Possession preexistente](EXACT-TECHNICAL-CONTRACTS-1.0.10.json) · hook/QA física pendentes |
| ✅ | `alexscaves:relentless_darkness` | [Contrato técnico estático](enchantments/relentless-darkness.md) · [selo individual](EXACT-RELENTLESS-DARKNESS-CONTRACT-1.0.10.json) · cadência contínua e carga visual distintas; hooks e QA física pendentes |
| ✅ | `alexscaves:sated_blade` | [Contrato técnico estático](enchantments/sated-blade.md) · [selo individual](EXACT-SATED-BLADE-CONTRACT-1.0.10.json) · saturação condicional e binding delimitados; hooks e QA física pendentes |
| ✅ | `alexscaves:sea_swing` | [Ficha estática](enchantments/sea-swing.md) · [prova exata de owner/NBT/dano](EXACT-SEA-SWING-STATIC-1.0.10.md); hooks e QA física seguem pendentes |
| ✅ | `alexscaves:seapairing` | [Contrato técnico estático](enchantments/seapairing.md) · [selo individual](EXACT-SEAPAIRING-CONTRACT-1.0.10.json) · reparo passivo e fronteira do setter delimitados; hooks e QA física pendentes |
| ✅ | `alexscaves:second_wave` | [Contrato individual estático](enchantments/second-wave.md) · [prova SHA-exata](EXACT-SECOND-WAVE-STATIC-1.0.10.md) · duas ondas retardadas por iteração; hooks e QA física pendentes |
| ✅ | `alexscaves:seekcandy` | [Contrato individual estático](enchantments/seekcandy.md) · [prova SHA-exata](EXACT-SEEKCANDY-STATIC-1.0.10.md) · targeting Mob/LoS, homing condicionado, speed resetado no tick, owner/NBT; hooks e QA física pendentes |
| ✅ | `alexscaves:shaded_respite` | [Contrato técnico estático](enchantments/shaded-respite.md) · [selo individual](EXACT-SHADED-RESPITE-CONTRACT-1.0.10.json) · luz, munição e desgaste separados; hooks e QA física pendentes |
| ✅ | `alexscaves:sharp_cane` | [Contrato técnico estático](enchantments/sharp-cane.md) · [selo individual](EXACT-SHARP-CANE-CONTRACT-1.0.10.json) · snapshot, busca e callback de hit separados; hooks e QA física pendentes |
| ✅ | `alexscaves:sightless` | [Contrato estático individual](enchantments/sightless.md) · [prova de gates e glow SHA-exata](EXACT-SIGHTLESS-STATIC-1.0.10.md) · olhar dinâmico, limpeza de glow e desgaste cliente; hooks e QA física pendentes |
| ✅ | `alexscaves:soak_seeking` | [Contrato técnico estático individual](enchantments/soak-seeking.md) · [manifesto SHA-exato](EXACT-SOAK-SEEKING-STATIC-1.0.10.json) · [prova reprodutível](EXACT-SOAK-SEEKING-STATIC-1.0.10.md) · hooks e QA física pendentes |
| ❌ | `alexscaves:solar` | Sem ficha individual no checkpoint histórico; ausência de comportamento não comprovada |
| ⚠️ | `alexscaves:spell_lasting` | [`EXACT-TECHNICAL-CONTRACTS-1.0.10.json`](EXACT-TECHNICAL-CONTRACTS-1.0.10.json) |
| ❌ | `alexscaves:straight_hook` | Sem ficha individual no checkpoint histórico; ausência de comportamento não comprovada |
| ❌ | `alexscaves:swiftwood` | Sem ficha individual no checkpoint histórico; ausência de comportamento não comprovada |
| ⚠️ | `alexscaves:targeted_ricochet` | [`EXACT-GUMBALL-CONTRACTS-1.0.10.json`](EXACT-GUMBALL-CONTRACTS-1.0.10.json) |
| ⚠️ | `alexscaves:taxing_bellow` | [`EXACT-TECHNICAL-CONTRACTS-1.0.10.json`](EXACT-TECHNICAL-CONTRACTS-1.0.10.json) |
| ⚠️ | `alexscaves:triple_splash` | [`EXACT-TECHNICAL-CONTRACTS-1.0.10.json`](EXACT-TECHNICAL-CONTRACTS-1.0.10.json) |
| ⚠️ | `alexscaves:triple_split` | [`EXACT-GUMBALL-CONTRACTS-1.0.10.json`](EXACT-GUMBALL-CONTRACTS-1.0.10.json) |
| ❌ | `alexscaves:tsunami` | Sem ficha individual no checkpoint histórico; ausência de comportamento não comprovada |
| ⚠️ | `alexscaves:twilight_perfection` | [`EXACT-DREADBOW-CONTRACTS-1.0.10.json`](EXACT-DREADBOW-CONTRACTS-1.0.10.json) |
| ⚠️ | `alexscaves:x_ray` | [`EXACT-RAYGUN-CONTROL-1.0.10.json`](EXACT-RAYGUN-CONTROL-1.0.10.json) |

## Consumidores selecionados que já possuem evidência causal parcial

**`gamma_ray` e `x_ray`:** a [ficha Raygun](damage-types/raygun.md) e os manifestos [desvios de condicionais](EXACT-RAYGUN-CONDITION-BRANCHES-1.0.10.json), [consumidores de ramos](EXACT-RAYGUN-BRANCH-CONSUMERS-1.0.10.json) e [guards de radiação](EXACT-RAYGUN-RADIATION-GUARDS-1.0.10.json) documentam seleções de condições compiladas. Na região observada, `gamma_ray` seleciona dano **solicitado** 2,0f/1,5f e status `Irradiated` de 800 ticks com amplifier 4/0; `x_ray` seleciona caminhos distintos de targeting/trace. Esses fatos **não** comprovam ficha individual integral, valores finais de alcance ou dano, identidade de um hook, efeito aceito, autenticação de pacote, PvP, claims, datapacks ativos ou testagem física.

**Demais referências:** os manifestos de [ações](EXACT-TECHNICAL-CONTRACTS-1.0.10.json), [Dreadbow](EXACT-DREADBOW-CONTRACTS-1.0.10.json), [Desolate Dagger](EXACT-DESOLATE-DAGGER-CONTRACTS-1.0.10.json), [Gumball](EXACT-GUMBALL-CONTRACTS-1.0.10.json) e [Spirit Dinosaur](EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json) ajudam a localizar pontos de partida. A presença de um token em seus manifestos não foi promovida a prova de funcionamento, efeitos completos, nível/custo/slots ou comportamento de encantamento. Vários manifestos podem repetir um mesmo nome e devem ser deduplicados por ID do recurso.

## Critério de conclusão por encantamento

Para receber ✅ **na coluna de contrato técnico estático**, verificar no JAR 1.0.10: identidade/JSON/registro; comportamento e consumidores; parâmetros/custos/slots; targeting, dano e tempo; recursos e consequências; fronteiras de integração/autoria/servidor; evidência reproduzível e estado de validação explícito. `N/A` exige justificativa. O certificado estático deve manter os estados de hook e QA separados: `mutating_hook=NOT_VERIFIED` e `physical_qa=NOT_TESTED` não são convertidos em aprovações de runtime. Sem hook e aceitação física próprios, **⛔ NO_MUTATION** continua aplicável às perks que alteram o pipeline.

A **próxima identidade em ordem alfabética** sem ficha individual é `alexscaves:solar`; Sightless é modificador de controle do Totem e não cria raiz semântica nova. Sharp Cane, Shaded Respite e os demais contratos anteriores permanecem documentados. A fila global permanece em **Alex's Caves Continued**. Raygun e Tremorzilla Beam continuam parciais; o provider tem agora **48/70 contratos estáticos entre fichas observadas**, incluindo 40 fichas de encantamentos. Esses 69 objetos observados do provider não são o mesmo universo dos 51 recursos de encantamento.
