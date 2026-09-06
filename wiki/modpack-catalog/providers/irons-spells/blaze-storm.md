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
