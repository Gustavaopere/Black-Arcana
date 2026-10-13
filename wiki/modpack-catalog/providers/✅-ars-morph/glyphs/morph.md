# Ars Morph 2.0.0 — Morph (dossiê individual)

Estado: ✅ registry único registrado na fonte alinhada à release; ⚠️ JAR-runtime/Identity2 atual/config física não reproduzidos; ⛔ adapter RPG sem hook/QA.

## Identidade

- **ID:** `ars_morph:glyph_morph`, único `EffectMorph.INSTANCE` adicionado por `ArsNouveauRegistry.registerGlyphs()`.
- **JAR atual:** `ars_morph-1.21.1-2.0.0.jar`, SHA-1 físico `68ff47cc58c0ffe9570bb907f65c2910311ed45f`; Identity2 no pack 2.2.4, host Ars Nouveau 5.13.1.
- **Source pin:** [`EffectMorph.java`](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/java/com/alexthw/ars_morph/glyphs/EffectMorph.java); [`ArsNouveauRegistry.java`](https://github.com/Alexthw/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/java/com/alexthw/ars_morph/ArsNouveauRegistry.java). Release-aligned 2.0.0, **não** prova corpo binário byte-idêntico.
- **Tier:** II; **mana Ars default:** 200; **escola:** Conjuration; **augments compatíveis:** nenhum; config `max_hp_morph` default 100, admissível 20..Integer.MAX_VALUE.

## Engenharia de perks — cadeia de execução

- **Servidor e ator:** `onResolveEntity` só atua se `level instanceof ServerLevel`, shooter é `ServerPlayer` e `isRealPlayer(shooter)` passa, e o hit é `LivingEntity`. `FamiliarEntity` é rejeitado. Turret, FakePlayer ou client não obtêm morph nesse caminho.
- **Seleção da forma:** prioridade de tipo `MobJarItem` da offhand com `MobJarItem.fromItem(...) instanceof LivingEntity`; senão tipo do alvo; se tipo ainda for o do alvo e houver `SpawnEggItem` na offhand, substitui por `egg.getType(...)`. A prioridade real torna o item portado parte do targeting, mas não uma permissão externa.
- **Recipient:** se o alvo atingido é `ServerPlayer`, esse target é recipient; caso contrário o próprio caster. Se o hit é Player e tipo escolhido é `EntityType.PLAYER`, chama `IdentityProgression.clearMorph(targetPlayer)` e envia smoke **sem consultar retorno**; as partículas dessa branch não comprovam resultado de clear.
- **Morph novo:** chama `type.create(world)`; retorna em null; exige `morph.getMaxHealth() < GENERIC_INT.get()` **estrito** (igualdade falha). Quando alvo e candidato implementam `IDecoratable`, copia item cosmético. Em seguida solicita `IdentityProgression.morph(recipient,BuiltInRegistries.ENTITY_TYPE.getKey(type),morph.serializeNBT(...))`, soltando partículas apenas quando essa função devolve true.
- **Sem timer neste método:** código de `limitedMorphTime`/status de duração está comentado. Não criar duração finita, cooldown extra ou lógica de revert automática com base nesta classe. O state de identidade e suas condições de aquisição são authority Identity2.
- **Perks e segurança:** uma alteração RPG em maxHP/UUID/origem de morph não é provada por hook. Validar PvP/friendly targeting, consentimento, política de identidade Identity2, limite de health, restore/logout/restart e idempotência antes de conceder perks. Não duplicar `IdentityProgression.morph` nem premiar pelas partículas.

## Critérios pendentes

⚠️ Confrontar bytecode instalado com o source release-aligned, execução Identity2 2.2.4, limites de player, serializer de variantes e multiplayer. ⛔ Sem bridge real Black Arcana/RPG para substituir/observar transação com atribuição exactly-once. Catálogo **+0** identidades (1/1 já documentada).

[Inventário legado](../GLYPH-MORPH.md) · [README](../README.md) · [padrão técnico](../../../meta/PERK-READY-TECHNICAL-STANDARD.md).
