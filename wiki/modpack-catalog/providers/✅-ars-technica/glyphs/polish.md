# Ars Technica 2.7.6 — Polish

Estado: ✅ identidade source/JAR registry; ⚠️ implementação física, config, addons e QA; ⛔ bridge de perk não implementada.

## Identidade e provenance

- **Registry ID:** `ars_technica:glyph_polish`. Tipo: **Effect**; Tier source: **II**; mana default: **120**; escola: **Manipulation**.
- **Augments:** AOE. Valores são defaults do source pin, não custo efetivamente debitado no modpack.
- **JAR instalado:** `ars_technica-1.21.1-2.7.6.jar`, SHA-1 físico `adb2641d538375f6eff6a22f0196bb330ab0b171`; registro 11/11 comprovado em auditoria binária anterior.
- **Fonte da classe:** [`EffectPolish.java`](https://github.com/zeroregard/Ars-Technica/blob/bf34b58ff8908837e5894dee773d3afbd98aa3e3/src/main/java/com/zeroregard/ars_technica/glyphs/EffectPolish.java), commit `bf34b58ff8908837e5894dee773d3afbd98aa3e3`. Não há prova de igualdade byte-a-byte do método com o JAR físico. Host de compilação Ars 5.11.0 e Create 6.0.8 diferem dos hosts instalados Ars 5.13.1 / Create 6.0.10.

## Engenharia para perks — caminho causal individual

- **Bifurcação:** se hit Block é `DepotBlock`, instancia `ArcanePolishEntity` vinculada ao Depot e retorna; caso contrário herda busca AABB de ItemEntity e filtra com `SandPaperPolishingRecipe.getMatchingRecipes`, criando uma entidade de processamento na posição do item válido mais próximo.
- **Capacidade/velocidade:** `aoeBuff=(int)Math.round(aoeMultiplier)`, `maxAmount=Math.round(4*(1+aoeBuff))*(focus?2:1)`, `speed=2.0*(focus?2.5:1)` via `SpellResolverHelpers.hasTransmutationFocus(resolver)`; não garantir igualdade de número de outputs sem ler o worker `ArcanePolishEntity`.
- **Perks:** foco Transmutation e AOE possuem papéis independentes em throughput; uma perk que recrie polimento lado RPG violaria a autoridade Create/Ars Technica. Exigir budget por entidades de processamento e persistência.

## Authority, gap e critérios de implementação

- **Authority:** Ars Nouveau mantém a gramática, mana, spell context e casting; Ars Technica mantém processamento auxiliar, itens/fluidos e receita; Create mantém suas recipes e capacidades. RPG Skill Tree só progression/perks/gates via contrato real, não executa a conversão/efeitos.
- **Gap de magia original:** reproduzir uma receita Create com VFX não estabelece identidade de magia Black Arcana. Requer mecanismo original distinto, custos transacionais, proof de targeting, caps/performance, e WorldEffectPolicy para efeitos próprios sobre blocos.
- **Status de hook:** ⛔ sem adapter ou mutabilidade específica provada/testada. ⚠️ Precisa validar jar 2.7.6 contra host 5.13.1, receitas/datapack, reivindicações/protection, FakePlayer, restart, contagem de item/fluido, ciclo das entidades e causalidade exactly-once.
