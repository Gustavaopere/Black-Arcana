# Wall Of Fire

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Fire
- **Níveis:** 1–5
- **Raridade:** Common → Legendary
- **Cast:** Instant
- **Mana:** 30–50
- **Cooldown:** 30 s
- **Dano AOE:** 4–8
- **Alcance/comprimento listado:** 13–25 blocos

## O que faz

Usa recasts para posicionar pontos-âncora. Ao encerrar o cast, ou ao atingir o comprimento máximo, esses pontos formam uma parede de fogo que bloqueia projéteis e incendeia criaturas que a atravessam.

## Escalonamento

O catálogo atual confirma dano AOE 4–8 e alcance/comprimento 13–25 blocos. Número máximo de anchors, duração e geometria exata ficam `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação / authority

Já cobre barreira linear construída por anchors, com bloqueio de projéteis e hazard de fogo. Ordem/Infernal não podem reivindicar gap apenas por usar uma linha/barreira semelhante. Recasts e anchors pertencem a um único lifecycle do provider e não devem gerar créditos/casts raiz duplicados em bridges.

## Fonte / evidência

Catálogo oficial atual: `https://iron.wiki/spells/` — consulta em 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`WallOfFireSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/fire/WallOfFireSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:wall_of_fire` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `COMMON`; maxLevel `5`; cooldown `30` segundos; cast `INSTANT`.
- **Campos Java:** `baseManaCost`=`30`; `manaCostPerLevel`=`5`; `baseSpellPower`=`4`; `spellPowerPerLevel`=`1`; `castTime`=`0`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getEmptyCastData()`, `getRecastCount()`, `onCast()`, `onRecastFinished()`, `getDamageSource()`, `getWallLength()`, `getDamage()`.
- **Fórmulas numéricas com retorno direto:** `getRecastCount = 3`; `getWallLength = 10 + spellLevel * 3 * getEntityPowerMultiplier(entity)`; `getDamage = getSpellPower(spellLevel, sourceEntity)`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `SpellDamageSource`, `addFreshEntity`.

**Contrato de perks:** escola `fire` não certifica que todo dano/incêndio seja fire damage; verificar fonte de dano, duração de burning e entidades de projétil. Separar atributo de spell power nativo de mutações de área/contagem/efeito, que exigem hook específico, caps e world safety. Sem contrato comprovado: ⚠️ condicionado/fail-closed. RPG Skill Tree gerencia perks, Mastery e gates; Iron's mantém cast, mana e efeitos nativos; Black Arcana mantém seu runtime e WorldEffectPolicy para efeitos próprios. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).

## Mecânica confirmada — leitura causal do código-fonte

- **Ciclo de recasts:** `getRecastCount=3`; primeira ação cria `FireWallData` e `RecastInstance` com janela de `40` ticks. `addAnchor` registra pontos de solo sob raio de escolha de alvo de 20 blocos; `onRecastFinished` instancia `WallOfFireEntity` com a coleção de âncoras.
- **Parâmetros diretos:** `getWallLength(level,caster)=10+level*3*getEntityPowerMultiplier(caster)`, limitando o comprimento acumulado de segmentos. `getDamage=getSpellPower`; fonte de dano aplica `setFireTicks(80)`.
- **Superfície da perk:** extensão de comprimento e tempo de fogo devem observar âncoras, limite de recast e entidade de parede. Não ampliar a cadeia ou criar segunda parede sem autorizações de custo, WorldEffectPolicy e deduplicação.

**Nível de prova:** inspeção do método do spell fixado no source 3.16.3; efeitos internos da entidade/projétil, possibilidade de patch por hooks externos e runtime Survival não validados.
