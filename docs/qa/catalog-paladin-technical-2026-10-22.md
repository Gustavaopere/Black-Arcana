# Paladin Spells — reauditoria por campo, 22/10/2026

Base Black Arcana `01c42361d4c9a6fd581745b33ffdb84b4464406c`, posterior às PRs #872/#873. RPG `ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc`, Enshrouded `a41dbb51aacb94b7b5db6517f1514b0b7aee3e83`, Factory `518278ae9c0d264a537cc1bc6ee4974e01270fdf`. Source oficial Paladin `31f64ccdb39d062b21cc25d434cb62d6463b486e`, checkout detached inspecionado; nenhum código upstream importado.

## Entrega

Cinco fichas existentes enriquecidas com matriz por campo, limites, fase, consumidores e links permanentes. [Dossiê de integração](../../wiki/modpack-catalog/providers/✅-paladin-spells/PERK-BOUNDARIES-1.1.1.md). Correção factual: `BedrockSkinEvent#onLivingDamage(LivingDamageEvent.Pre)` existe no mesmo pin e consome a redução armazenada; não há justificativa documental para adicionar segundo handler. Sworn Protector: raio calculado 36–90 não supera automaticamente a busca AABB inflada em 64; onCast cliente continua incompatível com a dependência de estado server do handler no source. Ram: knockback não depende do retorno de hurt e não prova dano entregue. Taunt: aplicação inicial e repetição por tick têm filtros diferentes. Bulwark: modifier 0.0 continua achado source sem confirmação física.

Barra por mod: **5/5 fichas com matriz e consumidores reauditados**, sem promover mutadores/compatibilidade física. Barra global indeterminada, 164 providers no painel, mínimos mágicos e campanha de identidade 38/39 preservados; +0 identidades novas. Nenhum código runtime de Black Arcana/RPG/Enshrouded modificado.

## Validação executada

- `PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/global_magic_catalog_test.py`: **52/52 PASS**.
- `PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/catalog_physical_ledger_test.py`: **5/5 PASS**.
- `PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/magic_pendency_tracker_test.py`: **26/26 PASS**.
- Conferência local de links em todos os Markdown de Paladin e no painel: **381 destinos locais existentes**, **63 links source-pinned com arquivos/âncoras de linha válidos** nos checkouts exatos. Não é validação de gameplay nem prova de conteúdo mutável.
- Revisão do diff e `git diff --check` sem erro de whitespace.

## Limitações do ambiente e publicação

JDK Temurin 21.0.8+9 instalado fora do repo com SHA-256 do publicador conferido; Gradle 9.2.1 bootstrap passou seu checksum. Proxy e truststore do sistema configurados fora do checkout. O comando `test build stage05QaFixtureJar catalogQaProbeJar` para antes da compilação ao resolver `net.neoforged:neoform-runtime:2.0.24`: HTTP 403 de `maven.neoforged.net`. Não é teste JUnit falhando ou defeito confirmado do mod; JUnit/build/GameTests/server smoke não executados. Domínios de dependências e API GitHub salvos no draft do ambiente, sem aplicação/publicação automática.

Git read funciona; `gh api repos/Gustavaopere/Black-Arcana` retorna Forbidden para api.github.com no proxy. PR/CI/merge remoto não foram validados por este relatório; registrar resultado real no handoff. Não substituir revisão/CI por push direto na main. Após aplicar a configuração de rede, retomar setup e gates; runtime, Survival e modpack continuam PENDING.


## Continuação na mesma revisão

Revisão independente confirmou as fórmulas/contratos e levou aos anchors de helpers Taunt e à auditoria source-pinned do host: `SpellOnCastEvent` precede débito/onCast e o RPG escuta esse evento para prática de Mastery. `super.onCast` base contém somente debug/finish sound; sua ausência não remove os outros passos do caminho jogador. O [boundary](../../wiki/modpack-catalog/providers/✅-paladin-spells/PERK-BOUNDARIES-1.1.1.md) registra os permalinks. A API GitHub passou a funcionar pela rota HTTPS do proxy com a autenticação existente; PR #874 aberta, CI pendente no momento desta nota. O Maven NeoForge também respondeu. Setup local avançou usando a propriedade suportada `launcherManifestUrl` de NeoForm Runtime para o endpoint oficial Piston; validação completa será registrada no rascunho do ambiente quando concluída. Os bloqueios anteriores descrevem a primeira tentativa, não falta atual de credenciais.
