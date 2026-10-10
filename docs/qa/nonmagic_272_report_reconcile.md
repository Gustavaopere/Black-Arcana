# #272 — Reconciliação dos relatórios físicos (sem promoção semântica)

## Objetivo e autoridade

O script read-only nonmagic_272_report_reconcile.py compara dois relatórios distintos do mesmo alvo físico #272 da modlist congelada em neoforge-rpg-skilltree@de80b186357cad20ba5b81892a8682777e96e35a. O primeiro vem da triagem ZIP (nomes de membros e SHA-1/SHA-256); o segundo, da sonda dos metadados embutidos NeoForge.

As duas ferramentas anteriores já usam descritores únicos dentro de cada coleta. Esta etapa detecta divergência de SHA-256 entre as coletas, como a troca do JAR no intervalo. **Não prova** que relatórios foram capturados na instância real; JSONs podem ser sintéticos ou obsoletos. Hash coincidente significa somente *consistência dos valores relatados*. Não valida scripts, registries, mod ID no runtime, feitiços, aquisição em Survival nem o dossiê ausente. A posição permanece ⛔.

## Uso, quando a instância real estiver disponível

Na raiz do Black Arcana, com Python 3.11+ e pasta mods/ autorizada:

    python3 docs/qa/nonmagic_physical_jar_triage.py --instance "/caminho/da/instancia" --physical-numbers "272" > nonmagic-272-triage.json
    python3 docs/qa/nonmagic_272_metadata_probe.py --instance "/caminho/da/instancia" > nonmagic-272-metadata.json
    python3 docs/qa/nonmagic_272_report_reconcile.py --triage nonmagic-272-triage.json --metadata nonmagic-272-metadata.json > nonmagic-272-reconciliation.json

O reconciliador aceita também a triagem completa de 489 posições, se a #272 aparecer exatamente uma vez e as contagens forem coerentes. Os relatórios devem vir da mesma instância/rodada operacional; igualdade de hash isolada não comprova isso.

## Estados de saída

| Estado | Interpretação |
|---|---|
| REPORTED_HASHES_AND_MOD_ID_CONSISTENT | SHA-256 dos relatórios concordam, triagem indica FINGERPRINTED e metadata afirma MATCHED_EMBEDDED_MOD_ID. **Não é PASS de catálogo.** |
| SHA256_MISMATCH | Hashes diferentes; investigar troca, atualização ou fonte |
| EMBEDDED_MOD_ID_NOT_CONFIRMED | Hash coincide, mas mod ID não foi confirmado |
| COLLECTOR_BLOCKED | Captura ZIP ou metadata recusada |
| INVALID_REPORT | Schema, origem, identidade, hashes, duplicações, flags ou contagens incompatíveis |

Saída: JSON limitado, sem reproduzir nomes de membros ou conteúdos. Código de saída 0 apenas para consistência de relatórios; 2 para os demais. **Exit 0 não comprova o JAR real ou registries.**

Testes locais e CI (relatórios sintéticos):

    python3 docs/qa/nonmagic_272_report_reconcile_test.py

## Pendências preservadas

- ⛔ #272: sem dossiê certificado, registry e feitiços desconhecidos.
- ✅ 346/347 dossiês OTHER, 453 cross-domain individualizados.
- ⚠️ 39 provas binary-exact pendentes e 14 rotas de Survival.
- Mínimo estrito: 1851 objetos globais, 1849 no escopo.
- ⛔ Stage 06.05: ritual veil_anchor_consecration sem player ingress legítimo.

Nenhuma coleta física na instalação do usuário foi realizada nesta contribuição.

## Evidência de versão embutida (2026-10-10)

A sonda `nonmagic_272_metadata_probe.py` agora informa `expected_version=0.1.0`, `version_evidence` e, quando seguro, `embedded_version` da **mesma** entrada `[[mods]]` correspondente ao mod ID alvo. O reconciliador preserva o antigo `status=MATCHED_EMBEDDED_MOD_ID` como evidência somente de ID e rejeita a consistência final em caso de conflito ou ausência de versão literal comprovada:

- `SOURCE_VERSION_MISMATCH` — dois relatórios podem ter hashes e mod ID coerentes, mas versão embutida diferente da declarada;
- `SOURCE_VERSION_UNVERIFIED` — `${file.jarVersion}` não resolvido ou valor de versão inválido/ausente;
- `INVALID_REPORT` — JSON sem a nova evidência de versão, com verdicto inconsistente, ou sem o vínculo documental exigido;
- `REPORTED_HASHES_AND_MOD_ID_CONSISTENT` — mantido por compatibilidade de rótulo, mas agora **exige adicionalmente** `MATCHED_SOURCE_LITERAL`.

O status combinado ainda atesta somente *consistência de valores informados em relatórios*, não captura real, registry de magia nem obtenção. Mesmo uma correspondência literal `0.1.0` não fecha o dossiê #272; `346/347 OTHER`, `39` provas binárias e `14` rotas Survival continuam inalteradas. Ver [NeoForge 1.21.1 — Mod Files](https://docs.neoforged.net/docs/1.21.1/gettingstarted/modfiles/).
