# Wind Jump

**Registro estático:** ✅ `COUNTED_EXACT` no JAR 1.0.5; [prova binária](../EXACT-BINARY-SPELLS-1.0.5.md). Config, números e Survival ⚠️.

- **ID:** `wind_spellbooks:wind_jump`
- **Classe runtime:** `net.raptorzizi.wind_spellbooks.spells.wind.WindJumpSpell`
- **School:** Wind
- **Provider/JAR:** Wind's Spellbooks / `wind_spellbooks-1.0.5.jar`
- **Status:** PRESENTE — registration observado no runtime
- **Upgradable:** sim, conforme descrição oficial do conjunto de sete spells

## Contract confirmado

O bytecode carregado no pack foi classificado com `createsEntity`, `usesImpulseCastData`, `createsProjectile` e `usesAddEffect`. Portanto Wind Jump é um contract de mobilidade/impulso que também instancia conteúdo provider-native e aplica effect; o comportamento fino da entity/projectile permanece authority do addon.

## NÃO VERIFICADO

Níveis exatos, rarity, mana, cooldown, cast time, magnitude/direção do impulso, projectile purpose, damage, duração do effect, fall-damage behavior, target rules, PvP e aquisição específica.

## Deduplicação / fail-closed

Não criar um segundo impulso/projectile/effect para o mesmo cast. Uma perk/bridge deve reagir a causalidade comprovada do cast, nunca inferir Wind Jump apenas por alteração brusca de velocidade.

## Evidência

Release 1.0.5 (CurseForge file 8485822) + logs runtime do pack/ASM FundamentalPrinciples.

## Verificação JVM exata dos consumidores por método — 24/10/2026

