# Wind's Spellbooks 1.0.5 — opcode e owner de `AeropicEffect.getRecastCount`

**Data:** 24/10/2026 · **Estado:** ✅ inventário de opcodes no JAR exato aprovado; ⚠️ receptor, despacho e runtime continuam não verificados.

## Fonte e contrato

- A modlist atual do sibling `neoforge-rpg-skilltree` fixa `wind_spellbooks-1.0.5.jar` (posição 571) e Iron's Spells 3.16.3 (posição 342). IronSable X Wind's 1.0.0 é outra dependência. Este gate executa apenas sobre o JAR Wind's com SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`.
- O PR #889 provou que `ModMobEffectRegistry.ACROBATICS` está associado **no compilado** à factory `AeropicEffect`. O PR #888 provou que `AeropicSpell` estende `AbstractSpell` e declara override ABI compatível de `getRecastCount(int, LivingEntity)`.
- O PR #887 comprovou referência JVM ao método **`AbstractSpell.getRecastCount`** nas rotas `AeropicEffect.applyEffectTick` e `onEffectAdded`, mas o *invoke opcode* em cada ponto ainda não estava fixado no catálogo.

## A nova prova

`docs/qa/winds_105_aeropic_recast_invokes.py` revalida o JAR, os inventários anteriores de efeitos e o contrato ABI, e inspeciona exclusivamente os dois métodos de `AeropicEffect` com `javap -c -p`. Publica **apenas** nome de método, símbolo do owner/descritor, `invoke*` explícito, referências relacionadas a `PlayerRecasts`/`RecastInstance` no mesmo método e limites de certeza. Sem sequências completas de bytecode, offsets, assets ou código protegido.

Critérios de `FAIL_CLOSED`: JAR inválido, método ausente ou sobrecarregado, invocação de outro owner/descriptor, invocações múltiplas inesperadas, erro de `javap`. O contrato não interpreta co-presença de `PlayerRecasts` com `getRecastCount` como fluxo ou alteração de estado comprovada.

**Nota de JVM:** até uma chamada `invokevirtual AbstractSpell.getRecastCount` comprovaria somente o **tipo simbólico do owner na constant pool e a família de instrução**. O alvo dinâmico depende da classe real do receptor, estado, argumentos, guards e implementação do host Iron's 3.16.3. A herança de `AeropicSpell` não prova o receptor utilizado. A ausência de inspeção do JAR exato do host deve ser declarada `host_JAR_abi: NOT_VERIFIED`.

## Requisitos de aceite

- Dez fixtures sintéticas para método, owner, descritor, opcode, chamadas inesperadas, SHA e proibição de promoção do receiver.
- Rodar o JAR oficial, obter o artefato `aeropic-recast-invokes.json` e examinar o resultado **antes** de registrar qualquer constatação nas fichas.
- CI específico e Black Arcana CI (`verify` + `stage05_qa_companion_smoke`) no HEAD final e comparação SHA/diff com `main` imediatamente antes de merge.
- Runtime do Black Arcana preservado; Wind's/Iron's mantêm casting, efeitos e recasts; RPG Skill Tree fornece progressão por contratos existentes, não autoridade mágica. **⛔ SEM_HOOK_SEGURO** para perks de recast.
- Stages preservados: 06.05 🟡, 09 físico pendente. Catálogo Wind's 7/7 spells, 9/9 getters selecionados, 64 classes compiladas; campanha binária 38/39; global mínimo ≥1.856, percentual indeterminado.

## Resultado confirmado no JAR físico — 24/10/2026

Fonte: [Wind CI #40144903731](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40144903731) `SUCCESS`, `aeropic-recast-invokes.json` baixado e inspecionado, SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`. O recorte encontrou **duas instruções `invokevirtual` com owner constante `AbstractSpell` e descritor `(ILnet/minecraft/world/entity/LivingEntity;)I`**, ambas dentro de `AeropicEffect`.

| Chamador compilado | Retorno declarado | Opcode/owner | Chamadas relacionadas co-presentes | Certeza |
|---|---|---|---|---|
| `applyEffectTick(LivingEntity,int)` | `boolean` | `invokevirtual AbstractSpell.getRecastCount` | `PlayerRecasts.addRecast`, `hasRecastForSpell`, `RecastInstance.<init>` | Arestas de invocação e co-presença do método comprovadas, **não** fluxo de valores |
| `onEffectAdded(LivingEntity,int)` | `void` | `invokevirtual AbstractSpell.getRecastCount` | Nenhuma referência `PlayerRecasts`/`RecastInstance` dentro desse recorte restrito | Owner/opcode exatos, sem prova de receptor/resultado |

**Distinção de rigor:** `invokevirtual` é opcode de despacho dinâmico em potencial, mas a instrução não determina a classe concreta do receiver ou qual override é executado. A compatibilidade binária já comprovada de `AeropicSpell.getRecastCount` com a assinatura de `AbstractSpell` não prova que o objeto empilhado é um `AeropicSpell`. O retorno de `getRecastCount` não foi rastreado até um argumento de `PlayerRecasts` ou qualquer setter. Não qualificar recast efetivo, dano, cooldown ou perk pelo opcode.

`docs/qa/winds_105_aeropic_recast_contract.py` congela 2/2 chamadas, ABI, métodos, opcode `invokevirtual`, símbolos relacionados, SHA do JAR e estado `NOT_PROVEN` para dispatch, receiver, consumer e mutações. **Dez testes de mutação** rejeitam owner/opcode/descriptor errados e promoções falsas. O host Iron's 3.16.3 não foi binariamente auditado nesta entrega.
