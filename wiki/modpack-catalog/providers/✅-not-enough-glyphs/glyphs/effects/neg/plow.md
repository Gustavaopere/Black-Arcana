# Plow — engenharia de perks, Not Enough Glyphs 4.6.2

**ID de registro:** `not_enough_glyphs:glyph_plow` · **Classe:** `alexthw.not_enough_glyphs.common.glyphs.effects.EffectPlow` · **Mana default (fonte):** **0** (retificação: a ficha anterior dizia 5) · **Tier:** não sobrescrito localmente · **Estado:** ✅ registrado; ⚠️ config/execução.

**Fonte 4.6.2:** [common/glyphs/effects/EffectPlow.java](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/effects/EffectPlow.java), [registro condicional](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/init/ArsNouveauRegistry.java) e [prefixo de IDs](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/CompatRL.java). Pin `45604dd18d9d2e3e7ca80a2c616b3309f42aca77`. Defaults do source não equivalem ao débito efetivo do servidor.

## Mecanismo causal e números verificáveis

- `onResolveBlock` percorre `SpellUtil.calcAOEBlocks(shooter, hitPos, hit, aoeMultiplier, count(Pierce))` e chama `doTill` para cada bloco. O único augment explicitamente compatível é **AOE**; Pierce constar do cálculo não comprova que possa ser aplicado ao glyph.
- `doTill` instancia uma **Diamond Hoe** temporária, aplica encantamentos e obtém `ANFakePlayer` com UUID do caster. `dupeCheck` rejeita block entities com item handler ou `Container`. Exige `BlockUtil.destroyRespectsClaim(fakePlayer, level, pos)`.
- Após admissões, chama `BlockState.useItemOn`; somente quando o resultado não é `FAIL` chama também `hoe.useOn`. Um cast pode efetuar várias ações de bloco: não contar cada uso de ferramenta como cast novo para Mastery.
- `doTill` converte `Level` para `ServerLevel` sem guard próprio; percurso server-side depende de chamadas do host. Escola `ELEMENTAL_EARTH`. A área precisa de limite de trabalho e cada posição precisa manter a verificação de claim.

## Interoperabilidade e evidência

- **Authority:** Ars Nouveau/Not Enough Glyphs/Sauce executam a spell, calculam custo e liquidam efeitos. Black Arcana não deve repetir o cast, aplicar o mesmo dano/efeito novamente nem criar outro ledger de mana. RPG Skill Tree só assume progressão, Mastery e perks através de um contrato real.
- **Perks:** parâmetros nativos identificados no código-fonte **não** são hooks comprovados. API/evento de mutação para esta identidade: **NÃO VERIFICADO**; adapter RPG: **⛔ NÃO IMPLEMENTADO (fail-closed)**. Requer caps/budgets, identidade causal e testes antes de alterar alcance, custo, dano ou número de efeitos.
- **Estado:** código-fonte público declarado 4.6.2 localizado, mas corpos compilados no JAR físico, configurações SERVER efetivas, execução dedicada/GameTest, claim/PvP, Save/Restart e Survival **⚠️ NÃO TESTADOS neste lote**. O pacote físico indicado no catálogo é `not_enough_glyphs-1.21.1-4.6.2.jar`, SHA-1 registrado `32eea2c478a346ee7499f6a0db156241116f73e9`. Nenhuma identidade nova.
- **Clean-room:** apenas fatos, parâmetros e localizadores; sem cópia de implementação ou assets.

[Matriz 4.6.2](../../../PERK-ENGINEERING-MATRIX-4.6.2.md) · [Padrão global](../../../../../meta/PERK-READY-TECHNICAL-STANDARD.md).
