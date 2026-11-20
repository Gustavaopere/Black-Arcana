# Candy Cane Hook — auditoria física 1.0.10

Estado: 🟡 **DISCOVERY / NOT CERTIFIED**. Esta reserva preserva o percurso alfabético após a #1130. Não cria raiz mágica, não certifica o objeto, não altera ledger nem índices e não habilita hooks.

**Publisher exato:** `alexscaves-1.0.10-neoforge+1.21.1.jar`; 75.279.314 bytes; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Minecraft 1.21.1, NeoForge 21.1.250 no snapshot sibling, Java 21. Nenhum dump de instalação/QA atualizado.

## Evidência pré-existente
A [descoberta seis classes](../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-BURROWING-CAVE-MAP-DISCOVERY-1.0.10.md), já na main pela PR #1130, sela a classe `CandyCaneHookItem` SHA-256 `d999251e494c45420e58881181e9d67757247b6865dc4a547bf0da8a46cf8e44`, 13 corpos próprios, 7 owners tipados e 36 sites. O catálogo do [registry](../wiki/modpack-catalog/providers/✅-alexs-caves-continued/systems/item-registry.md) localiza `alexscaves:candy_cane_hook` via `lambda$static$179` e não prova spawn aceito.

O item implementa `ACEnchantableItem` e `ACTickingItem`. Interfaces, encantamentos e presenter continuam contratos separados. Nenhum destes comprova comportamento final do hook.

## Pesquisa em andamento
A coleta automatizada faz leitura SHA-exata de `CandyCaneHookItem`, `CandyCaneHookEntity`, `GumWormSegmentEntity`, `ACCompat` e três consumidores client-side (`ClientEvents`, `ACItemPredicates`, `CandyCaneHookRenderer`). Primeiro localizar release física e hashes, depois analisar causas de:
- `use`, `canLaunchHook`, `isHookLaunchedInWorld`, `acInventoryTick`;
- criação/owner, lançamento, attachment, reeling, distância, vetores, cooldown e custo de durabilidade;
- UUID, `CUSTOM_DATA`, persistência, dimensionamento e estados em memória;
- seletor de mão, enchantments, dano, controle de entidade, presença `GumWormSegmentEntity`;
- side authority, retorno real de `addFreshEntity`, disparo/replay, interação com encantamentos e deduplicação;
- parâmetros seguros para perks e Mastery com boundary real.

O novo workflow é **read-only** e guarda transcrições completas `javap -v -c -p -s` e hashes em artefato de CI, sem guardar JAR do terceiro. Não é evidência de execução física.

**Gates:** `NO_MUTATION`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `provider_universe_closed=false`. Até certificação individual, qualquer ficha nova deve ser ⚠️ e não pode aumentar numeradores estáticos. A PR #1130 pré-merge passou 27 checks; pós-merge não deve ser declarado concluído sem consulta final.
