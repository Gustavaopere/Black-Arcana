# Ray — engenharia de perks, Not Enough Glyphs 4.6.2

**ID de registro:** `toomanyglyphs:glyph_ray` · **Classe:** `alexthw.not_enough_glyphs.common.glyphs.forms.MethodRay` · **Mana default (fonte):** **15** · **Tier:** não sobrescrito localmente · **Estado:** ✅ fallback porque toomanyglyphs ausente; ⚠️ config.

**Fonte 4.6.2:** [common/glyphs/forms/MethodRay.java](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/forms/MethodRay.java), [registro condicional](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/init/ArsNouveauRegistry.java) e [prefixo de IDs](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/CompatRL.java). Pin `45604dd18d9d2e3e7ca80a2c616b3309f42aca77`. Defaults do source não equivalem ao débito efetivo do servidor.

## Mecanismo causal e números verificáveis

- `fireRay` parte dos olhos do caster. Comprimento `base_range + bonus_range_per_augment*aoeMultiplier` com defaults de configuração **16 + 16×AOE blocos** (valores configuráveis até `Double.MAX_VALUE`, sem budget local de comprimento). Não assumir default de multiplicador de AOE sem host.
- `Sensitive=0`: clip de blocos COLLIDER; `Sensitive>=1`: OUTLINE; `Sensitive>=2`: fluidos ANY, limite Sensitive default **2**. Procura primeiro hit de entidade viva diferente do caster no segmento truncado pelo bloco; senão usa o bloco.
- Em `MISS` com Sensitive>=2, fabrica `BlockHitResult` no fim do raio e chama `resolver.onResolveEffect`. Em MISS normal não chama resolução de efeito; **todos os ramos retornam SUCCESS**, inclusive sem hit.
- `send` cria partículas de intervalo **0.5 ou 0.25 blocos**, sem cap local proporcional à distância. Augments declarados AOE/Sensitive. Range e VFX de uma nova perk requerem caps; `SUCCESS` não é evidência de dano/efeito confirmado para Mastery.

## Interoperabilidade e evidência

- **Authority:** Ars Nouveau/Not Enough Glyphs/Sauce executam a spell, calculam custo e liquidam efeitos. Black Arcana não deve repetir o cast, aplicar o mesmo dano/efeito novamente nem criar outro ledger de mana. RPG Skill Tree só assume progressão, Mastery e perks através de um contrato real.
- **Perks:** parâmetros nativos identificados no código-fonte **não** são hooks comprovados. API/evento de mutação para esta identidade: **NÃO VERIFICADO**; adapter RPG: **⛔ NÃO IMPLEMENTADO (fail-closed)**. Requer caps/budgets, identidade causal e testes antes de alterar alcance, custo, dano ou número de efeitos.
- **Estado:** código-fonte público declarado 4.6.2 localizado, mas corpos compilados no JAR físico, configurações SERVER efetivas, execução dedicada/GameTest, claim/PvP, Save/Restart e Survival **⚠️ NÃO TESTADOS neste lote**. O pacote físico indicado no catálogo é `not_enough_glyphs-1.21.1-4.6.2.jar`, SHA-1 registrado `32eea2c478a346ee7499f6a0db156241116f73e9`. Nenhuma identidade nova.
- **Clean-room:** apenas fatos, parâmetros e localizadores; sem cópia de implementação ou assets.

[Matriz 4.6.2](../../../PERK-ENGINEERING-MATRIX-4.6.2.md) · [Padrão global](../../../../../meta/PERK-READY-TECHNICAL-STANDARD.md).
