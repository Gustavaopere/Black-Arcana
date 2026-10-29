# Wind Blade — projétil

- Registro: `aero_additions:wind_blade`, `EntityType<WindBladeProjectile>`, categoria `MISC`, tamanho **0.5×0.5**, tracking **64**.
- Ativação: **REGISTERED**; produtor ativo: [Wind Blade](../spells/wind-blade.md). Compartilha path com a magia em registry diferente; contribuição estrita de magias **0**.
- Estado: `documentary=SOURCE_PINNED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; identidade instalada **NOT_VERIFIED**; certificação **0**.

Source `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`, versão `1.2.8`. [Prova comum](../SOURCE-CONTRACTS-1.2.8.md) · [manifesto](../SOURCE-CATALOG-MANIFEST-1.2.8.json) · [limites](../SOURCE-CATALOG-CLOSURE-1.2.8.md). O SHA-1 instalado histórico com 35 caracteres permanece inválido/desconhecido.

## Física, dano e lifecycle

`WindBladeProjectile extends AbstractMagicProjectile implements IEntityWithComplexSpawn`. Construtor do produtor define owner=caster; no cast cria **um** projétil na altura ocular menos metade da hitbox, `shoot(lookAngle)`, `setDamage(0.5×getSpellPower(level,caster))` e `setNoGravity(true)`. O override de velocidade retorna **1.75**. Algoritmo de `shoot`, colisão, antimagia, range, tempo máximo e filtros de owner pertencem ao superclass Iron's; não há override local que feche esses contratos.

Em `onHitEntity`, primeiro chama superclass; então, para qualquer `LivingEntity` atingida, chama `knockback(D, projectile.x−target.x, projectile.z−target.z)`, onde D=`getDamage`. Depois tenta `DamageSources.applyDamage(target,D,AASpells.WIND_BLADE.get().getDamageSource(projectile,owner))` e descarta. O knockback precede a chamada local de dano, não checa seu resultado e não possui gate local de friendly fire. Não prometer que cancelamento de dano evita movimento. No hit de bloco chama superclass e descarta. Há som de impacto `WIND_CHARGE_BURST`, partículas SPIT no impacto e trilha aleatória SPIT/POOF.

Não há campos locais de NBT nem override de save/read; damage, owner, dados de spawn/sync e lifecycle são herdados. `defineSynchedData` apenas chama superclass, sem campo novo no addon. O renderer usa um `ItemStack` de `AAItems.WIND_SWORD`, orientado pela velocidade, e oculta os primeiros dois ticks perto da câmera (`distance²<12.25`). A espada é representação visual: não é item dropado, ataque melee nem identidade de magia adicional. Renderer retorna textura null porque usa o modelo de item.

## Matriz para perks

| Eixo | Consumidor real | Fronteira de mutação |
|---|---|---|
| Dano/knockback | `WindBladeSpell.getDamage` → campo herdado → `onHitEntity` | Spell power alimenta **ambos** os eixos; intensidade D não é dano final aceito. Hook individual adicional **NOT_VERIFIED**. |
| Física/hitbox | `AASpells.Entities`, `getSpeed`, spell `setNoGravity` | Tamanho/velocidade constantes e host de colisão não expõem contrato certificado de perk por caster. |
| Atribuição | DamageSource da magia Wind Blade com projétil/owner | Validar retorno/evento de dano e refletidos; não somar spawn, trail ou knockback como acerto. |
| Persistência | `AbstractMagicProjectile`, `IEntityWithComplexSpawn` | Sem schema próprio local; reload/sync herdados exigem QA. |
| Apresentação | `WindBladeRenderer`, partículas e som | Alterar item renderizado não altera dano/alcance nem concede equipamento ao jogador. |

QA: superclass de hit, i-frames/cancelamento, knockback em aliado, reflexão e owner, antimagia, range/lifetime/sync herdados. Nenhum adapter certificado.

## Localizadores fixos

- [AASpells.java — registro L102–106](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L102-L106).
- [WindBladeSpell.java — spawn L49–58](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_blade/WindBladeSpell.java#L49-L58); [fórmula L69–71](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_blade/WindBladeSpell.java#L69-L71).
- [WindBladeProjectile.java — partículas L27–44](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_blade/WindBladeProjectile.java#L27-L44); [velocidade/owner/sync/hit L46–85](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_blade/WindBladeProjectile.java#L46-L85).
- [WindBladeRenderer.java L18–47](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_blade/WindBladeRenderer.java#L18-L47).
