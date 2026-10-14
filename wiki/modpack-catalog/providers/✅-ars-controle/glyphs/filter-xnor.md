# Filter: XNOR

State: `SOURCE-PINNED 1.6.15 / RUNTIME QA PENDING`

- Registry id: `ars_controle:glyph_filter_xnor`
- Kind: adaptive binary Filter
- Tier: I
- Base mana: 0
- Scribe XP: 27
- Recipe: `minecraft:comparator` + `minecraft:redstone` + `minecraft:redstone_torch`

## Behavior

Evaluates the next two valid filters and resolves when both boolean results are equal: both true or both false.

Like the other adaptive binary filters, it consumes nested filter grammar and fails closed when the expected filter structure cannot be resolved.

## Engenharia para perks — execução pinada à release 1.6.16

- **Source exato 1.6.16:** [FilterBinary.java](https://github.com/Vonr/Ars-Controle/blob/14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0/src/main/java/dev/qther/ars_controle/spell/filter/FilterBinary.java), `Vonr/Ars-Controle@14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0`. Registrado no JAR físico 1.6.16; *identidade binária* comprovada separadamente, execução ainda sem teste de equivalência de método a bytecode.
- **Operação:** `FilterBinary.XNOR` usa `a.get()==b.get()` e só passa quando os dois resultados são iguais; isso inclui ambos falsos. Diferente de OR/AND, não exige que qualquer condição seja verdadeira.
- **Parser/custo:** consulta dois `IFilter` não adaptativos, incluindo augments do primeiro no salto de cursor, e retorna false em client/ausência/exception; `BinaryFilterValidator` valida estrutura. Propriedade `res` compartilhada no singleton requer QA de reentrância.
- **Perks:** uma checagem XNOR verdadeira com dois falsos não significa dois acertos ou alvos admitidos; status 'both false' é semântica original do provider e não dá ao RPG permissão de ignorar os filtros de segurança da Black Arcana.
- **Estado:** ✅ localização do source e IDs físicos; ⚠️ interleaving de contextos, config instalada, erros de validação e Survival/host QA em aberto; ⛔ hooks/adapters RPG não implementados ou testados. O Ars controla gramática, mana e retomadas.
