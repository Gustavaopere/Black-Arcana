# Frost Step

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:frost_step`
- **JAR/versão instalada:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Ice
- **Níveis:** 1–8
- **Raridade:** Rare → Legendary
- **Cast:** Instant
- **Mana:** 15–50
- **Cooldown:** 12 s
- **Range atual:** 8–11,5 blocos
- **Shatter damage atual:** 4–11

## O que faz

Teleporta o caster para onde olha e deixa um Ice Shadow no ponto de origem. O shadow atrai aggro próximo e se estilhaça após 5 s ou ao sofrer dano.

## Source audit 3.16.3 — commit `e4056af...`

- usa `TeleportSpell.TeleportData`/`TeleportSpell.findTeleportLocation` e `Utils.handleSpellTeleport`;
- cria `FrozenHumanoid` com shatter damage = spell power e death timer 100 ticks;
- executa `Utils.performTaunt` em raio 10 com predicate derivado de hostility/last attacker;
- range: `(8 + (level - 1) * 0.5) * entityPowerMultiplier`;
- desmonta o caster se estiver montado, reseta fall distance e envia `FrostStepParticlesPacket`;
- som `FROST_STEP`.

## Targets / PvP / bosses / summons

- **Target primário:** destino de teleporte; não é um spell de target ofensivo direto.
- **Taunt do Ice Shadow:** predicate/raio source-auditados; comportamento específico contra players, bosses e summons `NÃO VERIFICADO`.
- **World/teleport gates finos dentro de `Utils.handleSpellTeleport`:** `NÃO VERIFICADO`; não contornar o helper em bridge.

## Obtenção, requisitos e aprendizado

- pipeline geral de scrolls/spellbooks;
- rotas específicas `NÃO VERIFICADO`;
- requisitos adicionais `NÃO VERIFICADO`;
- itens/focus/rituais específicos `NÃO VERIFICADO`.

## Integrações / QA / fail-closed

- **Teleport authority:** helpers do próprio provider 3.16.3.
- **Bridge específica:** `NÃO VERIFICADO`.
- **VFX:** packet de Frost Step confirmado no source; assets finais/QA client-real `NÃO VERIFICADO`.
- Não criar teleporte paralelo, segundo taunt ou segundo shatter settlement.

## Deduplicação

Já cobre blink Ice + decoy/taunt + shatter. Mobilidade glacial nova precisa de delta real e deve ser comparada também com Teleport/Blood Step.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/` — consulta 2026-09-06.
- Source 3.16.3 `e4056af...`: `FrostStepSpell.java` + `gradle.properties`.
