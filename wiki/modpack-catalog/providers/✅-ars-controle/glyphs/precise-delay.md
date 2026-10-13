# Precise Delay

State: `SOURCE-PINNED 1.6.15 / RUNTIME QA PENDING`

- Registry id: `ars_controle:glyph_precise_delay`
- Kind: Effect
- Tier: II
- School: Manipulation
- Base mana: 0
- Scribe XP: 55

## Acquisition

Ars glyph recipe inputs:

- `ars_nouveau:manipulation_essence`
- `minecraft:clock`
- `minecraft:comparator`

## Executable behavior

If there is still spell content after this part, it schedules the remainder through Ars Nouveau's `DelayedSpellEvent` / server `EventQueue`.

Delay duration is:

`1 << ExtendTimeCount`

That is `2^n` ticks for `n` Extend Time augments. The addon allows Extend Time up to 20 on this glyph and overrides its augment mana contribution to 0. A provider client packet presents the delay effect nearby; that packet is presentation, not authority.

If the spell is already at its end, the glyph returns without scheduling additional work.

## Boundary

The delayed continuation remains the same Ars spell causal chain. Black Arcana must not charge a second resource/cooldown/Mastery/Arcane Danger settlement when the delayed event resumes.

## Engenharia para perks — execução pinada à release 1.6.16

- **Source exato 1.6.16:** [EffectPreciseDelay.java](https://github.com/Vonr/Ars-Controle/blob/14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0/src/main/java/dev/qther/ars_controle/spell/effect/EffectPreciseDelay.java), `Vonr/Ars-Controle@14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0`. Registrado no JAR físico 1.6.16; *identidade binária* comprovada separadamente, execução ainda sem teste de equivalência de método a bytecode.
- **Agendamento real:** `sendPacket` sai sem agendar se `currentIndex>=spell.size()`; senão calcula `duration=1 << getBuffCount(AugmentExtendTime.INSTANCE)` e cria `DelayedSpellEvent` com duração efetiva `duration` quando não há evento retrasado anterior, ou **`duration+1`** quando `spellContext.getDelayedSpellEvent()!=null`. Registra o evento em `EventQueue.getServerInstance().addEvent`, e `spellContext.delay(delayEvent)`; pacote `PacketClientDelayEffect(duration,...)` é apenas visualização.
- **Limites/defaults:** custo base mana=0 e override de mana de ExtendTime=0; limite padrão do augment 20, portanto deslocamento máximo nominal `1<<20=1,048,576` ticks, sujeito à gramática/caps host. Valor longo exige performance e lifecycle de fila/servidor; não autoriza retenção de chunks ou tentativa de cast extra.
- **Perks:** uma execução agendada e sua retomada pertencem à mesma raiz Ars. Mastery/custo/cooldown não podem ser pagos duas vezes no retorno de evento; sem observador de `DelayedSpellEvent` seguro para o RPG, somente classificação/documentação.
- **Estado:** ✅ localização do source e IDs físicos; ⚠️ interleaving de contextos, config instalada, erros de validação e Survival/host QA em aberto; ⛔ hooks/adapters RPG não implementados ou testados. O Ars controla gramática, mana e retomadas.
