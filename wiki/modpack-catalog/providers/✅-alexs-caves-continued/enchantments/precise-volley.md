# Precise Volley — `alexscaves:precise_volley` (Alex's Caves Continued 1.0.10)

**Conclusão individual:** ✅ apenas o contrato **técnico estático** `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`, condicionado à CI da PR. **Hook mutador:** `NOT_VERIFIED`; **QA física:** `NOT_TESTED`; **mutação:** `NO_MUTATION`; **universo integral do provider:** aberto. Nenhuma certificação de perk executável ou Stage resulta desta ficha.

## 1. Identidade, texto original e proveniência

- **Provider:** Alex's Caves Continued (`alexscaves`), versão **1.0.10**, Minecraft 1.21.1/NeoForge, Java 21; modlist sibling registra `alexscaves-1.0.10-neoforge+1.21.1.jar`.
- **Publisher:** CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` e SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Registro/ResourceKey:** `alexscaves:precise_volley`. Recurso `data/alexscaves/enchantment/precise_volley.json`, **363 bytes**, SHA-256 `59efc44222dcd59530e13a50cb413a2db0c875213ced1a2ac9de2ef982615f53`. 
- **Descrição literal inglesa (`en_us.json`):** “Dreadbow arrows rain down from the sky to a more central position”. Tradução explicativa: a chuva de flechas do Dreadbow converge mais para a região central. O efeito real depende de mira, spawn, movimento, colisões e outros mods; a descrição não fornece porcentagem ou raio resultante.
- **Equipamento declarado:** `#alexscaves:enchantable/dreadbow`; o recurso `data/alexscaves/tags/item/enchantable/dreadbow.json` (SHA-256 `f22db4f6335af0cc185f0478c482c3c666a86afa430f06bdabc78ccc662076d5`) declara apenas `alexscaves:dreadbow`.

A [sonda publisher](../../../../../docs/qa/alexscaves_1010_precise_volley_probe.py) verificou fisicamente JSON, tag, tradução, classes e âncoras do mesmo JAR. O [manifesto binário Dreadbow/Dark Arrow 1.0.10](../EXACT-DREADBOW-CONTRACTS-1.0.10.json) já contém o código compilado do consumidor, com SHA de classe, métodos e offsets. O [selo individual](../EXACT-PRECISE-VOLLEY-CONTRACT-1.0.10.json) reutiliza esse manifesto e fixa a ficha sem copiar código proprietário. O snapshot público `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**, sendo apenas corroboração adjacente.

## 2. JSON, nível e custos declarativos

| Campo | Valor publisher 1.0.10 | Limitação |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.precise_volley` | Chave de tradução |
| `supported_items` | `#alexscaves:enchantable/dreadbow` | Tag embarcada; elegibilidade efetiva do pack não testada |
| `weight` | **2** | Peso do encantamento, não chance de acerto |
| `max_level` | **1** | Apenas nível I publicado; Java usa predicado `L>0` |
| `min_cost` | base **1**, incremento **18** | Nível I: **1** |
| `max_cost` | base **41**, incremento **10** | Nível I: **41** |
| `anvil_cost` | **4** | Custo declarativo; não desgaste da arma por flecha |
| `slots` | `["mainhand"]` | Slot permitido segundo o recurso |
| `effects` e `exclusive_set` | Não constam deste JSON | Não demonstram ausência de exclusividade em outros encantamentos/engine |

O consumer `DreadbowItem.releaseUsing` consulta `ACCompat.enchantLevel(stack, PRECISE_VOLLEY)` e trata **qualquer nível positivo** como `precise=true` (`@43–57`), sem multiplicar bônus pelo nível. Níveis forçados fora de I não estão homologados. A regra declarativa de exclusividade de `RELENTLESS_DARKNESS` com Precise Volley pertence à sua própria configuração, enquanto o body de `releaseUsing` desvia com `level(RELENTLESS_DARKNESS)>0` **antes** de consultar Precise; não supor que ambos disparem juntos.

## 3. Gatilho e conservação da salva nativa

