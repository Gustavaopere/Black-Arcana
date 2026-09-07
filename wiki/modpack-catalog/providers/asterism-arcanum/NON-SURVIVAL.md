# Conteúdo registrado fora do survival — Asterism Arcanum 0.1.0

## Astral Gateway

- ID: `asterismarcanum:astral_gateway`
- escola: Astral
- rarity: Legendary
- nível: 1
- mana: 300
- cooldown: 60 s
- cast: LONG, 40 ticks / 2 s, sem cast-time scaling
- radius: 8
- registry: **ativo**
- survival: **não aprovado**

O lang file da release descreve explicitamente o spell como `not fully implemented or craftable`, e a release o trata como creative-only. A classe transporta o ServerPlayer entre a dimensão Astral Sea e seu destino de retorno.

### Inconsistência de aquisição

A classe não sobrescreve `allowLooting()` e seu `DefaultConfig` não desabilita crafting. A escola Astral usa defaults `allowLooting=true`; o Astromancer gera scrolls aleatórios filtrados apenas pela escola. No Iron's 3.16.3 do pack, isso cria caminho estático para Gateway aparecer em loot/crafting se nenhum config/datapack adicional o bloquear.

**Black Arcana: fail-closed.** Não promover Gateway para a progressão canônica, não criar perk que dependa dele e não adicionar fonte de aquisição.

## Trailblaze

`TrailblazeSpell` existe no source 0.1.0, mas o registration em `ASARSpellRegistry` está comentado. Não é spell de runtime e não recebe ficha individual.