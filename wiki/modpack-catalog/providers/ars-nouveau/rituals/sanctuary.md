# Sanctuary

State: `SOURCE-PINNED 5.13.1 / RUNTIME QA PENDING`

Provider: Ars Nouveau 5.13.1
Registry id: `ars_nouveau:ritual_sanctuary`
Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Função

Sanctuary impede determinados spawns hostis dentro de uma área ao redor do Ritual Brazier. O comportamento é event-driven: o ritual participa da decisão de spawn em vez de executar uma varredura periódica de entidades.

## Regras confirmadas

- Raio base: `32` blocos.
- `FinalizeSpawnEvent`: cancela apenas `MobSpawnType.NATURAL` quando a entidade é `Enemy` ou está na whitelist própria do ritual, exceto tipos presentes na blacklist própria.
- `VillageSiegeEvent`: também pode cancelar a tentativa de siege dentro do raio.
- O ritual precisa estar ativo (`tile.isOff == false`).
- Cada Rotten Flesh consumido adiciona `+1` ao campo `radius` durante `onStart`.
- O código aceita Rotten Flesh enquanto a contagem consumida desse item for menor que `128`.
- Source cost declarado: `500`.
- Quando ao menos um spawn foi negado, `deniedSpawn` fica verdadeiro; a cada `1200` ticks, se esse flag estiver ativo, o ritual limpa o flag e chama `takeSourceNow()`.
- `radius` e `deniedSpawn` são persistidos no NBT/contexto do ritual.

## Divergência de documentação a validar

A descrição provider-native afirma que Rotten Flesh aumenta o raio "by 1 each, up to 128". O path executável observado limita a **quantidade consumida** de Rotten Flesh a 128, partindo de raio base 32; isso não demonstra de forma inequívoca que o raio final seja limitado a 128. O catálogo não normaliza essa divergência por inferência.

Status dessa divergência: `RUNTIME QA REQUIRED`.

## Boundary Black Arcana

- Ars Nouveau continua authority de `Source`, Ritual Brazier, lifecycle deste ritual, tags de whitelist/blacklist e sua própria decisão de spawn.
- Black Arcana não deve criar um segundo Sanctuary nem processar novamente o mesmo `FinalizeSpawnEvent` para reproduzir o efeito do Ars.
- Qualquer interação futura com Forbidden Domains/Arcane Danger deve consumir apenas contratos reais do provider e preservar causalidade/deduplicação.
- A existência deste ritual não autoriza Black Arcana a contornar seus próprios budgets ou `WorldEffectPolicy`.

## QA pendente

1. Confirmar em runtime 5.13.1 a interpretação do limite de Rotten Flesh/raio final.
2. Confirmar custo temporal efetivo quando múltiplos spawns são negados dentro do mesmo minuto.
3. Validar coexistência com outros mods do pack que interceptem natural spawn ou village sieges.
4. Confirmar comportamento após chunk unload/reload e reload de configuração/provider state.
