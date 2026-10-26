# Ars Nouveau — Rotate

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_rotate`
- Display name: Rotate
- School: Manipulation
- Default tier: 1
- Default mana cost: 10
- Compatible augments: Amplify, Sensitive, AOE, Pierce, Dampen, Randomize
- Default Sensitive limit: 1
- Default Randomize limit: 1

## Provider-native behavior

Rotate changes entity/block orientation. Amplification adds clockwise rotations; Dampen produces counter-clockwise rotation; Sensitive changes block axis where possible or forces entity look direction; Randomize selects arbitrary rotation. Projectile velocity is rotated alongside projectile orientation. AOE/Pierce expand block coverage.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this orientation/projectile-direction utility. Black Arcana should not duplicate generic rotation control or replay provider projectile movement.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectRotate`).

## Engenharia para perks — caminho causal individual

- **Código exato:** [`EffectRotate.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectRotate.java), Ars 5.13.1.
- **Entidades:** `counterClockwise` quando `(int)ampMultiplier<0`; laço `i<1+abs(ampMod)` gira 90° na direction escolhida ou angle aleatória `world.random.nextFloat()*360`. Sensitive afeta look; sem Sensitive define YRot; se `Projectile`, também altera delta vector por `rotateVec`.
- **Blocos:** `SpellUtil.calcAOEBlocks` gera candidatos; Randomize altera `AXIS` ou `FACING` quando propriedades existem e faz `state.rotate(...Rotation.getRandom)`; no determinístico aplica `1+abs(ampMod)` passos clockwise, mas quando counterClockwise o limite do loop é apenas `abs(ampMod)` (sem +1). Sensitive muda AXIS/FACING com switches especiais.
- **QA de matemática e claims:** `rotateVec` passa o parâmetro chamado `angle` diretamente a `Math.cos/Math.sin`, enquanto callsites geram ângulos 90/−90 ou valores 0..360. Como `Math.cos/sin` esperam radianos, isso é possível divergência de direção estática; exige teste físico para verificar comportamento real. `world.setBlockAndUpdate` por candidato não exibe claim gate local. Nenhuma correction ou exploit declarada.
- **Estado:** ✅ assinatura/source; ⚠️ integração de plugins proteção, configs e gameplay pending; ⛔ nenhum adapter RPG testado nem permissão para duplicar a cadeia causal/perk/mastery.

## Certificação técnica estática — Rotate (25/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** ID `ars_nouveau:glyph_rotate` ↔ `EffectRotate` fixado pelo JAR 5.13.1 SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` apenas quanto à classe/registro, **sem equivalência do bytecode dos métodos**. Fonte `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`: [EffectRotate.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectRotate.java).

| Eixo de perk | Caminho source-pinned e pontos não homologados |
|---|---|
| Entidades e quantidade | `onResolveEntity` usa `ampMod=(int)spellStats.getAmpMultiplier()`, `counterClockwise=ampMod<0`, `for(i=0;i<1+Math.abs(ampMod);i++)`: **pelo menos uma** tentativa de rotação por entidade, mesmo para amp0. Em modo normal usa `entity.rotate(CLOCKWISE_90/COUNTERCLOCKWISE_90)`; Randomize gera `world.random.nextFloat()*360` para `angle`. Sensitive aplica `entity.lookAt(Anchor.FEET,entity.position.add(entity.getLookAngle().yRot(angle)))`, caso contrário `entity.setYRot(angle)`. `entity.hurtMarked=true` ao fim de cada iteração. |
| Projéteis e unidades de ângulo | `entity instanceof Projectile` também altera `projectile.setDeltaMovement(rotateVec(vec3d,...))`; o método `rotateVec` calcula `Math.cos(angle)` e `Math.sin(angle)` **sem converter graus para radianos**. Callers transmitem `90`, `-90` ou `world.random.nextFloat()*360` como valor do mesmo parâmetro. Esta é uma **divergência de unidade no código inspecionado**, não prova de defeito reproduzido no JAR ou comportamento físico. Não desenhar perks que pressuponham giro exato de 90° na velocidade sem QA de bytecode/movimento. |
| Rotação de blocos | `onResolveBlock` usa `SpellUtil.calcAOEBlocks`, e itera cada `BlockState`. Em Randomize: modifica `BlockStateProperties.AXIS` ou `FACING`, se existentes, por `Axis.getRandom`/`Direction.getRandom`, depois chama `state.rotate(world,pos,Rotation.getRandom)`. Em determinístico, loop de rotações tem `(counterClockwise?0:1)+Math.abs(ampMod)`: diferente da fórmula de entidades; se amp0, há uma rotação clockwise. Sensitive alterna `AXIS` ou `FACING` por switches, sem Sensitive usa `state.rotate(...Rotation.CLOCKWISE_90/COUNTERCLOCKWISE_90)`. |
| Mutação sem verificação | Para **todo candidato** da lista, chama `world.setBlockAndUpdate(pos,state)` mesmo se properties/rotation não causaram mudança observável e **ignora boolean**; logo chama `ShapersFocus.tryPropagateBlockSpell(rayTraceResult,world,...)` usando **o hit original**, não um `BlockHitResult` gerado para `pos`. Não há `destroyRespectsClaim`, `world.isInWorldBounds` ou `BlockEvent.EntityPlaceEvent` **explícitos** em `EffectRotate`; não inferir ausência de outras policies do modpack, apenas falta de gate local. |
| Defaults e ownership | `getDefaultManaCost()=10`, Tier ONE, augments `Amplify`, `Sensitive`, `AOE`, `Pierce`, `Dampen`, `Randomize` (Sensitive e Randomize limite default1). Nada expõe hook de alteração de velocidade, dano, targeting ou escala por classe RPG. `WorldEffectPolicy` continua apenas para world effects próprios Black Arcana; resolver, transformações, efeitos e projéteis neste caminho são Ars. |

**QA pendente:** conferir radianos e trajetória de projectile no bytecode 5.13.1, Network interpolation/velocity, duração, BlockState sem AXIS/FACING, veto de claims/world bounds, retorno do `setBlockAndUpdate`, multiplas chamadas ShapersFocus em AOE, mundos protegidos, custo de mana e multiplayer. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Sem promoção de Stage 06.05/09.
