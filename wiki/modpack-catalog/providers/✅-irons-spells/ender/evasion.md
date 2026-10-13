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

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`EvasionSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/EvasionSpell.java), pin `e4056af90302d37eb1739f5ff05020b020e6e252` (Iron's 1.21.1-3.16.3).
- **ID no source:** `irons_spellbooks:evasion`; escola `ender`.
- **Config na classe:** minRarity `NÃO EXTRAÍDO`, maxLevel `NÃO EXTRAÍDO`, cooldown `NÃO EXTRAÍDO` segundos, cast `NÃO EXTRAÍDO`.
- **Campos Java:** `baseManaCost`=`40`; `manaCostPerLevel`=`20`; `baseSpellPower`=`0`; `spellPowerPerLevel`=`1`; `castTime`=`0`.
- **Métodos para localizar no Codex:** `getUniqueInfo()`, `getDefaultConfig()`, `getCastType()`, `getSpellResource()`, `onCast()`.
- **Fórmulas com retorno numérico direto verificadas nesta classe:** não extraídas (inspecionar onCast/helpers/entidades). Essas fórmulas não cobrem cálculos imperativos ou de entidades auxiliares.
- **Pistas técnicas detectadas:** `MobEffectInstance`, `addEffect`; verificar semântica na classe.

**Orientação para perks:** estudar as chamadas de `onCast`, `checkPreCastConditions` e os métodos acima antes de alterar alvo/raio/duração/dano; `getSpellPower` e custo aplicam config/atributos nativos. A disponibilidade de eventos genéricos não comprova alteração de variáveis locais ou entidades. Sem adapter verificado, **⚠️ condicionado / fail-closed**. Preserve casting do Iron's, Mastery/perks/gates do RPG Skill Tree e runtime próprio do Black Arcana. Registro estático, sem QA físico. [Contrato de referência](../TECHNICAL-PERK-MAP.md).
