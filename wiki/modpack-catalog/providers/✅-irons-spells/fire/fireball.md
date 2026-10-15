# Fireball

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Fire
- **Níveis:** 1–5
- **Raridade:** Rare → Legendary
- **Cast:** Long
- **Mana:** 60–120
- **Cooldown:** 25 s
- **Dano:** 10–30
- **Raio:** 3–7 blocos

## O que faz

Manifesta e arremessa uma bola de fogo que explode no impacto, causando dano elevado em área.

## Escalonamento

O catálogo atual confirma dano 10–30 e raio 3–7 blocos. Velocidade e falloff ficam `NÃO VERIFICADO`.

## World interaction

O changelog do rework registra que Fireball só pode quebrar ou incendiar blocos quando o `spellGriefing` do provider está habilitado; o padrão documentado desse sistema é não permitir spell griefing. Black Arcana não deve contornar nem duplicar essa authority por um pipeline paralelo.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação

Já cobre o arquétipo de grande projétil explosivo de fogo. Uma versão Black Arcana não é gap apenas por maior dano, cor ou raio.

## VFX / animação / áudio

O changelog confirma rework dos visuais de explosão na linha 3.1.0; a aparência final, animação e áudio no runtime real do pack ainda ficam `NÃO VERIFICADO` neste passe.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Changelog oficial: `https://iron.wiki/changelog/`
- Consulta: 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`FireballSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/fire/FireballSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:fireball` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `RARE`; maxLevel `5`; cooldown `25` segundos; cast `LONG`.
- **Campos Java:** `baseManaCost`=`60`; `manaCostPerLevel`=`15`; `baseSpellPower`=`1`; `spellPowerPerLevel`=`1`; `castTime`=`40`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `onCast()`, `getDamage()`, `getRadius()`.
- **Fórmulas numéricas com retorno direto:** `getDamage = 5 + 5 * getSpellPower(spellLevel, caster)`; `getRadius = 2 + (int) getSpellPower(spellLevel, caster)`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `addFreshEntity`, `Explosion`.

**Contrato de perks:** escola `fire` não certifica que todo dano/incêndio seja fire damage; verificar fonte de dano, duração de burning e entidades de projétil. Separar atributo de spell power nativo de mutações de área/contagem/efeito, que exigem hook específico, caps e world safety. Sem contrato comprovado: ⚠️ condicionado/fail-closed. RPG Skill Tree gerencia perks, Mastery e gates; Iron's mantém cast, mana e efeitos nativos; Black Arcana mantém seu runtime e WorldEffectPolicy para efeitos próprios. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).

## Mecânica confirmada — leitura causal do código-fonte

- **Controle explícito em `FireballSpell`:** `getDamage(level,caster) = 5 + 5*getSpellPower(level,caster)`; `getRadius(level,caster) = 2 + (int)getSpellPower(level,caster)`. `onCast` cria `MagicFireball`, configura `setDamage` e `setExplosionRadius`, posiciona perto dos olhos e atira na direção da mira. A entidade `MagicFireball` aplica a colisão/explosão; não há setter universal de raio acessível apenas por `SpellOnCastEvent` comprovado nesta análise.
- **Riscos de perks:** raio inteiro aumenta de forma discreta e o custo de efeitos em área não cresce linearmente; impor teto explícito em qualquer adapter e respeitar a política de mundo aplicável. Não confundir raio da explosão com alcance do projétil.

**Nível de prova:** inspeção do método do spell fixado no source 3.16.3; efeitos internos da entidade/projétil, possibilidade de patch por hooks externos e runtime Survival não validados.
