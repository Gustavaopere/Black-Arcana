# Black Arcana — Exceção física #272: identidade atestada, dossiê ausente

**Data:** 2026-10-09. **Classificação:** ⛔ bloqueado para fechamento documental/semântico; não equivale a mod mágico não catalogado confirmado.

## Evidência primária disponível

A [modlist certificada do sibling, commit `de80b186`](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/de80b186357cad20ba5b81892a8682777e96e35a/PROJECT-INSTRUCTIONS/modlist/modlist.md) informa explicitamente, tanto no parágrafo **Exceções estruturais e bloqueios** quanto na linha **#272** da tabela física:

| Atributo | Evidência da modlist pinada | Limite epistemológico |
|---|---|---|
| Posição | **#272** | Pertence ao snapshot histórico de 587 posições |
| Nome | Factory Construction Registry Probe | Nome catalográfico da modlist |
| JAR | `factory_construction_registry_probe-0.1.0.jar` | Filename declarado no índice; bytes do JAR **não foram examinados** nesta auditoria |
| Versão | `0.1.0` | Versão declarada pelo sibling, não versão reextraída do arquivo |
| Mod ID | `factory_construction_registry_probe` | Mod ID **declarado pela fonte**, ainda **não conferido em `META-INF/neoforge.mods.toml` ou no runtime** |
| Dossiê próprio | **Ausente** | Não criar dossiê `✅-` retroativamente |
| Categoria | Não atribuída | `OTHER` é triagem da auditoria Black Arcana, não categoria temática de provider |
| SHA-1/SHA-256 | Não disponível | Não atribuir fingerprint sem ler o JAR exato |
| Feitiços, rituais, registry ou poderes | **Desconhecidos** | Não inferir presença *nem ausência* de magia a partir do nome `Probe` |

A identidade de filename/versão/mod ID acima **já estava documentada no sibling**. A [auditoria do lote 11](AUDITORIA-OTHER-LOTE-11-2026-10-09.md) caracterizava corretamente a ausência de dossiê, mas seu trecho sobre `mod ID` não distinguia o ID declarado pela modlist de um ID revalidado no JAR. Esta nota **retifica apenas a proveniência desse ID**, sem transformar fonte textual em extração binária ou alterar contagens.

Um registro de proveniência legível por máquina fica em [`nonmagic_missing_dossier_272_2026-10-09.json`](../../../docs/qa/nonmagic_missing_dossier_272_2026-10-09.json).

## Próxima evidência necessária

No perfil Minecraft real autorizado, usar o coletor existente somente para #272:

```bash
python3 docs/qa/nonmagic_physical_jar_triage.py --instance "/caminho/da/instancia" --physical-numbers "272" > nonmagic-272-triage.json
```

Este comando, **não executado na instância real nesta revisão**, apenas confirma legibilidade ZIP, fingerprint e caminhos de membros (heurística). O operador deve verificar depois a identidade `neoforge.mods.toml` do JAR físico, os registros runtime, config habilitada, scripts/datapacks e superfície de jogador. Não basta uma correspondência de nome, nem `0` hints léxicos equivale a `0` magias.

## Estado do catálogo

- ✅ **346/347** dossiês `OTHER` efetivamente lidos e **453** dossiês cross-domain individuais reconciliados, conforme snapshot certificado; não somar #272 como dossiê revisado.
- ⛔ **#272** permanece sem dossiê e com registry/jogabilidade **não examinados**, mesmo com mod ID *declarado*.
- ⚠️ **0/489** JARs não-Magic da instância efetivamente inspecionados nesta série; **39** providers aguardam revalidação binária, **14** rotas aguardam evidência Survival.
- ⛔ Stage **06.05** ainda bloqueada pelo ingresso player-facing do ritual `black_arcana:veil_anchor_consecration`. Nenhuma mudança de runtime, estágio, domínio ou mínimo semântico (**1851 global / 1849 escopo**).

**Gate de encerramento da exceção:** hash SHA-256 do JAR real, metadados extraídos, owner e possível registry identificados; dossiê source/metadata verificável se disponível. Só então revisar se o objeto merece ficha de provider/magia. Na ausência de JAR: **⛔**, não ✅.
