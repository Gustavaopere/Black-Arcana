# Aeromancy 1.2.8 — fechamento documental da versão-fonte

```text
CATALOG_SOURCE_SCOPE_ONLY
snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c
version=1.2.8
artifact_sha1=dee32c9fa84a9b3796e39846608f8f77591ea56f
installed_artifact_identity=NOT_VERIFIED
physical_qa=NOT_TESTED
mutating_hook=NOT_VERIFIED
```

**✅ 58/58 fichas do escopo documentadas.** O [manifesto](SOURCE-CATALOG-MANIFEST-1.2.8.json) cobre exatamente os 205 arquivos rastreados e 73 Java da revisão fixa, associa cada arquivo a objetos ou suporte justificado, e sela os hashes das 58 fichas individuais. Há dez spells ativos e 48 fichas de suporte: seis efeitos, cinco entidades, nove itens, dois atributos, uma escola, um attachment, quatro payloads, dois mixins, nove sistemas e nove contratos de dados. Isso não representa 58 magias nem 58 adapters.

O fechamento alfabético pode avançar para **Alex's Caves Continued**. Alterar, remover ou acrescentar uma ficha invalida este fechamento até renovar a evidência. [Índice do provider](INDEX.md) · [índice geral](../INDEX.md) · [mapa de contratos](SOURCE-CONTRACTS-1.2.8.md).

## Disposições de suporte

| Grupo do manifesto | Disposição |
|---|---|
| `AGGREGATE:bootstrap-and-registry-wiring` | Entrypoint e wiring compartilhado não criam uma habilidade adicional. Todos os registros e consumidores com comportamento têm fichas próprias. [Mapa técnico](SOURCE-CONTRACTS-1.2.8.md). |
| `AGGREGATE:build-and-release-provenance` | Doze arquivos de projeto/build e template de release delimitam versão, dependências e proveniência. Wrapper, workflow e metadados não são ações de gameplay. [Fonte e dependências](SOURCE-CONTRACTS-1.2.8.md). |
| `AGGREGATE:package-nullability-annotations` | Sete package-info.java aplicam defaults de nullabilidade; não possuem registro ou execução de habilidade. Seus caminhos e hashes são preservados individualmente. |

Os assets e dados usados por entidades, itens, spells, rede e visual são associados às fichas consumidoras. Classes de spells inativos, helpers de itens e Shockwave recebem análise própria; não são ocultados em um agregado genérico. O mapa de arquivos compartilhados pode citar várias fichas sem duplicar o caminho inventariado.

## Evidência e gates separados

O publisher 8251034 foi verificado: 753884 bytes, SHA-1 acima e SHA-256 `b2dad354467a2cf1a92519ba68c8e2c32807a976d7b235132d625b7f0f90eea8`. Os 119 recursos da fonte estão presentes e iguais em bytes ou somente após normalização de fim de linha. Os 85 classfiles correspondem por SourceFile aos 73 Java. Essa comparação não certifica equivalência de implementação, compilação reproduzível ou identidade da instalação. A [prova anterior das dez identidades](EXACT-PUBLISHER-SPELLS-1.2.8-PHYSICAL-SHA-BLOCKED.md) permanece delimitada ao publisher.

| Medida | Estado |
|---|---|
| Catálogo da versão-fonte | **58/58**, fechado no universo e nos hashes declarados |
| Raízes semânticas Aero | **10**, COUNTED_SOURCE_PINNED; acréscimo desta conclusão **0** |
| Certificação estática individual para perks | **0/58**; manifesto de certificações inalterado |
| Hook mutador / adapter executável | **NOT_VERIFIED**; setters e assinaturas isoladas não homologam mutações |
| JAR instalado | **NOT_VERIFIED**; o checksum legado tem 35 caracteres, sem SHA-1 válido |
| QA física | **NOT_TESTED**; boot, mixins, casting, PvP, proteção, multiplayer, save/reload e aquisição pendentes |

O índice deve exibir ✅ na coluna **Catálogo** e manter os gates técnicos próprios. Nenhum provider passa a COMPLETE_PERK_READY; nenhum Stage, runtime, Enshrouded ou RPG Skill Tree é alterado por este fechamento.
