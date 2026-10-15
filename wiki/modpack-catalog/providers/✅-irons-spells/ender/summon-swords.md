# Summon Swords

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Ender
- **Níveis:** 1–5
- **Raridade:** Rare → Legendary
- **Cast:** Long
- **Mana:** 80–140
- **Cooldown:** 150 s
- **Quantidade:** 3 summons
- **Dano relativo listado:** 100%–140%
- **Vida relativa listada:** 100%–180%

## O que faz

Conjura três armamentos espectrais com papéis distintos: shortsword orientada a combate direto, rapier mais ágil e claymore de função resistente/tanking. O catálogo oficial atribui a criação do spell ao Ancient Magician Hazentouvel.

## Escalonamento

A quantidade permanece em três summons. O catálogo atual confirma crescimento de dano relativo de 100% para 140% e de vida relativa de 100% para 180%. A base exata usada por esses percentuais, AI, duração e regras de ownership ficam `NÃO VERIFICADO` neste passe.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Fontes específicas de loot/crafting permanecem `NÃO VERIFICADO`.

## Deduplicação

Já cobre trio de summons espectrais com funções de combate diferenciadas. Black Arcana não deve aprovar uma família equivalente de três armas/servos apenas por alterar nomes, VFX ou elemento.

## Authority / causalidade

Iron's permanece authority dos summons e de seu dano. Integrações Black Arcana devem preservar owner/root-cast quando observável e não conceder crédito duplicado por ataques dos três summons.

## VFX / animação / áudio

`NÃO VERIFICADO` no runtime real do pack neste passe.

## Fonte / evidência

Catálogo oficial atual: `https://iron.wiki/spells/` — consulta em 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe:** [`SummonSwordsSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/SummonSwordsSpell.java) (`iron431@e4056af90302d37eb1739f5ff05020b020e6e252`, versão 1.21.1-3.16.3).
- **ID no source:** `summon_swords` (namespace esperado Iron's; confirmar no registry se não extraído).
- **DefaultConfig:** minRarity `RARE`; maxLevel `5`; cooldown `150` s; cast `LONG`.
- **Campos Java:** `baseManaCost`=`80`; `manaCostPerLevel`=`15`; `baseSpellPower`=`1`; `spellPowerPerLevel`=`2`; `castTime`=`20`.
- **Métodos de efeito/seleção:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `getHealthBonus()`, `getDamageBonus()`, `getRecastCount()`, `onRecastFinished()`, `getEmptyCastData()`, `onCast()`.
- **Fórmulas diretas localizadas:** `getRecastCount = 2`.
- **Pistas de código:** `SummonManager`, `SpellSummonEvent`, `RecastInstance`, `addFreshEntity`.

**Regra de integração:** dados estáticos e nomes reais são pontos de entrada para o Codex; quantidades e alcance devem ser verificados no helper ou entidade que aplica o efeito. Perks/gates/Mastery são do RPG Skill Tree; cast e custos do Iron's; runtime mágico próprio do Black Arcana. Eventos disponíveis não garantem mutabilidade do efeito: sem contrato, fail-closed; caps e prevenção de duplicação são mandatórios. QA real pendente. [Mapa geral](../TECHNICAL-PERK-MAP.md).
