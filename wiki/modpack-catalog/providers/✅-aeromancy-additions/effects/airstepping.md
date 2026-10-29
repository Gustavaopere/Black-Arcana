# Airstepping — marcador de saltos

- Registro: `aero_additions:airstepping`, `MobEffect`, implementação `MagicMobEffect`, categoria `BENEFICIAL`, cor `0xd3ebea`.
- Ativação: **REGISTERED**; produtor ativo: [Airstep](../spells/airstep.md). Contribuição estrita de magias **0**.
- Estado: `documentary=SOURCE_PINNED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; identidade instalada **NOT_VERIFIED**; certificação **0**.

Source `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`, versão `1.2.8`. [Prova comum](../SOURCE-CONTRACTS-1.2.8.md) · [manifesto](../SOURCE-CATALOG-MANIFEST-1.2.8.json) · [limites](../SOURCE-CATALOG-CLOSURE-1.2.8.md). SHA-1 instalado histórico de 35 caracteres não é identidade válida.

## Estado e consumidores

O efeito não possui subclasse local, dano, atributos ou NBT próprios. `AirstepSpell.onCast` aplica amplifier `level−1` e duração `(int)(getSpellPower(level,caster)×30)` ticks, além de inicializar separadamente `AeromancySpellData.airStepHitsRemaining=1+level` (**2–8** nos níveis default). Ter efeito sem saldo não autoriza salto; ter saldo sem efeito também não. O contador e sua persistência/sync pertencem ao contrato de estado/rede, não ao `MobEffectInstance`.

`canJump` exige saldo `>0`, efeito presente e `!onGround`. `airstepJump` usa input X/Z normalizado, rotacionado pelo olhar e escalado em **0.5** no plano horizontal; substitui a velocidade por esse vetor mais Y=`JUMP_STRENGTH+getJumpBoostPower`, zera fall distance, define impulso, emite som/partículas e subtrai um saldo. O método não contém o filtro `isFallFlying`/spectator do consumidor client de tecla; esses gates do cliente não equivalem a validação server-side do payload.

Em todo `LivingFallEvent` com efeito, o handler recupera `spellLevel=1+amplifier` e repõe saldo para `1+spellLevel` (**amplifier+2**). Apenas o subramo distância `>=SAFE_FALL_DISTANCE && saldo>0` zera o multiplicador de dano de queda. Remove e Expired limpam o contador. O marcador também é lido pelo mixin do packet listener para resetar contagem vanilla de flutuação, e pela GUI `AirstepCounterBar`, que desenha o contador sincronizado enquanto há efeito/HUD visível/jogador não spectator. O antigo handler de caminhar na água está comentado.

## Matriz para perks

| Eixo | Consumidor real | Fronteira de mutação por perk |
|---|---|---|
| Tempo/amplifier | `AirstepSpell.onCast`, fall/remove/expired handlers | Amplifier altera saldo reposto; duração depende de spell power. Não duplicar o cast para reabastecer. |
| Movimento | `airstepJump`, caller client e `AirstepPacket` server | Input e saldo são estado provider-owned; limites/replay/latência precisam QA. Hook individual **NOT_VERIFIED**. |
| Queda | `protectFall(LivingFallEvent)` | Dano zerado só no gate; reset de saldo é independente da distância. Sem dano ofensivo. |
| Estado/HUD | `AeromancySpellData`, `AirstepCounterBar`, packet-listener mixin | Efeito é marcador e transporte/HUD não são procs de Mastery. NBT do contador não é NBT deste efeito. |

QA: efeito aplicado externamente sem contador, amplifiers extremos, recarga no fall event, remoção/expiração/reload, input client/server e anticheat. Nenhum adapter certificado.

## Localizadores fixos

- [AASpells.java — marcador L168–172](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L168-L172).
- [AirstepSpell.java — aplicação/queda L77–96](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/airstep/AirstepSpell.java#L77-L96); [salto/limpeza L98–131](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/airstep/AirstepSpell.java#L98-L131); [duração L139–145](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/airstep/AirstepSpell.java#L139-L145).
- [AirstepCounterBar.java L13–26](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/airstep/AirstepCounterBar.java#L13-L26); [AAClientEvents.java — input L87–102](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAClientEvents.java#L87-L102); [ServerPacketListenerMixin.java L13–23](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/mixin/ServerPacketListenerMixin.java#L13-L23).
