# Blaze Storm

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Fire
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Continuous
- **Mana:** 5–14
- **Cooldown:** 20 s
- **Dano público listado:** 2–5,59
- **Cast duration auditado:** `55 + 5*level` ticks
- **Cadência auditada:** 1 `SmallMagicFireball` a cada 5 ticks
- **Damage source auditado:** 40 fire ticks; i-frames `0`

## O que faz

Enquanto canalizado, dispara uma barragem irregular de pequenas fireballs de Blaze à frente do caster. A auditoria do provider 3.16.3 confirma o lançamento de `SmallMagicFireball` a cada 5 ticks durante a janela do cast.

## Escalonamento

O catálogo público atual lista dano de 2–5,59. A auditoria de source 3.16.3 registra `damagePerProjectile = spellPower * 0.4`, spell power `5 + 1/level` e cast duration `55 + 5*level` ticks. Dispersão exata e regras finas de ignite sobre blocos ficam fora do que foi congelado nesta ficha.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação / causalidade / world safety

Já cobre canal contínuo de múltiplos projéteis incendiários. Os projéteis derivados pertencem ao lifecycle do mesmo cast raiz e não devem gerar crédito/procs como novos casts independentes. O fato de o provider produzir efeitos incendiários não autoriza Black Arcana a criar spread ou mutações paralelas; qualquer integração continua sujeita às authorities de world safety.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/` — consulta em 2026-09-06.
- Auditoria source 3.16.3 canônica: `wiki/providers/irons-spellbooks/spells/fire/blaze-storm.md`.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`BlazeStormSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/fire/BlazeStormSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:blaze_storm` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `COMMON`; maxLevel `10`; cooldown `20` segundos; cast `CONTINUOUS`.
- **Campos Java:** `baseManaCost`=`5`; `manaCostPerLevel`=`1`; `baseSpellPower`=`5`; `spellPowerPerLevel`=`1`; `castTime`=`60 - 5`.
- **Métodos no código:** `getUniqueInfo()`, `getCastTime()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `onCast()`, `onServerCastTick()`, `getDamage()`, `getDamageSource()`.
- **Fórmulas numéricas com retorno direto:** `getCastTime = castTime + 5 * spellLevel`; `getDamage = getSpellPower(spellLevel, caster) * .4f`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `SpellDamageSource`, `addFreshEntity`.

**Contrato de perks:** escola `fire` não certifica que todo dano/incêndio seja fire damage; verificar fonte de dano, duração de burning e entidades de projétil. Separar atributo de spell power nativo de mutações de área/contagem/efeito, que exigem hook específico, caps e world safety. Sem contrato comprovado: ⚠️ condicionado/fail-closed. RPG Skill Tree gerencia perks, Mastery e gates; Iron's mantém cast, mana e efeitos nativos; Black Arcana mantém seu runtime e WorldEffectPolicy para efeitos próprios. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
