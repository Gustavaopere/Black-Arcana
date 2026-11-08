# Second Wave — ondas retardadas da Ortholance (Alex's Caves Continued 1.0.10)

**Estado: ⚠️ contrato estático individual em auditoria, NÃO certificado.** Esta ficha registra a prova compilada de `OrtholanceItem.releaseUsing` e a cadeia já auditada de `WaveEntity`; a atribuição do universo de consumidores, integração externa e homologação permanecem separadas. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. Não implementar perks a partir de um símbolo localizado.

## Identidade e proveniência do artefato

| Propriedade | Evidência do publisher exato |
|---|---|
| Provider / mod ID | Alex's Caves Continued / `alexscaves` |
| Minecraft, loader, Java | 1.21.1, NeoForge, Java 21 |
| JAR físico da modlist | `alexscaves-1.0.10-neoforge+1.21.1.jar`; 75.279.314 bytes |
| SHA-1 / SHA-256 | `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` / `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| Resource ID / registro | `alexscaves:second_wave` / `ACEnchantmentRegistry.SECOND_WAVE` |
| JSON | `data/alexscaves/enchantment/second_wave.json`; 413 bytes; SHA-256 `68d843242cc39b33eb952142b168fa8e72a2695bfa8adea6de3e4bba6febb97c` |
| Item tag | `#alexscaves:enchantable/ortholance`, com `alexscaves:ortholance`; SHA-256 `1c96a26e08800182b9c4b3b2f5ba4043389fe1bec0dcd5b12f1e5392cc28a5ac` |
| Descrição funcional (paráfrase da localização `en_us`) | Após o lançamento do usuário pela Ortholance, solicita ondas adicionais **com atraso** |
| Produtor | `OrtholanceItem.releaseUsing(ItemStack, Level, LivingEntity, int):void` |
| Método compilado | 435 instruções, digest `00705e7177cb6fe2914531158bd978b64d497ca4c8262f8e7634c1b4ec9ef7ae` |
| Consumidor de ondas | `WaveEntity.tick` e `WaveEntity.attackEntities`, previamente selados no mesmo JAR |

Fontes de reprodução: [sonda read-only exata](../../../../../docs/qa/alexscaves_1010_second_wave_probe.py), [manifesto de descoberta](../EXACT-SECOND-WAVE-DISCOVERY-1.0.10.json), [inventário de Flinging/lançamento](../EXACT-FLINGING-1.0.10.json) e [contrato WaveEntity de Sea Swing](../EXACT-SEA-SWING-STATIC-1.0.10.md). A fonte pública adjacente 1.1.1 **não é autoridade** para esse JAR 1.0.10.

## Dados declarativos do encantamento

| Campo | Valor exato |
|---|---|
| `supported_items` | `#alexscaves:enchantable/ortholance` |
| `weight` | 2 |
| `max_level` | I (1) |
| `min_cost` | base 1; incremento por nível acima de I: 12 |
| `max_cost` | base 41; incremento por nível acima de I: 10 |
| `anvil_cost` | 4 |
| `slots` | `mainhand` |
| `exclusive_set` | contém `alexscaves:tsunami` |

Esses custos dizem respeito ao encantamento, não são mana, cooldown, dano, chance de hit ou custo por onda. O `exclusive_set` vem do JSON e não substitui auditoria dos datapacks efetivamente carregados.

## Ativação, gates e quantidade

`releaseUsing` calcula a carga como `C = clamp(getUseDuration(stack,null) - remainingUseTicks,0,60)` (@0–15). O método lê os níveis de Flinging e Tsunami e retorna se `C <= 0` (@43–45). O desgaste da arma é solicitado com `ACCompat.hurtAndBreakUsedHand(stack,1,usuário)` (@132–135), **anterior** ao ramo de Second Wave. É um custo do uso nativo, não uma cobrança adicional por cada onda secundária.

No ramo posterior à primeira emissão de ondas (@459), o registro `SECOND_WAVE` é consultado com `ACCompat.enchantLevel` (@460–463). `ifle @466` pula a criação secundaria quando o nível é 0 ou negativo. Para nível positivo não há outro multiplicador numérico do nível no trecho observado. O número de iterações é `N = max(1, B-1)` (@469–477), onde `B` é o contador local 10 formado anteriormente no lançamento. No caminho normal, esse contador recebe divisão inteira de `C/5` (@138–142); o método também contém uma substituição de `B` no ramo Tsunami. **O JSON declara exclusividade com Tsunami, mas níveis forçados/datapacks são fronteira não homologada.**

Para `i = 0, ..., N-1`, a região @482–702 constrói **duas instâncias de WaveEntity por iteração** (@529–535 e @614–620), totalizando `2N` **pedidos** de spawn, não `2N` inserções ou hits garantidos. Ambos os `addFreshEntity` têm retorno booleano descartado (@610–613 e @695–698). O laço incrementa `i` (@699) e retorna para a condição (@702–482).

## Parâmetros, geometria e timing

