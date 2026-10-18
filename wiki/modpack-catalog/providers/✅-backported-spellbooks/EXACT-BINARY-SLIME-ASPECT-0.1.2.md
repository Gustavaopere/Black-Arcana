# Backported Spellbooks 0.1.2 — Slime Aspect: parâmetros e consumers no JAR publisher

**18/10/2026 · ✅ `EXACT_PUBLISHER_COMPILED_CALLSITES_ONLY` para `AspectOfTheSlimeSpell.onCast` e `ModMobEffects.lambda$static$2`; ⚠️ host/cliente/atributos finais; ⛔ mutation adapters.**

## Proveniência e método

- **Distribuição:** Backported Spellbooks 0.1.2, arquivo oficial CurseForge projeto `1543731` / arquivo `8158731`, 209.868 bytes, SHA-1 `747847c1f38c73250ebac05ea06b41a381187850` (mesmo valor certificado da modlist física). Metadata embutida `0.1.0` não equivale a versão de distribuição `0.1.2`.
- **Prova:** workflow Java21 [#39149742796](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39149742796) **SUCCESS** no HEAD `d266973473cf8f3ad91b75ccc6c089fc9e0a0ce0` (primeira execução bem-sucedida); 9/9 novos autotestes e `PASS_BACKPORTED_012_SLIME_BOUNDED_BYTECODE`, `deviations=[]`. [Relatório JSON #12144269318](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39149742796/artifacts/12144269318).
- [Verificador fail-closed](../../../../docs/qa/backported_012_slime_aspect_bytecode.py) usa `javap -p -c` em três classes depois de checar SHA-1 do JAR e presença das classes; [workflow](../../../../.github/workflows/backported-spellbooks-012-perk-bytecode.yml) também reinspeciona Sulfur Clouds/Release/Resin Spray e Sulfur Bomb/Pale Thorn. Não grava JAR/código de terceiros no repo.
- Primeira tentativa [#39149640669](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39149640669) falhou corretamente: exigia `ldc float` nos parâmetros da API de atributos, enquanto o bytecode usa `ldc2_w double`. A implementação do gate foi corrigida conforme **operandos compilados**, sem alterar nem arredondar as constantes para fingir igualdade.

## Cadeia `onCast` compilada

`net.redreaper.backported_spellbooks.spells.nature.AspectOfTheSlimeSpell.onCast` contém na ordem:

1. referência a `ModMobEffects.SLIME_ASPECT`, chamada de `getSpellPower`, constante **`float 20.0f`**, `fmul`, `f2i` (truncamento para ticks);
2. carregamento do nível, `iconst_1`, `isub`: **amplificador `spellLevel-1`** na instrução observada no `javap`;
3. `MobEffectInstance.<init>(Holder,IIZZZ)`, uma chamada `LivingEntity.addEffect`, descarte do valor booleano via `pop` e `AbstractSpell.onCast` depois da tentativa de aplicar o buff.

Não há `DamageSources.applyDamage` direto no método. Isso prova operação compilada e ordem de callsites **nesse método**; a expressão de duração depende de `getSpellPower` do host, configuração e caster. Não medimos efeito ou tooltip de jogador.

## Atributos registrados no supplier compilado

No JAR exato, `ModMobEffects.lambda$static$2` instancia `SlimeAspectMobEffect` e chama `addAttributeModifier` **três vezes** na seguinte ordem:

| Atributo compilado | Constante no classfile (`ldc2_w`) | Operação compilada | Implicação de perk |
|---|---|---|---|
| `com.blackgear.vanillabackport...ModAttributes.BOUNCINESS` | `double 0.5d` | `ADD_VALUE` | parâmetro de elasticidade, não `ATTACK_DAMAGE` |
| `net.minecraft...Attributes.JUMP_STRENGTH` | `double 0.15000000596046448d` | `ADD_MULTIPLIED_TOTAL` | parâmetro de salto, não `MOVEMENT_SPEED` |
| `com.blackgear.vanillabackport...ModAttributes.AIR_DRAG_MODIFIER` | `double -0.10000000149011612d` | `ADD_MULTIPLIED_TOTAL` | parâmetro de resistência do ar, não `SPELL_POWER` |

Os dois últimos operandos representam conversão de constantes `float32` de fonte para o argumento `double` da API `addAttributeModifier`, **não** novos valores de balanceamento arbitrários. A inspeção `javap` também observa no inicializador estático a sequência `String slime_aspect`, `InvokeDynamic #2`, `DeferredRegister.register` e `putstatic SLIME_ASPECT`; a prova automatizada exige o literal de registro e o supplier que contém as três operações, **mas não reconstrói formalmente a tabela BootstrapMethods**.

## Riscos e fronteiras

- **Causalidade:** um cast aplica um buff self; três modificadores de atributo **não são três casts ou hits**. A tooltip `getPercentAttackDamage/getPercentSpeed/getPercentSpellPower` não muda os alvos dos modificadores observados.
- **Separação de equipamentos:** `SlimeBootsArmorItem` possui seu próprio conjunto de modifiers e `ServerEvents.onFallEvent` cancela queda quando o jogador usa as botas. Nada no método `onCast` prova cancelamento de queda causado por Slime Aspect.
- **⚠️ Pendente:** valor de atributo final com amplificador, `MobEffect`/Iron's 3.16.3/VanillaBackport físicos, presença efetiva no registry carregado, stacking/recast, relog, consumo de mana e cooldown, movimento/queda em player conectado, multiplayer e QA de Survival.
- **⛔ Não autorizado:** converter em AOE/target ou mudar duration/atributos mediante hook público presumido; cobrar mana ou conceder Mastery por atributos aplicados, tick ou movimento. Nenhum setter/callback externo seguro foi certificado.

**Autoridades:** addon para definição do efeito, Iron's para casting/mana/cooldown, host VanillaBackport/Minecraft para interpretação dos atributos; RPG Skill Tree para progression/perks/Mastery por boundary real; Black Arcana apenas seu runtime. Nenhum runtime Java, adapter ou perk alterado.

**Contagem:** Backported Spellbooks permanece **6/6 identidades `COUNTED_EXACT`**, **6/6 fichas técnicas source-pinned**, agora **6/6 identidades com pelo menos um consumer/método compilado delimitado certificado**. Isso fecha apenas essa **métrica binária delimitada**, não os métodos completos ou integração/QA. Piso global semântico **1.857 objetos / 1.855 estritos**, universo total aberto (**—%**); **+0** magias e **+0** adapters. Stage 06.05 🟡, Stage 09 físico PENDING; PR #825 permanece draft até gates de revisão e integração.
