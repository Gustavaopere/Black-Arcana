# Somake 1.0.9 — Funeral Bloom: consumidores do raio, Spell → Controller → Bud

**Estado:** 🟡 auditoria binária de callsites em andamento; nenhum novo hook mutador certificado.

## Fonte exata

- Modlist sibling `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`, `somakespells-1.0.9-1.21.1.jar`, CurseForge File 8867079, mod ID `somakespells`, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`.
- [Probe clean-room](../../../../docs/qa/somake_109_radius_consumers.py), [testes](../../../../docs/qa/somake_109_radius_consumers_test.py) e [workflow Java21](../../../../.github/workflows/somake-109-radius-consumers.yml). Examina três classes compiladas já identificadas: `FuneralBloomSpell`, `FuneralBloomControllerEntity`, `FuneralBloomBudEntity`.

## Critérios de prova

São inventariados os callsites e os descritores da JVM por **método de origem**, incluindo `getRadius`, construção da controller, `launchWave`, criação da bud, `AABB.inflate`, consulta de entidades, dano, cura e owner quando aparecem. Não se declara automaticamente passagem de um valor entre métodos a partir de referências na mesma classe, nem equivalência entre área de alvo, hitbox e raio do getter.

| Eixo | Estado anterior |
|---|---|
| `getRadius` — dois retornos JVM | ✅ expressões e guard `caster != null` em [#835](EXACT-BINARY-FUNERAL-BLOOM-RADIUS-TYPED-1.0.9.md) |
| `onCast` → controller | ⚠️ construção e getRadius conhecidos; mapeamento dos argumentos precisa dataflow |
| controller → bud | ⚠️ referências de `launchWave`/entidade existem; parâmetros e loop real pendentes |
| bud → queries/hit | ⚠️ referências a `AABB`, targets, damage e heals; condição por vítima pendente |
| perks de área/targeting | ⛔ `FAIL_CLOSED` — nenhuma API versionada mutadora homologada |

Este lote usa somente evidência estática; prova de carregamento de modpack, client, multiplayer e Survival permanece sob D035/Stage 09. Stage 06.05 permanece 🟡. Somake continua com 83/83 identidades catalogadas; nenhuma magia ou adapter nova.
