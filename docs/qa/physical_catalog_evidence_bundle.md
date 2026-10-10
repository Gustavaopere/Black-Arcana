# Black Arcana — coleta única de evidências físicas para o catálogo

**Estado da ferramenta:** read-only sobre a instância, sem análise binária de registries e sem promoção automática de feitiços. Base documental certificada: `neoforge-rpg-skilltree@de80b186357cad20ba5b81892a8682777e96e35a`. A ferramenta **não foi executada na instância física do usuário** nesta contribuição.

## Execução na instância real

Executar a partir da raiz do repositório Black Arcana com Python 3.11+:

```bash
python3 docs/qa/physical_catalog_evidence_bundle.py \
  --instance "/caminho/da/instancia" \
  --output-dir "/caminho/seguro/black-arcana-evidence-2026-10-10"
```

O diretório de destino deve ser **novo, inexistente e fora da instância Minecraft**. A ferramenta se recusa a sobrescrever uma coleta anterior ou gravar dentro da instância. A pasta `mods/` deve ser diretório real sem symlink. Para mundo externo e log específico:

```bash
python3 docs/qa/physical_catalog_evidence_bundle.py \
  --instance "/caminho/da/instancia" \
  --output-dir "/caminho/seguro/black-arcana-evidence-2026-10-10" \
  --world "/caminho/do/servidor/world" \
  --probe-log "/caminho/do/servidor/logs/latest.log"
```

`--world` pode ser repetido. Não é necessário copiar JARs, saves, scripts completos ou os conteúdos brutos dos arquivos de configuração; os coletores existentes emitem somente evidência delimitada conforme seus guias.

## Relatórios e dependências

| Arquivo de saída | Fonte / interpretação |
|---|---|
| `nonmagic-489.json` | Triagem read-only de nomes ZIP/SHA de 489 JARs fora de Magic; zero pistas não implica ausência de magia |
| `providers-69.json` | Identidade/fingerprint de 69 JARs reconciliados; não prova registry |
| `physical-272-metadata.json` | Metadata NeoForge da posição #272, mod ID e versão literal; JAR ausente/divergência mantém bloqueio |
| `physical-272-reconciliation.json` | Comparação do SHA entre triagem e metadata #272; depende dos dois relatórios anteriores |
| `provider-39-queue.json` | Fila dos 39 providers source/release-bounded; depende do fingerprint 69 e nunca autoriza promoção |
| `deployed-evidence.json` | Configuração, KubeJS, customização e runtime probe filtrado; não comprova obtenção real em Survival |
| `bundle-index.json` | Índice de seis etapas, códigos de saída, arquivos e estados. Não inclui caminho completo da instância |

A orquestração invoca scripts versionados do próprio repositório, via argumentos de subprocesso sem shell. Quando uma etapa necessária falha, suas derivadas são `SKIPPED`, mas as independentes continuam; `COLLECTION_INCOMPLETE` informa falha operacional. A sonda e o reconciliador #272 aceitam exit 2 como `BLOCKED` **somente com saída JSON válida**, não como prova de conclusão.

`REPORTS_CAPTURED_CATALOG_UNVERIFIED` significa que os seis procedimentos emitiram arquivos válidos; **não** significa correspondência com um publisher oficial, registry carregado, magias registradas, disponibilidade em Survival ou validação de release. O bundle mantém `registry_proofs_completed=0`, `catalog_spells_added=0` e `stage_promotion_allowed=false`, inclusive se todos os JARs tiverem hash.

**Privacidade:** embora os coletores excluam corpos de scripts, configs e JARs, os JSONs podem conter nomes relativos de arquivos, hashes e dados específicos do pack. Revisar os relatórios antes de compartilhá-los publicamente. O índice não traz o caminho absoluto da instância.

## Integridade mínima dos relatórios (2026-10-10)

O índice do bundle **não aceita apenas um subprocesso encerrado com código zero e qualquer objeto JSON**. Cada etapa passa por validação específica de `schema`, `evidence`, versão da modlist pinada quando aplicável, identidade da posição #272, cardinalidade/contagem dos manifests de **489 / 69 / 39**, estrutura dos registros e flags de não promoção. A sonda e o reconciliador #272 relacionam os códigos de saída 0/2 a estados compatíveis; um JSON inválido é **`FAILED`**, não `BLOCKED` ou `COLLECTED`. Se uma dependência falhar, o seu derivado será `SKIPPED`.

Esta validação evita falsas classificações decorrentes de saída truncada, de outra versão da ferramenta ou de formato incorreto. **Não autentica a procedência de um arquivo JSON fabricado** e não substitui hashes do JAR real, registro carregado de spells nem teste de aquisição em Survival. A saída de um bundler jamais concede prova semântica por si mesma.

## Gates que permanecem

- #272 ⛔ — sem dossiê certificado e sem JAR real inspecionado nesta contribuição
- 39 providers ⚠️ — sem certificação binary-exact de registry
- 14 rotas de configuração/Survival ⚠️ — sem validação de aquisição real
- Stage 06.05 ⛔ — sem ingresso legítimo do jogador para `black_arcana:veil_anchor_consecration`
- Mínimo semântico inalterado: **1851** global e **1849** no escopo

## Testes

```bash
python3 docs/qa/physical_catalog_evidence_bundle_test.py
```

A suíte testa a execução/propagação de bloqueios, recusa de sobrescrita, isolamento de destino, passagem de parâmetros e rejeição de promoção falsa. Testes com estruturas sintéticas não substituem uma coleta efetiva da instância.
