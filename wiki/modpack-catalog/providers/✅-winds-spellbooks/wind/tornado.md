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
