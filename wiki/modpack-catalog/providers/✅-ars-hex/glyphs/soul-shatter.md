# Ars Hex 5.0.4b — Soul Shatter

Estado: **✅ `COUNTED_SOURCE_PINNED` — ficha da única identidade de glyph própria do provider**; **⚠️ JAR/registro em runtime e gameplay físico condicionados**.

## Identidade e condicionamento

- **Identidade de registry no source alinhado à release:** `ars_hex:glyph_soul_shatter`.
- **Nome do glyph:** Soul Shatter.
- **Mod ID:** `ars_hex`; JAR instalado `ars_hex-1.21.1-5.0.4b.jar`; SHA-1 físico `2354710ea312e2a6e0fbc3eb2dbafb8e06f10cf4`.
- **Fonte auditada:** `Alexthw46/Ars-Unity@b25528adf8c0135585cd6d654582efa147e0a227` (source retarget para 5.0.4b). A correspondência de release **não** demonstra compilação byte-idêntica ao JAR físico.
- **Registration:** exatamente um glyph provider-owned em `ArsNouveauRegistry.registerCompatGlyphs()`, condicionado a `ModList.isLoaded("malum")`. Malum **está na modlist física**; logo o ramo de registro é elegível, mas ainda requer inspeção/QA do registry do JAR/runtime real.
- **Tipo no source:** `AbstractEffect` + `IDamageEffect`. Tier II. Mana base 30.
- **Dano source-default:** 5.0, incremento de Amplify +3.0 por unidade do multiplicador de amp Ars; limite explícito de Amplify 2; augments compatíveis Amplify e Dampen.
- **Fórmula observada no source:** `damage = DAMAGE + AMP_VALUE * spellStats.getAmpMultiplier()`, antes do processamento host Ars/Malum.
- **Dano e escola:** resolução por helper Ars `attemptDamage(...)` usando `VOODOO` de Malum. Enquanto Ars Elemental estiver carregado (como no pack), a escola source-selecionada é Necromancy. Se Ars Elemental estiver ausente, a escola herdada não foi redefinida artificialmente.
- **Target exclusion:** o efeito não aplica sua resolução de dano a `ItemEntity`.
- **Receita de aprendizado gerada no source e condicionada a Malum:** `ars_nouveau:glyph`, XP 55, insumos `ars_nouveau:manipulation_essence`, `malum:wicked_spirit` e `malum:soul_stained_steel_sword`. **Não** equivale a prova de receita disponível/funcional sob os datapacks e configs efetivos do pack.
- **Contagem:** **uma identidade semântica `COUNTED_SOURCE_PINNED` já contabilizada** no ledger do Ars Hex; criar esta ficha = **+0 novas identidades**.

## Limites causais

A descrição pública associa Soul Shatter a liberação eventual de espíritos. Porém, a classe `EffectSoulShatter` auditada **não implementa fórmula/RNG explícito de spirit-release**: apenas solicita dano Voodoo ao host. Não inventar chance de drop, recurso entregue ou transação espiritual de Malum sem evidência de execução host-native.

**⚠️ NÃO VERIFICADO no runtime físico:** compatibilidade com Ars Nouveau 5.13.1, Ars Elemental 0.7.10.1, Iron's 3.16.3 e Lodestone 1.8.2, recipe/research efetiva, custo final, alcance, protections, Spirit Spoils, lifecycle, balance, no-server duplicate processing, scripts datapack e sucesso em Survival.

Ars Nouveau mantém autoridade sobre custos de mana, casting, resolver/context e dano Ars; Malum mantém tipo Voodoo, espíritos e eventual liquidação de recompensas. Ars Hex mantém o efeito de compatibilidade. Black Arcana não aplica segundo dano, segunda resolução de espíritos, novo mana ledger ou proc chain paralela. Qualquer bridge deve ser provider-causal, server-authoritative e **⛔ fail-closed** até hook/API comprovados.

## Evidência e proveniência

- [Auditoria source do glyph e limite spirit-release](../GLYPHS.md).
- [Registro condicional versus dormant](../REGISTRIES.md).
- [Aquisição exata no source](../ACQUISITION.md).
- [Riscos de integração e versões](../README.md).

**Clean-room:** somente identidades e parâmetros factuais da auditoria técnica já existente. Sem implementação, código, assets, tooltips ou prosa criativa copiados.
