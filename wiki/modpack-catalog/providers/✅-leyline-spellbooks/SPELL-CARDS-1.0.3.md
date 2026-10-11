# Leyline Spellbooks — 14 fichas individuais de feitiços (1.0.3)

Estado: **✅ 14/14 identidades `COUNTED_EXACT` documentadas objeto a objeto**. Isto materializa registros **já contados** no catálogo, não cria feitiços novos.

## Fonte e limite da evidência

- **JAR da modlist física:** `leylines-1.0.3.jar`, Minecraft 1.21.1/NeoForge; `modId=leylines`.
- **SHA-1 físico/artefato publisher:** `dfa6908731f432905caaaa1e53b4aedeaa26ed59`; CurseForge project/file `1636676/8565076`.
- **Registry:** `dev.semeth.leylines.registry.LeySpellRegistry` contém 14 fornecedores de `AbstractSpell` incondicionais, todos com `DefaultConfig` da escola `leylines:ley`. A comparação foi encerrada no audit de release [exata](EXACT-1.0.3-ARTIFACT-AUDIT.md).
- **Proveniência das identidades:** [inventário exato com campo/classe/ID](EXACT-1.0.3-SPELL-INVENTORY.md). As nove fichas de assinatura pública foram reconciliadas; cinco registros ausentes da listagem pública agora possuem páginas.
- **Autoridade:** Leyline mantém spells, carga, portais, âncoras, rifts e progressão; Iron's mantém casting, mana/cooldown genéricos. Nenhuma segunda execução é atribuída ao Black Arcana.
- **Gate documentado:** não existe spell lock próprio detectado; a escola tem `requiresLearning=false` e `allowLooting=true` nos contratos exatos já auditados de Iron's 3.16.3. Config real, loot modificado, drop e aquisição em Survival ainda exigem verificação direta.

## Índice de identidades exatas

| # | Registro | Campo no registry | Classe exata | Ficha individual |
|---:|---|---|---|---|
| 1 | `leylines:charge_leyline` | `CHARGE_LEYLINE` | `ChargeLeylineSpell` | [Charge Leyline](spells/charge-leyline.md) |
| 2 | `leylines:blink_step` | `BLINK_STEP` | `BlinkStepSpell` | [Blink Step](spells/blink-step.md) |
| 3 | `leylines:beam` | `BEAM` | `BeamSpell` | [Beam](spells/beam.md) |
| 4 | `leylines:tether_gaze` | `TETHER_GAZE` | `TetherGazeSpell` | [Tether Gaze](spells/tether-gaze.md) |
| 5 | `leylines:ley_veil` | `LEY_VEIL` | `LeyVeilSpell` | [Ley Veil](spells/ley-veil.md) |
| 6 | `leylines:leyline_discharge` | `LEYLINE_DISCHARGE` | `LeylineDischargeSpell` | [Leyline Discharge](spells/leyline-discharge.md) |
| 7 | `leylines:ley_blast` | `LEY_BLAST` | `LeyBlastSpell` | [Ley Blast](spells/ley-blast.md) |
| 8 | `leylines:ley_eclipse` | `LEY_ECLIPSE` | `LeyEclipseSpell` | [Eclipse](spells/eclipse.md) |
| 9 | `leylines:ley_resonance` | `LEY_RESONANCE` | `LeyResonanceSpell` | [Ley Resonance](spells/ley-resonance.md) |
| 10 | `leylines:rift_gate` | `RIFT_GATE` | `RiftGateSpell` | [Rift Gate](spells/rift-gate.md) |
| 11 | `leylines:chrono_tether` | `CHRONO_TETHER` | `ChronoTetherSpell` | [Chrono Tether](spells/chrono-tether.md) |
| 12 | `leylines:fissure` | `FISSURE` | `FissureSpell` | [Fissure](spells/fissure.md) |
| 13 | `leylines:temporal_stutter` | `TEMPORAL_STUTTER` | `TemporalStutterSpell` | [Temporal Stutter](spells/temporal-stutter.md) |
| 14 | `leylines:anchor_recall` | `ANCHOR_RECALL` | `AnchorRecallSpell` | [Anchor Recall](spells/anchor-recall.md) |

## Deduplicação e pendências

- Exatamente **14 IDs e 14 classes do registry**, nenhum segundo registro criado a partir de efeitos, projeto-page, scrolls, focus, escola, Codex, staff ou loot.
- A lista pública original de nove nomes não era exaustiva. Os cinco extras na auditoria binária são `charge_leyline`, `tether_gaze`, `ley_veil`, `leyline_discharge`, `ley_resonance`.
- `charge_leyline` tem rota de loot de scroll nível 1 no JAR exato; para os demais a via genérica Iron's é somente elegibilidade de catálogo, sem confirmação de drop efetivo.
- O custo numérico, níveis, cooldown, targeting preciso, efeitos, interação de cargas, PvP, compatibilidade exata e aquisição efetiva não são inferidos de classe, nome ou defaults.
- **Total semântico neste trabalho: +0**. Permanecem os mínimos globais documentados **1.851 / 1.849 no escopo solicitado**, com denominador final aberto.
- O runtime segue **⚠️ QA condicionado**: configurações implantadas, observação em Survival, API de integração, persistência/portais e multiplayer. A etapa 06.05 não é promovida por esta catalogação.

Inspeção clean-room: não copiar implementação, resources, assets ou descrição criativa upstream sem licença apropriada.
