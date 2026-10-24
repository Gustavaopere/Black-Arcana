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
