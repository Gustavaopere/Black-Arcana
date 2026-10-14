# 39 providers — fila de evidências para validação binária

**Checkpoint atual 2026-10-14 — Reliquified Iron's 0.2.7:** [binário 24/24 + 25/25](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38595504032) **SUCCESS** em JAR publisher SHA-equal à modlist #478. Fila congelada: **✅ 27/39** proofs independentes, **⚠️ 12/39** pendentes. `registry_proofs_completed=0` no coletor de fingerprint continua correto porque esse coletor **não executa nenhuma dessas provas**. Config/Survival, Relics rank, e Iron's mana não foram validados em jogo. Checkpoints anteriores históricos.

**Checkpoint atual (2026-10-14) — Apprentice's Codex 0.9.7.1:** [83/83 callsites compilados exatos](apprentice-codex-registry-binary-2026-10-14.md), [run #38578571735](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38578571735) **SUCCESS**. **✅ 26/39** provas independentes e **⚠️ 13/39** pendentes; +0 raízes, mínimos **1857/1855** mantidos. Fingerprint collector continua `registry_proofs_completed=0`, pois não executa nenhuma das 26 auditorias independentes. `AC-P01–AC-P05` PENDING e Stage 06.05 sem promoção. Snapshots abaixo históricos.

**Checkpoint Paladin 2026-10-12:** [cinco IDs binários exatos](../../wiki/modpack-catalog/providers/✅-paladin-spells/EXACT-BINARY-SPELLS-1.1.1.md) auditados em [run #38308575364](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38308575364). **5/39** exatos e **34/39** pendentes; +0 novos, 1851/1849 inalterados. Fingerprint collector segue em `registry_proofs_completed=0`; checkpoints abaixo permanecem históricos.

**Checkpoint 2026-10-12:** a [prova de Dreamless Spells 1.1.9](../../wiki/modpack-catalog/providers/✅-dreamless-spells/EXACT-BINARY-SPELLS-1.1.9.md) ([run #38302406303](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38302406303)) eleva as provas **independentes** a **4/39**; **35/39** ainda exigem JAR/registro. +0 magias, mínimos 1851/1849. O fingerprint collector não promove nenhuma delas e continua com `registry_proofs_completed=0`; números dos checkpoints antigos abaixo são históricos.

**Checkpoint 2026-10-12:** a [prova binária independente de Crystal Chronicles 0.1.3-alpha](../../wiki/modpack-catalog/providers/✅-crystal-chronicles/EXACT-BINARY-SPELL-0.1.3-alpha.md) ([run #38298343874](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38298343874)) eleva para **3/39** os registries estáticos exatos documentados (Ars Additions, Ars Hex, Crystal Chronicles). **36/39** pendentes, +0 novos, mínimos 1851/1849. A saída do fingerprint collector ainda relata `registry_proofs_completed=0` porque nunca comprova registry por si. As linhas originais abaixo são históricas.

**Escopo:** unificar as 39 entradas `COUNTED_SOURCE_PINNED` ou `COUNTED_RELEASE_BOUNDED` com os 69 nomes exatos de JAR do crosswalk e o relatório read-only de fingerprints. Fonte física do sibling: `de80b186357cad20ba5b81892a8682777e96e35a` (snapshot 587 posições). O programa **não** lê registry, não inspeciona binários adicionais e não certifica conteúdo semântico.

## Execução após coleta física autorizada

Na raiz do repositório Black Arcana:

```bash
python3 docs/qa/physical_provider_fingerprint_collector.py --instance "/caminho/da/instancia" > providers-69-fingerprint.json

python3 docs/qa/provider_39_evidence_queue.py --fingerprints providers-69-fingerprint.json > providers-39-registry-queue.json
```

O segundo script é offline e somente leitura. Exige **exatamente 69** identidades únicas coerentes com o crosswalk, todas as contagens de status, os formatos SHA-1/SHA-256 e **exatamente 39** linhas documentais da matriz. Mismatches/entradas adicionais/duplicadas/ausentes interrompem a geração sem parcial que pareça aprovado. Nenhuma informação do corpo de JAR é incorporada ao relatório.

Por provider são emitidos: nome, JAR exato, versão do ledger, quantidade semântica **já identificada**, classe documental atual, status do fingerprint e próximo estado de trabalho. Para `FINGERPRINTED`, SHA-1/SHA-256 são encaminhados como referência **do relatório**; não se presume que ele tenha sido gerado da instância real. Para falhas físicas, não há hashes.

Os estados possíveis de fila são `FINGERPRINTED_PENDING_REGISTRY` e `PHYSICAL_ARTIFACT_BLOCKED`. **Ambos ainda requerem confirmação do registry** e retêm `registry_verified=false`, `survival_verified=false`, `promotion_allowed=false`. A saída fixa `registry_proofs_completed=0`; não é mecanismo para aprovar status `COUNTED_EXACT`.

## Aceite binário externo à fila

Para cada um dos 39: atestar bytes do JAR da instalação, metadados/versionamento, lista exaustiva de IDs de spells/rituais/glyphs, owner, gates, deduplicação e cardinalidade. Configuração ativa e obtenção em Survival são gates independentes. Sem provas binárias efetivas, os **39/39 seguem ⚠️** e nenhuma magia é acrescida ao mínimo global **1851** ou operacional **1849**. A posição OTHER **#272** continua ⛔, 346/347 dossiês OTHER documentais e Stage 06.05 ⛔.

## Testes

```bash
python3 docs/qa/provider_39_evidence_queue_test.py
```

O teste de integração confirma que os **39** registros reais pertencem aos **69** do crosswalk (subtotal documental 909 objetos); os demais são fixtures sintéticas, não JARs instalados. Nenhum relatório físico real foi consumido nesta alteração.
