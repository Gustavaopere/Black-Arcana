# Tailwind

**Registro estático:** ✅ `COUNTED_EXACT` no JAR 1.0.5; [prova binária](../EXACT-BINARY-SPELLS-1.0.5.md). Config, números e Survival ⚠️.

- **ID:** `wind_spellbooks:tailwind`
- **Classe runtime:** `net.raptorzizi.wind_spellbooks.spells.wind.TailwindSpell`
- **School:** Wind
- **Provider/JAR:** Wind's Spellbooks / `wind_spellbooks-1.0.5.jar`
- **Status:** PRESENTE

## Contract confirmado

Fingerprint ASM: `usesAddEffect`. O changelog 1.0.1 registra um fix específico de **fall damage de Tailwind**, provando que o effect participa de uma interação de mobilidade/queda na linha incorporada pela 1.0.5.

## NÃO VERIFICADO

Níveis, rarity, mana, cooldown, cast time, exact effect, velocidade/movimento, duração, magnitude de redução/negação de fall damage, stacking, target rules e aquisição específica.

## Deduplicação / fail-closed

Tailwind ocupa um buff/effect Wind com interação de queda. Não adicionar segundo listener de fall damage ou modifier de movimento sem identificar o effect/hook provider-native exato.

## Evidência

Runtime registry + ASM do pack; release 1.0.5; changelog 1.0.1.

## Verificação JVM exata dos consumidores por método — 24/10/2026

