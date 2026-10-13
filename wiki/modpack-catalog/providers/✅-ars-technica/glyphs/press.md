# Ars Technica 2.7.6 — Press

Estado: ✅ identidade source/JAR registry; ⚠️ implementação física, config, addons e QA; ⛔ bridge de perk não implementada.

## Identidade e provenance

- **Registry ID:** `ars_technica:glyph_press`. Tipo: **Effect**; Tier source: **II**; mana default: **100**; escola: **Manipulation**.
- **Augments:** AOE, Extract, Sensitive, Superheat. Valores são defaults do source pin, não custo efetivamente debitado no modpack.
- **JAR instalado:** `ars_technica-1.21.1-2.7.6.jar`, SHA-1 físico `adb2641d538375f6eff6a22f0196bb330ab0b171`; registro 11/11 comprovado em auditoria binária anterior.
- **Fonte da classe:** [`EffectPress.java`](https://github.com/zeroregard/Ars-Technica/blob/bf34b58ff8908837e5894dee773d3afbd98aa3e3/src/main/java/com/zeroregard/ars_technica/glyphs/EffectPress.java), commit `bf34b58ff8908837e5894dee773d3afbd98aa3e3`. Não há prova de igualdade byte-a-byte do método com o JAR físico. Host de compilação Ars 5.11.0 e Create 6.0.8 diferem dos hosts instalados Ars 5.13.1 / Create 6.0.10.

## Engenharia para perks — caminho causal individual

- **Ramos em ordem:** hit em `DepotBlock` cria diretamente `ArcanePressEntity` vinculada ao depot. Em entidades de item: **Sensitive tem prioridade** e cria `ArcanePackEntity` se `canDoAnyPack`; senão **Extract** agrega fluidos via `ArcaneFusionFluids.pickupFluidsAround(...,8)` ao redor do impacto e do caster quando distinto e cria `ArcaneCompactEntity` se receita; default cria `ArcanePressEntity` sobre itens com receitas de pressing.
- **Capacidade:** `maxAmount=Math.round(4*(1+(int)Math.round(AOE)))*(TransmutationFocus?2:1)`. `speed=4.0*(focus?2.5:1)`. Packing grid `clamp((int)ampMultiplier+2,1,3)`. O valor real de itens consumidos deve ser confirmado nos executores de processamento.
- **Heat/gramática:** para Extract, `AugmentSuperheat` seleciona `SUPERHEATED`; senão próximo `EffectSmelt` seleciona `HEATED`; caso contrário `NONE`. `getPressModeFromCluster` e `ISubsequentEffectProvider` tornam dependente da ordem da sequência. Não fazer `Smelt` separado para um mesmo cluster sem contrato.
- **Perks:** manipular custo, heat, throughput ou Source externamente pode duplicar processamento; o provider mantém a liquidação de fluidos/itens e o controle Create.

## Authority, gap e critérios de implementação

- **Authority:** Ars Nouveau mantém a gramática, mana, spell context e casting; Ars Technica mantém processamento auxiliar, itens/fluidos e receita; Create mantém suas recipes e capacidades. RPG Skill Tree só progression/perks/gates via contrato real, não executa a conversão/efeitos.
- **Gap de magia original:** reproduzir uma receita Create com VFX não estabelece identidade de magia Black Arcana. Requer mecanismo original distinto, custos transacionais, proof de targeting, caps/performance, e WorldEffectPolicy para efeitos próprios sobre blocos.
- **Status de hook:** ⛔ sem adapter ou mutabilidade específica provada/testada. ⚠️ Precisa validar jar 2.7.6 contra host 5.13.1, receitas/datapack, reivindicações/protection, FakePlayer, restart, contagem de item/fluido, ciclo das entidades e causalidade exactly-once.
