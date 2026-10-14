# Apprentice's Codex 0.9.7.1 — engenharia causal: magia persistente, combate e mundo

**Checkpoint:** 2026-10-14. **✅ 83/83 identidades source-catalogadas**, **🟡 34/83 dossiês aprofundados** (6 do catálogo anterior + 8 no [lote de alto risco](PERK-ENGINEERING-MATRIX-HIGH-RISK-0.9.7.1.md) + 10 no [lote de lifecycle](PERK-ENGINEERING-MATRIX-LIFECYCLE-0.9.7.1.md) + **10 neste lote**). **49/83** ainda carecem de engenharia causal de mesma profundidade. **+0** raízes semânticas.

**Modlist atual:** sibling `Gustavaopere/neoforge-rpg-skilltree/main@82d7b7a8d15ab96ed7c59cc0c3e870edfe02cf4d` no arquivo `PROJECT-INSTRUCTIONS/modlist/Addons + Armor, Tools, and Weapons + Magic/✅-apprentices-codex v0.9.7.1.md`, JAR `apprentice_codex-0.9.7.1+mc1.21.1.jar`, mod ID `apprenticecodex`, SHA-1 `b514315add32b93b0049c8673075627d7ef812e0`. **Fonte de mecanismos:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` declarado 0.9.7.1. **⚠️ Não equivale** a uma prova de bytecode corpo-a-corpo, configuração física ou teste no jogo instalado.

| Identidade da spell | Dossiê source-localizado | Classe/métodos verificados | Contrato e risco importante |
|---|---|---|---|
| `apprenticecodex:assist_wings` | [assist_wings](ender/assist-wings.md) | `AssistWings.onCast; AssistWingsWingEntity.tickOnServer` | DoneJump, broom gate, 10 ticks grace e item-tag que condiciona fall protection |
| `apprenticecodex:manifestation_grimoire` | [manifestation_grimoire](ender/manifestation-grimoire.md) | `ManifestationGrimoire.onCast` | ItemEntity Ender Grimoire com pickup delay 20 e partícula server-only |
| `apprenticecodex:bullet_stream` | [bullet_stream](lightning/bullet-stream.md) | `BulletStreamMinigunEntity.tickOnServer/fire/releaseWeapon` | Raycast de mira ≠ raycast de dano; channel tick ≠ cast novo |
| `apprenticecodex:healing_bloom` | [healing_bloom](nature/healing-bloom.md) | `HealingBloomManager.getManagedBloomUuid; HealingBloomEntity.tickOnServer` | Entity UUID, regen/undead/luz e reconciliação de unload |
| `apprenticecodex:heavenly_fist` | [heavenly_fist](nature/heavenly-fist.md) | `HeavenlyFistFistEntity.impact; HeavenlyFistPressingProcessor.processItems` | Um impacto: dano, pressing/Create opcional, crystal harvest e partículas |
| `apprenticecodex:edge_dancer` | [edge_dancer](evocation/edge-dancer.md) | `EdgeDancerManager.activate/deactivate/validateActiveMirrorLocation` | UUID mirror, offhand e recast Iron's mutuamente exclusivos |
| `apprenticecodex:world_flatter` | [world_flatter](nature/world-flatter.md) | `WorldFlatterDrillEntity.processBlockBreak/collectBreakableBlocks` | Plano de até 9 blocos, hardness e break by player hands |
| `apprenticecodex:divine_possession` | [divine_possession](holy/divine-possession.md) | `DivinePossession.canBeCastedBy/onCast` | Quatro slots Element Maiden Robe; MobEffect sem mana paralela |
| `apprenticecodex:otherworld_lens` | [otherworld_lens](eldritch/otherworld-lens.md) | `OtherworldLensTargetSafety.validate; OtherworldLensSessionManager.start/finish` | Raycast server validado, sessão em memória e cleanup de lens block |
| `apprenticecodex:totem_of_permafrost` | [totem_of_permafrost](ice/totem-of-permafrost.md) | `TotemOfPermafrostTotemEntity.tickOnServer/pulse` | Pulso 15 ticks, owner + LOS, freeze apenas após dano aplicado |

## Conclusões condicionadas à versão de source (sem generalizar para o runtime físico)

- **Summons e inventário:** Assist Wings e Edge Dancer mantêm estado por owner/UUID de entidade ou item, exigindo limpeza cuidadosa; Manifestation Grimoire instancia ItemEntity, não um segundo cast independente quando alguém usa o item gerado.
- **Efeitos por tick:** Bullet Stream tem raycast para mira a 64 e outro com `range` para hit; Healing Bloom pulsa regen/undead, produz frutos, ocupa posição e cria luz local; Totem of Permafrost aplica freeze/slowness somente quando `CombatTools.applyDamage` foi bem-sucedido. Nenhum timer/visuais constitui uma raiz adicional.
- **World effects:** World Flatter revalida estado/tool a cada bloco num plano máximo 3×3 e usa `BlockTools.breakBlockByPlayerHands` do provider; Otherworld Lens revalida block target com raycast server e mantém uma sessão em mapas locais, apagando o próprio bloco na limpeza. Checagens de bloco **não comprovam** proteção integral contra claims nem autorizam BA a executar os efeitos.
- **Combate e addons:** Heavenly Fist faz dano, pressing de item e Crystal Harvest em um impacto. A integração com Create usa caminhos de receita específicos e pode estar desabilitada. Divine Possession depende das peças exatas de `ElementMaidenRobeItem`; outros efeitos derivados dependem de `DIVINE_POSSESSION` no host, não de uma segunda cast pipeline.
- **Authority e adapters:** Iron's governa school, mana e casting base; Apprentice's governa suas entidades, inventários e efeitos; Black Arcana governa **somente seu runtime mágico**. RPG Skill Tree provê Mastery/atributos/perks exclusivamente via contratos reais. Sem hook real **⛔ fail-closed**. Runtime/Stage 06.05 inalterados.
- **QA ainda ⚠️:** full modpack dedicated/client, bytecode do JAR, configurações, survival/multiplayer, proteção de terrenos, NBT/unload/relog, ataques PvP, interferência de equipamentos/efeitos, retentativas e budget de tarefas.

**Escopo da mudança:** 10 fichas anteriores ampliadas + esta matriz + README do provider + ledger global = 13 Markdown e 0 Java; sem mudança de contagem global de magias.

[Registry 83/83](README.md) · [Ledger global](../../meta/PERK-READY-COVERAGE-LEDGER.md) · [Padrão técnico](../../meta/PERK-READY-TECHNICAL-STANDARD.md).
