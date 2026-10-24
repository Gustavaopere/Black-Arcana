# Aeropic

**Registro estático:** ✅ `COUNTED_EXACT` no JAR 1.0.5; [prova binária](../EXACT-BINARY-SPELLS-1.0.5.md). Config, números e Survival ⚠️.

- **ID:** `wind_spellbooks:aeropic`
- **Classe runtime:** `net.raptorzizi.wind_spellbooks.spells.wind.AeropicSpell`
- **School:** Wind
- **Provider/JAR:** Wind's Spellbooks / `wind_spellbooks-1.0.5.jar`
- **Status:** PRESENTE

## Contract confirmado

Fingerprint ASM: `hasRecasts`, `usesImpulseCastData`, `usesAddEffect`. Aeropic é portanto um spell Wind com janela/lifecycle de recasts, mobilidade por impulso e effect provider-native.

## NÃO VERIFICADO

Número de recasts, janela, níveis, rarity, mana, cooldown, cast time, impulso por recast, effect, dano, target rules, cancel/finish semantics e aquisição específica.

## Deduplicação / fail-closed

Não implementar contador paralelo de recasts nem um segundo impulse ledger. O recast state do provider deve permanecer autoridade causal.

## Evidência

Runtime registry + ASM do pack; release oficial 1.0.5.

## Verificação JVM exata dos consumidores por método — 24/10/2026

