# Somake Spells 1.0.9 — sete overrides de aquisição e contrato de perks

**Checkpoint:** 2026-10-18; escopo documental / zero código de produção / zero adapters. Fonte de identidade: `somakespells-1.0.9-1.21.1.jar`, mod ID `somakespells`, SHA-1 físico = publisher `171841ac9f802be9309ecc166c1d972ac6d404c0` (CurseForge File `8867079`). A versão na modlist `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd` permanece `1.0.9`.

## Inventário verificável

- Registry real: `com.somake.somakespells.registries.ModSpells`; **83 IDs únicos** com `DeferredRegister<AbstractSpell>`; **67** inscrições incondicionais e **16** condicionadas à presença de outros providers.
- No perfil físico registrado, os providers de gate estão presentes e os 83 IDs são admitidos pelas condições **de registro**. Os gates efetivos de Iron's, `enableSpellLockSystem`, crafting, loot, Survival, datapacks e client/modpack **permanecem pendentes**.
- **0/83** novas magias adicionadas ao numerador estrito por esta alteração; cadastro estrutural e mutabilidade são métricas independentes.
- As 83 classes têm **zero overrides de `isEnabled()`**; isso não prova que os spells estão enabled no host.
- Exatamente **7/83** classes sobrescrevem `allowCrafting()`; a auditoria física classificou 3 como `false` constante e 4 com fluxo não constante.

| Spell registry ID | Resultado do override `allowCrafting()` | Consequência documentada para perks |
|---|---|---|
| [`somakespells:fragmented_requiem`](registry-1.0.9/fragmented-requiem.md) | `CONSTANT_FALSE` | crafting ordinário bloqueado neste método; outras aquisições desconhecidas |
| [`somakespells:rose_secret`](registry-1.0.9/rose-secret.md) | `CONSTANT_FALSE` | mesma condição; castability não inferida |
| [`somakespells:comforting_lullaby`](registry-1.0.9/comforting-lullaby.md) | `CONSTANT_FALSE` | mesma condição; alternativa de loot/progressão desconhecida |
| [`somakespells:funeral_bloom`](registry-1.0.9/funeral-bloom.md) | `NON_CONSTANT` | predicado completo não auditado; hook de desbloqueio ⛔ |
| [`somakespells:withered_rose_vortex`](registry-1.0.9/withered-rose-vortex.md) | `NON_CONSTANT` | predicado completo não auditado; hook de desbloqueio ⛔ |
| [`somakespells:custodia_caeli`](registry-1.0.9/custodia-caeli.md) | `NON_CONSTANT` | predicado completo não auditado; hook de desbloqueio ⛔ |
| [`somakespells:jingle_bell`](registry-1.0.9/jingle-bell.md) | `NON_CONSTANT` | predicado completo não auditado; hook de desbloqueio ⛔ |

Os **76 restantes** não possuem override de `allowCrafting()` próprio no release auditado; não inferir `true` efetivo porque herança, host, config e datapack podem impor outras condições.

## Matriz de evidência causal e engenharia

| Dimensão | Situação para estas sete magias |
|---|---|
| Registro e presença do provider | ✅ `EXACT_BINARY` (hash de release + ID + predicate group) |
| Forma do `allowCrafting()` | ✅ `EXACT_BINARY` na classificação `constant false` / `non-constant` |
| Lógica da condição não constante | ⛔ NÃO VERIFICADA; não inferir estados ou eventos |
| Casting, tipo/alcance do alvo, LOS, AoE, projeto/hitbox/velocidade | ⚠️ NÃO VERIFICADOS pelos gates estruturais atuais |
| Dano, escola/damage type, buffs, duração, level e scaling | ⚠️ NÃO VERIFICADOS pelos gates estruturais atuais |
| Mana, cooldown, custo e aquisição efetiva | ⚠️ Provider/host efetivos desconhecidos |
| API/evento para perk modificadora | ⛔ FAIL-CLOSED até método e assinatura concretos |
| QA real de Survival, player/reload e modpack | ⛔ PENDENTE |

**Integração:** Somake decide lógica específica de spell/acquisition; Iron's controla seu pipeline host; o RPG Skill Tree só fornece perks/Mastery/gates através de boundary real. Black Arcana permanece autoritativo apenas pelo runtime mágico próprio. Uma perk de alcance/projétil/custo/dano de Somake exige provas adicionais, não pode ser implementada com base apenas no nome de método `allowCrafting()`. Não aplicar dano duas vezes nem transferir cooldown/mana.

**Próximo gate preciso:** no artifact 1.0.9 inspecionar por spell `getSpellResource`, `onCast`, classes de projétil/efeito, extensão verificada e condições `allowCrafting` completas; testar estado `enableSpellLockSystem` efetivo e host Iron's 3.16.3 em servidor controlado antes de liberar qualquer mutação.

**Fontes locais:** [registry exata](EXACT-1.0.9-REGISTRY-AUDIT.md), [mapa de predicados opcionais](EXACT-1.0.9-REGISTRATION-GATE-MAP.md), [checklist de revalidação](CURRENT-1.0.9-REVALIDATION-CHECKLIST.md), [catálogo de 83 IDs](SPELL-CATALOG-1.0.9.md). Nenhum byte de código, JAR ou texto proprietários foi copiado; foram conservados fatos funcionais necessários à interoperabilidade.
