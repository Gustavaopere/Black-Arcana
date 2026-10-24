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
