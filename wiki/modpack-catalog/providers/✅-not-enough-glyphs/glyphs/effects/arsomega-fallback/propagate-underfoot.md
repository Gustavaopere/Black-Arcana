# Propagate Underfoot — engenharia de perks, Not Enough Glyphs 4.6.2

**ID de registro:** `arsomega:glyph_propagate_underfoot` · **Classe:** `alexthw.not_enough_glyphs.common.glyphs.propagators.PropagateUnderfoot` · **Mana default (fonte):** **100** · **Tier:** II · **Estado:** ✅ fallback porque arsomega ausente; ⚠️ config/host.

**Fonte 4.6.2:** [common/glyphs/propagators/PropagateUnderfoot.java](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/propagators/PropagateUnderfoot.java), [registro condicional](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/init/ArsNouveauRegistry.java) e [prefixo de IDs](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/CompatRL.java). Pin `45604dd18d9d2e3e7ca80a2c616b3309f42aca77`. Defaults do source não equivalem ao débito efetivo do servidor.

## Mecanismo causal e números verificáveis

- `onResolve` chama `copyResolver` (cadeia Sauce `IPropagator`, `getTypeIndex()=8`). `propagate` encaminha o **restante** da sequência para uma nova resolução; não representa nova iniciativa do jogador.
- No hit de bloco, muda `blockPos` para `below()`. No hit de entidade, quando o alvo é `LivingEntity` com `getVehicle()!=null`, a nova resolução atinge o **veículo**; sem veículo, um hit de bloco abaixo da posição da entidade. Outros resultados não produzem `onResolveEffect`.
- O método delega seus augments compatíveis a `MethodUnderfoot.INSTANCE.getCompatibleAugments()` do Ars host; não há lista independente no código NEG. Escola `MANIPULATION`.
- A seleção de veículo é visível na fonte 4.6.2, sem teste físico. Não atribuir a transação derivada a um segundo caster, nem cobrar/conceder Mastery uma segunda vez sem evento idempotente.

## Interoperabilidade e evidência

- **Authority:** Ars Nouveau/Not Enough Glyphs/Sauce executam a spell, calculam custo e liquidam efeitos. Black Arcana não deve repetir o cast, aplicar o mesmo dano/efeito novamente nem criar outro ledger de mana. RPG Skill Tree só assume progressão, Mastery e perks através de um contrato real.
- **Perks:** parâmetros nativos identificados no código-fonte **não** são hooks comprovados. API/evento de mutação para esta identidade: **NÃO VERIFICADO**; adapter RPG: **⛔ NÃO IMPLEMENTADO (fail-closed)**. Requer caps/budgets, identidade causal e testes antes de alterar alcance, custo, dano ou número de efeitos.
- **Estado:** código-fonte público declarado 4.6.2 localizado, mas corpos compilados no JAR físico, configurações SERVER efetivas, execução dedicada/GameTest, claim/PvP, Save/Restart e Survival **⚠️ NÃO TESTADOS neste lote**. O pacote físico indicado no catálogo é `not_enough_glyphs-1.21.1-4.6.2.jar`, SHA-1 registrado `32eea2c478a346ee7499f6a0db156241116f73e9`. Nenhuma identidade nova.
- **Clean-room:** apenas fatos, parâmetros e localizadores; sem cópia de implementação ou assets.

[Matriz 4.6.2](../../../PERK-ENGINEERING-MATRIX-4.6.2.md) · [Padrão global](../../../../../meta/PERK-READY-TECHNICAL-STANDARD.md).
