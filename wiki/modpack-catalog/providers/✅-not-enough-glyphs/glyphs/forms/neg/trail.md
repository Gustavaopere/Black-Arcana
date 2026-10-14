# Echoing Trail — engenharia de perks, Not Enough Glyphs 4.6.2

**ID de registro:** `not_enough_glyphs:glyph_trail` · **Classe:** `alexthw.not_enough_glyphs.common.glyphs.forms.MethodTrail` · **Mana default (fonte):** **200** (retificação: antes 50) · **Tier:** III (retificação: antes II) · **Estado:** ✅ registrado; ⚠️ config/execução.

**Fonte 4.6.2:** [common/glyphs/forms/MethodTrail.java](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/forms/MethodTrail.java), [registro condicional](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/init/ArsNouveauRegistry.java) e [prefixo de IDs](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/CompatRL.java). Pin `45604dd18d9d2e3e7ca80a2c616b3309f42aca77`. Defaults do source não equivalem ao débito efetivo do servidor.

## Mecanismo causal e números verificáveis

- `summonProjectiles` cria `1 + count(Split)` entidades `TrailingProjectile`, velocidade `max(0.1, 0.75+accMultiplier/2)`, delay `(int)durationMultiplier`. O overload de `onCastOnBlock(BlockHitResult,...)` tem rota alternativa: projéteis lançados verticalmente acima do bloco.
- [`TrailingProjectile.java`](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/spell/TrailingProjectile.java) usa `getExpirationTime = getProjectileLifespan()*20`; default `max_lifespan=60` segundos. A partir de `age>5`, `castSpells` ocorre quando `age % max(2,12-2*getDelay()) == 0`, se `totalProcs<maxProcs=20`.
- Sem Sensitive, a iteração de entidades próximas cessa quando `i>5` (até seis contadas por passagem). Com Sensitive, percorre posições de bloco e pode chamar `resolver.onResolveEffect` muitas vezes por passagem; contador cresce por `max(1,int(counter/(10+aoe)))`, **não** por cada resolução real. Assim, o teto **20 no contador de procs não é teto de 20 efeitos**.
- Augments: Sensitive, Accelerate, Decelerate, AOE, Split, Pierce, Extend Time, Reduce Time. Invalid combos: Linger, Wall, Burst. Não transformar cada tick/child resolve em cast novo ou proc de Mastery.

## Interoperabilidade e evidência

- **Authority:** Ars Nouveau/Not Enough Glyphs/Sauce executam a spell, calculam custo e liquidam efeitos. Black Arcana não deve repetir o cast, aplicar o mesmo dano/efeito novamente nem criar outro ledger de mana. RPG Skill Tree só assume progressão, Mastery e perks através de um contrato real.
- **Perks:** parâmetros nativos identificados no código-fonte **não** são hooks comprovados. API/evento de mutação para esta identidade: **NÃO VERIFICADO**; adapter RPG: **⛔ NÃO IMPLEMENTADO (fail-closed)**. Requer caps/budgets, identidade causal e testes antes de alterar alcance, custo, dano ou número de efeitos.
- **Estado:** código-fonte público declarado 4.6.2 localizado, mas corpos compilados no JAR físico, configurações SERVER efetivas, execução dedicada/GameTest, claim/PvP, Save/Restart e Survival **⚠️ NÃO TESTADOS neste lote**. O pacote físico indicado no catálogo é `not_enough_glyphs-1.21.1-4.6.2.jar`, SHA-1 registrado `32eea2c478a346ee7499f6a0db156241116f73e9`. Nenhuma identidade nova.
- **Clean-room:** apenas fatos, parâmetros e localizadores; sem cópia de implementação ou assets.

[Matriz 4.6.2](../../../PERK-ENGINEERING-MATRIX-4.6.2.md) · [Padrão global](../../../../../meta/PERK-READY-TECHNICAL-STANDARD.md).
