# Wololo

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Evocation
- **Níveis:** 1
- **Raridade:** Legendary
- **Cast:** Long
- **Mana:** 10
- **Cooldown:** 10 s

## O que faz

`NÃO VERIFICADO` em nível mecânico neste passe. A documentação oficial atual expõe o spell e seus metadados, mas a descrição pública disponível é apenas “Wololo!”, o que não é evidência suficiente para inferir targeting, transformação, controle, dano ou outro efeito.

## Escalonamento

Spell de nível único. Nenhuma fórmula adicional é inferida.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's quando aplicável. Rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação / fail-closed

Wololo é catalogado como capacidade existente, mas não deve bloquear nem justificar uma mecânica Black Arcana específica até seu comportamento real ser confirmado por documentação adicional ou observação clean-room do runtime. Bridges também não devem presumir seu efeito a partir do nome/referência cultural.

## VFX / animação / áudio

`NÃO VERIFICADO`.

## Fonte / evidência

Catálogo oficial atual: `https://iron.wiki/spells/` — consulta em 2026-09-06. A fonte não fornece semântica mecânica suficiente além dos metadados acima.

## Parâmetros de implementação para perks — source auditado

- **Classe de referência:** [`WololoSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/evocation/WololoSpell.java) (`e4056af90302d37eb1739f5ff05020b020e6e252`, 3.16.3).
- **ID fonte:** `irons_spellbooks:wololo` (não inferir quando não extraído).
- **Config:** raridade `LEGENDARY`, maxLevel `1`, cooldown s `10`, cast `LONG`.
- **Campos Java:** `baseManaCost`=`10`; `manaCostPerLevel`=`5`; `baseSpellPower`=`4`; `spellPowerPerLevel`=`1`; `castTime`=`30`.
- **Métodos:** `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `checkPreCastConditions()`, `onCast()`.
- **Fórmulas de retorno simples:** não extraídas; checar métodos e auxiliares.
- **Pistas técnicas:** `TargetEntityCastData`.

**Para Codex:** seguir implementação e entidades auxiliares antes de gerar perks sobre alvo, status, duração, raio ou projéteis. Custo e spell power são provider-native com configs/atributos, não literais injetáveis em eventos. Sem hook comprovado manter ⚠️ condicionado/fail-closed e limites de custo/cap/deduplicação. Iron's: cast/custos. RPG Skill Tree: perks/Mastery/gates. Black Arcana: runtime próprio. Fonte estática, QA físico pendente. [Contrato geral](../TECHNICAL-PERK-MAP.md).
