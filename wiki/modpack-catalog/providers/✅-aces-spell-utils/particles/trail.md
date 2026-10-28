# trail — ParticleType de Ace's Spell Utils 1.2.7.2

**ID:** `aces_spell_utils:trail` · **Registry:** `minecraft:particle_type` · **Estado:** ⚠️ source-pinned; apresentação cliente não é evidência de cast.

[`ASParticleRegistry.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ASParticleRegistry.java) registra um `ParticleType<TrailParticleOptions>(false)` via `DeferredRegister<ParticleType<?>>`. O `codec()` retorna `TrailParticleOptions.CODEC` e `streamCodec()` retorna `TrailParticleOptions.STREAM_CODEC`.

[`TrailParticleOptions.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/particles/TrailParticleOptions.java) define dois parâmetros serializados: `color` (`Vector3f`, `ExtraCodecs.VECTOR3F`) e `scale` (`SCALE`; serialização rede `ByteBufCodecs.FLOAT`). O helper `of(int rgb,float scale)` converte cor RGB em vetor. O [client setup](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/AcesSpellUtils.java) vincula `TrailParticle.Provider` pelo `RegisterParticleProvidersEvent`.

**Targeting/range/shape/tempo:** partículas vêm de produtores/consumidores; essa declaração não determina trail width, spawn rate, lifetime ou dano. `trail` não registra spell. Não usar evento de render para confirmar dano/cast no servidor, nem criar canal de Mastery para VFX.

**QA:** validação dos codecs e registro com pack 1.21.1/NeoForge, client render, shader e sincronização de visual, com JAR exato ainda não inspecionado. Fonte `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, SHA-1 instalado anotado `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`; `physical_qa=NOT_TESTED`; `mutating_hook=NOT_VERIFIED`; `COMPLETE_PERK_READY=false`.
