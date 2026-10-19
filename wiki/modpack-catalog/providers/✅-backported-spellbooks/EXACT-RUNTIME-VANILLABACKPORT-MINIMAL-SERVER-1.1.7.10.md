# Vanilla Backport 1.1.7.10 — bootstrap NeoForge 21.1.250 e relatórios de Mixin no servidor mínimo

**18/10/2026 · ✅ `ISOLATED_MINIMAL_DEDICATED_SERVER_STARTUP_LOG_ONLY` e `EXACT_TARGET_MIXING_LOADER_REPORTS` · ⚠️ bytecode pós-transformação, modpack completo e jogador real · ⛔ hooks externos de perks.**

## Material auditado e limites de autoridade

- **Modlist física histórica (#001, #445, #560):** NeoForge `21.1.250`, `Platform-neoforge-1.21.1-1.3.3.jar` e `VanillaBackport-neoforge-1.21.1-1.1.7.10.jar` para Minecraft `1.21.1`/Java 21. A modlist não disponibiliza SHA novo dos binários locais nem cópia atual do mundo, e o snapshot 587 linhas continua distinto das adições pós-snapshot. **Nada instalado no computador do usuário foi alterado ou revalidado fisicamente.**
- **Instalador NeoForge:** `neoforge-21.1.250-installer.jar`, SHA-256 `0e47a91ba2139a8db4bf7627af081f7b5789b508bb039ee8dea1272b79693d60`, conferido contra o `.jar.sha256` do [Maven oficial NeoForged 21.1.250](https://maven.neoforged.net/releases/net/neoforged/neoforge/21.1.250/). `--installServer` executado no ambiente efêmero do runner, sem reutilizar server de runs anteriores.
- **Platform 1.3.3:** [CurseForge #8075942, projeto 997634](https://www.curseforge.com/minecraft/mc-mods/platform/files/8075942); publisher `Platform-neoforge-1.21.1-1.3.3.jar`, **489.341 bytes**, SHA-256 `2d7175e43943d22cbb4f8d4533f0ad620f87a3ac12c77a4f15c3a35d965c4f18`. O hash foi fixado no segundo run para impedir deriva de distribuição.
- **Vanilla Backport 1.1.7.10:** [CurseForge #8229724, projeto 417430](https://www.curseforge.com/minecraft/mc-mods/vanillabackport/files/8229724); publisher `VanillaBackport-neoforge-1.21.1-1.1.7.10.jar`, **54.902.084 bytes**, SHA-256 `ecd807ac358e243ede17819455788c7b7a0ce5e0af4aecee82c1c62c586d818d`. Identidade SHA-256 idêntica àquela usada nas provas de bytecode de atributos, manifesto e seletores.
- **Distribuição distinta:** o NeoForge exato do usuário é **21.1.250**, não versões 21.1.259 ou posteriores publicadas upstream. A versão do build Black Arcana no README (`21.1.248`) não deve ser silenciosamente tratada como a versão do runtime do perfil.

## Execuções e evidência de CI

| Etapa | Run GitHub Actions | Evidência verificada |
|---|---|---|
| Primeiro smoke | [#39177903447](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39177903447) | **SUCCESS**; `Done (12.796s)`, sem erro fatal capturado, `PASS_VB_11710_MINIMAL_NEOFORGE_211250_BOOTSTRAP`; [JSON #12154947822](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39177903447/artifacts/12154947822) |
| Gate reforçado | [#39178310071](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39178310071) | **SUCCESS**; 10/10 autotestes, `Done (10.039s)`, Platform e Vanilla Backport SHA-256 exatos, três `Mixing` de alvos verificados, `deviations=[]`; [JSON #12154822835](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39178310071/artifacts/12154822835) |

O teste foi executado em **dedicated server mínimo**, com EULA aceita no diretório efêmero do runner, `mixin.debug.verbose=true` e timeout controlado **depois** do `Done` (`exit-code=124`). O timeout encerra o processo de observação; **não** é prova de falha de startup nem de shutdown gracioso. Os recursos do teste incluem **apenas** NeoForge 21.1.250, Platform 1.3.3 e Vanilla Backport 1.1.7.10, não os demais mods do perfil nem mundo do usuário. O teste não abre janela cliente, não conecta jogador, não inspeciona save existente e não testa magias.

O [verificador fail-closed](../../../../docs/qa/vanillabackport_11710_minimal_bootstrap.py) testa presença de `Done`, encerramento esperado do smoke, ausência de padrões de falha fatal, menção a providers e **três mensagens de mistura com alvos exatos, cada uma exatamente uma vez**, sem aceitar coincidência de nomes genéricos. O [workflow](../../../../.github/workflows/vanillabackport-11710-minimal-server-bootstrap.yml) publica somente relatório JSON resumido: JARs de terceiros, servidor gerado, arquivos `mixin.debug.export`, logs brutos e dados do mundo não são anexados ao repositório.

## Três relações do serviço Mixin realmente reportadas no servidor mínimo

| Config do provider | Mixin declarado | Classe alvo `into` reportada | Linhas exatas no log |
|---|---|---|---:|
| `vanillabackport.mixins.json` | `common.entities.EntityMixin` | `net.minecraft.world.entity.Entity` | **1** |
| `vanillabackport.mixins.json` | `common.entities.LivingEntityMixin` | `net.minecraft.world.entity.LivingEntity` | **1** |
| `vanillabackport.mixins.json` | `common.attributes.RangedAttributeMixin` | `net.minecraft.world.entity.ai.attributes.RangedAttribute` | **1** |

**Interpretação correta:** os logs do serviço Mixin reportaram a **mistura direcionada** das três classes do provider no servidor mínimo; o startup alcançou `Done` e o verificador não identificou sinal fatal. Isso demonstra mais que a presença de um `.class` e do JSON, mas **não** é inspeção pós-transformação do bytecode carregado nem prova de que todos os pontos `@At` disparam durante movimento real. O log pode informar preparação/aplicação do Mixin sem que cada handler tenha sido exercitado. O verificador registra `runtime_mixin_injection_applied=NOT_VERIFIED` deliberadamente.

No [alvo de servidor patchado sem outros mods](EXACT-NEOFORGE-211250-MIXIN-TARGETS.md), `LivingEntity.travel` contém quatro callsites `setDeltaMovement(DDD)V`, com `ordinal=3` no PC **1314**. A [configuração binária dos mixins](EXACT-BINARY-VANILLABACKPORT-MIXIN-INJECTION-SELECTORS-1.1.7.10.md) certificou o `@WrapOperation` com esse ordinal e o `@ModifyArg` com `index=1`. **As provas ainda não contam callsites depois de carregar todas as outras transformações do modpack.**

## Passivos, atributos e integração de magia

- `Slime Aspect` mantém sua raiz de magia única `backportedspellbooks:slime_aspect` e aplica efeito via o handler [auditado separadamente](EXACT-BINARY-SLIME-ASPECT-0.1.2.md); seus modifiers são próprios e não incluem o `LivingFallEvent` das botas.
- `Slime Boots` é um item, **não sétima magia**, e o cancelamento de queda pertence a `ServerEvents.onFallEvent` com verificação de `EquipmentSlot.FEET` e `ModItems.SLIME_BOOTS` ([prova binária](EXACT-BINARY-SLIME-BOOTS-FALL-0.1.2.md)).
- O host registra `minecraft:bounciness` com padrão 0 e limite declarado 0–1 e `minecraft:friction_modifier`/`air_drag_modifier` com padrão 1 e faixa 0–2048; esses valores são [de bytecode do publisher](EXACT-BINARY-VANILLABACKPORT-MOBILITY-HOST-1.1.7.10.md), **não leituras dos atributos resolvidos em jogador**.
- **O servidor mínimo não carregou Backported Spellbooks 0.1.2, Iron's 3.16.3 nem o conjunto físico do modpack.** Portanto não prova o cast, potência, stacking, cooldown, consumo, FallEvent real ou compatibilidade com os demais mixins. Não promove adaptadores de perks ou Mastery.

## Checklist físico restante

1. Validar SHA local e versões efetivamente instaladas de todos os providers relevantes (snapshot físico ainda sem novo dump); manter backup e perfil original intocados.
2. Verificar classfile **pós-transformação** ou aplicação/injeção completa no modpack com NeoForge 21.1.250 + Platform 1.3.3 + Vanilla Backport 1.1.7.10 + Iron's 3.16.3 + Backported Spellbooks 0.1.2 e demais mods de movimento/combate.
3. Cliente real e dedicated server com jogador conectado: nenhuma condição, apenas `slime_aspect`, apenas botas e ambos; medir atributos server-side, tempo/amplificador, salto, bounciness/colisões, atrito/arrasto, queda e dano, ingresso/saída de mundo, relog e respawn.
4. Interoperabilidade/ausência de dupla aplicação de efeitos com Epic Fight e outros mods de movimento; comparar resultados com hipóteses da matriz; documentar qualquer conflito fail-closed.
5. Não mover Stage 06.05/09 por simples `Done` em servidor mínimo. Stage 09 permanece obrigatório quando houver modpack real e QA de jogador.

**Estado técnico:** ✅ integridade de publisher/instalador, ✅ bootstrap de servidor mínimo e ✅ três target-mixing logs exatos; ⚠️ aplicação demonstrada com bytecode pós-transformação, modpack completo, servidor/cliente com jogador, stacking e QA físico; ⛔ APIs/hook de perks não certificados. **+0** magias e **+0** adapters. Backported Spellbooks continua **6/6** raízes de magia, fichas e identidades com ao menos um método compilado delimitado. Universo global mínimo documental **1.857 objetos semânticos / 1.855 estritos**, denominador aberto (**—%**). **Stage 06.05 🟡; Stage 09 pendente.** PR #825 draft; nenhum merge aprovado apenas por este smoke.
