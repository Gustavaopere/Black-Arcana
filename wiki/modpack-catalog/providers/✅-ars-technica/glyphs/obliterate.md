# Ars Technica 2.7.6 — Obliterate

Estado: ✅ identidade source/JAR registry; ⚠️ implementação física, config, addons e QA; ⛔ bridge de perk não implementada.

## Identidade e provenance

- **Registry ID:** `ars_technica:glyph_obliterate`. Tipo: **Effect**; Tier source: **III**; mana default: **100**; escola: **Manipulation**.
- **Augments:** Sensitive, Amplify, Fortune. Valores são defaults do source pin, não custo efetivamente debitado no modpack.
- **JAR instalado:** `ars_technica-1.21.1-2.7.6.jar`, SHA-1 físico `adb2641d538375f6eff6a22f0196bb330ab0b171`; registro 11/11 comprovado em auditoria binária anterior.
- **Fonte da classe:** [`EffectObliterate.java`](https://github.com/zeroregard/Ars-Technica/blob/bf34b58ff8908837e5894dee773d3afbd98aa3e3/src/main/java/com/zeroregard/ars_technica/glyphs/EffectObliterate.java), commit `bf34b58ff8908837e5894dee773d3afbd98aa3e3`. Não há prova de igualdade byte-a-byte do método com o JAR físico. Host de compilação Ars 5.11.0 e Create 6.0.8 diferem dos hosts instalados Ars 5.13.1 / Create 6.0.10.

## Engenharia para perks — caminho causal individual

- **Execução:** onResolveEntity ou onResolveBlock converte impacto em `ArcaneHammerEntity` via `resolve(...)`, faz `newContext=spellContext.makeChildContext()`, `spellContext.setCanceled(true)` e chama `resolver.getNewResolver(newContext)` na criação da entidade; block em Depot ainda chama `hammer.bindDepot(blockPos)`.
- **Augments:** Sensitive determina processamento de itens em vez de destruição no executor downstream, Amplify tamanho/dano, Fortune extração adicional com diminuição de retorno. **Fortune é limitada a 4** pela classe; não há fórmula de dano/loot dentro do método do glyph, portanto não preencher números sem `ArcaneHammerEntity`/config real.
- **Causalidade:** contexto filho e efeitos posteriores do hammer não representam casts novos. WorldEffectPolicy rege efeitos Black Arcana; quem altera blocos no hammer é o provider e requer QA de claims próprio.

## Authority, gap e critérios de implementação

- **Authority:** Ars Nouveau mantém a gramática, mana, spell context e casting; Ars Technica mantém processamento auxiliar, itens/fluidos e receita; Create mantém suas recipes e capacidades. RPG Skill Tree só progression/perks/gates via contrato real, não executa a conversão/efeitos.
- **Gap de magia original:** reproduzir uma receita Create com VFX não estabelece identidade de magia Black Arcana. Requer mecanismo original distinto, custos transacionais, proof de targeting, caps/performance, e WorldEffectPolicy para efeitos próprios sobre blocos.
- **Status de hook:** ⛔ sem adapter ou mutabilidade específica provada/testada. ⚠️ Precisa validar jar 2.7.6 contra host 5.13.1, receitas/datapack, reivindicações/protection, FakePlayer, restart, contagem de item/fluido, ciclo das entidades e causalidade exactly-once.
