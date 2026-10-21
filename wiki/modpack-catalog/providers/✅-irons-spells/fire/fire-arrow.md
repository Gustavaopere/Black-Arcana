# Fire Arrow

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Fire
- **Níveis:** 1–10
- **Raridade:** Rare → Legendary
- **Cast:** Long
- **Mana:** 40–85
- **Cooldown:** 8 s
- **Dano direto:** 11–20
- **Raio AOE:** 3 blocos
- **Dano AOE:** 5,5–10

## O que faz

Carrega uma flecha de magia de fogo que causa dano direto ao impactar e explode por dano reduzido em uma pequena área. O provider documenta trajetória inicialmente reta antes de a gravidade passar a afetá-la.

## Escalonamento

O dano direto cresce de 11 para 20 e o AOE de 5,5 para 10. Tempo antes da gravidade, velocidade e fórmula de impacto ficam `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Fire Arrow foi adicionado na linha 3.10.0; rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação

Já cobre flecha mágica com dano direto + explosão secundária. Integrações não devem transformar o impacto e o AOE em casts raiz independentes ou double-credit.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Changelog oficial: `https://iron.wiki/changelog/`
- Consulta: 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`FireArrowSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/fire/FireArrowSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:fire_arrow` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `RARE`; maxLevel `10`; cooldown `8` segundos; cast `LONG`.
- **Campos Java:** `baseManaCost`=`40`; `manaCostPerLevel`=`5`; `baseSpellPower`=`11`; `spellPowerPerLevel`=`1`; `castTime`=`20`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `onCast()`, `getDamage()`, `getRadius()`, `getCastStartAnimation()`, `getCastFinishAnimation()`.
- **Fórmulas numéricas com retorno direto:** `getDamage = getSpellPower(spellLevel, caster)`; `getRadius = 3`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `addFreshEntity`, `Explosion`.

**Contrato de perks:** escola `fire` não certifica que todo dano/incêndio seja fire damage; verificar fonte de dano, duração de burning e entidades de projétil. Separar atributo de spell power nativo de mutações de área/contagem/efeito, que exigem hook específico, caps e world safety. Sem contrato comprovado: ⚠️ condicionado/fail-closed. RPG Skill Tree gerencia perks, Mastery e gates; Iron's mantém cast, mana e efeitos nativos; Black Arcana mantém seu runtime e WorldEffectPolicy para efeitos próprios. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
