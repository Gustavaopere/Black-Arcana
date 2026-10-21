# Somake Spells 1.0.9 — Blood Cut: gate de evidência técnica para perks

**Estado:** 🟡 auditoria de método compilado proposta. Nenhuma conclusão binária nova antes de workflow completo e SHA-gate aprovado.

## Identidade corroborada

- Registry de referência: `somakespells:blood_cut`, inventariada entre as 83 identidades do Somake 1.0.9.
- Artifact instalado: `somakespells-1.0.9-1.21.1.jar`, SHA-1 físico/publisher `171841ac9f802be9309ecc166c1d972ac6d404c0`.
- Runtime host: Iron's Spells; progressão/perks: RPG Skill Tree mediante contrato real; Black Arcana: runtime próprio.
- A classe com nome candidato `BloodCutSpell` é **hipótese de localização**, submetida a prova de existência e unicidade no classpath compilado exato; não é uma FQCN ainda certificada.

## Gate executável

O [verificador de método](../../../../docs/qa/somake_109_blood_cut_refs.py) e o [workflow](../../../../.github/workflows/somake-109-blood-cut-refs.yml) testam SHA-1, mod ID, pacote/classe candidata, métodos, descritores JVM e referências simbólicas (invocação/campo); o artefato exportado contém apenas metadados derivativos, sem implementação do provider.

Os testes sintéticos cobrem ausência, ambiguidade, duplicação e tentativa de path traversal na descoberta de classe, além de uma classe Java 21 compilada de exemplo.

## Eixos que a evidência futura deverá preencher

| Dimensão | Resultado neste checkpoint |
|---|---|
| Classe real, métodos, descritores JVM | ⚠️ pendente de execução do gate SHA-exato |
| Cast type, custo, cooldown e nível | ⚠️ não aferidos |
| Self/entidade/bloco/área, raycast/LOS, filtros | ⚠️ não aferidos |
| Alcance, raio, hitbox, tamanho/velocidade do projétil | ⚠️ não aferidos |
| Fórmula e tipo de dano, aplicação de status | ⚠️ não aferidos |
| Duração, recast, quantidade de alvos, caps | ⚠️ não aferidos |
| Causalidade owner/cast/hit/múltiplos procs | ⚠️ não aferidos |
| Hook mutador por jogador para perks RPG | ⛔ FAIL_CLOSED |
| Gameplay no cliente/servidor e Survival | ⚠️ pendente |

**Nota de causalidade:** um `getDamage` ou `onCast` identificado estaticamente não significa que seus retornos sejam diretamente modificáveis. A confirmação de class/method refs é apenas a entrada para outra auditoria de dataflow e das entidades/effects downstream. Não atribuir Mastery a cada hit ou criar segundo settlement de mana/cooldown.

**Fontes:** [registry física](../EXACT-1.0.9-REGISTRY-AUDIT.md), [catálogo 1.0.9](../SPELL-CATALOG-1.0.9.md), [padrão editorial para perks](../../../meta/PERK-READY-TECHNICAL-STANDARD.md).
