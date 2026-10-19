# Somake Spells 1.0.9 — auditoria de métodos de aquisição (em verificação)

**Status:** 🟡 PROBE_PENDING_CI; ainda não é evidência de runtime ou hook mutador.

## Insumo físico fixado

- Mod: somakespells / somakespells-1.0.9-1.21.1.jar.
- JAR oficial CurseForge File 8867079; SHA-1 171841ac9f802be9309ecc166c1d972ac6d404c0 de acordo com o dossiê físico vigente.
- Registro exato anterior de 83 magias, com sete overrides de allowCrafting(): três com false constante, quatro de fluxo não constante.
- Auditoria nova: [script](../../../docs/qa/somake_109_perk_method_probe.py), [testes sintéticos](../../../docs/qa/somake_109_perk_method_probe_test.py) e [workflow](../../../.github/workflows/somake-109-perk-methods.yml).

## Novo gate, estritamente delimitado

O verificador exige identidade física por SHA-1, metadata do mod ID, classe concreta por nome único, método público allowCrafting():boolean, instruções terminadas em retorno e classificação estrutural compatível com auditoria anterior. Retém somente FQCN, descritor, cardinalidade de instruções e branches, e membros simbólicos chamados/lidos. Não exporta corpo do método, classes compiladas, recursos ou JAR.

A conclusão migrará de PROBE_PENDING_CI somente após inspecionar o run do HEAD final, as sete correspondências e qualquer desvio. Nenhuma afirmação sobre valores de dano, geometria, cooldown, aquisição real, disponibilidade em Survival ou hook por jogador decorre apenas desses símbolos.

| Eixo | Estado |
|---|---|
| IDs e registro do provider | ✅ inventário exato anterior |
| allowCrafting: forma do retorno | ✅ prova anterior 3/4 |
| allowCrafting: classes compiladas e referências por método no novo gate | 🟡 aguardando QA |
| Predicados com semântica completa e superfície pública de mutação | ⛔ não comprovado |
| Config efetiva, loot/crafting, castability, Survival | ⚠️ não testado |
| Targeting, AoE, hitbox, velocidade, dano, duração e recursos | ⚠️ não aferidos neste escopo |
| Perk de aquisição/efeito | ⛔ FAIL_CLOSED, sem adapter |

**Autoridades:** Somake mantém lógica própria, Iron's hospeda casting/custos/cooldowns, RPG Skill Tree fornece progressão somente por boundary comprovado; Black Arcana é autoridade exclusiva sobre seu runtime mágico. A existência de allowCrafting não torna disponível uma API para mudar alcance, dano ou custo.

**Referências:** [registro exato](EXACT-1.0.9-REGISTRY-AUDIT.md), [mapa de gates](EXACT-1.0.9-REGISTRATION-GATE-MAP.md), [matriz das sete fichas](PERK-REACHABILITY-GATES-1.0.9.md).
