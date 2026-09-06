# Evasion

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Ender
- **Níveis:** 1–5
- **Raridade:** Epic → Legendary
- **Cast:** Instant
- **Mana:** 40–120
- **Cooldown:** 180 s
- **Cargas verificadas:** 1–5 ataques evitados

## O que faz

Imbui o caster com energia Ender. Enquanto houver cargas, um ataque recebido pode consumir uma carga, teleportar o jogador a curta distância e evitar o dano daquele ataque. O efeito termina quando as cargas são esgotadas.

## Escalonamento

O catálogo público atual confirma o crescimento de 1 para 5 ataques evitados entre os níveis 1 e 5. Distância exata do teleporte, seleção do destino e demais detalhes internos ficam `NÃO VERIFICADO` neste passe.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Scrolls podem ser usados diretamente ou inscritos em spellbooks compatíveis; fontes de loot/crafting específicas de Evasion ainda estão `NÃO VERIFICADO`.

## Deduplicação

Já cobre a fantasia de esquiva automática com reposicionamento Ender. Um futuro efeito Black Arcana não é novo apenas por "evitar um golpe e teleportar"; deve demonstrar outro contrato, custo ou consequência.

## QA / interações relevantes

O changelog atual da linha 3.16.x registra correção para impedir que Evasion evite o dano diferido de Heartstop. Essa exceção deve ser preservada por integrações; Black Arcana não deve reprocessar o hit por um segundo pipeline de evasão.

## VFX / animação / áudio

`NÃO VERIFICADO` no runtime real do pack neste passe.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Changelog oficial atual: `https://iron.wiki/changelog/`
- Consulta: 2026-09-06.
