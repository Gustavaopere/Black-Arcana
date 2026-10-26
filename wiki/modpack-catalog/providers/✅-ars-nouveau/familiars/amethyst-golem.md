# Amethyst Golem Familiar

State: `SOURCE-PINNED 5.13.1 / CONSTRUCTOR-TYPE MISMATCH / RUNTIME QA PENDING`

Registry id: `ars_nouveau:familiar_amethyst_golem`
Conversion entity: Ars Nouveau `AmethystGolem`
Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Aquisição

O holder reconhece `AmethystGolem`. A entidade base pode ser criada pelo Ritual of Awakening a partir de Budding Amethyst; depois, Binding pode convertê-la em Bound Script para desbloquear o familiar.

## Behavior confirmado

### Knockback do owner

`FamiliarEvents.knockbackEvent` procura familiar `FamiliarAmethystGolem` vivo cujo owner seja o alvo do `LivingKnockBackEvent`. Se existir ao menos um, define:

`event.strength = event.strength * 0.5`

Ou seja, o knockback recebido pelo owner é reduzido pela metade nesse path.

### Contra-knockback

Em `LivingDamageEvent.Post`, quando:

- o dano não possui `BYPASSES_ARMOR`;
- o alvo é `Player`;
- existe Amethyst Golem familiar do alvo;
- a source entity é `LivingEntity`;
- o atacante está a menos de 3 blocos do jogador,
o atacante recebe `knockback(0.5f, ...)` para afastá-lo do owner.

### Amethyst Shard / Shielding

Interagir com o familiar usando item da tag NeoForge `GEMS_AMETHYST` aplica `ModPotions.DEFENCE_EFFECT` ao jogador por `20 * 60 * 3 = 3600` ticks (3 minutos) e consome 1 item fora de creative/infinite materials.

## Divergência de source — EntityType do constructor

O holder 5.13.1 cria `new FamiliarAmethystGolem(ModEntities.ENTITY_FAMILIAR_BOOKWYRM.get(), world)`, enquanto:

- `FamiliarAmethystGolem.getType()` retorna `ModEntities.FAMILIAR_AMETHYST_GOLEM.get()`;
- `ModEntities` registra um EntityType próprio para `FamiliarAmethystGolem` sob `familiar_amethyst_golem`.

Isso é um mismatch real no source checkpoint. O catálogo **não** assume se é benigno ou defeituoso em runtime; exige QA do JAR instalado antes de qualquer integração dependente do tipo da entidade.

## Authority e deduplicação

- Knockback mitigation, retaliation e Defence/Shielding são Ars-owned.
- Black Arcana/RPG Skill Tree não devem duplicar redução de knockback ou retaliatory knockback apenas por detectar o familiar.
- Bridges que dependam do EntityType devem falhar fechadas até o mismatch ser observado no runtime 5.13.1.

## QA pendente

1. Invocar o familiar no JAR instalado e confirmar EntityType/serialization real.
2. Validar persistência após relog/chunk unload.
3. Confirmar stacking de knockback reduction com armor/perks/outros mods.
4. Confirmar o behavior do `DEFENCE_EFFECT` no pack real.

## Certificação técnica estática — Familiar Amethyst Golem (2026-10-26)

**✅ somente `STATIC_TECHNICAL_CATALOG_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Fonte exata `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, versão física Ars 5.13.1 (`ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`). **O teste binário existente de 109 registros cobre glyphs/rituais, NÃO confirma o bytecode dos familiares ou o seu EntityType em execução.** [AmethystFamiliarHolder.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/familiars/AmethystFamiliarHolder.java) · [FamiliarAmethystGolem.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/familiar/FamiliarAmethystGolem.java) · [ModEntities.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/ModEntities.java) · [FamiliarEntity.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/familiar/FamiliarEntity.java) · [FamiliarEvents.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/FamiliarEvents.java) · [FamiliarData.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/capability/FamiliarData.java) · [PacketSummonFamiliar.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/network/PacketSummonFamiliar.java).

| Contrato | Comportamento confirmado no source |
|---|---|
| Identidade/Binding | `AmethystFamiliarHolder` aceita entidade `AmethystGolem` e usa `LibEntityNames.FAMILIAR_AMETHYST_GOLEM` como chave do holder; `FamiliarData.getEntity` cria o familiar e fixa `holderID`. A criação de Script/desbloqueio por Binding é Ars-owned, não feitiço autônomo do Black Arcana. |
| **Divergência de EntityType** | O holder instancia `new FamiliarAmethystGolem(ModEntities.ENTITY_FAMILIAR_BOOKWYRM.get(),world)`, mas `FamiliarAmethystGolem.getType()` retorna `ModEntities.FAMILIAR_AMETHYST_GOLEM.get()`, e `ModEntities` registra tipo próprio com `FamiliarAmethystGolem::new`. **A inconsistência de construtor/tipo é real no source fixado; efeito de serialização, rede, atributos e spawn no JAR instalado NÃO está verificado.** Falhar fechado em adapters que exijam EntityType correto. |
| Knockback do dono | `FamiliarEvents.knockbackEvent(LivingKnockBackEvent)` reduz `event.getStrength()*0.5f` **uma vez** se a lista filtrada de golems do owner não está vazia. A multiplicação não é por número de familiars. `livingHurtEvent(LivingDamageEvent.Post)` rejeita `DamageTypeTags.BYPASSES_ARMOR`, exige owner `Player`, origem `LivingEntity` e `BlockUtil.distanceFrom(...blockPosition())<3`; executa `livingTarget.knockback(0.5f,...)`. Isso não equivale a bloquear o dano. |
| Reagente/interação | `FamiliarAmethystGolem.mobInteract` executa no servidor, apenas mão principal. Se a stack está em `Tags.Items.GEMS_AMETHYST`, concede `ModPotions.DEFENCE_EFFECT` por `20*60*3=3600` ticks ao **player que interagiu**, descontando um gem se `!player.hasInfiniteMaterials()`. **O método não verifica explicitamente `player.equals(getOwner())` antes desse branch**; política multiplayer requer teste in-game. |
| Lifecycle/persistência/authority | `FamiliarEntity` usa `FAMILIAR_SET` (WeakHashMap-backed), `getOwnerID`, `terminatedFamiliar`, `PersistentFamiliarData` (`name/color/cosmetic`), `holderID` e NBT; a cada 20 ticks servidor descarta o familiar quando owner UUID não resolve ou terminated. `FamiliarEvents.maxManaCalc` adiciona `getManaReserveModifier()=0.15` ao primeiro familiar correspondente e retorna; **não somar por instância arbitrariamente**. Ars é autoridade desses handlers, reserva de mana, itens e entidades. RPG Skill Tree concede perks/Mastery só com boundary real; `WorldEffectPolicy` BA não intercepta knockback do Ars. |

**QA/bloqueios:** verificar bytecode da versão física e spawn do holder, owner offline/retorno, tipo real da entidade, interação não-owner, hierarquia de evento, concorrência com Epic Fight e outros knockback modifiers, tooltip de defesa, save/restart e atribuição causal. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Nenhum Stage promovido.
