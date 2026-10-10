# 39 providers — fila de evidências para validação binária

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
