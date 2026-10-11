# More Relics 1.7.7 — biojoint / cyberpsychosis

Estado: **✅ CATALOGADO / `COUNTED_EXACT`** no inventário de habilidades owner-scoped do artefato More Relics compatível com Relics 0.12.8; **⚠️ funcionamento em Survival não validado**.

## Identidade exata

- **Relíquia owner — root do inventário:** `biojoint`. O inventário auditado registra o owner sem prefixo de namespace; esta ficha não atribui um item registry ID não comprovado.
- **Ability root:** `cyberpsychosis`, argumento resolvido em `AbilityTemplate.builder(...)` na auditoria exata.
- **Identidade semântica:** par ordenado `biojoint` + `cyberpsychosis`; não confundir raízes homônimas de relics diferentes.
- **Posição editorial:** 2/61; não representa ordem de execução, prioridade de loot ou número de spell.
- **Provider:** More Relics, mod ID `morerelics`, runtime `1.7.7-forRelics-0.12.8-1.0` para NeoForge 1.21.1.
- **Artefato instalado/publicador:** `morerelics-1.7.7-forRelics-0.12.8-1.0-1.21.1.jar`; SHA-1 físico=publicador `bc220ed291187c97bd1896f1fdd29b2377879ae1`.
- **Contagem:** `COUNTED_EXACT`; esta ficha materializa uma identidade previamente incluída nas **61** habilidades owner-scoped. **+0 novas identidades**.

## Aquisição/evolução — evidência limitada

- **Registro literal no inventário:** exact JAR `LootEntries.THE_NETHER`.
- **Tipo de evidência:** Auditoria do JAR exato: categoria de loot registrada.

O item owner e o progresso da habilidade são autoridade de More Relics/Relics. A rota documental não prova que o item apareceu no loot final da instância, nem que uma evolução foi executada sem perda de dados.

## Mecânica e interoperabilidade

- **Efeito, trigger, rank, cooldown, estatísticas, custos e parâmetros exclusivos desta habilidade:** **NÃO VERIFICADOS individualmente** nesta ficha. Identidade de root não revela efeito de jogo, mesmo quando o nome sugere um comportamento.
- **Config ativa, obtenção/evolução em Survival, relog/restart, multiplayer e reentrância:** **⚠️ pendentes** no pack real.
- **Relics** mantém o framework e o estado de habilidade; **More Relics** mantém o conteúdo. Black Arcana não implementa segunda habilidade, XP, evolução, cooldown, proc ou settlement.
- **API/hook seguro de integração:** **NÃO VERIFICADO**. Sem contrato causal e versão exata, `fail-closed`; eventos downstream da mesma habilidade não viram novas identidades.
- **Clean-room:** fatos de identidade do inventário/auditoria própria; sem copiar JAR, código, recursos, assets ou textos de localização do publicador.

**Fontes:** [inventário hash-matched de 61 habilidades](../../ABILITY-INVENTORY-EXACT.md) · [auditoria exata](../../EXACT-1.7.7-REL0128-ARTIFACT-AUDIT.md) · [README do provider](../../README.md).
