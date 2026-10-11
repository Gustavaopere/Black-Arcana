# Hexalia 1.3.7 — Nature's Ritual `hexalia:bloomwrap_leggings_from_ritual_table`

Status: **✅ CATALOGADO / `COUNTED_SOURCE_PINNED`** com recipe ID, custos/outputs e caminho source-pinned; **⚠️ execução no pack físico não comprovada**.

## Identidade e contrato individual

- **Registry de receita:** `hexalia:bloomwrap_leggings_from_ritual_table` do tipo `hexalia:natures_ritual` (recipe, **não** um spell registry ID do Iron's/Ars).
- **Centro no Ritual Table:** leather leggings.
- **Offerings por Ritual Braziers:** peony; spirit bloom; silk fiber; honeycomb.
- **Resultado provider-owned:** `hexalia:bloomwrap_leggings`.
- **Quantidade de offerings / processamento base:** 4 / 160 ticks.
- **Requer captura de alma:** **não**.
- **Ordinal editorial:** 11/23; não constitui ID ou ordem de resolução.
- **Provider owner:** Hexalia, mod ID `hexalia`, físico `hexalia-neoforge-1.3.7.jar`, SHA-1 `ca90edf1664cf6d44fe7e5318c71069050499c7e` (Minecraft 1.21.1 / NeoForge).
- **Fonte:** release-correlated source pin `AstralyaStudios/Hexalia@98c22aaf70e069c616fed5ad2dc56d2b37fcd283`; posterior manutenção same-version não é projetada para trás. **Não há prova byte-a-byte do build do source contra o JAR físico.**
- **Estado semântico:** `COUNTED_SOURCE_PINNED`, objeto já presente no ledger de **29** ações provider-owned. A ficha acrescenta **+0 novas identidades**.

## Admission, custos e lifecycle

Um jogador inicia com `hexalia:hex_focus` em main/offhand, diante do Ritual Table com input central correspondente. A versão 1.3.7 procura Ritual Braziers não vazios em **raio horizontal 8**, ordenados por distância e posição. Cada brazier selecionado deve estar **SALTED=true**; sem sal, a ação não admite início. Não se presume layout fixo em quatro pontos cardeais.

A execução consome offerings de forma sequencial, uma por **40 ticks**, e limpa o estado de sal daquele brazier. Ausência do centro ou de offering necessário cancela o ritual. O parâmetro `naturesRitualCropRequirement` aceita **0..32** no source; quando positivo, crops maduras elegíveis no raio 8 são selecionadas e, no sucesso normal, reiniciadas para idade zero, não removidas. O default/override implantado não foi medido.

**Conclusão normal:** após a sequência de offerings, o resultado é liquidado pelo provider; não há fase `AWAITING_SOUL` nesta receita. Não duplicar o output e não contabilizar animações/crops como novos feitiços.

## Authority e pendências

Hexalia é autoridade da admissão, salted braziers, offerings, crop settlement, soul capture, timers, persistência, cancelamento e resultado. Black Arcana não cria um segundo altar, débito, summon, compensação ou world mutation; somente pode observar conclusões por hook comprovado e servidor autoritativo, sob **fail-closed**. Ingredientes exatos por registry/tag, configuração implantada, evento de cancelamento, continuidade de chunk/reconexão e execução real em Survival estão **⚠️ NÃO VERIFICADOS**.

**Fontes:** [inventário source-pinned e lifecycle](../../rituals/NATURES-RITUAL-CATALOG.md) · [provider](../../README.md). Clean-room: fatos técnicos do catálogo próprio, sem código ou recipe JSON upstream.
