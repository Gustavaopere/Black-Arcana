# Somake Spells 1.0.9 — five downstream entities: exact-JAR method audit

**Status: 🟡 PENDING_EXACT_BINARY_RUN.** Este dossiê separa a descoberta de símbolos JVM de evidência causal, fórmulas numéricas e QA real.

## Escopo físico e histórico

- Modlist atual `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`, entrada física #513: Somake 1.0.9, `somakespells-1.0.9-1.21.1.jar`.
- Publisher CurseForge File 8867079; SHA-1 já comprovado em #827/#828: `171841ac9f802be9309ecc166c1d972ac6d404c0`.
- Referência de origem: [sete classes de spell e seus callsites](EXACT-BINARY-CAST-CALLSITES-1.0.9.md), [verificador de entidades](../../../../docs/qa/somake_109_entity_method_probe.py), [testes sintéticos](../../../../docs/qa/somake_109_entity_method_probe_test.py) e [workflow Java 21](../../../../.github/workflows/somake-109-entity-refs.yml).

## Alvos da auditoria

| Registry de origem | Classe downstream encontrada nos callsites do `onCast` do JAR exato |
|---|---|
| `somakespells:fragmented_requiem` | `com.somake.somakespells.entity.FragmentedSwordRainEntity` |
| `somakespells:funeral_bloom` | `com.somake.somakespells.entity.FuneralBloomControllerEntity` |
| `somakespells:withered_rose_vortex` | `com.somake.somakespells.entity.WitheredRoseVortexEntity` |
| `somakespells:custodia_caeli` | `com.somake.somakespells.entity.CustodiaCaeliSigilEntity` |
| `somakespells:jingle_bell` | `com.somake.somakespells.entity.BellEntity` |

## Contrato de evidência

Coletar **somente** descritores/nomes de métodos e referências simbólicas a métodos/campos associados a dano, seleção de alvos, estados, cura, lifecycle, ownership e mundo. O parser exige hash de JAR, mod ID e classes concretas; recusa listas/métodos sem controle de tamanho. Nenhuma extração de corpos Java, bytecode, assets, textos de terceiros ou JAR é publicada.

Um símbolo `DamageSources.applyDamage` não prova dano ocorrido; `tick()` não prova frequência/ticks efetivos nem permanência; `AABB.inflate` não comprova raio; `discard()` não certifica descarte do efeito em todos os caminhos; um `getOwner` nominal não comprova deduplicação de Mastery. **Não preencher cálculos, setters ou caps sem evidência adicional do fluxo executado.**

**Pendente:** execução da versão exata e inspeção dos resultados das cinco classes; só então atualizar esta matriz e as fichas individuais. Hooks mutadores de perks: ⛔ `FAIL_CLOSED` até contrato do provider/host comprovado. Sem mudança de runtime, contagem semântica ou Stage.
