# Mixin — anti-floating com Airstepping

**Contrato:** suporte de Aeromancy Additions `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. Não é nova identidade de magia. `hooks=NOT_VERIFIED`; `physical_runtime=NOT_TESTED`; **0 certificações / +0 magias / +0 adapters aprovados**. O JAR oficial de publicação foi adquirido separadamente; isso não comprova paridade com o JAR instalado historicamente (SHA-1 histórico de 35 caracteres inválido). [Proveniência e limites](../SOURCE-CONTRACTS-1.2.8.md).

## Binding e alteração

`aeromancy.mixins.json` é `required=true`, `JAVA_21`, `minVersion=0.8` e `defaultRequire=1`; lista `ServerPacketListenerMixin` como mixin comum. O template do mod declara o config. Isso não comprova que o hook encaixa e executa no host instalado: `hooks=NOT_VERIFIED`.

`@Mixin(ServerGamePacketListenerImpl.class)` usa MixinExtras `@ModifyExpressionValue` em **`tick`**, no acesso `GETFIELD` de **`ServerGamePacketListenerImpl.clientIsFloating:Z`**. Mantém `@Shadow ServerPlayer player`. Para cada valor booleano capturado:

```text
se floating && player.hasEffect(AIRSTEPPING): retorna false
caso contrário: retorna floating
```

A expressão lida muda; não há atribuição ao campo `clientIsFloating`, cancelamento integral de `tick`, edição de outros campos de movimento ou gate de contador. Com MobEffect ativo, o retorno falso independe de cargas restantes. Sem MobEffect, conserva o valor original. Não tornar isso contrato geral de anticheat, bypass de voo, autorização de cast ou imunidade contra todas as desconexões.

| Eixo | Contrato para perks |
|---|---|
| Dano | N/A: nenhuma chamada de dano/fall damage. |
| Alcance | N/A: tick da conexão servidor. |
| Alvo | Player da instância `ServerGamePacketListenerImpl`. |
| Tempo | Leituras GETFIELD correspondentes em `tick`, enquanto MobEffect AIRSTEPPING estiver ativo. Não verifica contador. |
| Custo | N/A: sem mana/carga/cooldown ou spell settlement. |

[Input C2S](../payloads/airstep.md) valida cargas, MobEffect e airborne; este mixin apenas adapta a expressão vanilla. O host exato, outros mixins de movimento e a desconexão por floating exigem QA físico, sem adapter aprovado.


**Fonte imutável:** [ServerPacketListenerMixin.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/mixin/ServerPacketListenerMixin.java#L12-L22) · [Config obrigatório](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/resources/aeromancy.mixins.json#L1-L14) · [Declaração no template](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/templates/META-INF/neoforge.mods.toml#L28-L30) · [Validação C2S separada](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/airstep/AirstepSpell.java#L98-L124).
