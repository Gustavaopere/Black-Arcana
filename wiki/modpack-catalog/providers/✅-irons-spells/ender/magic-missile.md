# Magic Missile

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Ender
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Instant
- **Mana:** 10–28
- **Cooldown:** 1 s
- **Dano:** 6–10,5

## O que faz

Dispara imediatamente um projétil concentrado de magia arcana. É o projétil direto e de baixo cooldown da escola Ender no catálogo atual.

## Escalonamento

O dano listado cresce de 6 para 10,5 e o custo de mana de 10 para 28. Velocidade, homing e demais propriedades não são inferidos: ficam `NÃO VERIFICADO` quando não aparecem no catálogo público atual.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Fontes específicas de loot/crafting permanecem `NÃO VERIFICADO`.

## Deduplicação

Já cobre o arquétipo de míssil arcano simples, rápido e repetível. Uma variante Black Arcana precisa de mecânica própria além de dano/projétil/VFX.

## QA / VFX

O changelog atual da linha 3.16.x registra lens flare na renderização de Magic Missile. Demais detalhes visuais/áudio do runtime do pack permanecem `NÃO VERIFICADO`.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Changelog oficial atual: `https://iron.wiki/changelog/`
- Consulta: 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`MagicMissileSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/MagicMissileSpell.java), fixado em `e4056af90302d37eb1739f5ff05020b020e6e252` (versão 1.21.1-3.16.3).
- **ID declarado:** `irons_spellbooks:magic_missile` (se NÃO EXTRAÍDO, consultar registry).
- **Config na classe:** minRarity `COMMON`, maxLevel `10`, cooldown segundos `1`, cast `INSTANT`.
- **Campos Java:** `baseManaCost`=`10`; `manaCostPerLevel`=`2`; `baseSpellPower`=`12`; `spellPowerPerLevel`=`1`; `castTime`=`0`.
- **Métodos-chave:** `getUniqueInfo()`, `getDefaultConfig()`, `getCastType()`, `getSpellResource()`, `onCast()`, `getDamage()`.
- **Fórmulas numéricas de retorno direto:** `getDamage = getSpellPower(spellLevel, entity) * .5f`. Não são fórmulas completas de efeitos condicionais.
- **Pistas de efeito e targeting no source:** `addFreshEntity`.

**Para o Codex:** seguir `onCast` e métodos auxiliares até as classes que realmente aplicam dano/efeito. Campos extraídos documentam defaults, não a configuração efetiva no servidor. `getSpellPower` consulta atributos e escola nativos; eventos genéricos não demonstram modificabilidade de raio, quantidade ou alvo. Requer adapter/contrato real, cap, causalidade e fail-closed. Iron's mantém cast/custo/cooldown; RPG Skill Tree, perks/Mastery/gates; Black Arcana, o runtime mágico próprio. ⚠️ Auditoria estática sem testes físicos. [Especificação](../TECHNICAL-PERK-MAP.md).
