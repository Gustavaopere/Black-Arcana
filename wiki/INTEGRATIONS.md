# Integrações atuais

A Integration Layer atual separa o core do Black Arcana dos mods hospedeiros. Ausência de um mod opcional deve degradar para integração indisponível, não quebrar o core.

## Iron's Spells 'n Spellbooks

O código atual inclui:

- bootstrap opcional/server;
- bridge de integração;
- acesso NeoForge à mana do Iron's;
- provider de custo de mana;
- snapshot de mana;
- registro/dispatch de spell hospedada;
- spell de probe de integração;
- conteúdo sintético para testes.

O ponto importante é que o Black Arcana pode usar o Iron's como **host/canal de recurso** sem transformar todo o core em uma extensão do Iron's.

## Ars Nouveau

A camada Ars possui:

- bootstrap de servidor;
- bridge;
- acesso NeoForge à mana Ars;
- `ArsManaCostProvider`;
- snapshot;
- conteúdo sintético de teste.

Assim como no Iron's, a engine continua sendo Black Arcana e o recurso pode ser fornecido pelo host.

## Malum

A integração Malum possui:

- bridge e IDs próprios;
- bootstrap de servidor;
- acesso a inventário/espíritos;
- `MalumSpiritCostProvider`;
- conteúdo sintético para testes.

Isso permite representar custo em espíritos pela mesma abstração transacional de custo usada pela engine.

## Eidolon

A integração atual possui:

- bridge e IDs;
- bootstrap opcional/server;
- registro de ritual de probe;
- `EidolonArcanaProbeRitual`;
- receita/datapack de probe (`eidolon_integration_probe.json`).

Esse ritual é infraestrutura de verificação de integração. Não deve ser confundido com o Stage 06 — Rituals completo.

## Fail-closed

O core contém `FailClosedProgressionGate` e `UnavailableOptionalIntegration`. Quando um requisito/integration necessária não pode ser satisfeita de forma confiável, o desenho atual prefere negar o caminho em vez de assumir permissivamente que o jogador pode executar o conteúdo.

## O que ainda não está aqui

A presença dessas bridges não significa que todos os feitiços candidatos já foram distribuídos entre Iron's, Ars, Malum e Eidolon. O roteamento completo dos domínios e rituais pertence aos stages de conteúdo posteriores.