A variável local de progresso é `f = i/N` em float (@489–496). O trecho @498–507 calcula o inteiro de duração da onda: `T = 3 + trunc((1-f)*3)`. Para a faixa do laço, o valor solicitado pode variar entre **3 e 6**, sendo **6 para i=0**. Essa expressão vem do corpo JVM 1.0.10, não de versão adjacente; `T` é passado aos dois `setLifespan` de cada iteração (@563 e @648). **Lifespan não é duração física garantida**: a onda usa também espera, slam e descarte próprios.

As duas ondas de um par começam na mesma posição horizontal, derivada de `usuário.position()` e um deslocamento `vec9.scale(2*f)` do lançamento, com coordenada Y do usuário (@511–556 e @625–641). O vetor `vec9` é calculado pelo pipeline da Ortholance antes do ramo; não é alcance fixo do feitiço.

Para o yaw, o método usa `θ = -atan2(vec9.x,vec9.z) × 57.2957763671875` e solicita ângulos espelhados **`θ+60-15i`** (@578–597) e **`θ-60+15i`** (@663–682), em graus. Isso não define, por si só, o traçado efetivo das ondas em cada tick.

Ambas as instâncias recebem **`setWaitingTicks(8)`** (@602–604 e @687–689). O produtor Second Wave não chama `setWaveScale`; a entidade define escala basal `1F`, conforme manifesto SHA-exato de WaveEntity. A espera é decrementada no servidor no `tick` nativo da entidade; o valor de 8 não é cooldown global, duração da arma ou latência garantida de impacto.

## Efeitos, targeting, owner e persistência

Cada `WaveEntity(Level,LivingEntity)` recebe a entidade usuária como proprietário e seu setter registra o UUID do owner. A rotina nativa `WaveEntity.attackEntities` atua sobre `LivingEntity` em sua **AABB própria inflada em 0,5D por eixo**, utilizando DamageSource `mobProjectile(onda, owner)`. Exclui os aliados segundo filtros compilados, o próprio owner quando disponível e Deep One Base. Solicita `hurt(scale+1)`; **ignora seu booleano** e solicita `setSlamming(true)` e knockback `0,1+0,5×scale`. O `tick` passa `scale=2×getSlamAmount(1F)+1+getWaveScale`. Esses números são argumentos de chamadas nativas, não dano aceito/DPS ou distância efetiva.

O `tick` de `WaveEntity` guarda `attackEntities` atrás de verificação de lado servidor, mas o callback `releaseUsing` precisa ser avaliado em seu contexto de execução; não inferir segurança multiplayer ou política de claims por essas guardas locais. O uso principal da Ortholance também solicita empurrão do usuário e inspeciona entidades próximas/linha de visão em @705–869: não se deve classificar esse caminho como outro cast criado por Second Wave.

A entidade só grava em seu NBT próprio `Owner` (UUID, quando existe) e `Lifespan`. **`WAITING_TICKS` não aparece nesse salvamento próprio.** Após reload, um `getOwner()` posterior pode resolver UUID em `ServerLevel`; o consumidor de dano utiliza o campo `owner` diretamente. Por isso, autoria, filtragem de aliados, conservação do atraso após reload e creditamento de Mastery/XP precisam de QA física específica.

## Matriz de perks, atributos e Mastery

| Eixo | Contrato observável | Limite fail-closed |
|---|---|---|
| Gatilho | `releaseUsing`, carga positiva, nível Second Wave positivo | Não gerar um novo cast independente da Ortholance |
| Quantidade | `2×max(1,B-1)` pedidos adicionais em pares | Não contar spawns recusados ou duplicar ondas/custos por callbacks |
| Posição e direção | vetor nativo de impulso, deslocamento `2f`, yaw simétrico `±(60-15i)` | Não converter isso em alcance universal ou targeting por aim assist |
| Tempo | `setWaitingTicks(8)`; `setLifespan(T)` com `T=3+trunc((1-f)×3)` | Nenhum cooldown ou tempo final de hit certificado |
| Área e dano | Delegados à `WaveEntity` (AABB e dano solicitado) | Não executar hurt adicional e não creditar Mastery sem aceitação real |
| Custo | Um desgaste solicitado no uso da Ortholance antes do ramo | Não debitar por onda ou supor taxa de sucesso do desgaste |
| Owner e NBT | Owner inicial capturado; Owner UUID/Lifespan persistidos em overrides | Não presumir restauro automático de owner ou espera após load |
| Hooks mutadores | `NOT_VERIFIED` | ⛔ `NO_MUTATION`, sem implementar adapter imaginário |

## Limites e pendências para certificação estática

Este recorte de evidência é **read-only e condicionado**, mesmo com hashes exatos. Ainda se exige: fechamento da varredura de consumidores do provider, revisão independente do método completo e das variáveis locais; testes semânticos e selagem reproduzível; alinhamento dos índices globais com a `main` após as alterações de Seapairing em outro agente. QA física posterior precisa cobrir client/server, spawn recusado, proteção de mundo, PvP, aliados, reload, colisões, dano negado e compatibilidade com datapacks. Enquanto incompleto, **⚠️** não entra no numerador de contratos estáticos certificados. Nenhum código Java, hook, Stage ou gameplay foi alterado.
