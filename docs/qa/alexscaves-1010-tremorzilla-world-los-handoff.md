# Handoff — Tremorzilla Beam: geometria, LOS e efeitos de mundo no publisher 1.0.10

**Escopo:** evidência de ABI/JVM **somente estática** e limitada, para incorporação ao contrato principal de `damage-types/tremorzilla-beam.md` pelo trabalho alfabético. Não altera essa ficha, os contadores, a execução de Black Arcana nem a autoridade do provider.

## Proveniência e reprodutibilidade

- Modlist atual do sibling `neoforge-rpg-skilltree/main@59ff2a0e827fd08faa603f4482f8104ac433383c`: `Alex's Caves Continued 1.0.10`.
- Publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`: SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes.
- `TremorzillaEntity.class`: SHA-256 `e1ac60a8005f9414dde1d25a92a2110df65cef145c3225e9c2557c96672fe8dc`; 116 métodos compilados.
- Manifesto estrito: [EXACT-TREMORZILLA-WORLD-LOS-1.0.10.json](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-TREMORZILLA-WORLD-LOS-1.0.10.json). Sonda [read-only](alexscaves_1010_tremorzilla_world_los_probe.py) e [regressões sintéticas](alexscaves_1010_tremorzilla_world_los_probe_test.py).
- Proveniência de execução: [GitHub Actions — workflow dedicado](../../.github/workflows/alexscaves-1010-tremorzilla-world-los.yml). Só os métodos da versão instalada são selados; a fonte pública de outras versões não substitui o binário.

## Caminhos observados, sem inferir semântica além dos offsets

| Superfície | Localização JVM 1.0.10 | Fato comprovado | Não comprovado |
|---|---|---|---|
| Lado lógico | `tickBreath: Level.isClientSide @4` | Existe consulta do lado | Exatidão dos efeitos em execução física, thread e modpack transformado |
| Segmento / ponto final | `tickBreath: beamServerTarget @338/@352`, `getBeamShootFrom @346`, `ClipContext.Block.COLLIDER @383`, `Fluid.NONE @386`, `Level.clip @393` | Rota compilada de colisão por blocos e ponto inicial de disparo | Alcance e geometria efetiva após overrides, cargas e outros mods |
| Ocultação/linha de visão de alvo | `canEntityBeHurtByBeam: COLLIDER @27`, `NONE @30`, `Level.clip @37`, `BlockHitResult.getType @40` | Critério nativo consulta resultado do raycast; função separada da seleção AABB | Resultado de todos os caminhos, exceções, cliente real, proteção PvP |
| Varredura/dano | `tickBreath: getMaxBeamBreakLength @459`, `hurtEntitiesAround @552/@578` | Dois callsites nativos de seleção de entidades/causa de dano | Quantidade final de acertos ou duplicação; o `20.0f @545/@571` é operando de dano solicitado, **não** dano garantido |
| Controle de devastação | `ACServerConfig.devastatingTremorzillaBeam @494/@585`, `breakBlocksAround @525/@620` | Condição de config observada próxima a dois callsites de mutação | Efeito integral do toggle, todos os guards e proteção de terceiros |
| Permissão de griefing | `breakBlocksAround: ACPlatform.canEntityGrief @12`, `Level.isClientSide @22` | Helper possui consulta ao provider e ao lado lógico | Se o guard preserva **todos** claims, policies ou proteções do modpack |
| Seleção de blocos | `BlockPos.betweenClosed @93`, `getBlockState @131`, `getExplosionResistance @178`, `distToCenterSqr @211` | Iteração em posições, análise de estado e resistência | Raio/forma/filtragem final, chunks não carregados, cardinalidade de trabalho |
| Mutação de mundo | `Level.destroyBlock @249`, `ACCompat.onBlockExploded @268` | Existe uma rota nativa destrutiva com callback compatível | Aplicação de `WorldEffectPolicy` do Black Arcana, segurança de claims e rollback |
| Entidade adicional | `ACCompat.createEntity @296`, `NuclearBombEntity.setTime @340`, `Level.addFreshEntity @349` | Existe referência compilada à criação de uma entidade nuclear, incluindo argumento literal `300 @337` | Frequência, condições de disparo, identidade/permissão da entidade e efeito explosivo resultante |
| Alteração do comprimento | `getMaxBeamBreakLength @632`, literal `5.0d @635`, `setMaxBeamBreakLength @643` | Comprimento dinâmico é lido e escrito no provider durante `tickBreath` | Regra global de alcance e setter seguro para perks |

O feixe e o pisão/corpo **não devem compartilhar perk de dano por identidade presumida**. A prova anterior [EXACT-TREMORZILLA-BEAM-1.0.10.json](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-TREMORZILLA-BEAM-1.0.10.json) mostrou `tickBreath` usando o ramo `causeTremorzillaBeamDamage`, e outros chamadores do helper usando `mobAttack`. Esta auditoria acrescenta o recorte de mundo e LOS sem reaproveitar esse certificado como autorização de mutação.

## Limites de integração

1. **Dano e alvo:** a futura perk deve operar apenas por um boundary real verificado do provider; não criar outro `hurt()`, outro proc, outra atribuição de kill/XP ou repetir `Irradiated`.
2. **Geometria e duração:** inspecionar o CFG completo de `tickBreath`/`tickBeamTargeting`, `getMaxBeamBreakLength` e campos `beamTime`/`maxBeamTime` antes de expor raio, extensão, tick-rate, charge ou cooldown ao RPG Skill Tree.
3. **Efeitos destrutivos:** nenhuma perk deve amplificar `breakBlocksAround`, entidade nuclear ou explosões enquanto não houver prova de limites de trabalho, carregamento de chunks, proteções de terceiros e conformidade aplicável à `WorldEffectPolicy` de Black Arcana.
4. **Interprocedural e físico:** verificar `ACPlatform.canEntityGrief`, `ACCompat.onBlockExploded`, `ACCompat.createEntity` e a execução da classe efetivamente carregada com ModLauncher/modpack, em servidor dedicado e cliente real.

**Estado:** ⚠️ `STATIC_BYTECODE_OBSERVED_ONLY`; `NOT_CERTIFIED`; `NO_MUTATION`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Esta PR não promove o Tremorzilla a ✅, não atualiza os índices de 28/30 ou 166/2342, não fecha Stage e não substitui o trabalho do Codex.
