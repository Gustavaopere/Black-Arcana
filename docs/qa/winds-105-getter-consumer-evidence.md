# Wind's Spellbooks 1.0.5 — mapa de chamadas diretas aos nove getters

**Data:** 24/10/2026 · **Estado:** ✅ gate binário 9/9 arestas diretas selecionadas aprovado em CI; ⚠️ fluxo de operandos e hooks continuam pendentes.
**Provider:** `wind_spellbooks` · JAR físico `wind_spellbooks-1.0.5.jar` · SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`.
**Baseline:** Black Arcana `main@2a507d16cf3b5b5ce38dabc610203442c8bf1e00` (PR #883 integrado).
**Fonte:** extração clean-room de invocações JVM por método, reutilizando `docs/qa/winds_105_spell_metadata.py`; **nenhum código/bytecode do provider é reproduzido**.

## Chamadas diretas em classes dos próprios spells

| Spell | Getter | `getUniqueInfo` chama diretamente? | `onCast` chama diretamente? | Outra chamada direta na mesma classe |
|---|---|---|---|---|
| Aeropic | `getRecastCount(int, LivingEntity)` | Sim | **Não observado** | Nenhuma no recorte |
| Almighty Push | `getDuration(int)` | Sim | Sim | Nenhuma no recorte |
| Almighty Push | `getRange(int, LivingEntity)` | Sim | Sim | Nenhuma no recorte |
| Iron Slash | `getDistance(int, LivingEntity)` | Sim | Sim | Nenhuma no recorte |
| Tailwind | `getPercentAirSpeed(int)` | Sim | **Não observado** | Nenhuma no recorte |
| Tailwind | `getPercentJump(int)` | Sim | **Não observado** | Nenhuma no recorte |
| Tornado | `getDuration(int)` | Sim | Sim | Nenhuma no recorte |
| Wind Jump | `getFloatDuration(int, LivingEntity)` | Sim | Sim | Nenhuma no recorte |
| Wind Jump | `getJumpStrength(int, LivingEntity)` | **Não observado** | Sim | `getJumpHeight` |

**Leitura rigorosa:** a tabela registra somente `invoke*` com descritor JVM exato dentro dos métodos da classe do spell. `getUniqueInfo` é o nome de um método de informações; mesmo uma chamada **somente ali neste recorte não prova que o parâmetro seja cosmético ou restrito à interface**. Outras classes, métodos de efeitos, versões ou caminhos indiretos permanecem fora deste inventário. A ausência de chamada direta por `onCast` **não é prova de ausência de efeito gameplay**.

## Operações presentes em `onCast` — arestas independentes

Estes símbolos foram inventariados **no mesmo método** que eventuais chamadas a getters. Sem a pilha de operandos e CFG correspondentes, **não** foi demonstrado que o resultado de um getter chega ao setter.

| Spell | Observação de outro símbolo em `onCast` | Significado estrito |
|---|---|---|
| Almighty Push | `AlmightyPushEntity.setLifetime`, `setRadius` e escritas em `strength`/`amplifier` | Coexistem métodos de configuração da entidade, sem atribuição de operandos |
| Tornado | `TornadoEntity.setDamage`, `setDuration`, `setRadius` | Coexistem setters de parâmetros, **não** vínculo de valor com `getDuration` |
| Iron Slash | `TeleportSpell.findTeleportLocation` e `performDash` | Arestas de chamadas diretas, não distância nem destino final |
| Wind Jump | `ImpulseCastData.<init>`, `LivingEntity.addEffect` e escritas em `GustCollider.range`, `strength`, `amplifier` | Estruturas de impulso/collider presentes; argumentos e geometria não demonstrados |
| Tailwind | leitura de `ModMobEffectRegistry.TAILWIND` e `LivingEntity.addEffect` | Aplicação de efeito no método; os dois getters de percentual **não** aparecem como chamadas diretas |
| Aeropic | `ServerGamePacketListenerImpl.teleport`, `LivingEntity.setDeltaMovement` e leitura de `ACROBATICS` | Operações de movimento/efeito presentes; `getRecastCount` não é chamado diretamente por `onCast` |

## Critérios para avanço

- O scanner `docs/qa/winds_105_getter_consumer_edges.py` comprova **somente** as nove arestas exatas e as co-presenças selecionadas no mesmo `onCast`, verificado pelo SHA físico do JAR.
- Um símbolo divergente, mudança de chamador, ausência de setter ou overload ambíguo resulta em **`FAIL_CLOSED`**; nenhum hook é inferido.
- Próximo recorte: rastrear argumentos de chamadas e fluxos JVM de `onCast`/entidades/efeitos com guards e fronteiras host, sem copiar implementação externa. Também auditar os consumidores externos das duas percentagens de Tailwind e a lógica de recasts de Aeropic.
- **Sem QA provider-native, cliente real ou compatibilidade IronSable comprovados.** `SEM_HOOK_SEGURO` para perks que alterem essas superfícies; o RPG Skill Tree não possui casting, Wind's/Iron's permanecem authorities do spell e Black Arcana somente do próprio runtime.
- **Nenhuma contagem nova:** 7/7 fichas Wind's, 9/9 getters selecionados, campanha binária 38/39, global —%/≥1.856; Stage 06.05 🟡, Stage 09 físico pendente.

## Prova executada no JAR oficial

[Workflow #40130495377](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40130495377) concluiu `SUCCESS`; `getter-consumer-edges.json` foi baixado e revisado. Resultado `PASS_SHA_EXACT_DIRECT_CALL_EDGE_INVENTORY`, **9/9 getters selecionados em 6/7 classes de spells**, SHA-1 físico `8744886899bc245ae147a44baa2b183689cec7da`. A sétima classe (Wind Blade) continua no inventário 7/7, mas não pertence à população destes getters; nenhum novo feitiço foi criado. Todos os sinks co-presentes previstos foram encontrados. O scanner e os nove testes sintéticos passaram.

**Advertência de método científico:** esse `SUCCESS` significa somente arestas explícitas de chamada e coexistência de símbolos em métodos binários. `effective_consumer_argument_flow: NOT_PROVEN` para **9/9**; não é aprovação de alteração de raio, recarga, duração, alvo ou impulso por perks. Os consumidores de classes externas, condições, stack dos sinks e QA de cliente/Survival permanecem abertos.