**✅ Fonte binária exata:** `wind_spellbooks-1.0.5.jar`, SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`; [CI de inspeção Java 21 #40118955224](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40118955224) `SUCCESS` no passo de extração. **⚠️ Somente assinaturas e arestas de chamadas; não é prova de runtime, fórmula, parâmetros configurados nem hook mutador seguro.**

- Classe inspecionada: `net.raptorzizi.wind_spellbooks.spells.wind.TailwindSpell`.
- Contagem de métodos/declarações indexadas pelo parser: **12**; partes omitidas abaixo são deliberadamente fora do recorte de consumidores de perks.
- Grafo observável de invocações (`método de origem → símbolos referenciados`; a ordem causal e a entidade alvo exigem desambiguação adicional):
- `public java.util.List<net.minecraft.network.chat.MutableComponent> getUniqueInfo(int, net.minecraft.world.entity.LivingEntity);` → `getSpellPower:(ILnet/minecraft/world/entity/Entity;)F`
- `public void onCast(net.minecraft.world.level.Level, int, net.minecraft.world.entity.LivingEntity, io.redspace.ironsspellbooks.api.spells.CastSource, io.redspace.ironsspellbooks.api.magic.MagicData);` → `getSpellPower:(ILnet/minecraft/world/entity/Entity;)F`, `net/minecraft/world/effect/MobEffectInstance."<init>":(Lnet/minecraft/core/Holder;IIZZZ)V`, `net/minecraft/world/entity/LivingEntity.addEffect:(Lnet/minecraft/world/effect/MobEffectInstance;)Z`

- **Literais presentes em métodos selecionados (candidatos sem atribuição):** `public void onCast(net.minecraft.world.level.Level, int, net.minecraft.world.entity.LivingEntity, io.redspace.ironsspellbooks` = 0, 1.
- **Estado por campo:** alcance/geometria/dano/tipo/projétil/duração/targeting/cooldown/mana/execução efetiva ficam **NÃO VERIFICADOS** onde as arestas acima não determinarem operandos, guardas, fórmula e beneficiário. Nomes como `setRadius` ou `setDamage` provam apenas chamada simbólica, **não** o valor ou aplicabilidade de perk.
- **Boundary:** provider mantém efeitos/entidades próprias; Iron's mantém cast/mana/cooldown; Black Arcana não injeta segundo efeito nem delega autoridade de runtime ao RPG Skill Tree. Gate de mutação: **⛔ SEM_HOOK_SEGURO** até prova de contrato e QA provider-native.
- **Próxima inspeção:** reconstruir operandos/guards em chamadas relevantes usando bytecode exato, verificar host Iron's 3.16.3 e confirmar em client/servidor. `Stage 06.05` 🟡 e `Stage 09` ⚠️.

## Dependências compiladas adicionais — 24/10/2026

**Fonte:** [workflow de inventário exato #40120464325](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40120464325) (`SUCCESS`) e artefato JSON `wind-spellbooks-105-methods`; SHA-1 físico do provider `8744886899bc245ae147a44baa2b183689cec7da`. Dados extraídos de referências `javap` da classe acima, **não** de execução de gameplay.

| Método / região JVM | Evidência observada | Limite de atribuição |
|---|---|---|
| `getPercentAirSpeed(int)` | `fmul`, `i2f` | Percentual real não determinado. |
| `getPercentJump(int)` | `fadd`, `fmul`, `i2f`, `isub` | Não estabelece bônus efetivo por nível. |
| `onCast(Level, int, LivingEntity, CastSource, MagicData)` | Lê `ModMobEffectRegistry.TAILWIND`; `f2i`, `fmul`, `isub` | Duração, amplificador e stacking não determinados. |

O construtor ainda apresenta escritas de `baseManaCost`, `manaCostPerLevel`, `baseSpellPower`, `spellPowerPerLevel`, `castTime` e `defaultConfig`; seus valores não são inferidos desses nomes. Mesmo com os campos e operadores, **não há fluxo de operandos/guardas homologado, fórmula numérica aprovada, hook mutador seguro, nem QA provider-native**. Manter `NÃO VERIFICADO` e `SEM_HOOK_SEGURO` para integração de perks; denominadores e identidade 7/7 sem alteração.

## Fórmulas escalares adicionais verificadas — 24/10/2026

**🟡 Evidência binária de getters, sem QA de gameplay.** [Execução JVM exata #40126898432](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40126898432), artefato `wind-spellbooks-105-methods/mobility-getters.json`, verificado no JAR SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`. Os getters foram integralmente interpretados por parser conservador; `level` é o parâmetro inteiro no slot JVM 1. Fórmulas reproduzidas em notação matemática explicativa, **não** código do provider.

| Getter | Expressão compilada do retorno | Observação de tipo e operandos | Ainda NÃO VERIFICADO |
|---|---|---|---|
| `getPercentAirSpeed(int)` | `(((float)level * 0.15f) * 100.0f)` | Dois `fmul`, com conversão explícita `i2f`; manter ordem dos cálculos para respeitar arredondamento de `float`. | Nome do método não prova se a porcentagem é aditiva, multiplicativa, exibida na UI ou aplicada no movimento. |
| `getPercentJump(int)` | `((0.5f + (0.3f * ((float)(level - 1)))) * 100.0f)` | Subtração `isub` antes de `i2f`, seguida por `fmul`/`fadd`/`fmul`. | Não determina impulso real de salto, efeito de equipamentos, parâmetros de configuração ou stacking. |

A expressão compilada isolada não autoriza perk mutadora nem alteração em `onCast`. **⛔ SEM_HOOK_SEGURO** até confirmar chamador, geometrias e host; nenhuma alteração de mana, cooldown, efeitos, poderes, duração, entidades ou configuração foi implementada. Wind's/Iron's permanecem autoridades provider-native; Black Arcana possui seu runtime, RPG Skill Tree apenas progressão/perks por boundary real.

## Arestas de chamadas diretas e sinks co-presentes — 24/10/2026

**⚠️ Evidência restrita:** [CI exato #40130495377](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40130495377), artefato `getter-consumer-edges.json` com estado `PASS_SHA_EXACT_DIRECT_CALL_EDGE_INVENTORY` e SHA-1 oficial `8744886899bc245ae147a44baa2b183689cec7da`. O inventário examina chamadas diretas nos métodos desta classe de spell; não rastreia todas as classes do provider.

| Getter com expressão compilada já documentada | Chamador(es) diretos nesta classe | Invocação direta de `onCast` |
|---|---|---|
| `getPercentAirSpeed(int)` | `getUniqueInfo` | **não observado** |
| `getPercentJump(int)` | `getUniqueInfo` | **não observado** |

**Sinks/efeitos independentes no mesmo método:** `onCast` referencia `TAILWIND` e `LivingEntity.addEffect`, sem invocar diretamente os dois getters nesta classe. **Não significa que os percentuais sejam apenas de interface**: consumidores nas classes do efeito e do host ainda não foram examinados.

**Estado causal:** `SAME_METHOD_ONLY_NOT_GETTER_TO_SINK_DATAFLOW`. A presença do getter e de um setter no mesmo `onCast` **não** prova que o retorno chega àquele setter, nem seus guards/configuração/beneficiário. **⛔ `SEM_HOOK_SEGURO` para perks mutadoras**; não reproduzir efeitos provider-native nem alterar autoridades de Iron's/Wind's/Black Arcana/RPG Skill Tree. Stage 06.05 e Stage 09 sem promoção.

## Auditoria de chamadas entre classes do provider — 24/10/2026

**⚠️ Resultado estrutural, não efeito comprovado.** [Workflow de JAR exato #40135302517](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40135302517), `cross-class-getter-calls.json`, SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`: **64/64 classes** do namespace Wind's inspecionadas, **16 chamadas diretas** aos nove getters selecionados, **0 referências diretas a esses getters originadas em outras classes do próprio provider**.

`getPercentAirSpeed`: **1** instrução; `getPercentJump`: **1**; ambas no próprio `TailwindSpell`, nenhuma chamada direta por outras classes do namespace do Wind's. Na classe do spell, as chamadas diretas observadas são de `getUniqueInfo`. Isso **não** permite classificar os bônus como cosméticos nem exclui consumo pelo código do efeito/host.

A ausência de chamadas entre classes é relativa somente a `invoke*` explícitos no JAR Wind's 1.0.5; não inspeciona dependências host Iron's/IronSable, reflexão, dispatch virtual, effects indiretos, Mixins, calls via eventos nem fluxo JVM até os setters. **⛔ `SEM_HOOK_SEGURO`** para perks que modifiquem esses valores. Nenhum Stage ou contagem de spells foi alterado.

## Superfícies nativas do efeito no JAR exato — 24/10/2026

**✅ Evidência simbólica verificada; ⚠️ efeitos e valores runtime ainda não homologados.** [Workflow Wind #40136512061](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40136512061), artefato `effect-boundaries.json`, SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`. A classe `net.raptorzizi.wind_spellbooks.effect.TailwindEffect` está presente no JAR 1.0.5. A presença de classe e nome de método por si só não prova o registro/instanciação nem o resultado do jogo.

| Método da classe compilada | Evidência estrutural | Questões ainda abertas |
|---|---|---|
| `applyEffectTick(LivingEntity, int)` | Invoca `LivingEntity.getDeltaMovement`, `setDeltaMovement(DDD)` e `onGround`; lê `Player.xxa` e `Player.zza`; escreve `LivingEntity.fallDistance` | Fórmula/vetor/valor de fallDistance, guards, efetividade do tick e interactions físicas. |
| `onEffectStarted(LivingEntity, int)` | Lê `Attributes.JUMP_STRENGTH` e `AttributeModifier.Operation.ADD_MULTIPLIED_TOTAL`; invoca `AttributeInstance.addTransientModifier` e `removeModifier` | Valor do modifier, ordem/condições e vínculo com `getPercentJump`. |
| `onEffectRemoved(LivingEntity, int)` | Lê `Attributes.JUMP_STRENGTH` e `Attributes.MOVEMENT_SPEED`; invoca `removeModifier` | O método não demonstra onde o bônus de velocidade foi adicionado nem a política de cleanup. |

Os getters `getPercentJump` e `getPercentAirSpeed` continuam com **zero chamadas JVM diretas fora da classe TailwindSpell neste JAR**, mas isso **não** os classifica como cosméticos: `TailwindEffect` tem superfícies de movimento/atributos independentes. A chamada a `setDeltaMovement` não autoriza alterações no vetor; a chamada a `addTransientModifier` não estabelece o valor de porcentagem aplicado. O campo de registry `TAILWIND` é referenciado por `TailwindSpell.onCast`, sem factory/instance binding comprovado nesta etapa.

**⛔ Integração de perks:** sem hook mutador provider-native e sem contrato de stacking/efeito; não adicionar listener duplicado de queda/velocidade. Iron's/Wind's preservam a autoridade de casting/efeitos, Black Arcana seu próprio runtime, RPG Skill Tree apenas progressão.

## Registry compilado e hierarquia do efeito — 24/10/2026

**✅ Evidência estática, sem prova de factory-binding/runtime.** [CI Wind #40139355055](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40139355055), artefato `effect-registry-dispatch.json`, Wind's 1.0.5 SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`.

- `TailwindSpell` declara `extends AbstractSpell`; `TailwindEffect` declara `extends MagicMobEffect implements ISyncedMobEffect`.
- A classe `ModMobEffectRegistry` contém a string `tailwind`, campo `TAILWIND` (DeferredHolder), uso de `DeferredRegister.register(String, Supplier)` e dois sites `invokedynamic` na inicialização estática.
- O método auxiliar compilado `lambda$static$1` contém `new TailwindEffect` e a invocação do construtor `(MobEffectCategory, int)`. Isso é evidência da existência do **candidato** de factory, não de qual supplier bootstrap está conectado à entrada `TAILWIND`.
- O fluxo registry → supplier → classe concreta e os operandos que definem intensidade/duração do modifier não foram comprovados. Assim, os sinais anteriores de `JUMP_STRENGTH`, movimento e fallDistance permanecem **simbólicos** e não configuram novo ponto mutador seguro.

**⛔ SEM_HOOK_SEGURO:** não criar segundo `AttributeModifier`, recast ou listener de queda. O cast e os efeitos continuam provider-native; RPG Skill Tree permanece apenas provider de atributos/perks por contrato.

## Ligação compilada do registro `TAILWIND` — 24/10/2026

**✅ `PROVEN_BOUNDED_JVM_STACK_AND_BOOTSTRAP` no JAR oficial 1.0.5; runtime ⚠️ não testado.** A execução [Wind CI #40143051496](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40143051496) confirmou em `ModMobEffectRegistry.<clinit>` a cadeia exata: entrada literal `tailwind` → site `invokedynamic #1` para `Supplier` → method-handle `lambda$static$1` por `LambdaMetafactory` → chamada `DeferredRegister.register(String, Supplier)` → armazenamento no holder `TAILWIND`. A factory compilada `lambda$static$1` contém a criação de `TailwindEffect`.

A associação estática do holder à factory já tem prova; o registro em execução e a intensidade dos modificadores de `JUMP_STRENGTH`, movimento e `fallDistance` **não** foram validados. Os getters percentuais também não foram ligados por fluxo de operandos à aplicação do efeito. `runtime_instance_registration = NOT_TESTED`, `safe_mutating_hook = NOT_PROVEN`: **⛔ SEM_HOOK_SEGURO** para perks que alterem velocidade/salto/queda. Preservar efeitos provider-native.
