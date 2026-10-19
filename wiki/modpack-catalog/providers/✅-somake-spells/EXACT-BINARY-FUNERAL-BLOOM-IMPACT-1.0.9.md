# Somake Spells 1.0.9 — FuneralBloomImpactEntity: auditoria do último efeito identificado

**Estado:** 🟡 `PENDING_EXACT_SHA1_IMPACT_PROBE`. Sem prova de execução em jogo, fórmula ou hook per-player.

## Escopo pinado

- Release exato: `somakespells-1.0.9-1.21.1.jar`; CurseForge File `8867079`; SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`, conforme modlist de `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`.
- A classe `com.somake.somakespells.entity.FuneralBloomImpactEntity` apareceu no callsite de `FuneralBloomBudEntity.impact(ServerLevel)` da auditoria [do bud](EXACT-BINARY-FUNERAL-BLOOM-BUD-1.0.9.md).
- A nova auditoria de símbolos é executada com [probe](../../../../docs/qa/somake_109_funeral_impact_probe.py), [testes](../../../../docs/qa/somake_109_funeral_impact_probe_test.py) e [workflow](../../../../.github/workflows/somake-109-funeral-impact.yml).

## Matriz de verificação

| Dimensão | Investigação necessária | Resultado atual |
|---|---|---|
| Construção/identidade | Classe exata encontrada em arquivo do publisher | 🟡 Aguardar CI |
| Métodos/tick | Métodos e chamadas compiladas no classfile | 🟡 Aguardar CI |
| Dano/cura | Chamada direta a dano, cura, evento ou somente apresentação | ⚠️ Não comprovado |
| Geometria | AABB, tamanho, velocidade, raio, colisões | ⚠️ Não comprovado |
| Persistência/lifecycle | `tick`, descarte, NBT, spawn e remoção | ⚠️ Não comprovado |
| Hook por jogador | Parâmetros ou eventos de mutação seguros via contrato provider-host | ⛔ FAIL_CLOSED |

**Critério clean-room:** registrar só FQCN, descritores JVM, referências simbólicas e quantidades de branches. Não exportar implementação Java, bytecode, classes, JAR, recursos ou assets. Um método com nome `tick` não comprova dano/efeito efetivo. Ausência de callsites no classfile não exclui execução delegada ou herdada.

**Cadeia de investigação:** `FuneralBloomSpell.onCast` → `FuneralBloomControllerEntity.launchWave` → `FuneralBloomBudEntity.tick/impact` → `FuneralBloomImpactEntity`. Setas significam dependências observadas, não prova causal de todos os casts. Evitar dupla contagem de Mastery, aplicação de dano ou segunda mana. Black Arcana rege seu runtime próprio; Somake rege o efeito provider-native; Iron's o host; RPG Skill Tree fornece atributos/perks só por boundary verificado.

Nenhuma nova magia nem Stage promovida nesta etapa.