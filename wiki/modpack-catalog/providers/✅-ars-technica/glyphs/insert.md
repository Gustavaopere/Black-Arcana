# Ars Technica 2.7.6 — Insert

Estado: ✅ identidade source/JAR registry; ⚠️ implementação física, config, addons e QA; ⛔ bridge de perk não implementada.

## Identidade e provenance

- **Registry ID:** `ars_technica:glyph_insert`. Tipo: **Effect**; Tier source: **I (herdado no Ars host compilado)**; mana default: **15**; escola: **Manipulation**.
- **Augments:** AOE, Split. Valores são defaults do source pin, não custo efetivamente debitado no modpack.
- **JAR instalado:** `ars_technica-1.21.1-2.7.6.jar`, SHA-1 físico `adb2641d538375f6eff6a22f0196bb330ab0b171`; registro 11/11 comprovado em auditoria binária anterior.
- **Fonte da classe:** [`EffectInsert.java`](https://github.com/zeroregard/Ars-Technica/blob/bf34b58ff8908837e5894dee773d3afbd98aa3e3/src/main/java/com/zeroregard/ars_technica/glyphs/EffectInsert.java), commit `bf34b58ff8908837e5894dee773d3afbd98aa3e3`. Não há prova de igualdade byte-a-byte do método com o JAR físico. Host de compilação Ars 5.11.0 e Create 6.0.8 diferem dos hosts instalados Ars 5.13.1 / Create 6.0.10.

## Engenharia para perks — caminho causal individual

- **Scan espacial:** `AbstractItemResolveEffect` lê ItemEntity em AABB `2+aoe`; depois `getContainersInArea(pos,world,(int)(2+aoe))` varre **cada BlockPos** do cubo e seleciona BlockEntity que implementa `Container`. AOE grande cresce cubicamente, exigindo budget.
- **Sem Split:** usa `StorageHelpers.getValidStorePos` e `ItemHandlerHelper.insertItemStacked(handler,stack,false)`; descarta ItemEntity só quando inserted íntegro, senão mantém residual. **Com Split:** divide `totalItems/validPositions.size()` e resto por alvo, insere em cada cap e recalcula stack residual.
- **Risco source-only:** `processItemsSplit` calcula divisão/módulo por `validPositions.size()` sem teste local para lista vazia; a lista vem de helper e pode ter condição não óbvia. Não afirmar crash runtime sem teste. Tier I é herdado de `AbstractSpellPart.defaultTier()` da dependência Ars 5.11.0, não explícito em EffectInsert.
- **Perks:** não conceder ganho por quantidade de recipientes ou recolher stacks duas vezes. Observar capacidade NeoForge de cada container e invariantes de duplicação.

## Authority, gap e critérios de implementação

- **Authority:** Ars Nouveau mantém a gramática, mana, spell context e casting; Ars Technica mantém processamento auxiliar, itens/fluidos e receita; Create mantém suas recipes e capacidades. RPG Skill Tree só progression/perks/gates via contrato real, não executa a conversão/efeitos.
- **Gap de magia original:** reproduzir uma receita Create com VFX não estabelece identidade de magia Black Arcana. Requer mecanismo original distinto, custos transacionais, proof de targeting, caps/performance, e WorldEffectPolicy para efeitos próprios sobre blocos.
- **Status de hook:** ⛔ sem adapter ou mutabilidade específica provada/testada. ⚠️ Precisa validar jar 2.7.6 contra host 5.13.1, receitas/datapack, reivindicações/protection, FakePlayer, restart, contagem de item/fluido, ciclo das entidades e causalidade exactly-once.
