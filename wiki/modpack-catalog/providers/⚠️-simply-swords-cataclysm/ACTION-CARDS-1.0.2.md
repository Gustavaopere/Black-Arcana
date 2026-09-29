# Simply Swords: Cataclysm 1.0.2 — fichas canônicas de habilidades

Este índice materializa em fichas individuais as **4 identidades semânticas** fechadas pelo source pin exato da linha `1.0.2+1.21.1+neoforge`.

O provider permanece **⚠️ parcial/condicionado**. O denominador está fechado em quatro, mas o subconjunto ativo no pack atual depende dos valores efetivos do `ModConfig.Type.STARTUP` em `config/simplycataclysm-startup.toml`. Portanto estas fichas não alteram o strict global.

## Habilidades sobrenaturais — 4

- [Blazing Brand](actions/blazing-brand.md) — owner Ignitium
- [Accursed Rage](actions/accursed-rage.md) — owner Cursium
- [Mecha Pulse](actions/mecha-pulse.md) — owner Witherite
- [Mecha Smite](actions/mecha-smite.md) — owner Witherite

## Contagem e exclusões

- 4/4 fichas correspondem às raízes semânticas completas do source pin `a81158e53b2d215ff534fa59732edd08cfd1d4f4`;
- `Fireproof & Unbreakable` é propriedade de item/material e adiciona +0;
- `accursed_rage`, `blazing_brand`, `pulse_charge` e `pulse_cooldown` são estado/effect machinery e adicionam +0;
- Ancient Metal e Black Steel não expõem uma quinta habilidade equivalente no source tree exato;
- partículas, sons, lifesteal, stun, cooldown e demais consequências downstream não criam identidades adicionais.

## Alcance implantado

O collector read-only já sabe capturar os dez valores STARTUP relevantes, mas nenhum default de source/JAR substitui o arquivo efetivamente implantado.

- Blazing Brand depende de `blazingBrandChance`;
- Accursed Rage depende de `accursedRageChance`;
- Mecha Pulse depende de `mechaPulseChargeChance`;
- Mecha Smite exige classificação conjunta das branches harmful e regenerative através dos sete valores específicos documentados no checklist.

Até o arquivo implantado ser capturado contra o SHA-1 físico esperado, a contribuição deste provider permanece **+0 strict**.

Fontes canônicas: [SOURCE-1.0.2-ABILITY-INVENTORY.md](SOURCE-1.0.2-ABILITY-INVENTORY.md) e [DEPLOYED-CONFIG-CHECKLIST.md](DEPLOYED-CONFIG-CHECKLIST.md).
