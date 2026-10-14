# Ars Technica 2.7.6 — Telefeast

Estado: ✅ identidade source/JAR registry; ⚠️ implementação física, config, addons e QA; ⛔ bridge de perk não implementada.

## Identidade e provenance

- **Registry ID:** `ars_technica:glyph_telefeast`. Tipo: **Effect**; Tier source: **II**; mana default: **10**; escola: **Manipulation**.
- **Augments:** Sensitive, Pierce. Valores são defaults do source pin, não custo efetivamente debitado no modpack.
- **JAR instalado:** `ars_technica-1.21.1-2.7.6.jar`, SHA-1 físico `adb2641d538375f6eff6a22f0196bb330ab0b171`; registro 11/11 comprovado em auditoria binária anterior.
- **Fonte da classe:** [`EffectTelefeast.java`](https://github.com/zeroregard/Ars-Technica/blob/bf34b58ff8908837e5894dee773d3afbd98aa3e3/src/main/java/com/zeroregard/ars_technica/glyphs/EffectTelefeast.java), commit `bf34b58ff8908837e5894dee773d3afbd98aa3e3`. Não há prova de igualdade byte-a-byte do método com o JAR físico. Host de compilação Ars 5.11.0 e Create 6.0.8 diferem dos hosts instalados Ars 5.13.1 / Create 6.0.10.

## Engenharia para perks — caminho causal individual

- **Alvo:** onResolveBlock necessita BlockEntity e lê capability `FluidHandler.BLOCK` primeiro; se presente, segue fluid branch; caso contrário `ItemHandler.BLOCK`. Sensitive habilita uso tentativo de itens não-food/drink; Pierce usa `getBuffCount(Pierce)>0` para encaminhar consumível via `ItemProjectileEntity` em vez de aplicá-lo.
- **Lava:** se tanque contém LAVA e não há forwarding, `handler.drain(250,EXECUTE)` e causa `caster.hurt(lavaDamage,50)`; dano da engine/armadura não é valor de vida final garantido. Esse caminho consome um recurso do tanque antes de tentativa de dano, não deve ser reproduzido pelo RPG.
- **Item/potion:** itera slots, pode extrair unidade, tentar uso via `ConsumptionHelper` e devolver sobrante/recipiente. `PotionFlask` passa por `PotionProviderRegistry` e uso restante; fluid recipes de Create Filling podem drenar líquido. O helper/recipe determina efeitos consumíveis reais; o glyph não transfere comida automaticamente de qualquer fonte.
- **Perks:** não tratar encaminhamento de projétil como nova refeição nem duplicar item, tanque ou efeito. Owner do líquido/inventário é Create/NeoForge e provider.

## Authority, gap e critérios de implementação

- **Authority:** Ars Nouveau mantém a gramática, mana, spell context e casting; Ars Technica mantém processamento auxiliar, itens/fluidos e receita; Create mantém suas recipes e capacidades. RPG Skill Tree só progression/perks/gates via contrato real, não executa a conversão/efeitos.
- **Gap de magia original:** reproduzir uma receita Create com VFX não estabelece identidade de magia Black Arcana. Requer mecanismo original distinto, custos transacionais, proof de targeting, caps/performance, e WorldEffectPolicy para efeitos próprios sobre blocos.
- **Status de hook:** ⛔ sem adapter ou mutabilidade específica provada/testada. ⚠️ Precisa validar jar 2.7.6 contra host 5.13.1, receitas/datapack, reivindicações/protection, FakePlayer, restart, contagem de item/fluido, ciclo das entidades e causalidade exactly-once.
