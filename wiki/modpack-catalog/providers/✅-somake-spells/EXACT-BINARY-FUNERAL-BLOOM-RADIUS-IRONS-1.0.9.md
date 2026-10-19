# Somake 1.0.9 — Funeral Bloom: CFG exato do raio e contrato binário Iron's 3.16.3

**Estado:** ✅ assinaturas e grafo JVM verificados em dois artefatos oficiais de versões exatas; ⚠️ dataflow completo de alcance e cálculo de SpellPower condicionados; ⛔ hooks mutadores per-player não homologados.

## Fontes e gates físicos

- Sibling modlist `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`: Somake Spells `somakespells-1.0.9-1.21.1.jar` e Iron's `irons_spellbooks-1.21.1-3.16.3.jar` (Minecraft 1.21.1 / NeoForge / Java21).
- Artefato Somake do CurseForge File **8867079**, mod ID `somakespells`, SHA-1 **`171841ac9f802be9309ecc166c1d972ac6d404c0`**; validado antes da inspeção.
- API oficial addon-facing do Iron's: Maven `io.redspace:irons_spellbooks:1.21.1-3.16.3:api` de `https://code.redspace.io/releases`, declarada em `Black-Arcana/build.gradle`. **SHA-256 do JAR de API: `69e81104a9fd31a402d9c89ab09c2a6b2fd6d2ab98db5a37bb159517363ee9ad`**.
- [Primeira execução de prova binária #39246133056](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39246133056): `SUCCESS`, nove testes sintéticos, JAR Somake SHA-exato e JAR de API Iron's oficial versionado. O HEAD seguinte incorpora SHA-256 do Iron's e snapshots negativos de CFG/callsites; a conclusão do último HEAD deve ser confirmada separadamente.
- [Scanner](../../../../docs/qa/somake_109_radius_irons_contract.py), [testes](../../../../docs/qa/somake_109_radius_irons_contract_test.py) e [workflow Java21](../../../../.github/workflows/somake-109-radius-irons-contract.yml). Evidência restrita a métodos, descriptors, arestas/contagens de desvios e referências JVM; JARs, corpos compilados e assets de terceiros não são publicados.

## Distinção crítica de assinaturas

| Ponto | Signature JVM verificada |
|---|---|
| `FuneralBloomSpell.getImpactDamage` e `getRadius` do Somake | `(ILnet/minecraft/world/entity/LivingEntity;)F` — getter recebe `int` e `LivingEntity` |
| `getImpactDamage` → `getSpellPower` compilado do Somake | `(ILnet/minecraft/world/entity/Entity;)F` — chamada a host com tipo `Entity` |
| `AbstractSpell.getSpellPower` na API oficial Iron's 3.16.3 | `(ILnet/minecraft/world/entity/Entity;)F` — descriptor correspondente ao callsite |

Esta correspondência constitui uma **prova de compatibilidade de assinatura binária** entre o Somake e a API publicada para addons pelo Iron's 3.16.3; não comprova classloading no pack real, valor de potência por jogador, comportamento de override, configs finais nem permissão para alterar o retorno. O caster `LivingEntity` passado pelo getter é compatível por herança com o parâmetro `Entity` do método host.

## CFG compilado de `getRadius(int,LivingEntity)`

| Medida estrutural | Resultado do classfile Somake 1.0.9 |
|---|---|
| Total de instruções identificadas | **28** |
| Instruções alcançáveis pelo grafo | **28** |
| Branch condicional | **1** — `ifnonnull` |
| Branch incondicional | **1** |
| Pontos de junção | **1** |
| Arestas do grafo | **28** |
| Retornos | **1** |
| Back-edges | **0** |
| Assinaturas invocadas | `getSchoolType()`, `SchoolType.getPowerFor(LivingEntity):double`, `Math.max(float,float):float`, `Mth.clamp(float,float,float):float` |
| Clamp final identificado por dois operandos literais diretos | `10.0f` e `15.0f` (argumentos 2/3 da invocação) |

O opcode `ifnonnull` prova uma decisão por referência não nula, mas **não identifica sozinho qual objeto foi testado**. Não afirmar quais condições habilitam o ramo da escola, nem equivalência entre o clamp e alcance físico/área da magia. Formulação integral do getter permanece ⚠️ `NOT_PROVED`, sem prova de stack sobre ambos os caminhos.

## Superfície binária do `getSpellPower` do Iron's

O método do artefato de API (`AbstractSpell`) possui referências simbólicas compiladas a `SpellConfigManager.getSpellConfigValue`, `SchoolType.getPowerFor(LivingEntity)` e `LivingEntity.getAttributeValue`, além de `getSchoolType` e `Double.floatValue`. Isso demonstra **dependências de configuração, escola e atributos no corpo deste método da API**, mas não os valores efetivos, operações, pesos, caps ou a semântica de aplicação. O artefato de compilação por si só não substitui análise do mod completo efetivamente carregado.

## Impacto para catálogo/perks

- ✅ Referências de assinatura e CFG produzidas com gate de hash físico e `javap` Java21; `getImpactDamage` já tinha retorno float comprovado como `1.5f + (getSpellPower(level_input,caster)*0.75f)` no [dossiê anterior](EXACT-BINARY-FUNERAL-BLOOM-FLOAT-DATAFLOW-1.0.9.md).
- ⚠️ Continua necessário resolver o CFG de `getRadius`, condições de entrada em `SchoolType.getPowerFor`, origem de atributos/dados do Iron's 3.16.3, retorno em runtime, transferência de dano/área para Bud e eventos/modificadores.
- ⛔ **FAIL_CLOSED:** não conectar atributos do RPG Skill Tree diretamente à mana, cooldown, escala, alvo ou dano do provider sem contrato e evidência de player context, sem reexecutar uma segunda vez dano/Mastery/cast.
- ⚠️ Config efetiva, Survival, jogador conectado, multiplayer, client render e modpack completo permanecem pendentes sob D035. Stage 06.05 🟡; Stage 09 condicionado.

**Contagem:** `somakespells:funeral_bloom` permanece uma única magia entre 83/83 identidades do provider já cadastradas; nenhuma entidade nem ação semântica nova foi adicionada. Este lote aumenta a profundidade da ficha, sem inflar a barra geral.
