# Breathless

- Registro: `aero_additions:breathless`, `MobEffect`, classe `BreathlessEffect extends MagicMobEffect implements ISyncedMobEffect`, categoria `HARMFUL`, cor `0xd3ebea`.
- Ativação: **REGISTERED** em `AASpells.MobEffects`; produtor ativo: [Asphyxiate](../spells/asphyxiate.md). Contribuição estrita de novas magias **0**.
- Estado: `documentary=SOURCE_PINNED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; identidade instalada **NOT_VERIFIED**; certificação **0**.

Source `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`, versão `1.2.8`. [Prova comum](../SOURCE-CONTRACTS-1.2.8.md) · [manifesto](../SOURCE-CATALOG-MANIFEST-1.2.8.json) · [limites](../SOURCE-CATALOG-CLOSURE-1.2.8.md). Identidade do publisher não sana o SHA-1 instalado histórico inválido de 35 caracteres.

## Alvo, pulso e dano

Asphyxiate usa helper de alvo de alcance **15**, tolerância **0.15**, e rejeita alvo nulo ou tipo na tag `asphyxiation_immune` **no precast**. Durante o canal, quando `castDurationRemaining % 10 == 0`, resolve novamente o UUID e, se não nulo, reaplica Breathless por **10 ticks**, amplifier `spellLevel−1` (**0–2** nos níveis default 1–3). O pulso não repete o filtro da tag. O efeito em si não lê a tag: aplicações externas não recebem automaticamente a imunidade de precast.

O predicado de tick é `duration % (6−amplifier) == 0`, baseado na **duração restante** da instância, não em um relógio global de dano. Cada execução tenta `livingEntity.hurt(DamageSources.get(level,ASPHYXIATION), 1+0.2×amplifier)` e retorna true sem examinar o resultado de `hurt`. Para amplifier 0/1/2: divisor **6/5/4**, tentativa **1/1.2/1.4 HP**; reaplicações de 10 ticks e i-frames podem alterar a sequência de dano aceito. O damage source local não recebe caster, owner ou projétil: não inferir crédito de kill/mastery para o canalizador.

Não há clamp de amplifier neste efeito. Valor **6** gera divisor zero; valores externos fora do produtor default não são contrato de perk aprovado. Duração total do canal é `100+100×spellLevel` ticks (**200/300/400**); é distinta da duração de 10 ticks de cada aplicação.

O registro também instala `MOVEMENT_SPEED` **−0.3 ADD_MULTIPLIED_BASE** com ID `aero_additions:breathless_slow` e `ATTACK_DAMAGE` **−0.3 ADD_MULTIPLIED_BASE** com ID `aero_additions:breathless_weak`. São quantidades base de modificador; a escala padrão por amplifier/stacking pertence ao host `MobEffect`. Sem NBT, owner ou sincronizador adicional próprio no efeito. Os callbacks add/remove só chamam superclass; as antigas alterações de flags estão comentadas.

## Consumidores e matriz para perks

| Eixo | Consumidor real | Fronteira de mutação por perk |
|---|---|---|
| Duração/amplifier | `AsphyxiateSpell.onServerCastTick` | Renovação e level−1 são provider-owned. Escala por player ou amplifier arbitrário: hook **NOT_VERIFIED**. |
| Dano/intervalo | `BreathlessEffect.applyEffectTick` e `shouldApplyEffectTickThisTick` | Constantes não usam spell power; aumentar power não implica aumento deste DoT. Contar só dano aceito e com atribuição demonstrada. |
| Debuffs | `AASpells.MobEffects.BREATHLESS` | Velocidade e ataque são modificadores nativos, não dano Wind genérico. Evitar colidir IDs. |
| Visual no mundo | `WindySwirlRenderer.Vanilla` consulta Breathless para renderizar cabeça; camada instalada para skins slim/wide | É leitura direta de `hasEffect`, mesmo com flags antigas comentadas. Nenhuma mutação de combate. |
| Overlay local | `AAOverlay.render` consulta Breathless, oculta em HUD escondido/spectator e desenha textura de swirl | Não é evidência de execução server-side do DoT. |

QA: aplicações de 10 ticks, renovação perto dos divisores, i-frames, amplifier externo, alvo que ganha imunidade após precast, morte/unload, atribuição sem caster, debuffs e visuals dedicados. Nenhum adapter certificado.

## Localizadores fixos

- [AASpells.java — modificadores L154–162](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L154-L162).
- [BreathlessEffect.java — contrato completo L13–39](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/asphyxiate/BreathlessEffect.java#L13-L39).
- [AsphyxiateSpell.java — aplicação L40–48](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/asphyxiate/AsphyxiateSpell.java#L40-L48); [precast L60–72](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/asphyxiate/AsphyxiateSpell.java#L60-L72); [canal L93–96](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/asphyxiate/AsphyxiateSpell.java#L93-L96).
- [WindySwirlRenderer.java — cabeça L63–70 e leitura L139–144](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_shield/WindySwirlRenderer.java#L63-L70); [AAOverlay.java L23–39](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAOverlay.java#L23-L39); [camada slim/wide L57–75](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAClientEvents.java#L57-L75).

- [WindySwirlRenderer.java — leitura do efeito L142–144](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_shield/WindySwirlRenderer.java#L142-L144).