**✅ Fonte binária exata:** `wind_spellbooks-1.0.5.jar`, SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`; [CI de inspeção Java 21 #40118955224](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40118955224) `SUCCESS` no passo de extração. **⚠️ Somente assinaturas e arestas de chamadas; não é prova de runtime, fórmula, parâmetros configurados nem hook mutador seguro.**

- Classe inspecionada: `net.raptorzizi.wind_spellbooks.spells.wind.AeropicSpell`.
- Contagem de métodos/declarações indexadas pelo parser: **13**; partes omitidas abaixo são deliberadamente fora do recorte de consumidores de perks.
- Grafo observável de invocações (`método de origem → símbolos referenciados`; a ordem causal e a entidade alvo exigem desambiguação adicional):
- `private float getDamage(int, net.minecraft.world.entity.LivingEntity);` → `getSpellPower:(ILnet/minecraft/world/entity/Entity;)F`
- `private int getDamageInt(int, net.minecraft.world.entity.LivingEntity);` → `getDamage:(ILnet/minecraft/world/entity/LivingEntity;)F`
- `public int getRecastCount(int, net.minecraft.world.entity.LivingEntity);` → `java/lang/Math.max:(II)I`
- `public java.util.List<net.minecraft.network.chat.MutableComponent> getUniqueInfo(int, net.minecraft.world.entity.LivingEntity);` → `getDamage:(ILnet/minecraft/world/entity/LivingEntity;)F`, `getRecastCount:(ILnet/minecraft/world/entity/LivingEntity;)I`
- `public void onCast(net.minecraft.world.level.Level, int, net.minecraft.world.entity.LivingEntity, io.redspace.ironsspellbooks.api.spells.CastSource, io.redspace.ironsspellbooks.api.magic.MagicData);` → `getDamageInt:(ILnet/minecraft/world/entity/LivingEntity;)I`, `getSpellPower:(ILnet/minecraft/world/entity/Entity;)F`, `java/lang/Math.max:(DD)D`, `net/minecraft/server/network/ServerGamePacketListenerImpl.teleport:(DDDFF)V`, `net/minecraft/world/effect/MobEffectInstance."<init>":(Lnet/minecraft/core/Holder;IIZZZ)V`, `net/minecraft/world/entity/LivingEntity.addEffect:(Lnet/minecraft/world/effect/MobEffectInstance;)Z`

- **Literais presentes em métodos selecionados (candidatos sem atribuição):** `public int getRecastCount(int, net.minecraft.world.entity.LivingEntity);` = 0, 1; `public void onCast(net.minecraft.world.level.Level, int, net.minecraft.world.entity.LivingEntity, io.redspace.ironsspellbooks` = 0, 1, 10, 20.
- **Estado por campo:** alcance/geometria/dano/tipo/projétil/duração/targeting/cooldown/mana/execução efetiva ficam **NÃO VERIFICADOS** onde as arestas acima não determinarem operandos, guardas, fórmula e beneficiário. Nomes como `setRadius` ou `setDamage` provam apenas chamada simbólica, **não** o valor ou aplicabilidade de perk.
- **Boundary:** provider mantém efeitos/entidades próprias; Iron's mantém cast/mana/cooldown; Black Arcana não injeta segundo efeito nem delega autoridade de runtime ao RPG Skill Tree. Gate de mutação: **⛔ SEM_HOOK_SEGURO** até prova de contrato e QA provider-native.
- **Próxima inspeção:** reconstruir operandos/guards em chamadas relevantes usando bytecode exato, verificar host Iron's 3.16.3 e confirmar em client/servidor. `Stage 06.05` 🟡 e `Stage 09` ⚠️.

## Dependências compiladas adicionais — 24/10/2026

**Fonte:** [workflow de inventário exato #40120464325](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40120464325) (`SUCCESS`) e artefato JSON `wind-spellbooks-105-methods`; SHA-1 físico do provider `8744886899bc245ae147a44baa2b183689cec7da`. Dados extraídos de referências `javap` da classe acima, **não** de execução de gameplay.

| Método / região JVM | Evidência observada | Limite de atribuição |
|---|---|---|
| `getRecastCount(int, LivingEntity)` | `isub` (subtração inteira) | Não estabelece total de recasts nem janela. |
| `onCast(Level, int, LivingEntity, CastSource, MagicData)` | Lê `ModMobEffectRegistry.ACROBATICS`, `Vec3.{x,y,z}`; escreve `LivingEntity.{hasImpulse,hurtMarked,invulnerableTime}`; operações `dadd`, `dmul`, `dsub`, `fadd`, `fdiv`, `fmul`; ramo `ifeq` | Não identifica vetor, alvo de cada escrita, custos ou regra de imunidade. |
| `getUniqueInfo(int, LivingEntity)` | Desvio `if_icmple` | Texto de apresentação não prova regra gameplay. |

O construtor ainda apresenta escritas de `baseManaCost`, `manaCostPerLevel`, `baseSpellPower`, `spellPowerPerLevel`, `castTime` e `defaultConfig`; seus valores não são inferidos desses nomes. Mesmo com os campos e operadores, **não há fluxo de operandos/guardas homologado, fórmula numérica aprovada, hook mutador seguro, nem QA provider-native**. Manter `NÃO VERIFICADO` e `SEM_HOOK_SEGURO` para integração de perks; denominadores e identidade 7/7 sem alteração.

## Getter escalar com proveniência de operandos — 24/10/2026

**🟡 Expressão aritmética compilada verificada, sem homologação de gameplay.** A inspeção do JAR exato `wind_spellbooks-1.0.5.jar` (SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`) reconstruiu a pilha JVM integral do método selecionado, mediante gramática estrita e sem opcodes desconhecidos. Fonte: [CI específico #40124346655](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40124346655), artefato `wind-spellbooks-105-methods/scalar-getters.json`.

- **Método:** `getRecastCount(int, LivingEntity)`.
- **Expressão observável:** `Math.max(0, level - 1)`, onde `level` é o primeiro parâmetro `int` (local JVM 1), e as operações seguem semântica de inteiros da JVM.
- **Limite de interpretação:** O retorno é uma contagem inteira calculada por este método; janela, consumo, recast extra e configuração externa não foram inspecionados.
- **Escopo da promoção:** esta evidência atualiza exclusivamente o getter acima; as advertências anteriores continuam válidas para alcance, targeting, dano, impulso, efeitos, custo, cooldown e integração.
- **Perk mutadora:** ⛔ `SEM_HOOK_SEGURO`, até demonstrar consumidor, lifecycle, bounds e contrato host/provider com QA em runtime; Black Arcana não duplica efeitos e RPG Skill Tree não assume autoridade de casting.

## Arestas de chamadas diretas e sinks co-presentes — 24/10/2026

**⚠️ Evidência restrita:** [CI exato #40130495377](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40130495377), artefato `getter-consumer-edges.json` com estado `PASS_SHA_EXACT_DIRECT_CALL_EDGE_INVENTORY` e SHA-1 oficial `8744886899bc245ae147a44baa2b183689cec7da`. O inventário examina chamadas diretas nos métodos desta classe de spell; não rastreia todas as classes do provider.

| Getter com expressão compilada já documentada | Chamador(es) diretos nesta classe | Invocação direta de `onCast` |
|---|---|---|
| `getRecastCount(int, LivingEntity)` | `getUniqueInfo` | **não observado** |

**Sinks/efeitos independentes no mesmo método:** `onCast` contém chamadas de teleporte/alteração do movimento e leitura do efeito `ACROBATICS`; não contém invocação direta de `getRecastCount` nesta classe. Isso NÃO exclui controle de recast no host ou em outra classe.

**Estado causal:** `SAME_METHOD_ONLY_NOT_GETTER_TO_SINK_DATAFLOW`. A presença do getter e de um setter no mesmo `onCast` **não** prova que o retorno chega àquele setter, nem seus guards/configuração/beneficiário. **⛔ `SEM_HOOK_SEGURO` para perks mutadoras**; não reproduzir efeitos provider-native nem alterar autoridades de Iron's/Wind's/Black Arcana/RPG Skill Tree. Stage 06.05 e Stage 09 sem promoção.

## Auditoria de chamadas entre classes do provider — 24/10/2026

**⚠️ Resultado estrutural, não efeito comprovado.** [Workflow de JAR exato #40135302517](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40135302517), `cross-class-getter-calls.json`, SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`: **64/64 classes** do namespace Wind's inspecionadas, **16 chamadas diretas** aos nove getters selecionados, **0 referências diretas a esses getters originadas em outras classes do próprio provider**.

`getRecastCount`: **1** instrução `invoke*` no JAR; 0 a partir de outras classes do namespace do Wind's. A chamada observada permanece em `getUniqueInfo`; host/recasts e gameplay não foram comprovados.

A ausência de chamadas entre classes é relativa somente a `invoke*` explícitos no JAR Wind's 1.0.5; não inspeciona dependências host Iron's/IronSable, reflexão, dispatch virtual, effects indiretos, Mixins, calls via eventos nem fluxo JVM até os setters. **⛔ `SEM_HOOK_SEGURO`** para perks que modifiquem esses valores. Nenhum Stage ou contagem de spells foi alterado.

## Superfícies nativas de recast do efeito — 24/10/2026

**✅ Metadados simbólicos confirmados, ⚠️ execução/valores pendentes.** [Workflow Wind #40136512061](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40136512061), artefato `effect-boundaries.json` do JAR `wind_spellbooks-1.0.5.jar`, SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`. A classe `net.raptorzizi.wind_spellbooks.effect.AeropicEffect` foi localizada no binário instalado; vinculação de registry e dispatch de runtime não decorrem somente do nome.

| Método compilado | Símbolos observados | Limites |
|---|---|---|
| `applyEffectTick(LivingEntity, int)` | `AbstractSpell.getRecastCount`, `PlayerRecasts.addRecast`, `hasRecastForSpell`, `RecastInstance.<init>`, `DamageSources.applyDamage`; escritas em `LivingEntity.fallDistance`, `Entity.invulnerableTime` | Não comprova contagem máxima, consumo, janela, alvo, dano e condições de aplicação. |
| `onEffectAdded(LivingEntity, int)` | `AbstractSpell.getRecastCount`, `ServerPlayer.getPersistentData`, `CompoundTag.putInt`/`remove` | Persistência/recast referenciados; valores, nomes das chaves NBT e regras exatas não provados. |
| `onEffectRemoved(LivingEntity, int)` | `PlayerRecasts.decrementRecastCount`, `hasRecastForSpell`, `CompoundTag.remove`, `LivingEntityAccessor.setLivingEntityFlagInvoker` | Não comprova ordem de cleanup, bloqueio anti-replay ou ausência de dupla atualização. |

**Distinção crítica:** o efeito chama simbolicamente **`io.redspace.ironsspellbooks.api.spells.AbstractSpell.getRecastCount`**, e não `AeropicSpell.getRecastCount` pelo nome da classe concreta. Logo, o inventário anterior de **zero chamadas entre classes diretamente qualificadas ao getter Aeropic** continua válido, mas não exclui dispatch virtual ao override. Para validar a fórmula `max(0, level - 1)` no recast real é necessário analisar receiver concreto e host Iron's 3.16.3; não atribuir comportamento dinâmico apenas pelo símbolo.

**⛔ Integração de perks:** preservar `PlayerRecasts` e seu lifecycle provider-native; não criar segundo contador, NBT duplicado ou manipulador de recast. Stage 06.05 🟡 e Stage 09 físico pendente.

## Compatibilidade compilada com `AbstractSpell.getRecastCount` — 24/10/2026

**✅ Assinatura e hierarquia declaradas no JAR exato; ⚠️ dispatch dinâmico não provado.** [CI Wind #40139355055](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40139355055), artefato `effect-registry-dispatch.json`, SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`.

- `AeropicSpell` declara diretamente `extends io.redspace.ironsspellbooks.api.spells.AbstractSpell` no cabeçalho JVM.
- O override `getRecastCount(int, LivingEntity)` declara exatamente o descritor `(ILnet/minecraft/world/entity/LivingEntity;)I`; o `AeropicEffect` chama simbolicamente `AbstractSpell.getRecastCount` com o mesmo descritor.
- `AeropicEffect` declara `extends MagicMobEffect implements ISyncedMobEffect` no seu cabeçalho compilado.
- O registry `ModMobEffectRegistry` tem o texto de registro `aeropic`, o campo `ACROBATICS`, **dois** suppliers `invokedynamic` totais, e um factory method `lambda$static$0` que contém `new AeropicEffect` e sua chamada de construtor. **Não foi traçado o BootstrapMethods ou a pilha que liga o campo `ACROBATICS` à instância.**

**Limite de interoperabilidade:** ABI igual e herança de `AbstractSpell` tornam o override estruturalmente compatível, mas não demonstram qual objeto está no receiver, o dispatch efetivo, a quantidade de recasts, o cleanup ou o stacking. `runtime_dispatch_to_spell_override = NOT_PROVEN` e `registration_field_to_instance_binding = NOT_PROVEN`. **⛔ SEM_HOOK_SEGURO**; não duplicar `PlayerRecasts` nem a persistência.
