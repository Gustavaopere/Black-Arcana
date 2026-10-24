# Iron Slash

**Registro estático:** ✅ `COUNTED_EXACT` no JAR 1.0.5; [prova binária](../EXACT-BINARY-SPELLS-1.0.5.md). Config, números e Survival ⚠️.

- **ID:** `wind_spellbooks:iron_slash`
- **Classe runtime:** `net.raptorzizi.wind_spellbooks.spells.wind.IronSlashSpell`
- **School:** Wind
- **Provider/JAR:** Wind's Spellbooks / `wind_spellbooks-1.0.5.jar`
- **Status:** PRESENTE

## Contract confirmado

Fingerprint ASM: `usesPotentiation`, `createsEntity`, `usesImpulseCastData`, `usesTeleport`, `usesAddEffect`. Isso prova que Iron Slash combina lógica de potentiation do ecossistema, entity provider-native, impulso, teleport e effect dentro do mesmo spell contract.

## NÃO VERIFICADO

Níveis, rarity, mana, cooldown, cast time, weapon contribution, dano, teleport destination/range, impulse magnitude, effect, target rules, invulnerability frames, PvP/friendly-fire e aquisição.

## Deduplicação / fail-closed

É um espaço já ocupado de ataque Wind + mobilidade/teleporte/potentiation. Black Arcana não deve recriar um dash-slash equivalente nem executar segundo teleport/impulse/effect fora dos hooks do provider.

## Evidência

Runtime registry + ASM do pack; release oficial 1.0.5.

## Verificação JVM exata dos consumidores por método — 24/10/2026

