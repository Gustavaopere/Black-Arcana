# RoarCommand — comandos de VFX, não cast mágico

**Classe:** `commands/RoarCommand.java`; registra `/roar` em `RegisterCommandsEvent` com requisito `source.hasPermission(2)`. **Tipo:** interface administrativa de debug/apresentação, não spell, evento de dano ou autorização de perks. **Estado:** ⚠️ source-pinned.

## Subcomandos, limites e defaults

| Rota | Target | Defaults do source | Argumentos aceitos |
|---|---|---|---|
| `/roar zoom <source>` ou `/roar zoom at <pos>` | Entidade(s) ou posição | strength 0.9; sharpness 0.6; duration 30; easing EASE_OUT_QUAD | strength 0..1, sharpness 0..8, duration 1..1200 |
| `/roar ring <source>` ou `/roar ring at <pos>` | Entidade(s) ou posição | radius 1.2; thickness 0.18; blur 0.3; refraction 0.12; duration 30 | radius 0..2, thickness 0.01..1, blur/refraction 0..0.5, duration 1..1200 |
| `/roar shake at <pos>` | Posição | radius 24; magnitude 1.6; duration 10 | radius 1..256, magnitude 0..20, duration 0..1200 |
| `/roar dome at <pos>` | Posição | radius 8; duration 200; cor `0xFF2020` | radius 0.5..128; duration 1..1200 |

Rotas zoom/ring despacham a `RoarHandler.trigger(Entity|ServerLevel, ...)`; shake a `ShakeHandler.trigger` com `new ShakeConfig(radius,magnitude,duration,10)`; dome a `DomeHandler.trigger` com `DomeConfig.of`. O último argumento `10` de ShakeConfig foi **observado**, mas sua interpretação semântica depende de documentação do tipo. A versão com entidades pode retornar a quantidade de fontes; a versão posicional retorna 1 após o dispatch.

## Segurança e integração

Raio de `ring`, raio de `dome` e alcance visual do `shake` **não** autorizam alteração de alcance/hitbox de magias. Permission level 2 se aplica a comandos, não valida permissões de perks. Esse caminho de VFX deve permanecer separado do pipeline server-authoritative de efeitos de Black Arcana e dos casts nativos do Iron's. Nenhum pacote visual indica acerto, gasto de recurso ou proc ofensivo.

**Fonte exata:** [`commands/RoarCommand.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/commands/RoarCommand.java).

**Proveniência:** AceTheEldritchKing/Aces_Spell_Utils @ `a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, source `1.2.7.2-1.21.1`. O catálogo físico referencia `aces_spell_utils-1.2.7.2-1.21.1.jar`, sem prova independente de paridade classfile. Build desta revisão usa Iron's `3.16.2`, versus pack `3.16.3`.

**Gate:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `COMPLETE_PERK_READY=false`. Não gera spell registrado, proc, atributo, perk ou adapter novo. Black Arcana preserva seu runtime mágico; Iron's controla casting/mana/cooldown dos seus spells; RPG Skill Tree controla progressão somente via contrato real.
