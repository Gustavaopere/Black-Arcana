# Raygun 1.0.10 — desvios condicionais `X_RAY` e `GAMMA_RAY`

## Escopo e fonte de autoridade

Continua a [PR #1016](https://github.com/Gustavaopere/Black-Arcana/pull/1016) integrada em `Black-Arcana/main@8a6bb3ef44f58bea93872f48401363b1a662f5e6`. A versão física de autoridade é Alex's Caves Continued `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.

A [sonda read-only](alexscaves_1010_raygun_condition_branches_probe.py) usa a classe `RaygunItem.class` SHA-256 `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c` e o método exato `onUseTick(Level,LivingEntity,ItemStack,int):void` digest `b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5`, proveniente de `javap` Java 21.

## Objetivo delimitado

Esta rodada investiga *o primeiro desvio JVM posterior* a cada uma das **3 leituras do slot 9** (offsets `105`, `122`, `569`) e **5 leituras do slot 18** (`367`, `402`, `922`, `1029`, `1138`), estabelecidas pelo censo de classes da PR #1016. Para cada uma, guarda somente uma janela de 4 instruções anteriores e 6 posteriores e, quando o opcode imediatamente seguinte for `if...`, confirma os offsets de destino e fallthrough presentes na classe.

Outras seis janelas pequenas delimitam `ACCompat.enchantLevel @47`, atribuição `X_RAY @58`, `GAMMA_RAY @332`, atribuição no slot 18 em `@346`, ray trace `@69` e pedido de dano `@1041`. A CI exige SHA da classe/método, recusa offsets e destinos inválidos e executa regressões sintéticas fail-closed.

**A primeira CI é `UNSEALED DISCOVERY`.** O manifesto `EXACT-RAYGUN-CONDITION-BRANCHES-1.0.10.json` será criado exclusivamente com o resultado real e validado com `--seal` na HEAD final, juntamente com todos os workflows obrigatórios antes de qualquer merge.

## Limites de conclusão

Esta evidência cobre **desvios diretos observados, não CFG completo**. O método JVM pode ter estruturas de loop, exceções, reatribuições e domínios de seleção distintos. Mesmo uma condição `ifeq` imediatamente após `iload 9` **não certifica** que X_RAY ignora blocos, muda alcance efetivo ou ultrapassa proteção de claims. `GAMMA_RAY` e `local 18` não devem ser convertidos em dano final ou perk alterável sem validação da atribuição causal, guards e runtime.

A arquitetura continua: servidor autoritativo do Black Arcana, `WorldEffectPolicy`, custos/estado do provider, prevenção de duplicação e contracts reais; RPG Skill Tree permanece sibling de progressão. **Status:** ⚠️ Raygun parcial/condicionado; `NO_MUTATION`, `NOT_CERTIFIED`, `physical_qa=NOT_TESTED`; Stage 06 e índices de fichas inalterados.