**✅ Fonte binária exata:** `wind_spellbooks-1.0.5.jar`, SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`; [CI de inspeção Java 21 #40118955224](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40118955224) `SUCCESS` no passo de extração. **⚠️ Somente assinaturas e arestas de chamadas; não é prova de runtime, fórmula, parâmetros configurados nem hook mutador seguro.**

- Classe inspecionada: `net.raptorzizi.wind_spellbooks.spells.wind.IronSlashSpell`.
- Contagem de métodos/declarações indexadas pelo parser: **15**; partes omitidas abaixo são deliberadamente fora do recorte de consumidores de perks.
- Grafo observável de invocações (`método de origem → símbolos referenciados`; a ordem causal e a entidade alvo exigem desambiguação adicional):
- `private float getDamage(int, net.minecraft.world.entity.LivingEntity);` → `getSpellPower:(ILnet/minecraft/world/entity/Entity;)F`, `io/redspace/ironsspellbooks/api/util/Utils.getWeaponDamage:(Lnet/minecraft/world/entity/LivingEntity;)F`
- `private java.lang.String getDamageText(int, net.minecraft.world.entity.LivingEntity);` → `getDamage:(ILnet/minecraft/world/entity/LivingEntity;)F`, `getSpellPower:(ILnet/minecraft/world/entity/Entity;)F`, `io/redspace/ironsspellbooks/api/util/Utils.getWeaponDamage:(Lnet/minecraft/world/entity/LivingEntity;)F`
- `public java.util.List<net.minecraft.network.chat.MutableComponent> getUniqueInfo(int, net.minecraft.world.entity.LivingEntity);` → `getDamageText:(ILnet/minecraft/world/entity/LivingEntity;)Ljava/lang/String;`, `getDistance:(ILnet/minecraft/world/entity/LivingEntity;)F`
- `public void onCast(net.minecraft.world.level.Level, int, net.minecraft.world.entity.LivingEntity, io.redspace.ironsspellbooks.api.spells.CastSource, io.redspace.ironsspellbooks.api.magic.MagicData);` → `getDamage:(ILnet/minecraft/world/entity/LivingEntity;)F`, `getDistance:(ILnet/minecraft/world/entity/LivingEntity;)F`, `io/redspace/ironsspellbooks/spells/ender/TeleportSpell.findTeleportLocation:(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;F)Lnet/minecraft/world/phys/Vec3;`, `net/minecraft/world/entity/LivingEntity.stopRiding:()V`, `net/minecraft/world/level/Level.addFreshEntity:(Lnet/minecraft/world/entity/Entity;)Z`, `net/minecraft/world/level/Level.clip:(Lnet/minecraft/world/level/ClipContext;)Lnet/minecraft/world/phys/BlockHitResult;`
- `public void onServerCastTick(net.minecraft.world.level.Level, int, net.minecraft.world.entity.LivingEntity, io.redspace.ironsspellbooks.api.magic.MagicData);` → `io/redspace/ironsspellbooks/api/spells/AbstractSpell.onServerCastTick:(Lnet/minecraft/world/level/Level;ILnet/minecraft/world/entity/LivingEntity;Lio/redspace/ironsspellbooks/api/magic/MagicData;)V`

- **Literais presentes em métodos selecionados (candidatos sem atribuição):** `public void onCast(net.minecraft.world.level.Level, int, net.minecraft.world.entity.LivingEntity, io.redspace.ironsspellbooks` = 1; `public void onServerCastTick(net.minecraft.world.level.Level, int, net.minecraft.world.entity.LivingEntity, io.redspace.irons` = 0, 2, 3, 5.
- **Estado por campo:** alcance/geometria/dano/tipo/projétil/duração/targeting/cooldown/mana/execução efetiva ficam **NÃO VERIFICADOS** onde as arestas acima não determinarem operandos, guardas, fórmula e beneficiário. Nomes como `setRadius` ou `setDamage` provam apenas chamada simbólica, **não** o valor ou aplicabilidade de perk.
- **Boundary:** provider mantém efeitos/entidades próprias; Iron's mantém cast/mana/cooldown; Black Arcana não injeta segundo efeito nem delega autoridade de runtime ao RPG Skill Tree. Gate de mutação: **⛔ SEM_HOOK_SEGURO** até prova de contrato e QA provider-native.
- **Próxima inspeção:** reconstruir operandos/guards em chamadas relevantes usando bytecode exato, verificar host Iron's 3.16.3 e confirmar em client/servidor. `Stage 06.05` 🟡 e `Stage 09` ⚠️.

## Dependências compiladas adicionais — 24/10/2026

**Fonte:** [workflow de inventário exato #40120464325](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40120464325) (`SUCCESS`) e artefato JSON `wind-spellbooks-105-methods`; SHA-1 físico do provider `8744886899bc245ae147a44baa2b183689cec7da`. Dados extraídos de referências `javap` da classe acima, **não** de execução de gameplay.

| Método / região JVM | Evidência observada | Limite de atribuição |
|---|---|---|
| `getDistance(int, LivingEntity)` / `getDamage(int, LivingEntity)` | `fadd`, `fmul`, `i2f` / `fadd` | Escalas de distância e dano não verificadas. |
| `performDash(Level, LivingEntity, Vec3)` | Escreve `LivingEntity.hurtMarked:Z`; `ddiv`, `i2d`, `iadd`; desvio `ifle` | Não autoriza alterar vetor, alcance ou hitbox. |
| `onCast(Level, int, LivingEntity, CastSource, MagicData)` | Lê `Level.isClientSide:Z`, `Vec3.{x,y,z}`; desvios `if_acmpeq`, `ifeq` | O branch real de execução servidor/cliente e o alvo exigem reconstrução. |

O construtor ainda apresenta escritas de `baseManaCost`, `manaCostPerLevel`, `baseSpellPower`, `spellPowerPerLevel`, `castTime` e `defaultConfig`; seus valores não são inferidos desses nomes. Mesmo com os campos e operadores, **não há fluxo de operandos/guardas homologado, fórmula numérica aprovada, hook mutador seguro, nem QA provider-native**. Manter `NÃO VERIFICADO` e `SEM_HOOK_SEGURO` para integração de perks; denominadores e identidade 7/7 sem alteração.

## Fórmulas escalares adicionais verificadas — 24/10/2026

**🟡 Evidência binária de getters, sem QA de gameplay.** [Execução JVM exata #40126898432](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40126898432), artefato `wind-spellbooks-105-methods/mobility-getters.json`, verificado no JAR SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`. Os getters foram integralmente interpretados por parser conservador; `level` é o parâmetro inteiro no slot JVM 1. Fórmulas reproduzidas em notação matemática explicativa, **não** código do provider.

| Getter | Expressão compilada do retorno | Observação de tipo e operandos | Ainda NÃO VERIFICADO |
|---|---|---|---|
| `getDistance(int, LivingEntity)` | `10.0f + ((float)level * 2.0f)` | Expressão `float` formada por `fadd`/`fmul`/`i2f`. | Não comprova distância efetiva de dash/teleporte, distância de target, collision, cancelamentos ou limites de servidor. |

A expressão compilada isolada não autoriza perk mutadora nem alteração em `onCast`. **⛔ SEM_HOOK_SEGURO** até confirmar chamador, geometrias e host; nenhuma alteração de mana, cooldown, efeitos, poderes, duração, entidades ou configuração foi implementada. Wind's/Iron's permanecem autoridades provider-native; Black Arcana possui seu runtime, RPG Skill Tree apenas progressão/perks por boundary real.

## Arestas de chamadas diretas e sinks co-presentes — 24/10/2026

**⚠️ Evidência restrita:** [CI exato #40130495377](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40130495377), artefato `getter-consumer-edges.json` com estado `PASS_SHA_EXACT_DIRECT_CALL_EDGE_INVENTORY` e SHA-1 oficial `8744886899bc245ae147a44baa2b183689cec7da`. O inventário examina chamadas diretas nos métodos desta classe de spell; não rastreia todas as classes do provider.

| Getter com expressão compilada já documentada | Chamador(es) diretos nesta classe | Invocação direta de `onCast` |
|---|---|---|
| `getDistance(int, LivingEntity)` | `getUniqueInfo, onCast` | **observado** |

**Sinks/efeitos independentes no mesmo método:** `onCast` também invoca `TeleportSpell.findTeleportLocation` e `performDash`; o vínculo entre retorno de `getDistance`, argumentos do teleporte e deslocamento físico efetivo não foi demonstrado.

**Estado causal:** `SAME_METHOD_ONLY_NOT_GETTER_TO_SINK_DATAFLOW`. A presença do getter e de um setter no mesmo `onCast` **não** prova que o retorno chega àquele setter, nem seus guards/configuração/beneficiário. **⛔ `SEM_HOOK_SEGURO` para perks mutadoras**; não reproduzir efeitos provider-native nem alterar autoridades de Iron's/Wind's/Black Arcana/RPG Skill Tree. Stage 06.05 e Stage 09 sem promoção.

## Auditoria de chamadas entre classes do provider — 24/10/2026

**⚠️ Resultado estrutural, não efeito comprovado.** [Workflow de JAR exato #40135302517](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40135302517), `cross-class-getter-calls.json`, SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`: **64/64 classes** do namespace Wind's inspecionadas, **16 chamadas diretas** aos nove getters selecionados, **0 referências diretas a esses getters originadas em outras classes do próprio provider**.

`getDistance`: **2** instruções diretas, ambas em `IronSlashSpell`; nenhuma chamada direta por outras classes do namespace do Wind's. Isso não demonstra o fluxo até `findTeleportLocation` ou `performDash`.

A ausência de chamadas entre classes é relativa somente a `invoke*` explícitos no JAR Wind's 1.0.5; não inspeciona dependências host Iron's/IronSable, reflexão, dispatch virtual, effects indiretos, Mixins, calls via eventos nem fluxo JVM até os setters. **⛔ `SEM_HOOK_SEGURO`** para perks que modifiquem esses valores. Nenhum Stage ou contagem de spells foi alterado.
