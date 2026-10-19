# Somake 1.0.9 — Funeral Bloom: CFG do raio e contrato binário do Iron's

**Estado inicial:** 🟡 aguardando auditoria física no JAR exato do Somake e no artefato de API do Iron's 3.16.3. Nenhuma fórmula nova de raio ou hook de perk homologado.

## Origem física

- Modlist sibling `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`: `somakespells-1.0.9-1.21.1.jar` e `irons_spellbooks-1.21.1-3.16.3.jar`, Minecraft 1.21.1/NeoForge/Java21.
- Somake: CurseForge File 8867079, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`.
- Iron's: API oficial `io.redspace:irons_spellbooks:1.21.1-3.16.3:api`, repositório de dependência `https://code.redspace.io/releases` declarado no `Black-Arcana/build.gradle`. Este artefato de compilação **não** substitui a validação física do JAR completo em jogo.
- [Scanner CFG/API](../../../../docs/qa/somake_109_radius_irons_contract.py), [testes](../../../../docs/qa/somake_109_radius_irons_contract_test.py), [workflow](../../../../.github/workflows/somake-109-radius-irons-contract.yml).

## Restrições de prova

O parser verifica o grafo de saltos do bytecode compilado de `FuneralBloomSpell.getRadius`, recusa destino inválido, opcode de controle não suportado, offsets duplicados e instruções inalcançáveis. Publica apenas contagens e tipos de branch, invocações simbólicas e referências a clamp. Não publica o corpo do método, offsets, bytecode, código fonte do provider, assets ou JARs.

A ligação com Iron's exige verificar a assinatura binária `(ILnet/minecraft/world/entity/LivingEntity;)F` no callsite do Somake e no `AbstractSpell` do JAR da API da versão exata. Correspondência binária de método não comprova seu algoritmo, os atributos ativos do jogador, configuração do datapack nem interceptação por perks.

| Critério | Resultado antes do gate |
|---|---|
| Somake: dois desvios em `getRadius` | ✅ Evidência da PR #833 |
| Somake: operandos 10.0f/15.0f de `Mth.clamp(FFF)F` | ✅ Evidência da PR #832 |
| CFG estrutural e condições concretas dos desvios | 🟡 Verificação deste lote |
| Iron's `AbstractSpell.getSpellPower` na API oficial 3.16.3 | 🟡 Inspeção de classe e signature, sem afirmar o resultado previamente |
| Origem dos atributos e fórmula completa de raio | ⚠️ Exige auditoria causal adicional |
| Perks de alcance/dano por jogador | ⛔ `FAIL_CLOSED` sem adapter público e QA real |

**Autoridades:** Somake executa sua magia; Iron's conserva casting/recursos/contratos host; RPG Skill Tree fornece progressão por contratos reais; Black Arcana controla seu próprio runtime. Stage 06.05 continua 🟡 e Stage 09 guarda validações físicas sob D035.
