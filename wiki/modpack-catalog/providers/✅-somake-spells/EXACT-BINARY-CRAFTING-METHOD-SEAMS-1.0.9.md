# Somake Spells 1.0.9 — 7/7 métodos exatos de aquisição

**Status:** ✅ `EXACT_SHA1_ALLOW_CRAFTING_SYMBOLIC_CALLSITE_ONLY` / ⚠️ predicados efetivos e hooks por jogador não validados.

## Prova física reproduzível

- JAR: `somakespells-1.0.9-1.21.1.jar`, CurseForge File `8867079`, SHA-1 físico/publisher `171841ac9f802be9309ecc166c1d972ac6d404c0`.
- [Workflow Java 21 #39186593493](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39186593493) — `SUCCESS`; job `117850201891`; **7/7 testes sintéticos**, parser com casos negativos, correspondência de 7/7 métodos `public boolean allowCrafting()` e ausência de discrepâncias entre as classificações da auditoria anterior e as classes exatas.
- [Verificador limitado](../../../../docs/qa/somake_109_perk_method_probe.py), [testes sintéticos](../../../../docs/qa/somake_109_perk_method_probe_test.py) e [workflow](../../../../.github/workflows/somake-109-perk-methods.yml). Os logs mostram FQCN e símbolos de campos/métodos; o artefato de evidência JSON contém somente esses fatos, sem implementação ou JAR.
- Este gate **não** executou Minecraft, Iron's, Somake carregado, loot/crafting real, servidor modpack, player, perk ou adapter. É inspeção estática de `javap` sob SHA exata.

## Matriz exata por identidade

| ID do feitiço | Classe compilada | Método `()Z` | Referência de campo observada |
|---|---|---|---|
| `somakespells:fragmented_requiem` | `com.somake.somakespells.spells.blood.FragmentedRequiemSpell` | retorno `false` constante | nenhuma referência lida pelo método |
| `somakespells:rose_secret` | `com.somake.somakespells.spells.blood.RoseSecretSpell` | retorno `false` constante | nenhuma referência lida pelo método |
| `somakespells:comforting_lullaby` | `com.somake.somakespells.spells.sound.ComfortingLullabySpell` | retorno `false` constante | nenhuma referência lida pelo método |
| `somakespells:funeral_bloom` | `com.somake.somakespells.spells.blood.FuneralBloomSpell` | fluxo não constante, 2 branches | `Config.DISABLE_WITHERED_ROSE_SPELLS_CRAFTING_AND_LOOTING` |
| `somakespells:withered_rose_vortex` | `com.somake.somakespells.spells.blood.WitheredRoseVortexSpell` | fluxo não constante, 2 branches | `Config.DISABLE_WITHERED_ROSE_SPELLS_CRAFTING_AND_LOOTING` |
| `somakespells:custodia_caeli` | `com.somake.somakespells.spells.holy.CustodiaCaeliSpell` | fluxo não constante, 2 branches | `Config.DISABLE_CUSTODIA_CAELI_CRAFTING_AND_LOOTING` |
| `somakespells:jingle_bell` | `com.somake.somakespells.spells.sound.JingleBellSpell` | fluxo não constante, 2 branches | `Config.DISABLE_JINGLE_BELL_CRAFTING_AND_LOOTING` |

Os quatro métodos não constantes também apresentam invocações exatas de `net.neoforged.neoforge.common.ModConfigSpec$BooleanValue.get():java.lang.Object` e `java.lang.Boolean.booleanValue():boolean`. O verificador coleta as **referências simbólicas e a contagem de branches**, não recompõe o grafo de fluxo nem prova o mapa verdadeiro/falso do campo, seu default ou o valor de COMMON config na instância real.

**Relevância para perks:** dois feitiços compartilham o mesmo campo `DISABLE_WITHERED_ROSE_SPELLS_CRAFTING_AND_LOOTING`. Alterar hipoteticamente esse campo pode ter efeitos em conjunto; a evidência não autoriza uma perk individual que force crafting para apenas um deles. O método consultado tem descritor `()Z`, sem argumento explícito de jogador. Não foi verificado um evento, callback ou setter oficial que permita interceptá-lo por personagem. Essas identidades permanecem **⛔ sem hook mutador homologado**.

## Campos ainda condicionados

- `allowCrafting` trata a superfície provider/host de crafting; sua negativa não é prova de indisponibilidade de casting nem de ausência de rotas de obtenção por loot, item ou progressão.
- A presença de nomes de campos `...CRAFTING_AND_LOOTING` não demonstra que ambos os sistemas são executados nem seus valores efetivos no servidor. Config default, fase de carregamento e correlação com loot **NÃO VERIFICADOS**.
- Alcance, tipo de alvo, AoE, projéteis/hitbox, velocidade, dano, elemento, cooldown, mana, níveis, duração, scaling, recasts e procs não foram medidos por esse probe; não preencher números por analogia.
- Integrar somente mediante boundary real: Somake mantém execução própria; Iron's hospeda casting e recursos; RPG Skill Tree pode fornecer atributos/Mastery/perks sem assumir casting; Black Arcana rege seu próprio runtime. Evitar duplo custo/dano e Mastery repetida.

**Fontes contextuais:** [registro 1.0.9](EXACT-1.0.9-REGISTRY-AUDIT.md), [gates opcionais](EXACT-1.0.9-REGISTRATION-GATE-MAP.md), [7 fichas](PERK-REACHABILITY-GATES-1.0.9.md).
