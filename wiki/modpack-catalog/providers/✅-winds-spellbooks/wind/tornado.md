# Tornado

**Registro estático:** ✅ `COUNTED_EXACT` no JAR 1.0.5; [prova binária](../EXACT-BINARY-SPELLS-1.0.5.md). Config, números e Survival ⚠️.

- **ID:** `wind_spellbooks:tornado`
- **Classe runtime:** `net.raptorzizi.wind_spellbooks.spells.wind.TornadoSpell`
- **School:** Wind
- **Provider/JAR:** Wind's Spellbooks / `wind_spellbooks-1.0.5.jar`
- **Status:** PRESENTE

## Contract confirmado

Fingerprint ASM: `createsEntity`, `createsProjectile`, `usesRaycast`. O cast resolve alguma forma de alvo/posição por raycast e instancia entity/projectile provider-native. A release 1.0.3 registrou especificamente um fix de crash de Tornado em servidor, reforçando que o lifecycle server é parte sensível do contract.

## NÃO VERIFICADO

Níveis, rarity, mana, cooldown, cast time, raycast range, entidade concreta, duração, pull/knockback/damage, area, target/friendly-fire/PvP/boss rules e aquisição específica.

## Deduplicação / fail-closed

Não criar segundo tornado, scan, force solver ou projectile. Tratar o provider como authority do alvo resolvido, entity lifecycle e damage/force settlement.

## Evidência

Release 1.0.5 + changelog 1.0.3 + runtime ASM do pack.

## Verificação JVM exata dos consumidores por método — 24/10/2026

