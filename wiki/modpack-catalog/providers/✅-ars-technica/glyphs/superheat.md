# Ars Technica 2.7.6 — Superheat

Estado: ✅ identidade source/JAR registry; ⚠️ implementação física, config, addons e QA; ⛔ bridge de perk não implementada.

## Identidade e provenance

- **Registry ID:** `ars_technica:glyph_superheat`. Tipo: **Augment**; Tier source: **III**; mana default: **150**; escola: **Fire**.
- **Augments:** nenhum augment adicional. Valores são defaults do source pin, não custo efetivamente debitado no modpack.
- **JAR instalado:** `ars_technica-1.21.1-2.7.6.jar`, SHA-1 físico `adb2641d538375f6eff6a22f0196bb330ab0b171`; registro 11/11 comprovado em auditoria binária anterior.
- **Fonte da classe:** [`AugmentSuperheat.java`](https://github.com/zeroregard/Ars-Technica/blob/bf34b58ff8908837e5894dee773d3afbd98aa3e3/src/main/java/com/zeroregard/ars_technica/glyphs/AugmentSuperheat.java), commit `bf34b58ff8908837e5894dee773d3afbd98aa3e3`. Não há prova de igualdade byte-a-byte do método com o JAR físico. Host de compilação Ars 5.11.0 e Create 6.0.8 diferem dos hosts instalados Ars 5.13.1 / Create 6.0.10.

## Engenharia para perks — caminho causal individual

- **Natureza:** `AugmentSuperheat extends AbstractAugment`; `getDefaultManaCost=150`, Tier III, escola Fire, `getCompatibleAugments()` vazio. Não invoca efeito/receita por si.
- **Uso source-located:** `EffectFuse` detecta a presença de `AugmentSuperheat` em `spellStats.getAugments()` e escolhe fusion type `super`; `EffectPress` com Extract usa `hasBuff(AugmentSuperheat.INSTANCE)` para `HeatCondition.SUPERHEATED`.
- **Perks:** modificar Superheat não garante heating universal de magias Ars nem novo cast; precisa de compatibilidade na gramática e de validação da entidade de processamento/receita Create.

## Authority, gap e critérios de implementação

- **Authority:** Ars Nouveau mantém a gramática, mana, spell context e casting; Ars Technica mantém processamento auxiliar, itens/fluidos e receita; Create mantém suas recipes e capacidades. RPG Skill Tree só progression/perks/gates via contrato real, não executa a conversão/efeitos.
- **Gap de magia original:** reproduzir uma receita Create com VFX não estabelece identidade de magia Black Arcana. Requer mecanismo original distinto, custos transacionais, proof de targeting, caps/performance, e WorldEffectPolicy para efeitos próprios sobre blocos.
- **Status de hook:** ⛔ sem adapter ou mutabilidade específica provada/testada. ⚠️ Precisa validar jar 2.7.6 contra host 5.13.1, receitas/datapack, reivindicações/protection, FakePlayer, restart, contagem de item/fluido, ciclo das entidades e causalidade exactly-once.
