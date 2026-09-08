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
