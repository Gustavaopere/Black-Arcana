# Wind's Spellbooks 1.0.5 — opcode e owner de `AeropicEffect.getRecastCount`

**Data:** 24/10/2026 · **Estado:** 🟡 JAR exato aguardando prova CI nesta branch. Sem hook homologado.

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