O produtor é `com/github/alexmodguy/alexscaves/server/item/DreadbowItem.class`, método `releaseUsing(ItemStack,Level,LivingEntity,int)`. A execução exige Player e `RELENTLESS_DARKNESS<=0` (`@0–20`), e a potência calculada **`p>0.1D`** (`@113–117`) antes do disparo. O item aceita inicialmente uso com munição não vazia ou creative, e o `releaseUsing` chama `createArrow`; null encerra a execução sem concluir a salvo/cobrança.

`M=getMaxLoadTime(stack)` normalmente calcula `40−8×level(DARK_NOCK)`; `t=72000−remainingUseTicks`, `x=t/M`, e `p=min(1,(x²+2x)/3)` no domínio normal do uso, com **apenas clamp superior para p**, sem proteção independente contra denominadores anormais. Precise Volley não altera `M`, `p`, o gate `p>0.1` nem `getUseDuration=72000`.

A mira consulta `ProjectileUtil.getHitResultOnViewVector` a **`128F×p`** com fallback de **`42F×p`** se o primeiro resultado for MISS, com predicate nativo `canBeHitByProjectile`. Essas são distâncias de **raycast de seleção**, não alcance de voo ou área atingida automaticamente.

A posição inicial candidata de cada seta é `BlockPos` elevado a partir do impacto e jitter `(r×16−8,r×4−2,r×16−8)`, em uma caixa de **16×4×16**; há até seis sorteios adicionais em um caso de bloqueio, com fallback ao centro. A direção final solicitada a `AbstractArrow.shoot` é `hitLocation−spawnPosition`; a velocidade nominal é `0.5F+1.5F×random`, intervalo **[0,5;2)**, independentemente de Precise. Logo, **inaccuracy=0 não reduz a caixa onde as flechas são inicialmente criadas nem garante atingimento no ponto central**.

| Mecânica | Precise Volley ausente (`L=0`) | Precise Volley ativo (`L>0`) |
|---|---|---|
| Modo de uso | `releaseUsing` (se Relentless=0) | Mesmo `releaseUsing` |
| Inaccuracy passado a `shoot` | **Dark Arrow:** `20+10×r`; flecha não convertida: `5+10×r`, sujeito ao sorteio extra de 25% | **0F** para ambos os caminhos |
| `setShadowArrowDamage` em Dark Arrow | **3F** | **2F** |
| `setPerfectShot` em Dark Arrow | `perfect` calculado por Twilight Perfection | O mesmo `perfect` |
| Iterações (flecha conversível) | `ceil(30F×p)` | Mesma quantidade |
| Iterações (não conversível) | `ceil(8F×p)` | Mesma quantidade |
| Raycast, caixa inicial, velocidade | Inalterados | Inalterados |

**A conversibilidade é independente de Precise:** `isConvertibleArrow` exige `instanceof Arrow` e `Arrow.getColor()==−1`. No ramo conversível, o método cria novos `DarkArrowEntity` dentro do loop. No não conversível, usa os projéteis entregues pela factory do ArrowItem e Precise apenas escolhe inaccuracy=0; não transforma uma flecha incompatível em Dark Arrow nem muda seu dano-base por essa flag.

O valor `p` delimita **solicitações de criação**, não inserções aceitas: `Level.addFreshEntity` retorna booleano descartado, sem confirmação de sucesso para contagem ou custos. `Precise` não aumenta a contagem, nem altera targeting para seguir entidades após o disparo. A atribuição de Pickup ocorre antes da conversão em Dark Arrow: não certificar política de recuperação/pickup para cada seta convertida.

## 4. Cadeia de dano e outros encantamentos

`DarkArrowEntity.onHitEntity` começa de `getShadowArrowDamage()` e multiplica por **2F** apenas se `isPerfectShot()` (`@10–27`); solicita `ACDamageTypes.causeDarkArrowDamage` e chama `ACCompat.hurt` com owner, source e float (`@29–85`). Exclui owner e aliados pelos checks próprios quando owner existe; se `startFading`, não realiza hurt; após retorno true marca fading. É uma **solicitação de dano**, não pontos de vida removidos garantidos.

| Ramo Dark Arrow | `isPerfectShot=false` | `isPerfectShot=true` |
|---|---:|---:|
| Precise ausente, `shadowArrowDamage=3F` | 3F | 6F |
| Precise ativo, `shadowArrowDamage=2F` | 2F | 4F |

