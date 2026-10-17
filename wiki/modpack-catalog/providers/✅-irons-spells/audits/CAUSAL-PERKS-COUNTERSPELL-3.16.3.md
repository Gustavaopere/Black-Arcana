# Iron's 3.16.3 — Counterspell: boundary para perks de contramágica

**Estado:** ✅ caminho de fonte pinada, targeting e evento de veto identificados; ⚠️ compatibilidade com outros providers, tempo real e adapters não testados. Nenhum novo feitiço contado.

- ID `irons_spellbooks:counterspell`. Fonte [`CounterspellSpell`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/CounterspellSpell.java); [`CounterSpellEvent`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/CounterSpellEvent.java), código `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252` para MC 1.21.1 e versão-alvo 3.16.3.

## Execução comprovada

1. **Config:** escola Ender, rare, máximo 1, mana base 50, 10 s default, cast instantâneo e tempo base 0. [`CounterspellSpell`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/CounterspellSpell.java#L33-L64). Multiplicadores de config da classe-base podem modificar mana e cooldown; configuração implantada pendente.
2. **Target:** `onCast` cria raycast a partir do olho do caster, com direção para frente e **até 80 blocos**, checagem de blocos, inflação da bounding-box **0,35** e filtro `Utils.validAntiMagicTarget`. O filtro aceita `AntiMagicSusceptible`, `Player` ou `IMagicEntity` que não seja spectator. Isto **não** é AOE e não representa seleção arbitrária de alvos. [spell](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/CounterspellSpell.java#L67-L78), [filtro](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L618-L620).
3. **Ponto de veto:** havendo `EntityHitResult`, posta `new CounterSpellEvent(caster,target)` no `NeoForge.EVENT_BUS`. [Evento](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/CounterSpellEvent.java#L1-L15) implementa `ICancellableEvent` e expõe caster/target como campos públicos finais. **Há veto**, mas não setter oficial de target ou range neste evento.
4. **Efeito:** se o evento não for cancelado, `AntiMagicSusceptible.onAntiMagic` pode afetar entidades; summon próprio tem exceção condicionada a alvo de IA; jogadores em `ServerPlayer` recebem `Utils.serverSideCancelCast(...,true)` e limpeza dos recasts `COUNTERSPELL`; `IMagicEntity` pode ter cast cancelado; `LivingEntity` pode perder efeitos do tipo `MagicMobEffect`. [`CounterspellSpell`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/CounterspellSpell.java#L78-L107). O que ocorre em providers **não** implementadores destas interfaces é desconhecido.
5. **Visual:** partículas percorrem o vetor até o hit. Esse loop de apresentação não cria efeito em área nem uma segunda ação mágica. [`CounterspellSpell`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/CounterspellSpell.java#L109-L114).

## Matriz de perks

| Eixo | Prova | Estado |
|---|---|---|
| Cancelar/vetar dispel | `CounterSpellEvent` cancelável antes dos efeitos | ✅ `HOOK_VERIFICADO` para veto; ⚠️ adapter e runtime ainda sem teste |
| Alterar range | 80 é hardcode no raycast desta classe | ⛔ nenhum setter de alcance/target comprovado |
| Multi-target/AOE | um `EntityHitResult` é processado | ⛔ requer novo contrato seguro; não invocar `onAntiMagic` em outras entidades por conta própria |
| Compatibilidade entre mods | interfaces `AntiMagicSusceptible` / `IMagicEntity` | ⚠️ condicionado à participação real do provider alvo |
| Tempo/cooldown/custo | instant / 10s / 50 mana base | ⚠️ config e ordem de admissão do Iron's; sem segunda cobrança |
| Tipo/dano | counterspell não aplica damage por seu `onCast` | N/A para `SpellDamageEvent` desta ação |

## Política de integração

Uma perk de **resistência à contramágica** pode, em tese, vetar o `CounterSpellEvent` com condição validada do servidor, mas isso ainda precisa de contrato de autoridade entre RPG/perks e Iron's, além de teste de coexistência. A existência do evento **não autoriza** converter Counterspell em AOE, alterar range ou cancelar recursos de outros mods por reflexo. Não forçar execução quando o evento foi vetado.

### Pendências

- [ ] Validar JAR físico, order/listeners do evento e comportamento em dedicated-server/multiplayer.
- [ ] Confirmar compatibilidade alvo para efeitos Ars/Malum/Goety/Black Arcana sem atravessar as boundaries dos providers.
- [ ] Auditar caps, PvP/team claims e efeitos mágicos que não estendem `MagicMobEffect`.
- [ ] Testar `COUNTERSPELL` versus recasts/slots já ativos.
- [ ] Confirmar se algum contrato público adicional da versão exata permite alterar a geometria (até lá, fail-closed).

Complementa a [ficha individual](../ender/counterspell.md) e a documentação da PR #795 sem sobrescrevê-la.
