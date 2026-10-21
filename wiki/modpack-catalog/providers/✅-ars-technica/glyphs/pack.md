# Ars Technica 2.7.6 — Pack

Estado: ✅ identidade source/JAR registry; ⚠️ implementação física, config, addons e QA; ⛔ bridge de perk não implementada.

## Identidade e provenance

- **Registry ID:** `ars_technica:glyph_pack`. Tipo: **Effect**; Tier source: **I**; mana default: **10**; escola: **Manipulation**.
- **Augments:** Amplify, Dampen, AOE. Valores são defaults do source pin, não custo efetivamente debitado no modpack.
- **JAR instalado:** `ars_technica-1.21.1-2.7.6.jar`, SHA-1 físico `adb2641d538375f6eff6a22f0196bb330ab0b171`; registro 11/11 comprovado em auditoria binária anterior.
- **Fonte da classe:** [`EffectPack.java`](https://github.com/zeroregard/Ars-Technica/blob/bf34b58ff8908837e5894dee773d3afbd98aa3e3/src/main/java/com/zeroregard/ars_technica/glyphs/EffectPack.java), commit `bf34b58ff8908837e5894dee773d3afbd98aa3e3`. Não há prova de igualdade byte-a-byte do método com o JAR físico. Host de compilação Ars 5.11.0 e Create 6.0.8 diferem dos hosts instalados Ars 5.13.1 / Create 6.0.10.

## Engenharia para perks — caminho causal individual

- **Geometria:** pesquisa ItemEntity pelo helper de AABB (expansão `2+AOE`) e agrupa por item. `getPackGridSize(amplifier)` calcula `clamp((int)amplifier+2,1,3)`: Dampen=-1→1×1, baseline0→2×2, Amplify=1→3×3. Limites padrão Amplify e Dampen de 1 cada.
- **Admissão/settlement:** exige receita `RecipeType.CRAFTING` para grade cheia de `gridSize²` unidades. Para cada grupo calcula `totalPacks = floor(sum(itemCounts)/gridSize²)`, cria cada output por `CraftingHelpers.getItem` e remove `totalPacks*gridSize²` via `ItemHelpers.subtractItemsFromItemEntities`.
- **Perks:** cada recipe pode entregar múltiplas unidades, mas cast continua único; não duplicar output/débito, nem sobrescrever max grid clamp através de atributo RPG. Acesso/validade de receitas e output efetivo pedem QA.

## Authority, gap e critérios de implementação

- **Authority:** Ars Nouveau mantém a gramática, mana, spell context e casting; Ars Technica mantém processamento auxiliar, itens/fluidos e receita; Create mantém suas recipes e capacidades. RPG Skill Tree só progression/perks/gates via contrato real, não executa a conversão/efeitos.
- **Gap de magia original:** reproduzir uma receita Create com VFX não estabelece identidade de magia Black Arcana. Requer mecanismo original distinto, custos transacionais, proof de targeting, caps/performance, e WorldEffectPolicy para efeitos próprios sobre blocos.
- **Status de hook:** ⛔ sem adapter ou mutabilidade específica provada/testada. ⚠️ Precisa validar jar 2.7.6 contra host 5.13.1, receitas/datapack, reivindicações/protection, FakePlayer, restart, contagem de item/fluido, ciclo das entidades e causalidade exactly-once.
