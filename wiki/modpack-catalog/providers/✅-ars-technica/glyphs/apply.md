# Ars Technica 2.7.6 — Apply

Estado: ✅ identidade source/JAR registry; ⚠️ implementação física, config, addons e QA; ⛔ bridge de perk não implementada.

## Identidade e provenance

- **Registry ID:** `ars_technica:glyph_apply`. Tipo: **Effect**; Tier source: **I**; mana default: **80**; escola: **Manipulation**.
- **Augments:** AOE, Pierce. Valores são defaults do source pin, não custo efetivamente debitado no modpack.
- **JAR instalado:** `ars_technica-1.21.1-2.7.6.jar`, SHA-1 físico `adb2641d538375f6eff6a22f0196bb330ab0b171`; registro 11/11 comprovado em auditoria binária anterior.
- **Fonte da classe:** [`EffectApply.java`](https://github.com/zeroregard/Ars-Technica/blob/bf34b58ff8908837e5894dee773d3afbd98aa3e3/src/main/java/com/zeroregard/ars_technica/glyphs/EffectApply.java), commit `bf34b58ff8908837e5894dee773d3afbd98aa3e3`. Não há prova de igualdade byte-a-byte do método com o JAR físico. Host de compilação Ars 5.11.0 e Create 6.0.8 diferem dos hosts instalados Ars 5.13.1 / Create 6.0.10.

## Engenharia para perks — caminho causal individual

- **Fonte de item:** `PlayerCaster` usa **offhand** do player; caster embrulhado não-player usa `InventoryManager.findItem` para primeiro extratável. Sem fonte válida, branch Block pode cair para coleta de ItemEntity; item source permanece provider-owned.
- **Block path:** `SpellUtil.calcAOEBlocks(...,AOE,count(Pierce))`, procura receita de Create item application/deploying, eventualmente consome aplicador e modifica bloco via `world.setBlock(pos,resultBlock.defaultBlockState(),3)` ou gera ItemEntity com output. **O método não exibe checagem de claim explícita local**: testar permissões através do pipeline completo; não declarar bypass.
- **Item path:** `maxAmount=4*(1+(int)Math.round(aoeMultiplier))`; para cada stack válida, aplica `ItemApplicationRecipe` ou `DeployerApplicationRecipe` e decrementa ingredientes/stack, gera outputs como ItemEntity. O nested `InventoryApplyItemSource.consumeItems(count)` chama `manager.extractItem(...,1)` independentemente de count: discrepância source-level de contabilidade a validar no host físico antes de alegar dupe.
- **Perks:** receita Create, consumo do aplicador, trocas de bloco e sobras são uma única transação sob o provider; nenhuma perk RPG pode replicá-los em handler genérico.

## Authority, gap e critérios de implementação

- **Authority:** Ars Nouveau mantém a gramática, mana, spell context e casting; Ars Technica mantém processamento auxiliar, itens/fluidos e receita; Create mantém suas recipes e capacidades. RPG Skill Tree só progression/perks/gates via contrato real, não executa a conversão/efeitos.
- **Gap de magia original:** reproduzir uma receita Create com VFX não estabelece identidade de magia Black Arcana. Requer mecanismo original distinto, custos transacionais, proof de targeting, caps/performance, e WorldEffectPolicy para efeitos próprios sobre blocos.
- **Status de hook:** ⛔ sem adapter ou mutabilidade específica provada/testada. ⚠️ Precisa validar jar 2.7.6 contra host 5.13.1, receitas/datapack, reivindicações/protection, FakePlayer, restart, contagem de item/fluido, ciclo das entidades e causalidade exactly-once.
