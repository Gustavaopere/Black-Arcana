# Somake Spells 1.0.9 — Funeral Bloom Bud: auditoria binária do efeito secundário

**Estado deste checkpoint:** 🟡 `PENDING_EXACT_SHA1_BUD_PROBE`, sem execução de jogo, fórmula ou hook homologado.

## Origem e autoridade física

- Mod ID `somakespells`, modlist do RPG Skill Tree `main@ed5b65b890767b406ce41127bcb793775263c7bd`, entrada #513, JAR `somakespells-1.0.9-1.21.1.jar`, Minecraft 1.21.1/NeoForge.
- CurseForge File `8867079`, SHA-1 físico/publisher `171841ac9f802be9309ecc166c1d972ac6d404c0`.
- O dossiê anterior [das cinco entidades](EXACT-BINARY-ENTITY-CALLSITES-1.0.9.md) provou a referência de `FuneralBloomControllerEntity` a `FuneralBloomBudEntity` em métodos de cancelamento/pruning, mas não inspecionou o classfile da bud.
- A nova auditoria [scanner](../../../../docs/qa/somake_109_funeral_bud_probe.py), [testes](../../../../docs/qa/somake_109_funeral_bud_probe_test.py) e [workflow](../../../../.github/workflows/somake-109-funeral-bud.yml) verifica somente `com.somake.somakespells.entity.FuneralBloomBudEntity` do artefato exato.

## Perguntas para a engenharia de perks

| Dimensão | Precisa ser distinguido antes de autorizar perk | Estado |
|---|---|---|
| Origem de dano | `LivingEntity.hurt` direto, helper `DamageSources.applyDamage`, outra entidade ou efeito delegado | 🟡 Sob inspeção; nenhum evento assumido |
| Alvo/LOS | AABB, raycast, distância, aliados, espectador e regras de PvP | ⚠️ Limites, condições e caps não verificados |
| Cura/Wither | Entidade pode produzir efeitos indiretos após hit | ⚠️ Código causal downstream pendente |
| Ciclo de vida | tick, arming, impacto, expiração, anti-magic, cancelamento e remoção | ⚠️ Não inferir descarte em todas as branches |
| Proprietário | Caster/UUID/owner, bud/controller, correlação de impacto com cast | ⛔ Sem deduplicação de Mastery comprovada |
| Parâmetros para perks | raio, dano, duração, quantidades, velocidade, hitbox e alvo | ⛔ Sem setter seguro por personagem homologado |

**Clean-room:** serão preservados apenas os nomes/descritores de métodos, símbolos de chamadas, contagens de branches e campos. Sem decompilação exportada, método Java/bytecode ou assets do provider. As referências JVM não demonstram execução, fórmula, valores ou permissões da API. Não introduzir pipeline alternativo de dano, custos ou cooldown.

**Critério de conclusão deste recorte:** verificar a classe física, documentar resultados concretos a partir do job Java 21 no HEAD atual, integrar nas fichas afetadas e só então avaliar merge com todos os testes. A totalização de magias continua 83 identidades; nenhuma ação nova será presumida a partir de um bud.
