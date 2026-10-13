# Ars Nouveau 5.13.1 — contratos reais de eventos para perks do RPG Skill Tree

**Status:** `SOURCE-PINNED EVENT/API SURFACE VERIFIED` / `ADAPTER NOT IMPLEMENTED` / `DEDUP+SERVER TEST PENDING` / `FAIL-CLOSED WHEN UNSAFE`.

## Identidade e proveniência

- Modlist sibling: `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 físico registrado `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`.
- Código-fonte de referência fixo `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, NeoForge 1.21.1.
- O fato de um evento Java existir é **prova de uma superfície**, mas não de inscrição na event bus, carga em servidor, sucesso de perk ou compatibilidade com outras bridges do modpack.
- RPG Skill Tree continua autoridade de perks/Mastery/gates; Ars continua autoridade do `SpellResolver`, mana e efeitos; Black Arcana mantém somente seu cast/hazard/ritual runtime original.

## Pontos de extensão verificados em código

| Interface pública real | Chamada e fase observadas | Campos/setters relevantes | Permitido concluir | Não concluir |
|---|---|---|---|---|
| `SpellCastEvent` | `SpellResolver.postEvent()` em `onCast`/overloads após `canCast` e antes da Form; cancelável | `spell`, `context`; `getEntity()` do `LivingEvent` | veto de tentativa que passou por `canCast` | evento não prova `CastResolveType.SUCCESS`, mana efetivamente debitada nem proc ofensivo |
| `SpellResolveEvent.Pre` | `SpellResolver.resume(Level)`, server-only, antes dos Effects; cancelável | `world`, `shooter`, `rayTraceResult`, `spell`, `context`, `resolver` | veto da fase de resolução | um `resume` não representa necessariamente um cast novo, especialmente Delay/Rewind/Rune |
| `SpellResolveEvent.Post` | ao sair do laço de `resume`, não cancelável | mesmos campos | observação do encerramento de uma fase de `resume` | não é garantia de dano, sucesso por alvo ou exactly-once para spell composto |
| `EffectResolveEvent.Pre` | por Effect, em `SpellResolver.resume` após `SpellStats.Builder.build`, antes de `effect.onResolve`; cancelável | `spellStats` + `spell`, `context`, `resolveEffect`, `shooter`, `rayTraceResult`, `resolver` | fronteira **real** para examinar e potencialmente ajustar stats existentes **deste Effect** antes de resolver | não é API universal que garante alterar qualquer radius/dano/quantidade; alguns Effects leem contagem de Augments/configs/helpers |
| `EffectResolveEvent.Post` | após tentativa de resolver o Effect; também há caminho `STOP_ALL` que publica Post antes de `break` | mesmo payload | observação após o caminho da resolução | Post sozinho não atesta que `effect.onResolve` executou; nem que acertou alvo |
| `SpellCostCalcEvent.Pre` | `SpellResolver.getResolveCost` chamado na admissão `enoughMana` | `context`, `currentCost` público mutável | existência de ajuste do **custo consultado** antes de `enoughMana` | não altera automaticamente a cobrança posterior |
| `SpellCostCalcEvent.Post` | `SpellResolver.getExpendedCost` na `expendMana()` após `CastResolveType.SUCCESS` | `context`, `currentCost` público mutável | existência de ajuste do **custo debitado** | não é evento depois do débito; o nome `Post` não autoriza recompensa por cast |
| `DispelEvent.Pre` | `EffectDispel.onResolveEntity/onResolveBlock` antes de despir efeitos/IDispellable; cancelável | `rayTraceResult`, `world`, `shooter`, `augments` (SpellStats), `context` | veto específico do Dispel | modificar campos públicos não demonstra que o corpo do `EffectDispel` usará valores substituídos |
| `DispelEvent.Post` | após execução elegível do Dispel; não cancelável | mesmos campos | observação local do Dispel | nem todo ramo publica Post (ex.: entidade removida/sem vida) |

## Superfície real de `SpellStats`