**✅ Fonte binária exata:** `wind_spellbooks-1.0.5.jar`, SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`; [CI de inspeção Java 21 #40118955224](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40118955224) `SUCCESS` no passo de extração. **⚠️ Somente assinaturas e arestas de chamadas; não é prova de runtime, fórmula, parâmetros configurados nem hook mutador seguro.**

- Classe inspecionada: `net.raptorzizi.wind_spellbooks.spells.wind.TornadoSpell`.
- Contagem de métodos/declarações indexadas pelo parser: **13**; partes omitidas abaixo são deliberadamente fora do recorte de consumidores de perks.
- Grafo observável de invocações (`método de origem → símbolos referenciados`; a ordem causal e a entidade alvo exigem desambiguação adicional):
- `private float getDamage(int, net.minecraft.world.entity.LivingEntity);` → `getSpellPower:(ILnet/minecraft/world/entity/Entity;)F`
- `public float getRadius(int, net.minecraft.world.entity.LivingEntity);` → `getSpellPower:(ILnet/minecraft/world/entity/Entity;)F`
- `public java.util.List<net.minecraft.network.chat.MutableComponent> getUniqueInfo(int, net.minecraft.world.entity.LivingEntity);` → `getRadius:(ILnet/minecraft/world/entity/LivingEntity;)F`
- `public void onCast(net.minecraft.world.level.Level, int, net.minecraft.world.entity.LivingEntity, io.redspace.ironsspellbooks.api.spells.CastSource, io.redspace.ironsspellbooks.api.magic.MagicData);` → `getDamage:(ILnet/minecraft/world/entity/LivingEntity;)F`, `getRadius:(ILnet/minecraft/world/entity/LivingEntity;)F`, `io/redspace/ironsspellbooks/api/util/Utils.raycastForEntity:(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;FZ)Lnet/minecraft/world/phys/HitResult;`, `net/minecraft/world/level/Level.addFreshEntity:(Lnet/minecraft/world/entity/Entity;)Z`, `net/raptorzizi/wind_spellbooks/entity/spells/tornado/TornadoEntity.setDamage:(F)V`, `net/raptorzizi/wind_spellbooks/entity/spells/tornado/TornadoEntity.setDuration:(I)V`, `net/raptorzizi/wind_spellbooks/entity/spells/tornado/TornadoEntity.setRadius:(F)V`

- **Literais presentes em métodos selecionados (candidatos sem atribuição):** `private float getDamage(int, net.minecraft.world.entity.LivingEntity);` = 2; `public void onCast(net.minecraft.world.level.Level, int, net.minecraft.world.entity.LivingEntity, io.redspace.ironsspellbooks` = 1.
- **Estado por campo:** alcance/geometria/dano/tipo/projétil/duração/targeting/cooldown/mana/execução efetiva ficam **NÃO VERIFICADOS** onde as arestas acima não determinarem operandos, guardas, fórmula e beneficiário. Nomes como `setRadius` ou `setDamage` provam apenas chamada simbólica, **não** o valor ou aplicabilidade de perk.
- **Boundary:** provider mantém efeitos/entidades próprias; Iron's mantém cast/mana/cooldown; Black Arcana não injeta segundo efeito nem delega autoridade de runtime ao RPG Skill Tree. Gate de mutação: **⛔ SEM_HOOK_SEGURO** até prova de contrato e QA provider-native.
- **Próxima inspeção:** reconstruir operandos/guards em chamadas relevantes usando bytecode exato, verificar host Iron's 3.16.3 e confirmar em client/servidor. `Stage 06.05` 🟡 e `Stage 09` ⚠️.

## Dependências compiladas adicionais — 24/10/2026

**Fonte:** [workflow de inventário exato #40120464325](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40120464325) (`SUCCESS`) e artefato JSON `wind-spellbooks-105-methods`; SHA-1 físico do provider `8744886899bc245ae147a44baa2b183689cec7da`. Dados extraídos de referências `javap` da classe acima, **não** de execução de gameplay.

| Método / região JVM | Evidência observada | Limite de atribuição |
|---|---|---|
| `getRadius(int, LivingEntity)` | `fadd`, `fmul`, `i2f` | Não estabelece raio em blocos. |
| `getDamage(int, LivingEntity)` / `getDuration(int)` | `fmul` / `iadd`, `imul` | Dano, multiplicador e ticks ainda não determinados. |
| `onCast(Level, int, LivingEntity, CastSource, MagicData)` | Lê `Vec3.{x,y,z}`; desvio `ifeq`; as chamadas `TornadoEntity.setDamage`, `setRadius`, `setDuration` já foram inventariadas no PR #880 | Sem rastreio da pilha não é possível associar operandos aos setters. |

O construtor ainda apresenta escritas de `baseManaCost`, `manaCostPerLevel`, `baseSpellPower`, `spellPowerPerLevel`, `castTime` e `defaultConfig`; seus valores não são inferidos desses nomes. Mesmo com os campos e operadores, **não há fluxo de operandos/guardas homologado, fórmula numérica aprovada, hook mutador seguro, nem QA provider-native**. Manter `NÃO VERIFICADO` e `SEM_HOOK_SEGURO` para integração de perks; denominadores e identidade 7/7 sem alteração.

## Getter escalar com proveniência de operandos — 24/10/2026

**🟡 Expressão aritmética compilada verificada, sem homologação de gameplay.** A inspeção do JAR exato `wind_spellbooks-1.0.5.jar` (SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`) reconstruiu a pilha JVM integral do método selecionado, mediante gramática estrita e sem opcodes desconhecidos. Fonte: [CI específico #40124346655](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40124346655), artefato `wind-spellbooks-105-methods/scalar-getters.json`.

- **Método:** `getDuration(int)`.
- **Expressão observável:** `15 * (5 + (level * 2))`, onde `level` é o primeiro parâmetro `int` (local JVM 1), e as operações seguem semântica de inteiros da JVM.
- **Limite de interpretação:** O método retorna esse inteiro; duração efetiva de TornadoEntity depende da análise do chamador e do lifecycle, ainda pendentes.
- **Escopo da promoção:** esta evidência atualiza exclusivamente o getter acima; as advertências anteriores continuam válidas para alcance, targeting, dano, impulso, efeitos, custo, cooldown e integração.
- **Perk mutadora:** ⛔ `SEM_HOOK_SEGURO`, até demonstrar consumidor, lifecycle, bounds e contrato host/provider com QA em runtime; Black Arcana não duplica efeitos e RPG Skill Tree não assume autoridade de casting.

## Arestas de chamadas diretas e sinks co-presentes — 24/10/2026

**⚠️ Evidência restrita:** [CI exato #40130495377](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40130495377), artefato `getter-consumer-edges.json` com estado `PASS_SHA_EXACT_DIRECT_CALL_EDGE_INVENTORY` e SHA-1 oficial `8744886899bc245ae147a44baa2b183689cec7da`. O inventário examina chamadas diretas nos métodos desta classe de spell; não rastreia todas as classes do provider.

| Getter com expressão compilada já documentada | Chamador(es) diretos nesta classe | Invocação direta de `onCast` |
|---|---|---|
| `getDuration(int)` | `getUniqueInfo, onCast` | **observado** |

**Sinks/efeitos independentes no mesmo método:** `onCast` contém `TornadoEntity.setDamage`, `setDuration` e `setRadius`. A relação causal de `getDuration` com o argumento de `setDuration` ainda não foi comprovada por fluxo JVM; ticks/lifecycle também permanecem abertos.

**Estado causal:** `SAME_METHOD_ONLY_NOT_GETTER_TO_SINK_DATAFLOW`. A presença do getter e de um setter no mesmo `onCast` **não** prova que o retorno chega àquele setter, nem seus guards/configuração/beneficiário. **⛔ `SEM_HOOK_SEGURO` para perks mutadoras**; não reproduzir efeitos provider-native nem alterar autoridades de Iron's/Wind's/Black Arcana/RPG Skill Tree. Stage 06.05 e Stage 09 sem promoção.
