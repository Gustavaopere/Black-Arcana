# ImpactFrameHandler / ChromaticAberrationHandler — clamps S2C — Ace's Spell Utils 1.2.7.2

**Tipo:** superfície de manutenção/routing de VFX do provider · **Estado:** ⚠️ contrato source-pinned, QA física fail-closed.

## Arquivos exatos e responsabilidades

- [`utils/ImpactFrameHandler.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/ImpactFrameHandler.java)
- [`utils/ChromaticAberrationHandler.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/ChromaticAberrationHandler.java)
- [`network/TriggerImpactFramePacket.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/TriggerImpactFramePacket.java)
- [`network/TriggerChromaticAberrationPacket.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/TriggerChromaticAberrationPacket.java)
- [`client/impactframe/ImpactFrameTimeline.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/client/impactframe/ImpactFrameTimeline.java) e [`ImpactFrameEffect.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/client/impactframe/ImpactFrameEffect.java)
- [`client/chromaticaberration/ChromaticAberrationTimeline.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/client/chromaticaberration/ChromaticAberrationTimeline.java) e [`ChromaticAberrationEffect.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/client/chromaticaberration/ChromaticAberrationEffect.java)

**Fluxo source:** `ImpactFrameHandler` possui defaults `DEFAULT_THRESHOLD=0.5f`, `DEFAULT_FLICKER_TICKS=3` e `DEFAULT_ABERRATION_STRENGTH=0`, com overloads para player ou coleção. Antes do envio limita intensity/threshold/aberration a `0..1`, duration/flicker a pelo menos `1`. `ChromaticAberrationHandler` também suporta player ou coleção, limita strength a `0..1` e duration ticks a pelo menos `1`; os dois usam `PacketDistributor.sendToPlayer` para cada destinatário.

**Targeting/range/tempo/consumo:** Render dos clientes explicitamente destinatários; não há AABB/hitbox e não há mana/cooldown próprios. Os clamps são do produtor, e o pacote tem codec separado.

**Risco e dependências:** Não estender esses clamps para novas classes de pacote sem verificação: o decoder não repete validação em todos os campos. Impact frame rápido e shader podem prejudicar acessibilidade; QA de intensidade, concorrência, unload e cliente necessária.

## Timelines e concorrência no cliente

`ImpactFrameTimeline.start` substitui a execução anterior, zera elapsedTicks e limita duração a **1..1200 ticks**; intensity/threshold/aberration a **0..1**, com NaN→0/0.5/0. A duração por fase é `clamp(flickerTicks,1,max(1,duration/3))`: são três fases normal → invertida → normal, cada uma com esse comprimento, depois fade linear até expiry. `flickerTicks` **não é a duração total das três fases**. A aberração embutida acompanha a intensidade relativa; intensidade zero produz força zero. Bright/dark são RGB extraídos dos ints; não há alpha de combate.

`ChromaticAberrationTimeline` também é singleton/substituição e dura **1..1200 ticks**: conserva strength na primeira metade e faz fade linear na segunda. Seu `start` trata NaN como 0 e impõe só limite inferior 0, **sem clamp superior 1**; o helper de envio aplica 0..1, mas construção direta do packet não equivale a essa validação. O timeline de impact frame limita seus próprios floats separadamente.

Os Effect carregam PostChains `aces_spell_utils:shaders/impact_frame.json` e `aces_spell_utils:shaders/chromatic_aberration.json`, redimensionam com o render target e fecham a chain ao ficar inativos. IOException/RuntimeException marca `failed=true` e desabilita o efeito sem reset/retry explícito nessas classes. O calendário/processamento e a ordem entre efeitos estão em [VFX cliente](../systems/vfx-client-payloads.md); não existe stack de instâncias por caster nestes dois timelines.

## Interoperabilidade e QA

Esse sistema faz apresentação e manutenção do provider. Não cria `AbstractSpell` nem prova hit, gasto de mana, proc, ganho de Mastery ou atualização do mundo. Black Arcana permanece authority para seu próprio casting/hazards/domains/rituais/WorldEffectPolicy/Strain/Corruption/Arcane Danger; RPG Skill Tree só progressão com gates reais. Não implementar segundo handler de estado a partir de evento puramente visual.

Fonte `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, versão source `1.2.7.2-1.21.1`; arquivo físico catalogado `aces_spell_utils-1.2.7.2-1.21.1.jar` SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` sem verificação de classfile. Build source depende Iron's `3.16.2`; modpack declara `3.16.3`. **QA:** JAR e event handlers reais, client/dedicated server, tracking/clear/teleport, cenários multicaster, packet sequencing e budgets gráficos; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `COMPLETE_PERK_READY=false`.
