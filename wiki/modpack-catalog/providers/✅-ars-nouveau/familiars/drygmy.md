# Drygmy Familiar

State: `SOURCE-PINNED 5.13.1 / SOURCE-DESCRIPTION DIVERGENCE / RUNTIME QA PENDING`

Registry id: `ars_nouveau:familiar_drygmy`
Conversion entity: Ars Nouveau `EntityDrygmy`
Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Aquisição

O holder reconhece `EntityDrygmy`. Binding produz o Bound Script correspondente; o script desbloqueia o familiar no capability Ars.

## Behavior confirmado

### Earth spell modifier

`FamiliarDrygmy` implementa `ISpellCastListener`. Em `SpellModifierEvent`, quando o familiar está vivo, pertence ao caster e a spell part pertence à escola `ELEMENTAL_EARTH`, chama `event.builder.addDamageModifier(2.0f)`.

Há, porém, uma divergência importante no dispatcher comum: `FamiliarEvents` possui dois subscribers para `SpellModifierEvent` (`spellResolveEvent` e `modifierEvent`) e ambos encaminham o mesmo evento para todos os `ISpellCastListener`. O catálogo **não** conclui que o bônus runtime efetivo seja +4 sem QA; registra apenas que o source possui dois paths de dispatch aparentemente duplicados.

### Drygmy's Blessing / Looting

- A cada 60 ticks, o familiar aplica ao owner `ModPotions.LOOTING_EFFECT` por 600 ticks, amplifier 0.
- Esse efeito adiciona `+1.0` ao atributo Ars `PerkAttributes.DRYGMY`.
- O antigo path direto de `LootingLevelEvent` está comentado tanto no familiar quanto em `FamiliarEvents` com TODO para restaurá-lo.

Portanto, a descrição do livro — “chance to increase the amount of looting” — não é tratada como prova de um roll aleatório ativo no 5.13.1; o comportamento confirmado é o efeito/atributo acima.

## Authority e deduplicação

- Modificadores de Earth spell, `LOOTING_EFFECT` e `PerkAttributes.DRYGMY` pertencem ao Ars.
- Black Arcana/RPG Skill Tree não devem conceder um segundo +Earth damage ou Looting apenas porque um Drygmy familiar está ativo.
- Qualquer bridge futura precisa observar o `SpellModifierEvent`/atributo real e deduplicar o root cast.

## QA pendente

1. Medir o damage modifier efetivo em runtime devido aos dois subscribers de `SpellModifierEvent`.
2. Confirmar a semântica efetiva de `PerkAttributes.DRYGMY` no loot pipeline 5.13.1.
3. Confirmar que o antigo roll de Looting não está ativo por outro path não auditado.

## Certificação técnica estática — Familiar Drygmy (2026-10-26)

**✅ somente `STATIC_TECHNICAL_CATALOG_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Ars Nouveau JAR 5.13.1 SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; upstream fixo `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. **109 IDs compilados auditados apenas para glyphs/rituais, não para familiars.** [FamiliarDrygmy.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/familiar/FamiliarDrygmy.java) · [DrygmyFamiliarHolder.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/familiars/DrygmyFamiliarHolder.java) · [FamiliarEvents.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/FamiliarEvents.java) · [FamiliarEntity.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/familiar/FamiliarEntity.java) · [FamiliarEvents.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/FamiliarEvents.java) · [FamiliarData.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/capability/FamiliarData.java) · [PacketSummonFamiliar.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/network/PacketSummonFamiliar.java).

| Eixo | Fluxo fonte-pinned |
|---|---|
| Holder e validação de owner | `DrygmyFamiliarHolder` associa `EntityDrygmy` → `FamiliarDrygmy` por `ModEntities.ENTITY_FAMILIAR_DRYGMY`. `FamiliarEntity.onFamiliarSpawned` encerra outros familiars do mesmo owner após `FamiliarSummonEvent`; owner, holderID e dados persistentes são Ars-owned. |
| Earth spell modifier | `FamiliarDrygmy.onModifier(SpellModifierEvent)` exige `isAlive()`, `getOwner().equals(event.caster)` e `SpellSchools.ELEMENTAL_EARTH.isPartOfSchool(event.spellPart)`; executa `event.builder.addDamageModifier(2.0f)`. **Dois métodos distintos, `FamiliarEvents.spellResolveEvent` e `FamiliarEvents.modifierEvent`, são ambos `@SubscribeEvent` para a MESMA classe SpellModifierEvent e encaminham para `onModifier`**. Isso sugere duas oportunidades por evento no source; **não certificar +4 efetivos nem equivalência de bytecode/assinaturas sem QA do binário e da ordem de dispatch**. |
| Looting com refresh | `FamiliarDrygmy.tick` a cada `level.getGameTime()%60==0` no servidor, com owner presente, aplica `ModPotions.LOOTING_EFFECT` por `600` ticks, amplifier `0`, flags `false,false,true`. Outros consumers Ars mapeiam para `PerkAttributes.DRYGMY`; não declarar chance RNG de looting a partir do livro. |
| Evento antigo inativo | O antigo `onLootingEvent(LootingLevelEvent)` está **comentado** no familiar e o subscriber `FamiliarEvents.fortuneEvent` também está **comentado**, ambos com TODO. Não registrar roll antigo como funcional. Atributos e loot pipeline reais de outros mods precisam QA. |
| Custo, skin e dedup | Dye tag `Tags.Items.DYES` altera `COLOR` se constar em `EntityDrygmy.COLORS`; método mostra nenhuma redução de stack nesse caminho de dye. `getManaReserveModifier()=0.15` é um default compartilhado da base familiar, adicionado uma vez pelo primeiro correspondente em `FamiliarEvents.maxManaCalc`. Não aplicar uma segunda reserva de mana, Earth +2 ou status Looting por Mastery. |
| Boundary | `WorldEffectPolicy` do Black Arcana cobre apenas effects próprios; Ars controla custo, SpellModifierEvent, skills e loot. RPG Skill Tree integra pelo contrato de progressão, sem duplicar eventos de cast. |

**QA/bloqueios:** verificar dois listeners no classfile compilado, contagem real de alterações por root cast, impacto de addon Earth, sobreposição com loot perks, benefício de atributos e ordem de eventos, interação de dye e vida/owner. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`.

## Geometria e atributos de entidade no source

O `EntityType.Builder` do familiar declara `.sized(0.5f,0.5f)` (largura × altura) e `.setTrackingRange(10)`. O tracking declarado não é alcance de habilidade. [Registros e dimensões](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/ModEntities.java#L197-L210).

`FamiliarEntity.attributes()` fornece defaults `MAX_HEALTH=100`, `MOVEMENT_SPEED=0.2` e `FOLLOW_RANGE=16`; a criação dos atributos registra essa base para os seis tipos. Velocidade efetiva e distância de ação dependem dos consumidores/IA. [Base](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/familiar/FamiliarEntity.java#L206-L209) · [registro de atributos](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/ModEntities.java#L369-L375). O [contrato compartilhado](../FAMILIAR-STATIC-SIX-5.13.1.md) distingue esses parâmetros de raios de efeito, reserva de mana e evidência binária.
