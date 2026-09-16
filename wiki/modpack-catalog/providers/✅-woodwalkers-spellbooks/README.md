# Woodwalkers SpellBooks — catálogo canônico

## Estado

- Mod ID: `woodwalkers_spellbooks`
- JAR instalado: `woodwalkers_spellbooks-0.3.1-BETA.jar`
- Versão instalada: `0.3.1-BETA`
- Runtime alvo: NeoForge 1.21.1
- Providers base: Iron's Spells 'n Spellbooks + Woodwalkers
- Source pin: `jo-devnull/woodwalkers-spellbooks@fd52733f6ba6e00028492ba1fa945f6a851de1fd` (`1.21.1`, `mod_version=0.3.1-BETA`)
- Catálogo: **1/1 spell ativo documentado**
- Estado de evidência: `SOURCE-PINNED 0.3.1-BETA / CATÁLOGO 1/1 COMPLETO / RUNTIME QA PENDENTE`

A release pública de 1.21.1 corresponde ao artefato instalado e o branch `1.21.1` do source declara a mesma versão. `SpellRegistry` contém exatamente um registration ativo.

## Inventário 1/1

1. [Shapeshifting](evocation/shapeshifting.md) — `woodwalkers_spellbooks:shapeshifting`

## Identidade mecânica

Woodwalkers SpellBooks não cria um segundo sistema de transformação. Ele injeta um spell de Evocation no pipeline do Iron's e delega a forma/segunda forma ao Woodwalkers por `PlayerShapeChanger`, `ShapeType`, `PlayerShape` e `PlayerDataProvider`.

O primeiro cast com alvo vivo pode registrar a forma secundária e transformar o jogador. Depois de a segunda forma existir, casts sem alvo reutilizam essa forma. A transformação temporária é marcada pelo effect `woodwalkers_spellbooks:shapeshifter`; duração, custo de XP e permissões são configuráveis em `woodwalkers-spellbooks.toml`.

## Defaults provider-native

- duração por spell level 1–6: `30 / 45 / 75 / 90 / 120 / 240 s`;
- custo em níveis de XP ao desbloquear forma: `6 / 5 / 4 / 3 / 2 / 1`;
- XP obrigatório em survival por padrão; desabilitado em creative por padrão;
- transformação infinita: desabilitada por padrão em survival e habilitada por padrão em creative;
- uso de outros spells enquanto transformado: desabilitado por padrão.

## Authority e deduplicação

- Iron's é authority de cast, mana, cooldown e spell level.
- Woodwalkers é authority de forma, entidade transformada, segunda forma e habilidades da forma.
- O addon é authority do XP gate, timer/effect e bloqueio global de spellcast enquanto transformado.
- Black Arcana não deve criar segundo ledger de formas, segundo timer de transformação, segundo debit de XP ou segundo cancelamento de spellcast.

## QA obrigatório

1. validar o source 0.3.1-BETA contra Iron's 3.16.3, pois o pin compila contra Iron's 3.15.6;
2. validar transformação/destransformação em dedicated server;
3. validar desbloqueio de forma e débito de XP uma única vez por cast válido;
4. validar duração 1–6 e modos Infinity Spell/creative;
5. validar o gate `Spells while Transformed` em `SpellPreCastEvent`;
6. validar targeting: pre-cast helper usa 16 blocos, enquanto o fallback raycast interno usa 32 blocos;
7. validar persistência/limpeza de segunda forma em morte, logout/login e troca de dimensão conforme authority do Woodwalkers.

Ver [TECHNICAL-AUDIT.md](TECHNICAL-AUDIT.md).
