# Ars Nouveau 5.13.1 — quatro Effects: blocos temporários, luz, redstone e rotação

**Escopo:** certificações `STATIC_TECHNICAL_CATALOG_ONLY` para `Conjure Mageblock`, `Conjure Magelight`, `Redstone Signal` e `Rotate`. Nenhum runtime ou Stage alterado; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`.

## Autoridades e proveniência

- Modlist física no sibling RPG Skill Tree: Minecraft 1.21.1, `ars_nouveau-1.21.1-5.13.1.jar`, mod ID `ars_nouveau`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`.
- Código de referência imutável `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`.
- Identidades binárias dos 109 itens: [manifesto classe/ID](EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). A identidade **não** verifica bytecode de corpo do método, callbacks de terceiros, config carregada nem comportamento provider-live.

| Ficha | Mutação e consumidor source-pinned | Gate antes de implementação de perk |
|---|---|---|
| [Conjure Mageblock](glyphs/effects/conjure-mageblock.md): `EffectPhantomBlock` | `glyph_phantom_block`: AOE/Pierce, hit-face translation, `destroyRespectsClaim`, `MageBlock.TEMPORARY=!Amplify`. `MageBlockTile` persiste `age/permanent/modifier/lightColor`; expiração `age>300+100*lengthModifier` em game ticks processados | Placement `setBlockAndUpdate` sem retorno conferido; apenas `MageBlockTile` encontrado autoriza configuração e `ShapersFocus`; não inferir timer em wall-clock ou mutator Amplify. |
| [Conjure Magelight](glyphs/effects/conjure-magelight.md): `EffectLight` | `glyph_light`: `ILightable`, `NIGHT_VISION`, `GLOWING` e `PacketUpdateGlowColor` condicionais; bloco `LIGHT_BLOCK` se duração0 e `T_LIGHT_BLOCK` se não0; `WATERLOGGED` e `SconceBlock.LIGHT_LEVEL` clamped0..15. `TempLightTile` salva `age/modifier` e usa `age>300+100*modifier` | Claim feito na face/destino mesmo quando `ILightable` atua no bloco original; sign update não encerra o método. `setBlockAndUpdate` retorno ignorado; não confundir potions em entidade com lifetime do bloco. |
| [Redstone Signal](glyphs/effects/redstone-signal.md): `EffectRedstone` | `glyph_redstone_signal`: power=`clamp((int)AMP+10,1,15)`, delay=`max(base5+(int)duration*bonus10,2)`. Sensitive grava `RedstoneSavedData.SIGNAL_MAP` e notifica vizinhos; normal coloca `TemporaryBlock` após `EntityPlaceEvent` | **Sem EntityPlaceEvent ou destroyRespectsClaim locais no Sensitive**. `RedstoneSavedData` pausa ticks em chunks não carregados e sobrescreve mesmo pos; `TemporaryTile` usa prazo absoluto `gameTime+tickDuration`. Não equiparar durações nem criar segunda ledger BA. |
| [Rotate](glyphs/effects/rotate.md): `EffectRotate` | `glyph_rotate`: entidade `1+abs(ampMod)` voltas; bloco determinístico `(counterClockwise?0:1)+abs(ampMod)`; Randomize usa AXIS/FACING e Rotations. Em projéteis, `rotateVec` usa `Math.cos/sin(angle)` recebendo valores 90/−90 ou 0..360 | Divergência estática **graus vs radianos** exige QA de bytecode/trajectory; `setBlockAndUpdate` sem retorno checado, `ShapersFocus` acionado pelo hit original e sem preflight de claim explícito. |

## Contratos comuns

1. **Custo/tempos:** defaults de mana Mageblock **5**, Magelight **25**, Redstone **0**, Rotate **10**; são defaults, não custo de cast real. `MageBlockTile` e `TempLightTile` expiram por contagem incrementada somente em server ticks disponíveis, enquanto `TemporaryTile` expira ao comparar relógio de nível; `RedstoneSavedData.Entry` persiste remaining `ticks` com pausa unloaded e decrementa apenas para posições carregadas. Não projetar perks de duração supondo uma unidade universal.
2. **World authority:** Ars é proprietário de `MageBlockTile`, `TempLightTile`, `TemporaryTile`, `RedstoneSavedData`, color packets e callbacks de caster. `WorldEffectPolicy` do Black Arcana rege **somente** efeitos próprios BA, não intercepta nativamente o Ars.
3. **Progressão:** RPG Skill Tree fornece atributos, Mastery, perks e gates somente por boundary real, sem redefinir persistência nem reexecutar efeitos nativos. Nenhum `EffectResolveEvent.Pre` prova sozinho um hook seguro de alterar essas classes ou o resultado de setters.
4. **Safety:** validar claims, colisor e bounds na posição efetiva, callbacks de outros mods, `setBlockAndUpdate` falso, lado servidor, intensidade e volume de AOE, chunks, save/restart e duplicação de notificações.
5. **Stage 06.05/09:** não promovidos. Nenhum JAR modificado ou conteúdo proprietário transplantado; clean-room de referência e interoperabilidade.

**Contadores previstos após CI+merge:** Effects **51/67**, Glyphs **69/85**, Ars **93/138**, global **93/2075**, providers integralmente certificados **0/164**. Recorte limitado às fichas candidatas existentes.
