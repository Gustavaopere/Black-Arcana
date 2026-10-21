# Somake Spells 1.0.9 — Blood Cut: declaração de evento e rota de dano secundário

**Estado:** ✅ SHA_EXACT_ANNOTATION_AND_CALLSITES; ⚠️ filtros, configuração e gameplay; ⛔ perks mutadoras sem contrato real.

## Proveniência

- Registry: **somakespells:blood_cut**, uma das 83 identidades físicas da versão 1.0.9.
- CurseForge File **8867079**, JAR **somakespells-1.0.9-1.21.1.jar**, mod ID **somakespells** e SHA-1 físico/publicador **171841ac9f802be9309ecc166c1d972ac6d404c0**.
- [GitHub Actions Java 21 #39549751471](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39549751471): **SUCCESS**, hash conferido e **20 testes sintéticos** (7 de discovery + 9 Blood Cut + 4 de evento), sem executar Minecraft.
- Inspeção por [verificador](../../../../docs/qa/somake_109_blood_cut_event_gate.py), [testes](../../../../docs/qa/somake_109_blood_cut_event_gate_test.py) e [workflow](../../../../.github/workflows/somake-109-blood-cut-refs.yml).

## Anotações e fluxo exatos

| Superfície | Evidência compilada | Limite |
|---|---|---|
| Classe BloodCutEffect | RuntimeVisibleAnnotations: **net.neoforged.fml.common.EventBusSubscriber** | Anotação de inscrição declarativa; carregamento efetivo do servidor não foi observado |
| onLivingDamage(LivingDamageEvent.Post):void | RuntimeVisibleAnnotations: **net.neoforged.bus.api.SubscribeEvent** | Método anotado para consumir evento Post; despacho runtime ainda não testado |
| onLivingDamage | **103 instruções**, **5 desvios**: ifeq, ifeq, ifnull, ifne, goto | Predicados completos, short circuit e resultados ainda não certificados |
| getDamageModifier(int,LivingEntity):float | **19 instruções**, **2 desvios** e referência a BloodCutSpell.getEntityPowerMultiplier | Fórmula, ceiling, níveis e unidades ainda não comprovados |

Inspeção de anotação é prova de metadado binário, **não** homologação de API mutadora por jogador.

## Caminho de dano e referências verificadas

O classfile de BloodCutEffect contém um método de evento com referências a **LivingDamageEvent.Post.getNewDamage**, **LivingDamageEvent.Post.getSource**, **DamageSource.getEntity**, **LivingEntity.getEffect**, **MobEffectInstance.getAmplifier**, **BloodCutSpell.getDamageSource** e **DamageSources.applyDamage**. Uma chamada a applyDamage e uma a getNewDamage estão presentes no método compilado.

Na **ordem textual de callsites**, o acesso a getNewDamage antecede a construção do damage source de Blood Cut, que antecede applyDamage. Essa ordem **não prova** que todos os callsites sejam percorridos em cada evento: os desvios condicionais podem impedir o processamento.

O método também referencia entidades e partículas já documentadas no [dossiê original](registry-1.0.9/blood-cut-technical-gate.md). Nenhum valor efetivo de dano, redução, multiplicador, heal/lifesteal ou prioridade contra outros mods foi extraído desta auditoria.

## Implicações para perks e pendências

O mesmo método anotado para evento Post contém a aplicação potencial de novo dano. Antes de integrar perks do RPG Skill Tree, verificar filtros do damage source, caster e vítima, efeito ativo, proteção contra recursão/proc chains, multiplicador numérico, limites e identidade de acerto. Um trigger downstream não deve conceder Mastery/custo novamente sem correlação causal.

**QA pendente:** execução server/client/modpack, config host Iron's 3.16.3, eventos realmente despachados, aquisição Survival, proteção PvP/claims, multiplayer e restart. Nenhuma mutation hook per-player aprovada (⛔ FAIL_CLOSED).

**Autoridades:** Somake controla efeito específico; Iron's controla casting, custos, cooldowns e damage settlement; RPG Skill Tree fornece progressão/perks mediante contrato; Black Arcana não duplica o runtime externo.

**Progresso conservador:** +0 magias, +0 adapters; Somake **83/83 IDs**, **8/83** com métodos estáticos auditados no recorte, **5/83** no recorte aprofundado downstream anterior. Global **—%**, piso semântico **≥1.856**, denominador final aberto.


## Continuação — CFG normal e retorno de getDamageModifier (PR #859, 21/10/2026)

A [prova Java21 #39553030589](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39553030589) derivou o grafo normal do handler: **2 caminhos compilados para o único applyDamage / 3 sem passagem pelo callsite**, em **103 instruções** e **5 desvios**. Um intérprete de pilha independente derivou a fórmula de retorno do getter:

`((float)(a + 1) * (e != null ? BloodCutSpell.getEntityPowerMultiplier(e) : 1.0f)) * 0.1f`.

Esse valor é **o retorno do getter**, não o dano aplicado. Os parâmetros ainda exigem vínculo causal com os argumentos concretos de `onLivingDamage`, e os predicados dos guards não foram homologados. Ver [dossiê de CFG/float](EXACT-BINARY-BLOOD-CUT-CFG-MODIFIER-1.0.9.md). Sem hook, adapter, Stage promotion ou QA provider-loaded.

## Complemento causal exato — handler Post (PR #861)

O [novo gate Java21 #39599959888](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39599959888), com 73 testes sintéticos, provou a cadeia `DamageSource.getEntity` → `LivingEntity` → efeito `BLOOD_CUT` → amplificador → `getDamageModifier` → multiplicação por `getNewDamage`, além de `return` quando a origem do evento é `SpellDamageSource`. Isto melhora a avaliação de filtros de proc, mas não valida o destinatário/resultado final de `DamageSources.applyDamage` nem a interpretação do lifesteal. [Auditoria consolidada](EXACT-BINARY-BLOOD-CUT-CAUSAL-EVENT-1.0.9.md).
