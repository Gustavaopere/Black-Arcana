# Provider Audit Queue — delta Goety addons

Data: `2026-09-07`

Este arquivo é um **overlay de estado** sobre `PROVIDER-AUDIT-QUEUE.md` e prevalece somente para as linhas abaixo até a próxima regeneração/consolidação integral da fila. Ele existe para evitar reescrever a tabela completa de 103 providers durante uma PR longa de catálogo.

| Mod ID | Nome atual | JAR atual | Versão atual | Estado vigente da auditoria |
|---|---|---|---|---|
| `goety_cataclysm` | Goety Cataclysm | `goety_cataclysm-1.21.1-1.8.2.jar` | `1.21.1-1.8.2` | `EXACT-ARTIFACT-PINNED / PUBLIC SEMANTIC SURFACE AUDITED / EXACT 1.21.1 SOURCE REVISION UNLOCATED / ARR / GRANULAR REGISTRIES+HOOKS UNVERIFIED / RUNTIME QA PENDING / FAIL-CLOSED` |
| `goetyiron` | Goety Iron | `GoetyIron-1.21.1-NeoForge-3.1.jar` | `3.1` | `EXACT-ARTIFACT-PINNED / PUBLIC SERVANT SURFACE: 8 NAMES + 3.1 CHANGELOG AUDITED / SOURCE REVISION UNLOCATED / COMPLETE REGISTRIES+HOOKS UNVERIFIED / RUNTIME QA PENDING / FAIL-CLOSED` |

## Goety Cataclysm evidence boundary

- CurseForge File ID `8518940`;
- SHA-1 instalado `4e3052a082200371b36e1a88fdce05e294d82757`;
- release NeoForge 1.21.1 publicada em 2026-07-27;
- changelog público: primeira release 1.21.1;
- projeto `All Rights Reserved`;
- repositório público oficial localizado, mas a única branch pública auditada está em Minecraft 1.20.1 / mod version 1.20-1.9.1 e não fornece um pin exato da release instalada;
- sem decompilação ou promoção de internals de outra versão.

## Goety Iron evidence boundary

- CurseForge File ID `8662179`;
- SHA-1 instalado `c8529867e798661ed01fb2948abda23735888fc6`;
- release NeoForge 1.21.1 publicada em 2026-08-16;
- licença declarada `MIT`;
- página pública nomeia oito servants e descreve Focus/ritual acquisition, spell learning e upgrade orbs em alto nível;
- changelog 3.1 confirma spell-attribute config por servant, Tincture→Void Vault reset, Polar Bear/Vex replacement e fixes do Improved Ominous Fire Orb;
- nenhum source pin oficial exato foi localizado durante a auditoria; internals/API permanecem fail-closed.

## Disposição

Os dois addons deixam de ser `GUIA LIDO / CATÁLOGO GRANULAR PENDENTE` genérico e passam a estados **release/artifact-bounded**. Isso não significa catálogo completo, source-pinned ou runtime-validated.

Nenhuma capability de Phase 3 é desbloqueada por este delta. Goety continua authority do próprio resource/casting/servant framework; Iron's e Cataclysm conservam seus domínios nativos; Black Arcana não duplica settlement, mana/Soul Energy, servant ownership ou spell execution.

## Próximo checkpoint

Próximo provider base de alto valor: `malum` `1.8.2`.