**✅ Fonte binária exata:** `wind_spellbooks-1.0.5.jar`, SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`; [CI de inspeção Java 21 #40118955224](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40118955224) `SUCCESS` no passo de extração. **⚠️ Somente assinaturas e arestas de chamadas; não é prova de runtime, fórmula, parâmetros configurados nem hook mutador seguro.**

- Classe inspecionada: `net.raptorzizi.wind_spellbooks.spells.wind.WindJumpSpell`.
- Contagem de métodos/declarações indexadas pelo parser: **11**; partes omitidas abaixo são deliberadamente fora do recorte de consumidores de perks.
- Grafo observável de invocações (`método de origem → símbolos referenciados`; a ordem causal e a entidade alvo exigem desambiguação adicional):
- `public java.util.List<net.minecraft.network.chat.MutableComponent> getUniqueInfo(int, net.minecraft.world.entity.LivingEntity);` → `getFloatDuration:(ILnet/minecraft/world/entity/LivingEntity;)I`, `getJumpHeight:(ILnet/minecraft/world/entity/LivingEntity;)F`
- `public void onCast(net.minecraft.world.level.Level, int, net.minecraft.world.entity.LivingEntity, io.redspace.ironsspellbooks.api.spells.CastSource, io.redspace.ironsspellbooks.api.magic.MagicData);` → `getFloatDuration:(ILnet/minecraft/world/entity/LivingEntity;)I`, `getJumpStrength:(ILnet/minecraft/world/entity/LivingEntity;)F`, `getSpellPower:(ILnet/minecraft/world/entity/Entity;)F`, `io/redspace/ironsspellbooks/capabilities/magic/ImpulseCastData."<init>":(FFFZ)V`, `io/redspace/ironsspellbooks/entity/spells/gust/GustCollider."<init>":(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;)V`, `io/redspace/ironsspellbooks/entity/spells/gust/GustCollider.setDealDamageActive:()V`, `io/redspace/ironsspellbooks/entity/spells/gust/GustCollider.setPos:(Lnet/minecraft/world/phys/Vec3;)V`, `io/redspace/ironsspellbooks/entity/spells/gust/GustCollider.tick:()V`, `net/minecraft/world/effect/MobEffectInstance."<init>":(Lnet/minecraft/core/Holder;IIZZZ)V`, `net/minecraft/world/entity/LivingEntity.addEffect:(Lnet/minecraft/world/effect/MobEffectInstance;)Z`, `net/minecraft/world/level/Level.addFreshEntity:(Lnet/minecraft/world/entity/Entity;)Z`
- `public void onClientCast(net.minecraft.world.level.Level, int, net.minecraft.world.entity.LivingEntity, io.redspace.ironsspellbooks.api.spells.ICastData);` → `java/lang/Math.max:(DD)D`

- **Literais presentes em métodos selecionados (candidatos sem atribuição):** `public void onCast(net.minecraft.world.level.Level, int, net.minecraft.world.entity.LivingEntity, io.redspace.ironsspellbooks` = 0, 1, 5, 9.
- **Estado por campo:** alcance/geometria/dano/tipo/projétil/duração/targeting/cooldown/mana/execução efetiva ficam **NÃO VERIFICADOS** onde as arestas acima não determinarem operandos, guardas, fórmula e beneficiário. Nomes como `setRadius` ou `setDamage` provam apenas chamada simbólica, **não** o valor ou aplicabilidade de perk.
- **Boundary:** provider mantém efeitos/entidades próprias; Iron's mantém cast/mana/cooldown; Black Arcana não injeta segundo efeito nem delega autoridade de runtime ao RPG Skill Tree. Gate de mutação: **⛔ SEM_HOOK_SEGURO** até prova de contrato e QA provider-native.
- **Próxima inspeção:** reconstruir operandos/guards em chamadas relevantes usando bytecode exato, verificar host Iron's 3.16.3 e confirmar em client/servidor. `Stage 06.05` 🟡 e `Stage 09` ⚠️.

## Dependências compiladas adicionais — 24/10/2026

**Fonte:** [workflow de inventário exato #40120464325](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40120464325) (`SUCCESS`) e artefato JSON `wind-spellbooks-105-methods`; SHA-1 físico do provider `8744886899bc245ae147a44baa2b183689cec7da`. Dados extraídos de referências `javap` da classe acima, **não** de execução de gameplay.

| Método / região JVM | Evidência observada | Limite de atribuição |
|---|---|---|
| `getJumpHeight(int, LivingEntity)` / `getJumpStrength(int, LivingEntity)` | `fmul` / `dadd`, `dmul`, `d2f`, `i2d` | Não determina velocidade, altura ou vetor efetivo. |
| `getFloatDuration(int, LivingEntity)` | `imul` | Unidades/ticks e escala não reconstruídos. |
| `onCast(Level, int, LivingEntity, CastSource, MagicData)` | Escreve `GustCollider.{amplifier,range,strength}` e `LivingEntity.hasImpulse`; lê `MobEffects.SLOW_FALLING`, `Vec3.{x,y,z}` | É evidência de escrita em campos do collider, não de valor/range aplicado. |
| `onClientCast(Level, int, LivingEntity, ICastData)` | Lê `ImpulseCastData.{hasImpulse,x,y,z}` e escreve `LivingEntity.hasImpulse`; desvio `ifeq` | Não transferir autoridade ao cliente nem inferir equivalência entre client e server. |

O construtor ainda apresenta escritas de `baseManaCost`, `manaCostPerLevel`, `baseSpellPower`, `spellPowerPerLevel`, `castTime` e `defaultConfig`; seus valores não são inferidos desses nomes. Mesmo com os campos e operadores, **não há fluxo de operandos/guardas homologado, fórmula numérica aprovada, hook mutador seguro, nem QA provider-native**. Manter `NÃO VERIFICADO` e `SEM_HOOK_SEGURO` para integração de perks; denominadores e identidade 7/7 sem alteração.

## Getter escalar com proveniência de operandos — 24/10/2026

**🟡 Expressão aritmética compilada verificada, sem homologação de gameplay.** A inspeção do JAR exato `wind_spellbooks-1.0.5.jar` (SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`) reconstruiu a pilha JVM integral do método selecionado, mediante gramática estrita e sem opcodes desconhecidos. Fonte: [CI específico #40124346655](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40124346655), artefato `wind-spellbooks-105-methods/scalar-getters.json`.

- **Método:** `getFloatDuration(int, LivingEntity)`.
- **Expressão observável:** `100 * level`, onde `level` é o primeiro parâmetro `int` (local JVM 1), e as operações seguem semântica de inteiros da JVM.
- **Limite de interpretação:** Apesar do nome do método, a assinatura retorna int; a escala e o uso da duração pelo efeito SLOW_FALLING ainda não foram auditados.
- **Escopo da promoção:** esta evidência atualiza exclusivamente o getter acima; as advertências anteriores continuam válidas para alcance, targeting, dano, impulso, efeitos, custo, cooldown e integração.
- **Perk mutadora:** ⛔ `SEM_HOOK_SEGURO`, até demonstrar consumidor, lifecycle, bounds e contrato host/provider com QA em runtime; Black Arcana não duplica efeitos e RPG Skill Tree não assume autoridade de casting.
