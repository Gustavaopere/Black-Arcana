# Goety 3.1.4 — Fire Breath, Frost Nova e Electrocute: ABI exata e semântica source-adjacent

**Registro:** 27/10/2026
**Classificação:** ⚠️ `COUNTED_EXACT + EXACT_ABI_SYMBOLIC_ONLY + SOURCE_ADJACENT_311 / PHYSICAL_QA_NOT_TESTED`.
**Escopo:** três Focuses existentes no inventário exato de **123** Focuses Goety; não são três ações novas. Adapters, perk runtime e certificação continuam ⛔ **fail-closed**.

## Evidência e distinção entre versões

- **JAR instalado:** `goety-3.1.4.jar`, mod ID `goety`, Minecraft/NeoForge 1.21.1, CurseForge project/file `586095/8689429`, SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`. Identidades `fire_breath_focus`, `frost_nova_focus` e `electrocute_focus` demonstradas no [inventário exato do provider](EXACT-3.1.4-SEMANTIC-INVENTORY.md).
- **Novo probe binário:** [GitHub Actions #40498956210](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40498956210), job `122171486356`, `completed/success`, SHA-1 validado por `sha1sum -c` e sete classes-alvo encontradas.
- **Evidência textual:** artifact `goety-314-three-combat-focus-abi`, ID `12731937460`, digest `sha256:d1eb7ed7463fe04f71a58648b8d4b874c9a4723d4e17a9e81f4a79dc96aa3697`, retenção programada de 30 dias. Relatório produzido por símbolos/`javap`, **sem preservar corpo de método, operandos, branches, valores de constantes nem assets**.
- **Probe temporário, não-mergeável:** branch `audit/goety-314-three-combat-focuses-20261027`, HEAD `9fa180052ed31ea54e1f6c504e636077d0f566a4`, workflow `.github/workflows/goety-314-combat-focus-abi-temporary.yml`. Ele **não** entra na `main`.
- **Fonte semântica apenas adjacente:** repositório [`Vivideru/Goety-3@6c41a04f2d712097c4461f969a6bb8ee277149ef`](https://github.com/Vivideru/Goety-3/commit/6c41a04f2d712097c4461f969a6bb8ee277149ef), versão pública 3.1.1. Números, rotas de branch, fórmulas, inventário de efeitos, weather, condições e flags citados nas fichas **pertencem a essa revisão**. **Nenhuma equivalência com a semântica efetiva do JAR 3.1.4 foi inferida de nomes iguais de classe.**

## Matriz de ABI exata verificada — classfile 3.1.4

| Área | Métodos e relações de invocação comprovados no binário | Não demonstrado |
|---|---|---|
| **Fire Breath** | `FireBreathSpell.SpellResult` referencia `SpellStat.getRange`, `FireBreathSpell.baseDamage`, `getBreathTarget`, `ModDamageSource.fireBreath`, `magicFireBreath`, `Entity.hurt`, `Entity.igniteForSeconds`, `BaseFireBlock.getState` e **`ServerLevel.setBlockAndUpdate`**. `conditionsMet` referencia `Mob.getTarget`. `showWandBreath` existe. | Condições dos ramos, check de proteção, permissões, config efetiva, dano/range/cadência, bloqueios de aliados e mundo, alteração concreta no servidor. |
| **Breath comum** | `BreathingSpell` e `IBreathingSpell` existem; `IBreathingSpell.getBreathTarget` referencia `MobUtil.getTargets`. | Contrato de alvo em 3.1.4, filtragem PvP, grau de cone, frequência de calls por tick e autoria causal. |
| **Frost Nova** | `FrostNovaSpell.SpellResult` referencia `SpellStat.getRadius/getDuration`, `FrostNovaSpell.getTarget`, `ModAttributes.getCooldownDiscount` e **`SEHelper.addCooldown`**. `hasCustomCooldown` e `createParticleBall` presentes. | Fórmula do desconto, override real, método de dano, target shift, duração de freeze, quantidade de vítimas, duplicação de cooldown; `SpellExplosion` e hooks internos exigem prova própria. |
| **Electrocute / Electro Orb** | `ElectroOrbSpell.SpellResult` referencia `SpellStat.getRange`, `getTarget` e `ElectroOrb.setPos`, `setExtraDamage`, **`setStaff`**, `shoot` e **`ServerLevel.addFreshEntity`**. Classe `ElectroOrb` existe. | Mapeamento registry item→classe pelo ModItems exato não foi inspecionado nesta auditoria; fonte 3.1.1 faz essa ligação e JAR confirma identidade do Focus separadamente. |
| **Impacto Electro Orb** | `ElectroOrb.onHit` referencia `Entity.hurt`, `ElectroOrb.finalizeExplosion`, `getExtraDamage`; `finalizeExplosion` referencia `ElectroOrb.isStaff`; `tick` referencia `getTargetingVec`; `getDefaultGravity` referencia `getTarget`. | Homing, física, explosão, cadeia elétrica, chuvas, efeitos, filtros de alvo e dano final. O `SpellExplosion` anônimo/inner class não foi auditado nesta execução. |

**Atenção:** “referencia” significa que há **call-site estático** no classfile. Uma chamada pode pertencer a um ramo nunca executado em determinado cast. O teste de ABI não é GameTest de conjuração no modpack, não confirma o estado de `Soul Energy` e não certifica API mutadora.

## Dependências e riscos de design para perks

**Fire Breath:** a presença de `ServerLevel.setBlockAndUpdate` no corpo de `SpellResult` é uma superfície **potencial** de efeito persistente no mundo do **Goety**, não do Black Arcana. A fonte 3.1.1 condiciona o caminho a `RING_OF_THE_DRAGON` + `DragonFireGriefing`; confirmar condições/claims no 3.1.4 em dedicated server. **Não declarar o WorldEffectPolicy Black Arcana como tendo validado blocos alterados pelo provider.** Não oferecer perk de fogo no mundo enquanto esse contrato estiver desconhecido.

**Frost Nova:** o binário possui um caminho `SEHelper.addCooldown` interno ao resultado da spell e uma função `hasCustomCooldown`. A fonte adjacente 3.1.1 descreve modo centralizado no caster versus alvo ao agachar, com cooldown distinto. **Evitar que RPG Skill Tree ou Black Arcana registrem segundo cooldown ou contem uma nova conjuração ao aplicar debuff em múltiplos alvos.** Não concluir bug de multiplicação/arredondamento sem comparação binária das fórmulas e teste de saldo.

**Electrocute:** a fonte 3.1.1 usa `ElectroOrbSpell` para `electrocute_focus`, e `ElectroOrb` carrega hit direto, explosão condicional de staff e cadeias elétricas indiretas; são consumers e eventos causais separados. O probe 3.1.4 confirmou o caminho de spawn e impacto básicos; **não** confirmou quantidade de chains nem imunidade/ownership. **Perks de multi-shot, projétil maior, chain count ou status devem ser bloqueadas até deduplicação e orçamento de alvos.**

## Matriz de aceitação necessária (não executada)

1. **Binário/registry:** confirmar construção `ModItems` e referência exata `MagicFocus(new …Spell())` para os três itens; comparar config ativa/encantamentos/SpellStat do JAR 3.1.4.
2. **Fire Breath:** canalização e desconto per-second, início/interrupção, Ring of Dragon presente/ausente, `DragonFireGriefing` false/true, claims/proteções, survival/dedicated server, desgaste/fogo residual, PVP/aliados, budgets.
3. **Frost Nova:** blast centrado no caster e alvo, shift, duração e imunidade de freeze, geometria real, staff alternativo, cooldown custom e desconto, efeitos/morte durante cast, custo único.
4. **Electro Orb:** projétil sem alvo/com target, addon/staff, owner e aliados, colisão em bloco e em entidade, rain/thunder, cadeia elétrica, proc counts, persistência/reload, cap de perfuração/chain e segurança do mundo.
5. **Integração:** perfilar um cast provider-native e seus efeitos; não inferir Mastery de partículas, spawn, dano ou debuff simultaneamente. Sem hook causal verificado, **`mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, ⛔ fail-closed**.

**Autoridade:** o Goety mantém `Soul Energy`, casting, Focus, entidades e seus efeitos; o RPG Skill Tree fornece progressão/perks apenas por contrato real, e o Black Arcana não duplica recursos, casts ou WorldEffectPolicy de terceiros. **Nenhuma das sete evidências de certificação estrita foi preenchida com estes probes parciais.** Goety permanece **0/361** certificados e o [índice global](../INDEX.md) tinha **138/2075** certificados antes desta entrega; nenhum índice, manifesto `PERK-READY-CERTIFICATIONS.json`, runtime ou Stage foi alterado.
