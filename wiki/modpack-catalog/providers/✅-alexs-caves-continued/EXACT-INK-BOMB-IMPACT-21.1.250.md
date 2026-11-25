# Ink Bomb e Glow Ink Bomb — impacto, targeting, geometria e registro de efeitos (21.1.250)

**DISCOVERY_ONLY / NO_MUTATION.** Publisher 1.0.10, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`, 75.279.314 bytes. Minecraft 1.21.1, Java 21, NeoForge oficial 21.1.250. Sem dump instalado novo.

## Escopo e lacuna

Reusa [prova publisher](EXACT-HOLOCODER-HOT-CHOCOLATE-INK-BOMB-1.0.10.md), [downstream](EXACT-FOUR-ITEMS-DOWNSTREAM-21.1.250.md), [aquisição](EXACT-FOUR-ITEMS-ACQUISITION-1.0.10.md), [AI](EXACT-INK-BOMB-DEEP-ONE-INGRESS-1.0.10.md) e [defaults](EXACT-ITEM-ENTITY-DEFAULTS-21.1.250.md). O recorte novo fecha a projeção tipada dos corpos locais, seleção/deflexão do projétil e geometria do cloud, com janelas de registro de BLINDNESS/GLOWING/NIGHT_VISION/CONDUIT_POWER e THROWN. Classes cliente são candidatas opcionais; a ausência na distribuição server não prova ausência no cliente. Sem reimplementação de código publisher.

A sonda `docs/qa/alexscaves_1010_ink_bomb_impact_250_probe.py` usa oito pins de classe e nove Code hashes previamente observados. Exige distribuição e JAR exatos, método requerido presente, duas saídas idênticas, janelas de registry com escrita única de cada campo. A projeção não executa classes do jogo nem encerra todos os consumidores de status de Minecraft. Primeiro resultado pendente.

Fichas [Ink Bomb](items/ink-bomb.md) e [Glow Ink Bomb](items/glow-ink-bomb.md) continuam parciais; sem novo certificado, raiz, hook ou QA física.
