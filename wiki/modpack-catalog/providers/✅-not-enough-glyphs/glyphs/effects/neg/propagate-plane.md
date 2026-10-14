# Propagate Plane — engenharia de perks, Not Enough Glyphs 4.6.2

**ID de registro:** `not_enough_glyphs:glyph_propagate_plane` · **Classe:** `alexthw.not_enough_glyphs.common.glyphs.propagators.PropagatePlane` · **Mana default (fonte):** **200** · **Tier:** II · **Estado:** ✅ registrado; ⚠️ config/execução.

**Fonte 4.6.2:** [common/glyphs/propagators/PropagatePlane.java](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/propagators/PropagatePlane.java), [registro condicional](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/init/ArsNouveauRegistry.java) e [prefixo de IDs](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/CompatRL.java). Pin `45604dd18d9d2e3e7ca80a2c616b3309f42aca77`. Defaults do source não equivalem ao débito efetivo do servidor.

## Mecanismo causal e números verificáveis

- `onResolveBlock/onResolveEntity` fazem `copyResolver`; hit de entidade é traduzido ao bloco sob o alvo. `IPropagator.getTypeIndex()=8`. Sem prova do corpo Sauce, o acerto contábil de custos do filho permanece host-owned.
- Geometria: `width = 1 + aoeMultiplier`, `height = count(Pierce)`. `Sensitive` escolhe `circle` e, na ausência, `cube`; `Dampen` torna o desenho oco. `circle` converte `width` para raio inteiro e varre `SpellUtil.calcAOEBlocks(..., width*2, height)`. `cube` varre a bounding box host com `width,height`. Há `resolver.onResolveEffect` por posição aceita.
- `Randomize` descarta a posição se `nextFloat() <= count(Randomize)/4f`; **não há clamp local** da probabilidade. `isRealPlayer(shooter)` inverte direção do hit em `propagate`.
- Default `per_spell_limit=1`; augment Sensitive custa adicional **100** por override. Compatíveis: Randomize, AOE, Pierce, Dampen, Sensitive. Incompatibilidades explícitas com Wall, Linger, Burst e Chaining.
- Escola `MANIPULATION`. Expansão de AOE/profundidade é trabalho multiplicativo; o source da classe não demonstra teto local para resolver filhos, por isso qualquer perk geométrica exige budget e testes.

## Interoperabilidade e evidência

- **Authority:** Ars Nouveau/Not Enough Glyphs/Sauce executam a spell, calculam custo e liquidam efeitos. Black Arcana não deve repetir o cast, aplicar o mesmo dano/efeito novamente nem criar outro ledger de mana. RPG Skill Tree só assume progressão, Mastery e perks através de um contrato real.
- **Perks:** parâmetros nativos identificados no código-fonte **não** são hooks comprovados. API/evento de mutação para esta identidade: **NÃO VERIFICADO**; adapter RPG: **⛔ NÃO IMPLEMENTADO (fail-closed)**. Requer caps/budgets, identidade causal e testes antes de alterar alcance, custo, dano ou número de efeitos.
- **Estado:** código-fonte público declarado 4.6.2 localizado, mas corpos compilados no JAR físico, configurações SERVER efetivas, execução dedicada/GameTest, claim/PvP, Save/Restart e Survival **⚠️ NÃO TESTADOS neste lote**. O pacote físico indicado no catálogo é `not_enough_glyphs-1.21.1-4.6.2.jar`, SHA-1 registrado `32eea2c478a346ee7499f6a0db156241116f73e9`. Nenhuma identidade nova.
- **Clean-room:** apenas fatos, parâmetros e localizadores; sem cópia de implementação ou assets.

[Matriz 4.6.2](../../../PERK-ENGINEERING-MATRIX-4.6.2.md) · [Padrão global](../../../../../meta/PERK-READY-TECHNICAL-STANDARD.md).
