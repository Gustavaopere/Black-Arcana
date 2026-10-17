# Flush

**⚠️ Verificação do publisher 2026-10-13:** `aero_additions:flush` e sua classe foram confirmados por `javap` no JAR oficial CurseForge 1.2.8, [Java21 #38431639191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431639191). O SHA-1 do arquivo físico instalado **não foi comprovado** (dado histórico de 35 dígitos inválido): esta ficha segue `COUNTED_SOURCE_PINNED`, não `COUNTED_EXACT`; já contabilizada, **+0**. [Provenance/gate](../EXACT-PUBLISHER-SPELLS-1.2.8-PHYSICAL-SHA-BLOCKED.md). Runtime, aquisição e config ⚠️.


- Provider: **SnackPirate's Aeromancy Additions** (`aero_additions`)
- Version: `1.2.8`
- Registry id: `aero_additions:flush`
- Registered class: `FlushSpell`
- Provider school: `aero_additions:wind`
- Host registry: **Iron's SpellRegistry**
- Semantic state: `COUNTED_SOURCE_PINNED`
- Strict contribution: `1`

## Identidade semântica

Spell provider-owned ativo no `AASpells` do source pin 1.2.8. A identidade é contada pelo registro ativo do provider, não por nomes de classes, entities, effects ou assets auxiliares.

## Registration evidence

O source pin contém uma chamada ativa `registerSpell(new FlushSpell())` para esta identidade. O provider registry é ligado ao event bus sem branch provider-side de configuração que remova este registro.


## Evidence boundary

Esta ficha fecha ID, classe registrada, ownership, escola Wind e estado semântico source-pinned. Mecânica quantitativa, custo, cooldown, acquisition settlement, networking, compatibilidade e comportamento no modpack físico permanecem QA separado quando não explicitamente fechados pelo dossiê.

Source: `../EXACT-1.2.8-SPELL-INVENTORY.md`.

## Engenharia causal para perks — 17/10/2026

**Identidade:** mod ID `aero_additions`, versão `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. **⚠️ COUNTED_SOURCE_PINNED**: dez registros confirmados em JAR oficial de publicação ([Java 21 #38431639191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431639191)), mas SHA-1 do JAR *instalado* na modlist histórica é inválido/incompleto (35 dígitos); **NÃO** promover a COUNTED_EXACT instalada. JAR publisher `aero_additions-1.2.8.jar` SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f`. Todos os números abaixo vêm do source, não de configuração efetiva/QA físico. Iron's governa casting, mana/cooldown; Aero Additions governa efeitos; RPG Skill Tree somente progressão/perks por contrato real.

**Raiz `aero_additions:flush` — Flush.** Source-only; dados de domínio, raio, alvo e duração são mensurados conforme os métodos abaixo, quando aplicáveis.

| Eixo | Observação fonte-fixada | Mutabilidade por perk |
|---|---|---|
| Cast/custo | LONG, níveis 1–3, cooldown 15s, castTime 40, mana 50+15/nível, power 30+5/nível (power não usado no BFS examinado). | Custos do Iron's; efeito WORLD_MUTATION externo, não administrado automaticamente pelo Black Arcana. |
| Limites de BFS | onCast chama removeWaterBreadthFirstSearch(level,caster.blockPosition(),**2×spellLevel**). O helper chama `BlockPos.breadthFirstTraversal(pos,6+argument,40+25×argument,...)`, logo profundidade **8/10/12**, limite de visita **90/140/190** posições (default níveis 1–3). Se início for LiquidBlock, também altera start imediatamente. | Limites de traversal são argumentos, não prova de exatamente N blocos removidos. |
| Mutação e risco | Quando neighbor é BucketPickup, chama `pickupBlock(null,level,searchPos,state)`; em LiquidBlock executa level.setBlock(... AIR ...). Em outros blocos não algas, chama `getValue(WATERLOGGED)` sem `hasProperty` explícito e sem atribuir retorno de setValue; em seguida chama Block.dropResources e **level.setBlock(... AIR ...)**. | ⚠️ potencial de remover blocos não líquidos, dropar recursos e lançar exceção por propriedade ausente, dependendo de shouldHydrate/host; não afirmar bug reproduzido. Prioridade de QA WORLD SAFETY. |
| Proteção/side | Não há guard local server-only/claim/WorldEffectPolicy antes dessas mutações no body. O traversal recebe 6 vizinhos por posição; `spongeState.canBeHydrated(...)` restringe fluxo mas não é claim gate. | **⛔ BLOQUEADO para perks que expandam raio/quantidade ou reproduzam mutação** até provas físicas com claims, survival e proteção do mundo. |
| Tipo/target | Alvo posicional do caster; sem DamageSource/entidades ofensoras; efeitos permanentes em blocos podem exceder escopo de magia visual. | Mastery por remoção de água requer observação efetiva de bloco e orçamento, nunca por BFS visitado. |

**Localizadores:** [FlushSpell.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/flush/FlushSpell.java#L23-L105).

**QA pendente e fail-closed:** QA bloqueante com água, lava, waterlogged, baús/BlockEntity, claims, chunks, servidor dedicado/cliente, recurso drop, rollback/dedup e limites 90/140/190. Não aplicar WorldEffectPolicy BA em provider sem integração contratada. Os valores são defaults ou constantes, não provas de execução em servidor/cliente. **+0 novas magias; +0 adapters aprovados.**
