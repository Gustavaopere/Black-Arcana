# Ars Hex 5.0.4b — dataflow binário delimitado das três perks e do desconto da foice

**Evidência final desta tranche:** ✅ `PUBLISHER_BINARY_BOUNDED_DATAFLOW` para os três métodos `applyAttributeModifiers` e a assinatura de laço em `EnchanterScythe.getManaDiscount`; ⚠️ runtime real, consumo de mana, jogador conectado, equipamento e interop continuam condicionados; ⛔ perks/Mastery/adapters sem autorização. **+0 magias** e +0 novas identidades.

## Publicador, JAR e execução

- Provider `ars_hex`, versão física na modlist `5.0.4b`, Minecraft 1.21.1/NeoForge.
- Publisher [CurseForge 7404679](https://www.curseforge.com/minecraft/mc-mods/ars-hex-unity/files/7404679), JAR 273389 bytes, SHA-1 `2354710ea312e2a6e0fbc3eb2dbafb8e06f10cf4`. O SHA foi conferido **sobre o JAR publicado baixado pelo runner**, e corresponde ao hash do inventário físico histórico; não houve leitura nova do disco local do usuário.
- [Workflow Java 21 #39093013655](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39093013655), job `inspect_publisher_perk_bytecode` **SUCCESS**: 13/13 autotestes de referências + 12/12 de operandos + 12/12 de dataflow das perks + 11/11 de laço da foice; `PASS_BOUNDED_BYTECODE_REFERENCES`, `PASS_BOUNDED_NUMERIC_OPERANDS`, `PASS_BOUNDED_PERK_DATAFLOW` e `PASS_BOUNDED_SCYTHE_DISCOUNT_FLOW`.
- Artefato JSON publicado #**12122559466**, contendo as evidências delimitadas de bytecode, operandos, fluxo das perks e desconto, sem JAR redistribuído.
- Scripts auditáveis: [referências](../../../../docs/qa/ars_hex_504b_perk_bytecode.py), [operandos](../../../../docs/qa/ars_hex_504b_numeric_operands.py), [dataflow simbólico das perks](../../../../docs/qa/ars_hex_504b_perk_dataflow.py), [laço da foice](../../../../docs/qa/ars_hex_504b_scythe_discount_flow.py) e [workflow](../../../../.github/workflows/ars-hex-504b-perk-bytecode.yml).

## Associações binárias comprovadas

| Objeto | Caminho causal confirmado no classfile selecionado | Interpretação matemática |
|---|---|---|
| `ars_hex:thread_soul_ward` | `SOUL_WARD_CAPACITY` → constructor `AttributeModifier` com `iconst_2`, `iload_3`, `imul`, `i2d` e `ADD_VALUE` → `withModifierAdded` | `2 × slotValue` como contribuição aditiva |
| `ars_hex:thread_soul_ward` | `SOUL_WARD_INTEGRITY` → constructor com double `0.5`, `iload_3`, `i2d`, `dmul` e `ADD_MULTIPLIED_BASE` → `withModifierAdded` | `0.5 × slotValue` multiplicado sobre base |
| `ars_hex:thread_magic_proficiency` | `MAGIC_PROFICIENCY` → constructor com double `0.1`, `iload_3`, `i2d`, `dmul`, `ADD_MULTIPLIED_BASE` → `withModifierAdded` | `0.1 × slotValue` multiplicado sobre base Lodestone |
| `ars_hex:thread_soul_spoils` | `SPIRIT_SPOILS` → constructor com `iload_3`, `i2d`, `ADD_VALUE` → `withModifierAdded` | `slotValue` como contribuição aditiva |
| `ars_hex:enchanter_scythe` | `getManaDiscount`: inicializa soma double, itera `Spell.unsafeList()`, filtra por `NECROMANCY.isPartOfSchool(part)`, acumula `0.2 × getCastingCost()`, retorna `Mth.ceil(sum)` | `ceil(Σ custoNecromancy(part) × 0.2)` |

**Amplitude da prova:** o script das perks usa um interpretador simbólico original de pilha JVM com whitelist estrita e nenhuma ramificação admitida nesses métodos. Exige que a expressão chegue ao argumento de valor do `AttributeModifier`, associado ao atributo e à operação corretos, que por sua vez alimenta `withModifierAdded`. A assinatura da foice exige offsets/branches locais, origem do `getCastingCost`, constante e acumulação até `Mth.ceil` no método observado. Isto eleva a confiança na fórmula compilada **apenas nestes callsites**; não equivale a verificações formais completas de classloading ou gameplay.

## Como usar em perks e Mastery — limite contratual

- **Escala de atributo:** identificar antes se a perk RPG pretende mudar `slotValue`, adicionar outro `AttributeModifier` ou consumir um valor resultante. São semânticas diferentes; duplicação de operação em mesmo item/player pode inflar atributo.
- **DamageType, target, AOE, projétil, range, casting time e cooldown:** as três perks de thread fornecem modificadores de atributos e não criam setters dessas propriedades. A foice faz cast do spell inscrito via Ars Resolver; o desconto isolado não autoriza alterar a resolução de alvo/área/dano.
- **Mana:** `getManaDiscount` calcula um desconto. O teste **não** verifica se, quando ou quantas vezes o Ars aplica esse retorno à cobrança final. Não criar refund paralelo em Black Arcana.
- **Causalidade do on-hit:** `EnchanterScythe.hurtEnemy` e `MalumCompat.workaround` possuem referências binárias previamente confirmadas a resolver e boomerang; ainda faltam validação real de hit/dano, deduplicação, resource settlement e replay/Reactive.
- **Precisão de segurança:** sem `ServerPlayer` conectado e `AttributeInstance` real não declarar stacking, duração/remoção de modifiers, ausência de efeito residual, recompensas de espíritos, MagProficiency em dano, Mastery ou capacidade de retarget.

## Próximos gates físicos

1. Equip/unequip, dois slots, remoção e reload: medir `AttributeInstance` Malum/Lodestone em `ServerPlayer` conectado, registrar modificadores persistentes e clean exit.
2. Com Ars Nouveau 5.13.1, Malum 1.8.2 e Lodestone 1.8.2 instalados, verificar que descontos calculados são efetivamente usados uma vez no cast e observar custo de mana antes/depois.
3. Testar melee, boomerang, Reactive, múltiplos alvos, ataque bloqueado, reconnect/respawn e transição de mundo sem procs duplicados.
4. Só procurar hook de perks/Mastery após observar API/evento público realmente elegível; caso contrário **⛔ fail-closed**.

## Autoridade e contagem

Ars Nouveau controla spell, mana, thread e resolver; Malum controla Soul Ward/Spirit Spoils/arma, Lodestone seu próprio atributo, RPG Skill Tree apenas progressão/perks/gates por boundary real; Black Arcana controla seu runtime mágico e `WorldEffectPolicy`. O glifo Soul Shatter permanece **1/1 identidade mágica** do Ars Hex; as **3/3 perks + 1/1 foice** são superfícies técnicas auxiliares e **não** quatro feitiços novos.

**Global:** piso 1.857 semânticos / 1.855 estritos, denominador definitivo —%. **Stage 06.05 🟡**, Stage 09 físico PENDING; PR #825 draft; merge não realizado.
