# Magic Wind Charge — entidade

- Registro: `aero_additions:magic_wind_charge`, `EntityType<MagicWindCharge>`, categoria `MISC`; tamanho **0.3125×0.3125**, tracking configurado em **64**.
- Ativação: **REGISTERED**; produtor alcançável: [Wind Charge](../spells/wind-charge.md). [Summoned Breeze](summoned-breeze.md) também a instancia se sua entidade existir, mas a magia de summon está inativa. Contribuição estrita de magias **0**.
- Estado: `documentary=SOURCE_PINNED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; identidade instalada **NOT_VERIFIED**; certificação **0**.

Source `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`, versão `1.2.8`. [Prova comum](../SOURCE-CONTRACTS-1.2.8.md) · [manifesto](../SOURCE-CATALOG-MANIFEST-1.2.8.json) · [limites](../SOURCE-CATALOG-CLOSURE-1.2.8.md). O SHA-1 histórico instalado de 35 caracteres é inválido; publisher e instalação são identidades separadas.

## Movimento, impacto e força

`MagicWindCharge extends WindCharge implements AntiMagicSusceptible`. O construtor usado pelo spell define owner=caster; a magia posiciona na altura ocular menos metade da altura da hitbox e define o campo `damage` como `D=0.2×sqrt(getSpellPower)/0.6324555` (aprox. **0.31623×sqrt(power)**). `shoot(rotation)` substitui velocidade por `rotation×1.5`; não normaliza internamente. O spell passa look unitário; Breeze passa vetor normalizado já escalado em 0.5, produzindo velocidade nominal **0.75**. `isNoGravity()` retorna true. Não há range nem limite de vida próprio definidos no addon; lifecycle herdado de `WindCharge` exige contrato do host. Tracking 64 não é alcance de dano.

No hit de entidade, depois de chamar `super.onHitEntity`, o ramo server resolve owner como `LivingEntity` ou null, registra `setLastHurtMob(target)` quando há owner vivo e, se owner é `Player`, chama `setIgnoreFallDamageFromCurrentImpulse(true)` nesse **owner**. Tenta dano direto fixo **1.0F** por `damageSources().windCharge(this,livingOwner)`; somente quando `hurt` retorna true e alvo é LivingEntity executa efeitos pós-ataque de enchant. Depois chama `explode(position)`; `onHit` descarta no server. O chamado de superclass permanece uma fronteira externa: não deduzir contagem física total de impactos somente deste override.

No hit de bloco, depois do superclass, no server calcula ponto de explosão `hitLocation + faceNormal×0.25`, explode e descarta. A explosão usa raio **1.5**, fire=false, `Level.ExplosionInteraction.TRIGGER`, partículas small/large gust e `WIND_CHARGE_BURST`. O calculator literal é `SimpleExplosionDamageCalculator(true,false,Optional.of(K),blocksWindChargeExplosionsTag)` com **`K=1.22×D`**. No [host Minecraft 1.21.1](../SOURCE-CONTRACTS-1.2.8.md#host-minecraft-1211), o terceiro argumento é **multiplicador de knockback** e o segundo `false` faz `shouldDamageEntity` retornar false: **esta explosão não tenta dano de HP a entidades** no pipeline vanilla examinado. O push usa o multiplicador em caminho separado; flags de interação de blocos e integrações externas continuam fronteiras do engine. O campo chamado `damage` é usado aqui como força e como input visual; não substituir o hit direto de 1.0 por D. `onAntiMagic` explode na posição atual e descarta, sem guard de lado próprio.

## Persistência e visual

Salva `Damage` como Float e `Age` como Int, depois dos dados do superclass; lê os mesmos tipos em `damage` e `tickCount`. Não possui clamp, versão de NBT ou serializer de sincronização para o campo damage no addon. Owner/persistência herdados não foram auditados aqui; reload não prova preservação de atribuição.

`MagicWindChargeRenderer` usa textura/model layer vanilla de wind charge, esconde render nos primeiros dois ticks se a câmera estiver a menos de **3.5** blocos e calcula offset UV `age×0.03×D×1.2`. `MagicWindChargeModel` gira wind/charge em sentidos opostos a **16 graus por tick**. Esses termos são visuais, não hitbox ou velocidade de combate; `trailParticles`/`impactParticles` locais são vazios.

## Matriz para perks

| Eixo | Consumidor real | Fronteira de mutação |
|---|---|---|
| Força | `WindChargeSpell.getDamage` → `setDamage` → calculator `K` | Spell power chega à força; dano direto continua 1.0. Setter existe na entidade mas seam externo por jogador **NOT_VERIFIED**. |
| Movimento/range | `shoot`, `getSpeed`, `isNoGravity`, superclass vanilla | Um vetor pode já estar escalado. Não promover tracking ou raio de explosão a alcance do projétil. |
| Mundo/antimagic | `explode`, bloco/tag/engine e `onAntiMagic` | Antimagic provoca explosão; política de mundo Black Arcana não é aplicada automaticamente ao provider. |
| Crédito | Owner, `windCharge(this,owner)`, retorno de `hurt` | Partículas/spawn/explosão não são prova de hit aceito; persistência e reflexão podem mudar owner. |
| Save/sync | `Damage`, `Age` + superclass; renderer lê D local | Persistência não implica sincronização de D ao cliente; validar visual e reload separadamente. |

QA: superclass de impacto, dano direto e força física, bloco/tag/claims, reflexão/owner, antimagia, queda, NBT e sincronização de D. Nenhum adapter certificado.

## Localizadores fixos

- [AASpells.java — registro L80–88](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L80-L88).
- [WindChargeSpell.java — criação e fórmula L69–84](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_charge/WindChargeSpell.java#L69-L84).
- [MagicWindCharge.java — owner/velocidade L32–69](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_charge/MagicWindCharge.java#L32-L69); [impacto L71–120](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_charge/MagicWindCharge.java#L71-L120); [explosão/antimagia/NBT L122–164](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_charge/MagicWindCharge.java#L122-L164).
- [MagicWindChargeRenderer.java L15–42](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_charge/MagicWindChargeRenderer.java#L15-L42); [MagicWindChargeModel.java L8–23](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_charge/MagicWindChargeModel.java#L8-L23).