O [`SpellStats.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java) no commit fixo mostra métodos públicos de instância:

- leitura: `getAmpMultiplier()`, `getAoeMultiplier()`, `getAccMultiplier()`, `getDamageModifier()`, `getDurationMultiplier()`, `getDurationInTicks()`, `getBuffCount(AbstractAugment)`, `isSensitive()`, `isRandomized()`;
- escrita: `setAmpMultiplier(double)`, `setAccMultiplier(float)`, `setDamageModifier(double)`, `setDurationMultiplier(double)`, `setAugments(List<AbstractAugment>)`, `setModifierItems(List<ItemStack>)`;
- `SpellStats.Builder` possui `setAOE/addAOE`, mas a instância `SpellStats` recebida no `EffectResolveEvent.Pre` **não** expõe `setAoeMultiplier` nesta classe. Logo, escrever "hook geral para aumentar área em cada spell" seria inventar uma capacidade;
- trocar `setAugments` após `Builder.build` **não** recalcula automaticamente os multiplicadores numéricos já construídos. `getBuffCount` pode ser lido por consumidores, mas é preciso auditar cada consequência, ordem e cap.
- Alguns consumidores ignoram multiplicadores e usam contagens diretas (`Split`, `Pierce`, `Sensitive`, `Dampen`), ou instanciam entidades com estados próprios (`LightningEntity`, `EntityWallSpell`, `RuneTile`).

O evento de efeito permite investigar um adapter controlado por `resolveEffect` e `SpellContext`, com checks server-side, clamps e atribuição do mesmo cast. Não pressupor que todo setter produza resultado, nem que seja permitido sobrescrever autoridade de outros addons.

## Custos: dois pontos, risco de divergência

Na [`SpellResolver.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java) a verificação de mana chama `getResolveCost` → `SpellCostCalcEvent.Pre` e faz clamp `Math.max(0,currentCost)`. Depois, somente para `CastResolveType.SUCCESS`, `expendMana` chama `getExpendedCost` → `SpellCostCalcEvent.Post` e faz outro clamp `Math.max(0,currentCost)`.

**Risco de adapter:** aplicar desconto só em `Pre` permite aprovar um cast por saldo insuficiente para o débito previsto pelo `Post`; aplicar só em `Post` cobra valor não previsto na admissão. Um perk de custo só pode ser considerado apto após prova de equivalência dos dois cálculos, perfis de caster (turret/creative/fake player), ausência de reroll entre eventos e teste de rollback/cancelamento.

## Resolução e causalidade

Na [`SpellResolver.resume`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java), o servidor:

1. publica `SpellResolveEvent.Pre` e respeita cancelamento;
2. percorre parts não-Augment, cria `SpellStats` para cada Effect e publica `EffectResolveEvent.Pre`;
3. permite que `CapabilityRegistry.BLOCK_SPELL_RESOLVE_CAP`/`ENTITY_SPELL_RESOLVE_CAP` influenciem o `IResolveListener.ResolveStatus`, inclusive `STOP_ALL`;
4. chama `effect.onResolve(...)` apenas no ramo `CONTINUE`;
5. publica `EffectResolveEvent.Post` e, após a fase, `SpellResolveEvent.Post`.

**Não** converter cada `EffectResolveEvent.Post` em Mastery ou ataque confirmado. `Delay`, `Rewind`, `Orbit`, `Wall`, `Linger`, `Rune` e efeitos em AOE introduzem resumes, destinos, entidades e resultados posteriores. Um token de cast/provider de escopo real precisará ser demonstrado e testado; não inventar UUID/counter API.

## Arquivos do source inspecionados

- [`SpellCastEvent.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellCastEvent.java)
- [`SpellResolveEvent.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellResolveEvent.java)
- [`EffectResolveEvent.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/EffectResolveEvent.java)
- [`SpellCostCalcEvent.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellCostCalcEvent.java)
- [`DispelEvent.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/DispelEvent.java)
- [`SpellStats.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java)
- [`SpellResolver.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java)

## Critérios de promoção dos hooks para perks efetivas

`SOURCE-VERIFIED SYMBOL` (já provado) → `IMPLEMENTED ADAPTER` (não feito) → `DETERMINISTIC TEST` (não feito) → `REAL PROVIDER/CLIENT/SURVIVAL QA` (não feito). Testar cancelamento, recast, WorldEffectPolicy apenas em Black Arcana casts, multiplicadores extremos, opt-in/out, skills/cap de compatibilidade e parity `Pre/Post`. Sem isso, **⚠️ candidato de integração, ⛔ uso não autorizado no RPG**.

[Catálogo Ars](README.md) · [Matriz de perks por objeto](PERK-ENGINEERING-MATRIX-5.13.1.md) · [Padrão global](../../meta/PERK-READY-TECHNICAL-STANDARD.md).
