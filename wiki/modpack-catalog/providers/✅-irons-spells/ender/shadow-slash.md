# Shadow Slash

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Ender
- **Níveis:** 1–5
- **Raridade:** Common → Legendary
- **Cast:** Instant
- **Mana:** 30–90
- **Cooldown:** 15 s
- **Dano base listado:** 5–9

## O que faz

Executa um avanço com corte de energia arcana em área. O catálogo atual também documenta deflexão de projéteis atingidos e escalonamento a partir do dano corpo a corpo e encantamentos da arma empunhada.

## Escalonamento

O dano base listado cresce de 5 para 9. A fórmula exata que incorpora melee damage, enchantments, raio do arco e regras de deflexão permanece `NÃO VERIFICADO` enquanto não houver normalização adicional.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Fontes específicas de loot/crafting permanecem `NÃO VERIFICADO`.

## Deduplicação

Já cobre dash ofensivo + slash arcano + sinergia com arma + deflexão de projéteis. Um candidato Black Arcana equivalente precisa demonstrar regra própria em vez de apenas trocar o elemento/visual.

## VFX / animação / áudio

`NÃO VERIFICADO` no runtime real do pack neste passe.

## Fonte / evidência

Catálogo oficial atual: `https://iron.wiki/spells/` — consulta em 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`ShadowSlashSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/ShadowSlashSpell.java), fixado em `e4056af90302d37eb1739f5ff05020b020e6e252` (versão 1.21.1-3.16.3).
- **ID declarado:** `irons_spellbooks:shadow_slash` (se NÃO EXTRAÍDO, consultar registry).
- **Config na classe:** minRarity `COMMON`, maxLevel `5`, cooldown segundos `15`, cast `INSTANT`.
- **Campos Java:** `baseManaCost`=`30`; `manaCostPerLevel`=`15`; `baseSpellPower`=`5`; `spellPowerPerLevel`=`1`; `castTime`=`0`.
- **Métodos-chave:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `onClientCast()`, `getCastStartSound()`, `onCast()`, `getDamage()`, `getDamageText()`, `getCastStartAnimation()`.
- **Fórmulas numéricas de retorno direto:** `getDamage = getSpellPower(spellLevel, entity) + Utils.getWeaponDamage(entity)`. Não são fórmulas completas de efeitos condicionais.
- **Pistas de efeito e targeting no source:** `MobEffectInstance`, `DamageSources`, `addEffect`.

**Para o Codex:** seguir `onCast` e métodos auxiliares até as classes que realmente aplicam dano/efeito. Campos extraídos documentam defaults, não a configuração efetiva no servidor. `getSpellPower` consulta atributos e escola nativos; eventos genéricos não demonstram modificabilidade de raio, quantidade ou alvo. Requer adapter/contrato real, cap, causalidade e fail-closed. Iron's mantém cast/custo/cooldown; RPG Skill Tree, perks/Mastery/gates; Black Arcana, o runtime mágico próprio. ⚠️ Auditoria estática sem testes físicos. [Especificação](../TECHNICAL-PERK-MAP.md).
