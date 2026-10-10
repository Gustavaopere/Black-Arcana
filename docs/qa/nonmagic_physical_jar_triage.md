# Auditoria read-only dos 489 JARs fora da categoria Magic

Status: `SUPPORTED TOOL / NOT EXECUTED AGAINST USER ASSEMBLED INSTANCE / ZIP NAMES ARE CANDIDATES, NOT REGISTRY PROOF`

## Fonte física e aritmética

- Snapshot físico sibling `neoforge-rpg-skilltree@de80b186357cad20ba5b81892a8682777e96e35a` contém **587 entradas numeradas: 97 categorizadas Magic + 489 JARs fora de Magic + 1 modloader NeoForge**.
- Manifesto exato [nonmagic_physical_manifest_2026-10-08.json](nonmagic_physical_manifest_2026-10-08.json), campos `physical_number`, `name`, `filename`, `version`, `categories`, `triage_group` e source SHA. **Não** inclui o modloader no conjunto de JARs processáveis.
- Grupos de triagem de alta prioridade são disjuntos: **46** com correspondência lexical no nome, **96** por categoria RPG/equipamentos/mobs/dimensões que não caíram no grupo lexical, **347** outros JARs. Os 347 também estão no manifesto.
- `triage_group` é exclusivamente um filtro para ordenar investigação; ele não comprova presença nem ausência de magia ou feitiço no JAR.

## Executar sobre a instância real

Requisitos: Python 3.11+ e acesso autorizado à pasta real com `mods/`. A partir da raiz Black Arcana:

```bash
python3 docs/qa/nonmagic_physical_jar_triage.py --instance "/caminho/da/instancia" > nonmagic-physical-jar-triage.json
```

Para priorizar algumas posições da modlist física:

```bash
python3 docs/qa/nonmagic_physical_jar_triage.py --instance "/caminho/da/instancia" --physical-numbers "121,334,395,404,464" > selected-nonmagic-triage.json
```

Não é preciso enviar o conteúdo bruto dos JARs ou o save: este processo apenas lê ZIP member names, tamanhos, SHA-1 e SHA-256 dos filenames físicos explícitos. Não executa mod code, não extrai arquivo do ZIP, não decompila classes nem modifica o pack. Symlinks são rejeitados; ZIPs inválidos/ausentes/over-sized e archives com membros excessivos ficam com status de falha fechada.

## Interpretação dos resultados

- `status=FINGERPRINTED` significa **JAR estruturalmente ZIP e hash do arquivo capturado**, não que aquele JAR tem spell registry ou carregou no NeoForge.
- `lexical_hint_member_count` é apenas o número de nomes de entradas com expressões como `spell`, `glyph`, `ritual`, `ability`, `summon`, `power` ou `beam`. É insuficiente para definir action ownership ou castability; dependências podem aparecer nos nomes de classes e data genéricos.
- **Zero** `lexical_hint_member_count` não autoriza classificar o provider como sem conteúdo mágico. Registries declarativos/indiretos, bytecode dinâmico, scripts KubeJS e ativos encriptados podem não fornecer essas palavras nos caminhos.
- A tool retorna no máximo 16 caminhos candidatos por JAR, com até 256 caracteres cada; não retém corpos de classes/JSONs; a trilha de evidência é read-only.
- Este output prioriza a inspeção **individual e version-exact** dos JARs conforme a [auditoria cross-domain](../../wiki/modpack-catalog/meta/AUDITORIA-CROSS-DOMAIN-2026-10-08.md). Após encontrar ID de registry novo, validar a versão exata, registrar sua ficha e só então alterar contagens.

## Testes

```bash
python3 docs/qa/nonmagic_physical_jar_triage_test.py
```

Estes testes usam arquivos ZIP sintéticos, sem depender da instância real. Os resultados passam a ser parte da CI, mas **não** são prova de JAR físico carregado.


## Posição física #272 — dossiê ausente, identidade declarada

A [reconciliação #272](../../wiki/modpack-catalog/meta/EXCECAO-PHYSICAL-272-2026-10-09.md) informa que a modlist do sibling declara o arquivo `factory_construction_registry_probe-0.1.0.jar`, versão `0.1.0` e mod ID `factory_construction_registry_probe`, mas **não há dossiê certificado nem SHA do binário real**. A referência do mod ID é uma declaração documental, não extração do JAR.

Com a instância real disponível, executar somente esta posição:

```bash
python3 docs/qa/nonmagic_physical_jar_triage.py --instance "/caminho/da/instancia" --physical-numbers "272" > nonmagic-272-triage.json
```

Verificar se o resultado retornou `FINGERPRINTED` com hashes. Mesmo esse status não comprova registros de spells, mod ID embutido, gameplay ou configuração: isso exige verificação posterior de metadata e runtime. `MISSING`, `INVALID_ZIP_JAR`, `UNREADABLE` e demais falhas devem manter o caso **⛔**. O comando acima é um procedimento e **não foi executado na instalação do usuário**.

## Sonda read-only de metadados NeoForge para #272

O coletor geral acima analisa **nomes** de entradas ZIP e hashes, sem ler o conteúdo de metadados. Para validar especificamente a identidade embutida de **#272**, existe uma sonda separada e opcional:

```bash
python3 docs/qa/nonmagic_272_metadata_probe.py --instance "/caminho/da/instancia" > nonmagic-272-metadata.json
```

A sonda cruza o manifesto físico e a proveniência SHA-pinned do sibling. Ela aceita somente o arquivo exato `factory_construction_registry_probe-0.1.0.jar` na pasta `mods/`; dentro do ZIP, lê no máximo 64 KiB de `META-INF/neoforge.mods.toml`. Rejeita symlinks, duplicação/invalidez do metadata, JARs acima de 1 GiB e ZIPs com mais de 100.000 entradas. A leitura do TOML e o cálculo do SHA-256 agora usam **o mesmo descritor de arquivo aberto**, com `O_NOFOLLOW` quando disponível e conferência de identidade/alteração do arquivo; uma substituição ou alteração detectada durante a leitura retorna `CHANGED_DURING_SCAN` **sem hash nem mod IDs**. **Não executa código, não lê classes ou JSONs de feitiços, não decompila nem modifica o pack.**

- `MATCHED_EMBEDDED_MOD_ID`: o `modId` declarado em TOML coincide com o documentado no snapshot e um SHA-256 do arquivo foi calculado. Exit `0`. **Isso não certifica registries, feitiços, gameplay ou aquisição em Survival.**
- `MOD_ID_MISMATCH`, ZIP inválido, metadata ausente/ambígua ou outras falhas: bloqueio e exit `2`. Fonte/manifesto divergentes produzem erro.

Os testes de regressão usam JARs inteiramente sintéticos:

```bash
python3 docs/qa/nonmagic_272_metadata_probe_test.py
```

**O JAR da instalação real não foi lido nesta implementação.** Não alterar a contagem de 346/347 dossiês `OTHER`, 453 dossiês cross-domain, 39 provas binary-exact ou 14 rotas Survival apenas por disponibilizar a sonda.
