# Ars Technica 2.7.6 — Carve

Estado: ✅ identidade source/JAR registry; ⚠️ implementação física, config, addons e QA; ⛔ bridge de perk não implementada.

## Identidade e provenance

- **Registry ID:** `ars_technica:glyph_carve`. Tipo: **Effect**; Tier source: **I**; mana default: **10**; escola: **Manipulation**.
- **Augments:** Amplify, Dampen, AOE. Valores são defaults do source pin, não custo efetivamente debitado no modpack.
- **JAR instalado:** `ars_technica-1.21.1-2.7.6.jar`, SHA-1 físico `adb2641d538375f6eff6a22f0196bb330ab0b171`; registro 11/11 comprovado em auditoria binária anterior.
- **Fonte da classe:** [`EffectCarve.java`](https://github.com/zeroregard/Ars-Technica/blob/bf34b58ff8908837e5894dee773d3afbd98aa3e3/src/main/java/com/zeroregard/ars_technica/glyphs/EffectCarve.java), commit `bf34b58ff8908837e5894dee773d3afbd98aa3e3`. Não há prova de igualdade byte-a-byte do método com o JAR físico. Host de compilação Ars 5.11.0 e Create 6.0.8 diferem dos hosts instalados Ars 5.13.1 / Create 6.0.10.

## Engenharia para perks — caminho causal individual

- **Admissão/seleção:** herda `AbstractItemResolveEffect.onResolve`, que reúne `ItemEntity` em AABB de raio por eixo `2 + spellStats.getAoeMultiplier()` e agrupa as entidades por `Item`. Busca primeiro receita vanilla `STONECUTTING` válida para o item; se ausente, tenta Create `CUTTING`/`CuttingRecipe`.
- **Escolha por AMP:** `amplifier<0` pede resultado cujo identificador descritivo contenha `slab`; `>0` procura `wall` em Stonecutting e `stairs` no branch Create saw; zero procura `stairs`. Critério de matching é substring da `getDescriptionId` do item resultante, não contrato semântico universal de bloco; pode depender de datapacks e traduções de objetos.
- **Liquidação:** para cada entity com recipe, computa `inputCount * outputCount`, divide em stacks pelo maxStackSize, gera ItemEntity e então descarta a entity original. Métodos alternativos de crafting de slab/stair/wall estão presentes na classe mas **não são invocados por onResolveEntities nesta revisão**; não somar suas saídas.
- **Perks/risco:** limite padrão Amplify/Dampen 1. Não executar nova conversão de itens pelo RPG, nem emitir Mastery por unidade transformada; recipes de Create, overflow de contagem e deduplicação demandam QA.

## Authority, gap e critérios de implementação

- **Authority:** Ars Nouveau mantém a gramática, mana, spell context e casting; Ars Technica mantém processamento auxiliar, itens/fluidos e receita; Create mantém suas recipes e capacidades. RPG Skill Tree só progression/perks/gates via contrato real, não executa a conversão/efeitos.
- **Gap de magia original:** reproduzir uma receita Create com VFX não estabelece identidade de magia Black Arcana. Requer mecanismo original distinto, custos transacionais, proof de targeting, caps/performance, e WorldEffectPolicy para efeitos próprios sobre blocos.
- **Status de hook:** ⛔ sem adapter ou mutabilidade específica provada/testada. ⚠️ Precisa validar jar 2.7.6 contra host 5.13.1, receitas/datapack, reivindicações/protection, FakePlayer, restart, contagem de item/fluido, ciclo das entidades e causalidade exactly-once.
