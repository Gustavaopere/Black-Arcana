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

## Certificação técnica estática para perks — interceptação de spawn (25/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** `ars_nouveau:ritual_sanctuary` ↔ `DenySpawnRitual` confirmado no [manifesto binário](../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). Fonte fixada `112920ff774831f204031da75b4c4e73d3765157`: [`DenySpawnRitual.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/DenySpawnRitual.java), [`RangeRitual.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/ritual/RangeRitual.java), [`RitualEventQueue.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/ritual/RitualEventQueue.java), [`EventHandler.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/EventHandler.java), [`RitualBrazierTile.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/tile/RitualBrazierTile.java). JAR publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` prova **identidade de registro**, não equivalência integral dos métodos.

| Campo relevante | Evidência e limite de alteração |
|---|---|
| Registro/cadência do ritual | `DenySpawnRitual extends RangeRitual`. `RangeRitual.tick` em servidor a cada `gameTime%20==0` registra posição do brazier em `RitualEventQueue` se ainda não consta. **A prevenção de spawn não é um scan periódico de mobs**. A fila estática mapeia por dimensão e posição; `getRitual` considera somente brazier **loaded** e ritual da classe exata, selecionando o **primeiro match** do predicado, sem prioridade estável demonstrada se áreas se sobrepuserem. |
| Eventos executáveis e prioridade | `EventHandler.livingSpawnEvent(FinalizeSpawnEvent)` e `villageSiegeEvent(VillageSiegeEvent)` encaminham pela `RitualEventQueue.getRitual(...,DenySpawnRitual.class,...)` no lado servidor. Estes são eventos **observados na fonte do provider**, não um adapter de mutação Black Arcana/RPG. |
| Spawn natural e whitelist | `denySpawn` exige `!tile.isOff`, `getSpawnType()==MobSpawnType.NATURAL`, entidade `instanceof Enemy` **OU** tipo na `DENY_SPAWN_RITUAL_WHITELIST`, tipo **fora** da `DENY_SPAWN_RITUAL_BLACKLIST`, e `entity.distanceToSqr(brazierXYZ)<=radius*radius`. Quando verdadeiro chama `FinalizeSpawnEvent.setSpawnCancelled(true)` e marca `deniedSpawn=true`. **Não é veto universal** a mobs, spawners, raids ou summons e não equivale a cancelar colocação de entidade em todas as fases. |
| Village siege e limite | `denySiege(VillageSiegeEvent)` usa `!tile.isOff`, `getPos()!=null` e posição tentada até `radius*radius` de `getPos().getBottomCenter()`; chama `checkSpawn.setCanceled(true)` e marca flag. **Não aplica filtro NATURAL/Enemy/tags do outro evento**. Distance origin é diferente da do spawn natural, e diferenças de borda precisam de teste. |
| Raio, itens e NBT | `radius=32` no campo, `onStart` adiciona `i.getCount()` por `Items.ROTTEN_FLESH` consumido. `canConsumeItem` admite um novo stack se `itemConsumedCount(...)<128` *antes* de `onItemConsumed(stack.split(1))`. A descrição diz máximo 128 de **raio**, mas o limite codificado é de **quantidade consumida**; não presumir raio final limitado a 128 nem raio ilimitado: fluxo normal sugere até 32+128, com NBT/config ainda não validado. `read` usa `tag.getInt("radius")`, sem fallback local se chave ausente; `write` persiste `radius` e `deniedSpawn`, além do contexto herdado. |
| Source/settlement | `getSourceCost()=500` Source. Quando `deniedSpawn` é true e `gameTime%1200==0`, **primeiro limpa o flag, depois chama `takeSourceNow()`**. `AbstractRitual.takeSourceNow()` marca `needsSourceToRun=true` e delega a `RitualBrazierTile.takeSource()`; se falhar, o flag de custo pendente pode continuar para tentativas posteriores no próprio brazier. **Não comprova débito por spawn, atomicidade da prevenção nem custo de 500 por 20 ticks**. |
| Integração e segurança | Ars/NeoForge têm authority da decisão de evento de spawn e cancelamento; não introduzir segundo veto nem segunda cobrança no Black Arcana. `WorldEffectPolicy` se aplica às mutações próprias do BA, não vira automaticamente política de eventos do Ars. RPG Skill Tree pode fornecer progressão/Mastery/gates apenas por hook real, deduplicação por tentativa e controle de custos; `RitualEventQueue` é consumer nativo, **não** extensão mutadora pública validada para perks. |

**Pendências:** tags reais, colisões entre braziers, limpeza da fila estática, unload/chunk lifecycle, `radius` após NBT legado, devolutiva de cancelamento, cobrança quando Source falta, proteção por mod e testes multiplayer. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Alterações de spawn, radius ou Source são fail-closed.
