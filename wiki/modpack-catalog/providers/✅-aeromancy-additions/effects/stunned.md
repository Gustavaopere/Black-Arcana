# Stunned

- Registro: `aero_additions:stunned`, `MobEffect`, classe `StunEffect extends MobEffect implements ISyncedMobEffect`, categoria `HARMFUL`, cor `0xffff00`, partículas `ANGRY_VILLAGER`.
- Ativação: **REGISTERED** em `AASpells.MobEffects`, mas **sem produtor provider-side localizado** em qualquer uma das dez magias ativas. [Updraft](../spells/updraft.md) aplica `MOVEMENT_SLOWDOWN`, não este efeito; Thunderclap está [NOT_REGISTERED](../systems/unregistered-spell-code.md). Contribuição estrita de magias **0**.
- Estado: `documentary=SOURCE_PINNED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; identidade instalada **NOT_VERIFIED**; certificação **0**.

Source `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`, versão `1.2.8`. [Prova comum](../SOURCE-CONTRACTS-1.2.8.md) · [manifesto](../SOURCE-CATALOG-MANIFEST-1.2.8.json) · [limites](../SOURCE-CATALOG-CLOSURE-1.2.8.md). SHA-1 instalado histórico de 35 caracteres permanece inválido/desconhecido.

## Eventos e efeito real

A classe é `@EventBusSubscriber(modid=aero_additions)`. Seu handler de `MobEffectEvent.Applicable` consulta apenas `entity.hasEffect(STUNNED)` e então define `DO_NOT_APPLY`. **Não verifica qual efeito está sendo proposto**: enquanto a entidade já tem Stunned, o bloqueio atinge também outros efeitos candidatos, não apenas reaplicação de stun. O comentário “prevent stunlocking” é mais estreito que o predicado executável. Nenhum guard de lado ou filtro de caster aparece nesse handler.

Em `MobEffectEvent.Added`, apenas para entidade `Player` e instância adicionada de `STUNNED`, resolve `MagicData`, cria `SpellSelectionManager` e percorre **todas as opções de magia selecionáveis**. Para cada magia que ainda não está em cooldown, chama `cooldowns.addCooldown(spell, spell.getSpellCooldown()/2)`. Não substitui cooldown já ativo; usa divisão inteira do cooldown exposto pelo host e não chama cálculo explícito de cooldown reduction. Depois sincroniza ao próprio jogador se `ServerPlayer`. Repetições de uma magia na seleção dependem da verificação `isOnCooldown` após a primeira inclusão.

Não há duração/amplifier produzidos pelo addon, atributo de velocidade, impulso, dano, `hurt`, cancelamento local de canal, AI freeze ou tick de stun implementado nesta classe. Duração e amplifier dependem de aplicação externa/host; o código de cooldown não usa amplifier nem duração. Não há NBT ou serializer próprio: persistência da instância é do host.

## Matriz para perks

| Eixo | Consumidor real | Fronteira de mutação por perk |
|---|---|---|
| Entrada de efeitos | `tryApply(MobEffectEvent.Applicable)` | Gate nativo global enquanto já Stunned; aumentar duração pode prolongar bloqueio de buffs/debuffs externos. Hook individual **NOT_VERIFIED**. |
| Cooldowns | `onApply(MobEffectEvent.Added)`, `SpellSelectionManager`, `PlayerCooldowns` | Metade de `getSpellCooldown()` para magias fora de cooldown. Não é debuff de “todos os spells registrados” nem seam público para CDR de progressão. |
| Sync | `PlayerCooldowns.syncToPlayer(ServerPlayer)` e `ISyncedMobEffect` | Contrato de transporte/host não equivale a execução física certificada. |
| Dano/movimento | Nenhum consumidor local nesses eixos | Não conceder Mastery de dano ou prometer imobilização apenas pelo nome. |

QA: aplicação externa, outros efeitos durante Stunned, reaplicação antes/depois da expiração, magias duplicadas na seleção, cooldown existente, client/server e duração zero/externa. Nenhum adapter certificado.

## Localizadores fixos

- [AASpells.java — registro L168–173](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L168-L173).
- [StunEffect.java — eventos L18–47](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/StunEffect.java#L18-L47).
- [UpdraftSpell.java — status realmente aplicado L117–127](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/updraft/UpdraftSpell.java#L117-L127); [registros ativos/inativos L64–78](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L64-L78).
