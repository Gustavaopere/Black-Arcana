# Ars Technica 2.7.6 — Whirl

Estado: ✅ identidade source/JAR registry; ⚠️ implementação física, config, addons e QA; ⛔ bridge de perk não implementada.

## Identidade e provenance

- **Registry ID:** `ars_technica:glyph_whirl`. Tipo: **Effect**; Tier source: **II**; mana default: **40**; escola: **Manipulation, Air**.
- **Augments:** AOE, Extend Time. Valores são defaults do source pin, não custo efetivamente debitado no modpack.
- **JAR instalado:** `ars_technica-1.21.1-2.7.6.jar`, SHA-1 físico `adb2641d538375f6eff6a22f0196bb330ab0b171`; registro 11/11 comprovado em auditoria binária anterior.
- **Fonte da classe:** [`EffectWhirl.java`](https://github.com/zeroregard/Ars-Technica/blob/bf34b58ff8908837e5894dee773d3afbd98aa3e3/src/main/java/com/zeroregard/ars_technica/glyphs/EffectWhirl.java), commit `bf34b58ff8908837e5894dee773d3afbd98aa3e3`. Não há prova de igualdade byte-a-byte do método com o JAR físico. Host de compilação Ars 5.11.0 e Create 6.0.8 diferem dos hosts instalados Ars 5.13.1 / Create 6.0.10.

## Engenharia para perks — caminho causal individual

- **Output:** somente servidor em branches Block/Entity; instancia `ArcaneWhirlEntity` com `radius=1.5f+aoeMultiplier*0.33f` e `duration=360+Math.toIntExact(Math.round(durationMultiplier*40))` ticks. RuneCaster posiciona efeito no próprio caster; hit Depot recebe `bindDepot`.
- **Gramática:** examina próximo `AbstractEffect` e seleciona processamento Create: Conjure Water→`SPLASHING`, Flare→`SMOKING`, Smelt→`BLASTING`, Hex→`HAUNTING`; outro efeito deixa `processingType=null`. A lista `ISubsequentEffectProvider` também informa tooltip/cluster.
- **Perks:** AOE e duração podem afetar áreas persistentes e perf; não reutilizar a entidade do provider como origem independente para procs/charged casts. Mudanças de receita precisam preservar contexto e Source/itens.

## Authority, gap e critérios de implementação

- **Authority:** Ars Nouveau mantém a gramática, mana, spell context e casting; Ars Technica mantém processamento auxiliar, itens/fluidos e receita; Create mantém suas recipes e capacidades. RPG Skill Tree só progression/perks/gates via contrato real, não executa a conversão/efeitos.
- **Gap de magia original:** reproduzir uma receita Create com VFX não estabelece identidade de magia Black Arcana. Requer mecanismo original distinto, custos transacionais, proof de targeting, caps/performance, e WorldEffectPolicy para efeitos próprios sobre blocos.
- **Status de hook:** ⛔ sem adapter ou mutabilidade específica provada/testada. ⚠️ Precisa validar jar 2.7.6 contra host 5.13.1, receitas/datapack, reivindicações/protection, FakePlayer, restart, contagem de item/fluido, ciclo das entidades e causalidade exactly-once.
