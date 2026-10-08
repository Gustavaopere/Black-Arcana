# ShadowsZ 1.1.9 — fichas canônicas de ações

Este índice materializa em fichas individuais as **10 identidades semânticas** fechadas pela auditoria clean-room do artefato exato `shadowsz-1.1.9.jar`.

O provider permanece **⚠️ parcial/condicionado**. A auditoria fecha o denominador, mas o estado implantado ainda precisa provar o valor efetivo de `shadowszRestrictPowers` e `fusionEnabled`. Portanto estas fichas não alteram o strict global.

## Umbral spells — 3

- [`shadowsz:miasma`](spells/miasma.md)
- [`shadowsz:umbral_bond`](spells/umbral-bond.md)
- [`shadowsz:aura_of_the_monarch`](spells/aura-of-the-monarch.md)

## Ações sobrenaturais — 7

- [Shadow Eyes](actions/shadow-eyes.md)
- [Shadow Arising](actions/shadow-arising.md)
- [Summon Shadow](actions/summon-shadow.md)
- [Dismiss Shadow](actions/dismiss-shadow.md)
- [Position Swap](actions/position-swap.md)
- [Despawn Wild Shadows](actions/despawn-wild-shadows.md)
- [Shadow Fusion](actions/shadow-fusion.md)

Individual-card checkpoint: [`INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md`](INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md).

## Contagem e exclusões

- 10/10 fichas correspondem a raízes semânticas exatas do artefato físico/publisher hash-matched;
- Summon All, Dismiss All e ações equivalentes de grupo são aliases/batch das raízes Summon/Dismiss;
- attack order, roster, storage, equipment, progression, release e admin controls são gestão/lifecycle e adicionam +0;
- efeitos, entidades, partículas, buffs e helpers downstream não criam segunda identidade.

## Alcance implantado

Todas as superfícies de poder do jogador dependem de attunement. O valor default do artefato não substitui o gamerule efetivo do mundo.

- `shadowszRestrictPowers=false` permite a rota natural de attunement do provider;
- `shadowszRestrictPowers=true` restringe essa aquisição natural a operadores;
- Shadow Fusion também depende de `fusionEnabled`.

Até esses valores serem capturados no pack/mundo atual, a contribuição ShadowsZ permanece **+0 strict**.

Fontes canônicas: [EXACT-1.1.9-ARTIFACT-AUDIT.md](EXACT-1.1.9-ARTIFACT-AUDIT.md) e [DEPLOYED-STATE-CHECKLIST.md](DEPLOYED-STATE-CHECKLIST.md).
