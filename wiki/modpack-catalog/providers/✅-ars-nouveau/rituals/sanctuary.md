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

## Dossiê de implementação para perks — ritual exato

- **Classe fonte:** [`DenySpawnRitual.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/DenySpawnRitual.java), fonte `112920ff774831f204031da75b4c4e73d3765157` para Ars 5.13.1.
- **Tipo de execução:** `DenySpawnRitual extends RangeRitual`, expõe `denySpawn(FinalizeSpawnEvent)` e `denySiege(VillageSiegeEvent)` em vez de matar mobs por tick. Requer `!tile.isOff`; spawns naturais classificados como `Enemy` ou na whitelist e fora da blacklist são cancelados dentro de `radius*radius`; siege recebe veto separado.
- **Raio/config:** `radius=32` inicial; `onStart` soma ao raio a contagem de `ROTTEN_FLESH` consumida. `canConsumeItem` permite mais Rotten Flesh quando `itemConsumedCount()<128`; limite de **quantidade** não é prova de raio final máximo 128. Persistência de `radius` e `deniedSpawn` em NBT.
- **Resource:** `getSourceCost=500`; quando `deniedSpawn` está true e `gameTime%1200==0`, limpa flag e chama `takeSourceNow()`. Não confundir taxa por minuto com débito por cada spawn.
- **Perks:** alcance de admissão, whitelist/blacklist e consumo Source são semânticas separadas. Black Arcana não injeta segundo veto em spawn Ars nem altera saldo por heurística.
- **Mutabilidade externa:** ⛔ nenhum adapter RPG provado que altere lifecycle, Source ou raio sem duplicar settlement; 🟡 fórmula/lógica source-pinned; ⚠️ runtime, receitas/config física, addons e Survival pendentes.
