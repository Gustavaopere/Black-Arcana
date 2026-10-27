# MFTE 1.1.5 — reconciliação documental das 22 spells

**27/10/2026.** Base reconciliada: Black Arcana `901ae8ab0cc2bac795cc3cd74eb9a7a3d34d530e`, incluindo as contribuições Goety #927/#928 e Dreamless #926. Escopo deste lote: somente documentação de MFTE, seu progresso editorial e este registro de QA. Nenhum runtime, dependência, Stage ou código dos projetos irmãos foi alterado.

## Problema e resultado

O catálogo usava uma fonte que ainda declarava `1.1.5`, mas era posterior à publicação do JAR e divergia em parâmetros e lifecycle. Os 17 rascunhos preservados foram reconciliados e as cinco fichas restantes aprofundadas, totalizando **22/22 dossiês** com consumidores, fórmulas, targeting/geometria, tempo, recursos, invocações, persistência, matrizes por perk e limitações por campo.

Fonte candidata: **`WarPhan78/ISS_MagicFromTheEast-1.21.x@f2a095cbbc89f8d8428dca758140663adf54ae88`**, `RELEASE_BOUNDED_SOURCE`, anterior à criação oficial do arquivo CurseForge `7385201`. A [reconciliação de proveniência](../../wiki/modpack-catalog/providers/✅-iss-magic-from-the-east/RELEASE-SOURCE-RECONCILIATION-1.1.5.md) registra cronologia, hashes, diferenças entre fontes e confrontos binários estreitos. O [contrato comum](../../wiki/modpack-catalog/providers/✅-iss-magic-from-the-east/SPELL-PERK-BOUNDARIES-1.1.5.md) registra eventos e integração no host Iron’s 3.16.3.

O publisher revalidado tem **1680780 bytes**, SHA-1 **`e3552ea6b7b32b843c48bf0d857237d4b7129ab0`** e SHA-256 **`e5ab22492b300d8f5e797f3f9d196e1e06f4a4a1db3650ac5a5979e6956e4920`**. O SHA-1 coincide com o ledger físico histórico #346; não houve nova leitura do perfil original. Não há prova de equivalência integral fonte↔JAR. A fonte candidata declara Iron’s 3.14.8/NeoForge 21.1.187; o pack de referência usa 3.16.3/21.1.250.

## Verificações locais

- Inventário reconciliado: **22 inscrições da fonte**, **22 classes de spell no publisher**, **22 fichas com ID e classe correspondentes**. Preservadas as 11 Symmetry e 11 Spirit.
- Referências das 22 fichas e dos dois documentos comuns: **568 links de código pinados**, **103 arquivos-fonte distintos**, **97 links locais**, **38 tabelas**; arquivos e limites de linha conferidos. Isso valida localizadores, não sua equivalência com todos os métodos binários.
- Revisão semântica independente por grupos: ataques/projéteis, proxy/Spirit, campos/montaria e summons. Corrigidos consumidores de landing/knockback, fontes antigas de cooldown/recast, distinções de imunidade/aplicação por blocos e as limitações dos eventos.
- Confrontos JDK 21 `javap -c -p` limitados a campos, instruções e relações de chamadas nas classes indicadas nas fichas. Dune está declarada como escola no JAR; nenhuma das 22 spells pertence a ela. Esse achado não acrescenta identidade de spell.
- **108 testes documentais existentes passaram**: integridade dos índices (22), geração (3), catálogo global (52), ledger físico (5) e pendências (26).
- **509 índices verificados**, **2075 fichas candidatas**, **138 certificadas**, **0 providers integrais**, **0 problemas**; modo de conferência do gerador aprovado. O manifesto e os índices gerados permanecem inalterados.
- `git diff --check`, referências locais, definições Markdown e número de colunas das tabelas conferidos. CI pré e pós-merge devem ser consultadas no SHA correspondente no GitHub; os resultados locais não antecipam esses workflows.

Comandos dos testes existentes:

```sh
python3 scripts/catalog/check_perk_ready_indexes_test.py
python3 scripts/catalog/generate_perk_ready_indexes_test.py
python3 docs/qa/global_magic_catalog_test.py
python3 docs/qa/catalog_physical_ledger_test.py
python3 docs/qa/magic_pendency_tracker_test.py
python3 scripts/catalog/check_perk_ready_indexes.py
python3 scripts/catalog/generate_perk_ready_indexes.py --check
git diff --check
```

## Limites e contadores

**+0 identidades semânticas, +0 certificados estritos.** MFTE: **22/22 dossiês editoriais**, **0/22 certificados no manifesto**. Global observado: **138/2075**, **0/164 providers integralmente certificados**. Universo total de conteúdo integrável aberto. As barras editoriais e de certificação estão nomeadas separadamente no [README do provider](../../wiki/modpack-catalog/providers/✅-iss-magic-from-the-east/README.md) e no [painel corrente](../../wiki/modpack-catalog/meta/PROGRESSO-CATALOGO-ATUAL.md).

RPG foi consultado na `main` `59ff2a0e827fd08faa603f4482f8104ac433383c`; Enshrouded em `a41dbb51aacb94b7b5db6517f1514b0b7aee3e83`. O teste isolado do validador de lane confirma rejeição das strings MFTE normalizadas com `/`, sem reproduzir uma falha no jogo e sem implementar correção. Não foram homologados adapters ou novas integrações.

**PENDING:** campos/métodos binários não confrontados, configuração/datapacks efetivos, aquisição Survival, comportamento físico, custo/dano realmente aceitos, targeting/claims/PvP, lifecycle, persistência/sync e execução de mutações por perks. Fonte, assinatura pública e CI verde não comprovam esses eixos.
