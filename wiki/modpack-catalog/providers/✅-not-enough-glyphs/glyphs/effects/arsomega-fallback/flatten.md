# Flatten — engenharia de perks, Not Enough Glyphs 4.6.2

**ID de registro:** `arsomega:glyph_flatten` · **Classe:** `alexthw.not_enough_glyphs.common.glyphs.effects.EffectFlatten` · **Mana default (fonte):** **30** (retificação: a ficha anterior dizia 100) · **Tier:** II · **Estado:** ✅ fallback porque arsomega ausente; ⚠️ execução.

**Fonte 4.6.2:** [common/glyphs/effects/EffectFlatten.java](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/effects/EffectFlatten.java), [registro condicional](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/init/ArsNouveauRegistry.java) e [prefixo de IDs](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/CompatRL.java). Pin `45604dd18d9d2e3e7ca80a2c616b3309f42aca77`. Defaults do source não equivalem ao débito efetivo do servidor.

## Mecanismo causal e números verificáveis

- Blocos: `onResolveBlock` usa `SpellUtil.calcAOEBlocks`; `doFlat` usa `ANFakePlayer` com uma **Diamond Shovel**, recusa block entities com capacidade/inventário e chama `BlockState.useItemOn` **e** `shovel.useOn`. Não há chamada **local** a `BlockUtil.destroyRespectsClaim`, diferentemente de Plow. Isso é uma **lacuna de prova de proteção**, não prova de bypass em runtime.
- Entidades: lê a dureza `h` do bloco sob o alvo; para `h<0`, substitui por 50. Define `t=4sqrt(h)`; se `t>10`, `t=10+(t-10)/4`. Valor solicitado a `attemptDamage`: `clamp(0.165*t*(ampMultiplier+1)*3.5, 0.5, 500)`, antes do resultado real de dano/mitigação. Não existe uma segunda fórmula de dano confirmada.
- `buildConfig` declara também `addDamageConfig(3.0)` e `addAmpConfig(1.0)`, mas essa conta direta não lê tais campos. Augments explicitamente compatíveis: Amplify, Dampen, Fortune; limite default Amplify **2**. Escola `ELEMENTAL_EARTH`.
- Alterar raio, dano ou ferramenta exige QA de claims, proteção, versões do host e conciliação com os callbacks vanilla.

## Interoperabilidade e evidência

- **Authority:** Ars Nouveau/Not Enough Glyphs/Sauce executam a spell, calculam custo e liquidam efeitos. Black Arcana não deve repetir o cast, aplicar o mesmo dano/efeito novamente nem criar outro ledger de mana. RPG Skill Tree só assume progressão, Mastery e perks através de um contrato real.
- **Perks:** parâmetros nativos identificados no código-fonte **não** são hooks comprovados. API/evento de mutação para esta identidade: **NÃO VERIFICADO**; adapter RPG: **⛔ NÃO IMPLEMENTADO (fail-closed)**. Requer caps/budgets, identidade causal e testes antes de alterar alcance, custo, dano ou número de efeitos.
- **Estado:** código-fonte público declarado 4.6.2 localizado, mas corpos compilados no JAR físico, configurações SERVER efetivas, execução dedicada/GameTest, claim/PvP, Save/Restart e Survival **⚠️ NÃO TESTADOS neste lote**. O pacote físico indicado no catálogo é `not_enough_glyphs-1.21.1-4.6.2.jar`, SHA-1 registrado `32eea2c478a346ee7499f6a0db156241116f73e9`. Nenhuma identidade nova.
- **Clean-room:** apenas fatos, parâmetros e localizadores; sem cópia de implementação ou assets.

[Matriz 4.6.2](../../../PERK-ENGINEERING-MATRIX-4.6.2.md) · [Padrão global](../../../../../meta/PERK-READY-TECHNICAL-STANDARD.md).
