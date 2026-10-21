# Momentum — engenharia de perks, Not Enough Glyphs 4.6.2

**ID de registro:** `not_enough_glyphs:glyph_momentum` · **Classe:** `alexthw.not_enough_glyphs.common.glyphs.effects.EffectMomentum` · **Mana default (fonte):** **100**, valor inativo · **Tier:** III · **Estado:** ⚠️ REGISTRADO, PORÉM `isEnabled() == false`.

**Fonte 4.6.2:** [common/glyphs/effects/EffectMomentum.java](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/effects/EffectMomentum.java), [registro condicional](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/init/ArsNouveauRegistry.java) e [prefixo de IDs](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/CompatRL.java). Pin `45604dd18d9d2e3e7ca80a2c616b3309f42aca77`. Defaults do source não equivalem ao débito efetivo do servidor.

## Mecanismo causal e números verificáveis

- **Não é conteúdo ativo por padrão:** `ArsNouveauRegistry` registra `EffectMomentum.INSTANCE`, mas `EffectMomentum.isEnabled()` retorna explicitamente `false` no source 4.6.2. Não conceder perks/Mastery neste glyph por mera presença no registro.
- `onResolveEntity` troca o alvo pelo veículo-raiz caso seja passageiro. Normaliza movimento horizontal X/Z, evitando divisão por zero. Impulso horizontal `1.5 + AMP_VALUE*ampMultiplier`, com default `AMP_VALUE=1.5`.
- Projéteis ou entidades sem gravidade recebem **zero** impulso vertical; nos demais casos há ramificação conforme movimento Y e gravidade, com `verticalAmp = 1 + AMP_VALUE*ampMultiplier`. Soma o vetor ao movimento atual e marca `hurtMarked=true`.
- Limites do source: Amplify **3**, custo incremental Amplify **50**, `per_spell_limit=1`; único augment compatível Amplify. Tudo é **somente análise de classe desabilitada**, não teste de física nem recurso liberado ao jogador.

## Interoperabilidade e evidência

- **Authority:** Ars Nouveau/Not Enough Glyphs/Sauce executam a spell, calculam custo e liquidam efeitos. Black Arcana não deve repetir o cast, aplicar o mesmo dano/efeito novamente nem criar outro ledger de mana. RPG Skill Tree só assume progressão, Mastery e perks através de um contrato real.
- **Perks:** parâmetros nativos identificados no código-fonte **não** são hooks comprovados. API/evento de mutação para esta identidade: **NÃO VERIFICADO**; adapter RPG: **⛔ NÃO IMPLEMENTADO (fail-closed)**. Requer caps/budgets, identidade causal e testes antes de alterar alcance, custo, dano ou número de efeitos.
- **Estado:** código-fonte público declarado 4.6.2 localizado, mas corpos compilados no JAR físico, configurações SERVER efetivas, execução dedicada/GameTest, claim/PvP, Save/Restart e Survival **⚠️ NÃO TESTADOS neste lote**. O pacote físico indicado no catálogo é `not_enough_glyphs-1.21.1-4.6.2.jar`, SHA-1 registrado `32eea2c478a346ee7499f6a0db156241116f73e9`. Nenhuma identidade nova.
- **Clean-room:** apenas fatos, parâmetros e localizadores; sem cópia de implementação ou assets.

[Matriz 4.6.2](../../../PERK-ENGINEERING-MATRIX-4.6.2.md) · [Padrão global](../../../../../meta/PERK-READY-TECHNICAL-STANDARD.md).
