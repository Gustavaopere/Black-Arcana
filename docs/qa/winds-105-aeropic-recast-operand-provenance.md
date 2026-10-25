# Aeropic 1.0.5 — contexto dos operandos do recast (clean-room)

**Estado:** 🟡 auditoria em andamento, sem prova de receiver/fluxo de valores; 24/10/2026.

## Autoridade física

- Modlist atual do `neoforge-rpg-skilltree`: Wind's Spellbooks `wind_spellbooks-1.0.5.jar` (posição 571); Iron's Spellbooks `irons_spellbooks-1.21.1-3.16.3.jar` (posição 342); IronSable X Wind's `ironsable-wind-1.0.0.jar` (345).
- Wind's publisher JAR SHA-1 congelado `8744886899bc245ae147a44baa2b183689cec7da`; Iron's 3.16.3 publicou ABI de recast compatível no PR #891, porém não se comprovou igualdade bit a bit entre a distribuição de Iron's e o JAR local do modpack.
- PR #890 provou duas instruções `invokevirtual AbstractSpell.getRecastCount(int, LivingEntity)`, em `AeropicEffect.applyEffectTick` e `onEffectAdded`.

## Lacuna técnica

Para que uma perk altere recasts sem duplicar `PlayerRecasts`, precisamos distinguir o **owner na constant pool** do objeto efetivo do receptor. `invokevirtual` não fornece isoladamente o tipo concreto do objeto, e um método que também referencia `PlayerRecasts.addRecast` não estabelece que o valor retornado pela chamada seja seu argumento.

## Inspeção atual

`docs/qa/winds_105_aeropic_recast_operand_sites.py` inspeciona somente a classe `AeropicEffect` do JAR Wind's SHA-exato. Para cada um dos **dois métodos** obrigatórios, indexa uma janela conservadora de até 24 opcodes anteriores e 12 posteriores ao `invokevirtual`, com listas de nomes simbólicos de métodos, fields e classes, contagem de branches e os opcodes imediatamente adjacentes.

**Este inventário NÃO é simulação do operand stack:** símbolos co-presentes podem vir de caminhos distintos, um getter pode retornar tipo abstrato ou ser executado sob guarda, e os próximos opcodes não são necessariamente consumidores do resultado. Por isso o schema exige `receiver_object: NOT_TRACED`, `return_value_dataflow: NOT_TRACED`, `runtime_override_dispatch: NOT_PROVEN` e `safe_mutating_hook: NOT_PROVEN`. Não reproduzir código, bytecode completo, offsets, implementação ou recursos do provider no artefato.

## Critérios de aceite

- **10 testes sintéticos**: classificação das duas chamadas, opcode/owner/descriptor exato, sobrecargas, hashes, branches, offset drift e ausência de bytecode publicado.
- Workflow independente baixa o JAR oficial com SHA-1 fixado, confere os sete spells de acordo com o scanner canônico e publica apenas JSON de símbolos em torno das chamadas.
- Somente após revisão do JSON resultante registrar conclusões **simbólicas**, não dinamicamente causais, nas fichas. Exigir CI especializado e CI geral Black Arcana (`verify`, companion QA) no HEAD final, sincronização com a main, sem conflito com outros PRs.
- Sem alterações Java, listener, caster, cooldowns, registries, persistência, perks ou Stage. Black Arcana permanece autoridade do próprio runtime; o recast do Iron's/Wind's é provider-native; RPG Skill Tree é provider de progressão. **⛔ SEM_HOOK_SEGURO**.

**Painel de referência preservado:** Wind's ✅ 7/7 feitiços documentados; 9/9 getters selecionados; campanha binária ⚠️ 38/39; global ≥1.856 objetos (percentual —%); 06.05 🟡 e 09 físico pendente.
