# Sorcerous Strike — Bloodlines 3.0.9

Estado: **⚠️ REGISTRADO / EXCLUÍDO DA CONTAGEM SEMÂNTICA — SEM AQUISIÇÃO NORMAL COMPROVADA**

## Identidade e origem

- **Tipo:** `IAction` registrada pelo Bloodlines no registro de Actions do Vampirism; **não** é uma spell do Iron's/Ars.
- **Registry ID:** `bloodlines:gravebound_crit_action`.
- **Bloodline:** `Gravebound`.
- **Versão instalada:** `bloodlines-1.21-3.0.9.jar`, com Vampirism `1.10.13`; prova detalhada via source pin `TheDrOfDoctoring/bloodlines@c8fd517d204d09dfcb9a544c17d7df87755eaa5c`.
- **Tratamento semântico:** **EXCLUDED (+0):** Sorcerous Strike aparece em registro/skill/node/config do source 3.0.9, mas o skill node não está conectado à árvore Gravebound configurada nem consta dos quatro grants default por rank; o source auditado não comprova obtenção normal em Survival. O uso forçado por comando/admin ou datapack customizado não é classificado como rota normal e não justifica promoção.
- **Execução/settlement:** Vampirism `IActionHandler` e Bloodlines mantêm autoridade de ativação, cooldown, duração, skills, sangue, Souls, Phylactery, efeitos e limpeza; Black Arcana não adiciona custo, cast ou lifecycle duplicado.

## Contrato individual preservado da auditoria do projeto

Defaults:

- cooldown **90 s**;
- action window **10 s**;
- additional vanilla-critical damage multiplier **+1.25**.

The next qualifying vanilla critical consumes `critStrikeActive` and applies Wither.

Two static blockers are recorded:

1. the skill/action has registry/node/config entries but the node is absent from the configured Gravebound tree and from rank-default lists; survival reachability is unproven;
2. config defines `sorcerousStrikeWitherDuration=8 s`, but the hit implementation uses `sorcerousStrikeDuration` instead, producing **10 s** Wither with defaults. The specific Wither-duration config appears unused in the audited source.

## Limites e testes

Os números acima são observações/defaults de source-pinned 3.0.9, não valores medidos em `config/` implantado nem resultado de conjuração física. Aplicam-se os gates reais de Bloodline, skill tree, rank, estado e recursos. Verificar no modpack cliente/servidor a interoperabilidade com Vampirism 1.10.13 e demais addons antes de integrar ou certificar efetividade.

**Referências canônicas:** [ACTION-CATALOG.md](../ACTION-CATALOG.md) · [MAGIAS.md](../MAGIAS.md) · [TECHNICAL-AUDIT.md](../TECHNICAL-AUDIT.md) · [INTEGRATION-RULES.md](../INTEGRATION-RULES.md). Documento clean-room: transcrição da auditoria factual do próprio repositório, sem código ou assets upstream.