A condição de tiro perfeito exige `TWILIGHT_PERFECTION>0` e `getPerfectShotTicks(stack)>0`, com concessão de contador cliente e sincronização que necessitam QA. Para flecha **não convertível** num tiro perfeito, o item tenta multiplicar o `baseDamage` da entidade Arrow por `2D`; não há `setShadowArrowDamage` nesse objeto e portanto os números da tabela não se aplicam a ele. Fonte e efetividade de dano dos outros tipos pertencem ao provider/vanilla.

`DreadbowItem.onUseTick`, quando `RELENTLESS_DARKNESS>0` e `remainingUseTicks % 3 == 0`, tem outra rotina com 1–2 flechas convertíveis, `shadowArrowDamage=2F`, speed nominal `4F+3F×random` e inaccuracy crescente. Esse método **não lê PRECISE_VOLLEY**; o valor `2F` ali não é prova de que Precise atua no modo Relentless. A exclusividade nos JSONs e o desvio de `releaseUsing` devem permanecer distintos.

## 5. Recursos, sincronização e integração com perks

`releaseUsing` cobra **uma vez por salva** fora do modo criativo, sem usar o número de flechas como multiplicador: **1 de desgaste** pelo caminho normal, salvo Shaded Respite elegível, e **1 de munição**, salvo flecha comum protegida por Shaded Respite. O gate de Shaded Respite exige nível positivo e luz abaixo do critério do helper `DarknessIncarnateEffect.isInLight(...,11)`; o início do uso ainda depende do gate de munição. O enchantment `anvil_cost=4` é separado dos custos de release. Precise não instala mana/stamina, cooldown nem custo por acerto no consumidor nativo.

`DreadbowItem.use`, `releaseUsing` e `onUseTick` **não contêm guarda global própria server-only** nos corpos auditados. A operação efetiva depende de callbacks vanilla, mundo físico, autoridade de rede, mixins e outros providers. `ACItemstackRenderer` e os componentes `UseTime`, `PerfectShotTicks` e `LastUsedArrowType` refletem estados de apresentação/stack; não são provas de autorização de casts mutadores. A rede `UpdateItemTagMessage` envolve seleção por entidade/mão e não serve de autorização para uma perk sem validação adicional.

Campos relevantes para uma futura integração (apenas observáveis, não hooks homologados): `volley_inaccuracy`, `spawn_box_jitter`, `raycast_length`, `shot_power`, `requested_volley_count`, `converted_arrow_flag`, `shadow_damage_request`, `perfect_shot_flag`, `owner_alliance_guard`, `spawn_acceptance`, `ammo_debit_per_volley`, `durability_debit_per_volley`, `native_damage_source`, `server_authority` e `datapack_enchantment_gate`.

Uma perk que aumente precisão, número de projéteis, área de acerto, dano, velocidade, alcance ou probabilidade de ocorrência exige seam/hook comprovado no servidor, caps, deduplicação e preservação das políticas PvP/claims e dos custos nativos. **Não** disparar segunda chuva de flechas, novo `hurt`, nova cobrança ou processar `setShadowArrowDamage` como dano já aceito. Não transferir a autoridade de casting do Black Arcana ao RPG Skill Tree; não inventar API do provider.

## 6. Prova e conclusão limitada

- [Manifesto individual Precise Volley](../EXACT-PRECISE-VOLLEY-CONTRACT-1.0.10.json) — JSON/tag/idioma publisher, SHA da ficha e âncoras selecionadas dos consumers de Dreadbow/Dark Arrow.
- [Contrato Dreadbow/Dark Arrow preexistente](../EXACT-DREADBOW-CONTRACTS-1.0.10.json), [Dreadbow](../equipment/dreadbow.md) e [Dark Arrow](../damage-types/dark-arrow.md) — contextos compartilhados, sem duplicação da cadeia técnica.
- [Sonda SHA-exata](../../../../../docs/qa/alexscaves_1010_precise_volley_probe.py) e [regressões individuais](../../../../../docs/qa/alexscaves_1010_precise_volley_cards_test.py).

**Estado:** `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`, `provider_universe_closed=false`; conteúdo de Stage e runtime permanece inalterado.
