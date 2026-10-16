# Epic Fight 21.17.3.1 — gate de ordem de invocações no classfile (16/10/2026)

**Evidência:** `PASS_BOUNDED_ORDER` para **cinco métodos compilados** do publisher JAR físico `epic-fight-21.17.3.1-mc1.21.1-neoforge.jar`. **Não confundir** com equivalência de Java 21.17.3, controle de fluxo / branch, execução no servidor ou API de perk homologada.

## Prova auditável / ambiente

- [Workflow #38983851582](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38983851582): **SUCCESS**, Java 21, fingerprints SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0` e SHA-256 `8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526` confirmados no JAR oficial do CurseForge `405076/8175609`.
- [Novo verificador](https://github.com/Gustavaopere/Black-Arcana/blob/docs/catalog-perk-causality-20261015/docs/qa/epicfight_211731_invocation_order.py) lê a saída Java21 `javap -p -c` por **declaração individual de método**, inspeciona **apenas referências a invocações e offsets** dentro dela e compara uma sequência estrita crescente. O relatório publicado contém apenas IDs de métodos, fragments de chamadas e offsets, sem copiar bytecode, corpos de classe ou JAR de terceiros.
- Gate independente existente: **42/42 JSONs**, **43/43 classfiles** com símbolos, **21/21 testes sintéticos**. Novo gate: **5/5 métodos e 8/8 self-tests**, sem desvios.
- Primeiro run do gate de invocações [#38983766929](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38983766929) `FAIL_CLOSED` por assumir a classe proprietária `LivingEntity` na referência `distanceToSqr` de Blade Rush; a correção mantém a exigência de chamada real `distanceToSqr`, sem inferir owner. A versão corrigida passou no run #38983851582. Não removeram-se os checks de método ou ordem.

## Cinco verificações compiladas

| Classe e método no JAR exato | Ordem de referências de chamadas comprovada | Consequência delimitada |
|---|---|---|
| `Skill.loadDatapackParameters` | `CompoundTag.getFloat` → `getInt` → `Map.clear` → `Codec.parse` → `Optional.ifPresent` | O classfile **tenta parsear** modificadores após reset da coleção. **Não demonstra parse bem-sucedido** para `name/uuid` legados. |
| `PhantomAscentSkill.loadDatapackParameters` | `Skill.loadDatapackParameters` → `CompoundTag.getInt` → `getDouble` | O subclass loader chama primeiro o loader base e lê extras. **Não prova impulso/valor aplicado ao estado do jogador**. |
| `EviscerateSkill.executeOnServer` | `playAnimationSynchronized` → `WeaponInnateSkill.executeOnServer` | Duas referências de execução dentro do método, **não dois casts ou dois danos**. |
| `RushingTempoSkill.executeOnServer` | `Map.containsKey` → `playAnimationSynchronized` → `WeaponInnateSkill.executeOnServer` | A consulta ao mapa precede as chamadas da animação/super. **Não demonstra que o ramo de animação tenha sido tomado**. |
| `BladeRushSkill.checkExecuteCondition` | `LivingEntity.isAlive` → `distanceToSqr` | A checagem de alvo vivo precede a de distância no texto instrucional. **Não certifica raio efetivo, execution, impacto ou resultado de cast**. |

A contraparte no source fixado `Antikythera-Studios/epicfight@a78aa24b72e90a9d09f5fd61925e4369d117abaf` (versão declarada **21.17.3**, `SOURCE_ADJACENT`) é: [Skill.java L123–139](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/Skill.java#L123-L139); [PhantomAscentSkill.java L47–53](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/mover/PhantomAscentSkill.java#L47-L53); [EviscerateSkill.java L59–63](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/weaponinnate/EviscerateSkill.java#L59-L63); [RushingTempoSkill.java L30–45](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/weaponinnate/RushingTempoSkill.java#L30-L45); [BladeRushSkill.java L153–156](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/weaponinnate/BladeRushSkill.java#L153-L156).

## Contratos e próximos gates

- **⚠️ LEGACY_CODEC:** `adaptive_skin`, `adrenaline_fiend`, `catharsis`, `bonebreaker`, `vengeance` contêm campos `name/uuid` e operações legadas no JSON exato. A referência `Codec.parse` seguida de `Optional.ifPresent` **não valida** sucesso para esses formatos ou modifiers efetivos. Exigir teste usando a implementação codec real na versão física, loader e datapack atual, com dados de atributo observados.
- **⚠️ MÉTODO/BRANCH:** `javap` é informação estrutural de método e offsets; não constrói CFG, não verifica condição de salto `if*`, exceções, priorities, lado lógico, alteração de recurso ou hit settlement.
- **⛔ PERKS/MASTERY:** nenhum hook seguro foi aprovado; não reaplicar stamina, dano, kill, execute, guard puncture ou gauge de weapon innate. Black Arcana conserva seu runtime mágico; Epic Fight é autoridade do combate; RPG Skill Tree só fornece progressão via contrato verificado.
- **⛔ STAGE:** não há GameTest no modpack com provider ativo, observação cliente/servidor ou aceite Stage 09. Stage 06.05 permanece 🟡.

Este gate **não acrescenta nenhum feitiço** ao numerador global (piso **1.856 objetos identificados / 1.854 estritos**, denominador aberto). Epic Fight core permanece **43/43 IDs catalogados**, **42/42 resources JSONs físicos**.
