# Epic Fight 21.17.3.1 — cinemática delimitada do retorno de Everlasting Allegiance

**18/10/2026 · ✅ `EXACT_PUBLISHER_ORDERED_CONTIGUOUS_COMPILED_OPERANDS` · ⚠️ nenhuma trajetória real de jogador conectada/medida · ⛔ adaptação externa de velocidade, alcance ou Mastery.**

## Autoridade, artefato e reprodução

- Provider `epicfight`, release instalado no inventário histórico `21.17.3.1`, CurseForge projeto `405076` / arquivo `8175609`; JAR publisher validado pela pipeline Java 21 antes de `javap` com SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0` e SHA-256 `8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526`.
- [GitHub Actions #39103337112](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39103337112), job `exact_skill_parameters`: **SUCCESS**. O novo script registrou `PASS_EXACT_TRIDENT_RETURN_KINEMATICS_BOUNDED`, `deviations=[]`, com **8/8 autotestes**; os gates anteriores do mesmo workflow permaneceram aprovados.
- Artefato de evidências JSON **#12127228567**; [verificador SHA-gated read-only](../../../../docs/qa/epicfight_211731_trident_return_kinematics.py) e [workflow Java 21](../../../../.github/workflows/epicfight-211731-perk-binary.yml).
- O verificador confere **uma sequência contígua** de instruções e operandos no método compilado `ThrownTridentPatch.tickEnd()`: diferença de ticks, offset do olhar do proprietário, distância, potências e fatores, limites sucessivos, normalização do vetor, escala, zeragem da velocidade vetorial anterior e atualização de posição. Uma mutação sintética no atraso, coeficiente quadrático ou sequência de cálculos causa reprovação. Não valida fluxos de controle globais nem substitui GameTest.

## Cinemática sustentada pelo classfile exato

A ordem exata dos operandos no JAR 21.17.3.1 é compatível com a seguinte expressão:

```text
t = max(trident.tickCount - returnTick - 10, 0)
toOwner = owner.eyePosition() - trident.position()
distance = length(toOwner)
stepRequested = min(pow(t, 2.0) * 0.0005 + abs(t * 0.05),
                    min(10.0, distance))
direction = normalize(toOwner)
stepVector = direction * stepRequested
trident.setDeltaMovement(Vec3(0, 0, 0))
trident.setPos(previousPosition + stepVector)
```

| Campo útil para perks | Evidência exata | Cautela |
|---|---|---|
| Relógio da fase de retorno | `tickCount - returnTick - 10`, `Math.max(...,0)` | não é cooldown da skill, duração total nem cast time |
| Aceleração nominal | `pow(t,2)*0.0005 + abs(t*0.05)` | expressão de deslocamento solicitado, não velocidade medida em entidade real |
| Limite superior de cada atualização | `Math.min(10.0,distance)`, depois `Math.min(nominal,limite)` | teto nominal de **10 blocos por atualização**, não alcance máximo nem garantia de 10 blocos realmente percorridos |
| Direção | posição dos olhos do proprietário menos posição do tridente, `Vec3.normalize` | depende de proprietário e coordenadas válidas; sem ensaio de `null`, portal, dimensão ou alvo perdido |
| Aplicação | `setDeltaMovement(Vec3(0,0,0))` seguido de `setPos(position+direction*step)` | não demonstra que nenhuma outra física/mixin/tick ajusta a trajetória |

**Dedução limitada:** para valores finitos e distância não negativa, o comprimento solicitado é limitado superiormente por `min(10,distance)` neste ramo. O termo quadrático torna o deslocamento nominal crescente após o offset temporal; por si só isso não significa uma duração fixa ou garantia de captura. `tickCount - returnTick - 10` é um **offset no cálculo**, não prova de delay observado após o usuário ativar a skill.

O source público adjacente 21.17.3 do provider ([`ThrownTridentPatch.java`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/world/capabilities/projectile/ThrownTridentPatch.java)) oferece a mesma expressão; **neste caso específico** a sequência de operandos e operações foi certificada no JAR exato 21.17.3.1. Nenhum outro campo não testado do source adjacente foi automaticamente promovido.

## Separação entre alcance, área e dano

A prova anterior [`EXACT-TRIDENT-PHASE-OVERWRITE-RETURN-21.17.3.1.md`](EXACT-TRIDENT-PHASE-OVERWRITE-RETURN-21.17.3.1.md) confirmou `AABB.inflate(1,1,1)` como expansão **por eixo** da bounding box do tridente, e um `EpicFightDamageSource` construído independentemente do builder de fases com `HOLD`, `WEAPON_INNATE`, `setBaseArmorNegation(30)`, `ValueModifier.multiplier(1.4)` e input `8.0f` antes de encantamentos/mitigação. **Não** converter `AABB.inflate` em “raio esférico” e **não** interpretar o teto de 10 por atualização como alcance da skill.

Além disso, `EverlastingAllegiance.registerPropertiesToAnimation` é um método que retorna `this` sem escrever propriedades de `AttackAnimation.Phase`; alterações de `ARMOR_NEGATION_MODIFIER` no builder não provam modificações automáticas da source nativa criada dentro do patch do tridente.

## Implicações de integração e aceitação

- **Perks de velocidade/alcance:** a presença dessas constantes indica campos configurados internamente pelo provider, **não** uma API pública estável de modificação. Sem hook comprovado para alterar o movimento de forma segura, manter ⛔.
- **Mastery / repetição de dano:** o retorno, a varredura espacial e o dano são settlement de uma ação provider-owned. Nenhum novo cast deve ser registrado por tick de movimento, por entidade encontrada ou por `Entity.hurt` isolado.
- **Stage 09:** teste com cliente real e servidor exato precisa medir deslocamentos por tick e tempos de retorno em várias distâncias, interrompimentos e contato com entidades; também observar `ServerPlayerPatch.initialized`, consumo de `WEAPON_CHARGE` e `LivingDamageEvent.Post`. Nenhum desses resultados foi fornecido por `javap` ou pelo dedicated-server sem cliente.

**Estado do catálogo:** Epic Fight 43/43 IDs core catalogados (3/3 raízes sobrenaturais, 40 não mágicos para perks), +0 magias e +0 adapters. Global histórico mínimo 1.857 objetos semânticos / 1.855 estritos, denominador integral desconhecido (**—%**). Stage 06.05 🟡; Stage 09 físico ⚠️ PENDING; PR #825 draft, nenhum merge nesta auditoria.
