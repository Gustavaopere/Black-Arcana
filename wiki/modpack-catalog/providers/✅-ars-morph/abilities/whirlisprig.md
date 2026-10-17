# Whirlisprig — Ars Morph 2.0.0 / Identity2 ability

**Status: ✅ fonte por habilidade documentada · ⚠️ runtime e JAR físico pendentes · ⛔ perks sem contrato homologado.** Habilidade provider-native Identity2; NÃO constitui novo glifo, cast root Black Arcana ou forma independente de mana. `ars_morph-1.21.1-2.0.0.jar` SHA-1 físico documentado `68ff47cc58c0ffe9570bb907f65c2910311ed45f`; release-aligned source `Alexthw46/Ars-Morph@4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58`. Fatos abaixo **SOURCE_CAUSALITY**, não comparação de bytecode do JAR.

## Registro e valores do pack source-pinned

- **Identidade da habilidade/forma:** `ars_nouveau:whirlisprig` (ID de Ars ou Ars Elemental/Identity2, **não** `ars_morph:*` spell).
- **Config de Identity2 no arquivo de atribuição:** `cooldown=400`, `use_duration=20`. São **inteiros brutos nos JSONs upstream**; a interpretação da unidade (ticks, segundos), consumo no cancelamento, skill gates e sincronização são do Identity2 **2.2.4**, ainda não medidos no runtime do pack.
- **Admissão:** Registro no `ModEntities.WHIRLISPRIG_TYPE`, wrapper só aceita morph `Whirlisprig`.

## Matriz causal para perks

| Eixo | Observação fixa em source | Status de adaptação |
|---|---|---|
| Entrada | `MorphBoundAbility.execute(Entity host)` exige que host seja `Player`, `IdentityApi.getCurrentMorph(player)` não-null e seja instância da classe esperada; exceptions em `use` são capturadas/logadas. | `⛔` Não transpor gate de morph ou duplicar os eventos do Identity2. |
| Efeito ativo | Ativação dispara resolver Ars `EffectGrow + AugmentAOE×3`, com cor custom green (50,250,55), contra `BlockHitResult` no bloco imediatamente abaixo do jogador. A resolução só ocorre após `postEvent` não cancelado. | `⚠️` Runtime/settlement efetivo do host não foi testado. |
| Target / geometria | Centro do efeito é o bloco abaixo do jogador. Raio AOE resultante, tipo de planta, permissão de mundo/claim, quantidade de blocos e custo pertencem ao Ars, não ao adaptador. | `⛔` Sem hook provado para alterar tipo de alvo, AOE, range, dano ou hitbox. |
| Passivo e tempo | Override de `passiveTick` no servidor aplica `MobEffects.JUMP` por **40 ticks**, amplifier **2**, ambient=true, sem partículas. Reaplicação pode ocorrer por ticks do Identity2; não é cast e não deve creditar Mastery. | Efeito contínuo/callback passivo não corresponde a casts adicionais. |
| Causalidade | O método de Grow pode alterar o mundo; `WorldEffectPolicy` do Black Arcana NÃO governa automaticamente uma mutação provider-native. Perks de alcance/área são ⛔ sem seam. | Uma ativação Identity2 pode originar spell Ars, projétil, potion ou status: não criar segunda cobrança/cooldown/XP. |
| Bounds | Identidade depende da forma atual, servidor/cliente e dependências. Qualquer número de entities/hits ou change de bloqueio só é efetivo se o pipeline host o aceitar. | `⚠️` Testar cancelamento, persistência e resolução de efeito com versões atuais. |

## Evidência de código e arquivo de atribuição

- [java](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/java/com/alexthw/ars_morph/identity/ability/WhirlisprigAbility.java#L16-L40)
- [registry](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/java/com/alexthw/ars_morph/identity/IdentityReg.java#L56-L67)
- [Identity2 `whirlisprig.json`](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/resources/data/ars_nouveau/identity2/identity_ability/whirlisprig.json)
- [Base MorphBoundAbility](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/java/com/alexthw/ars_morph/identity/ability/MorphBoundAbility.java#L15-L62 ).

**QA requerido:** Testar Grow sob claims/Survival e em blocos sem planta, raio AOE×3 host, respawn, gasto Ars, passiveTick em jogador real, cancelamento event e deduplicação. Versões físicas usadas como alvo: Ars Nouveau 5.13.1, Identity2 2.2.4, Ars Elemental 0.7.10.1 quando presente, Gabou's Libs 1.8.7. **+0 novas raízes mágicas; 0 adapters implementados.**

## Semântica dos contadores Identity2 — verificação upstream 17/10/2026

**Evidência cruzada do código oficial `xGabou/Identity2`, ramo 1.21.1:** um snapshot anterior (27/05/2026, `847202234ae89a1596c6039b473566e34231c213`) e outro posterior (02/10/2026, `c634278ee637e8b94949a685072c94d67c9b3d4a`, versão fonte 2.2.4.1) mantêm `ModPackets.resolvePrimaryAbilityCooldown=max(0,cooldown+useduration)`; `EntityMixin.baseTick` decrementa contador 1/tick, e o servidor registra o cooldown **antes** de chamar `execute`. Para whirlisprig: JSON `cooldown=400` + `use_duration=20` → **420 ticks** para o contador primário, não 400 ticks. Valor usado pelo secundário comum: 400 ticks (sujeito às exceções próprias de outras formas). Um efeito ou resolver Ars derivado pode durar mais/menos e deve ser medido separadamente.

[Protocolo completo de prova e links de código](../IDENTITY2-ABILITY-COOLDOWN-SOURCE-BRACKET-2.2.4.md). **⚠️ SOURCE_BRACKET**, sem prova de equivalência binária da versão instalada Identity2 2.2.4 ou de execução real; **⛔ nenhum hook de cooldown per-player homologado**.

