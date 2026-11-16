# Flinging 1.0.10 — prova causal estática e reprodução

**Objeto:** `alexscaves:flinging`, encantamento nativo da Ortholance. **Escopo:** `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Integração:** `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`; universo integral do provider aberto. A [ficha individual](enchantments/flinging.md) documenta o contrato para design de perks; o [selo causal](EXACT-FLINGING-CAUSAL-1.0.10.json) permite reproduzir a evidência. Nenhum resultado físico ou hook executável é homologado por esta prova.

## Autoridade e preservação

| Artefato | Identidade verificada |
|---|---|
| Release instalada | `alexscaves-1.0.10-neoforge+1.21.1.jar`, Minecraft 1.21.1 / NeoForge / Java 21 |
| Publisher | [CurseForge projeto 1645389, arquivo 8856293](https://www.curseforge.com/minecraft/mc-mods/alexs-caves-continued/files/8856293) |
| Tamanho do JAR | **75.279.314 bytes** |
| JAR SHA-1 | `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` |
| JAR SHA-256 | `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| Selo causal desta revisão | [EXACT-FLINGING-CAUSAL-1.0.10.json](EXACT-FLINGING-CAUSAL-1.0.10.json), **155.598 bytes**, SHA-256 `d12793a00f4d59033d30ceb5bfb3490be8d00eb0a9b281c093434754ff07fa5f` |
| Evidência anterior conservada | [EXACT-FLINGING-1.0.10.json](EXACT-FLINGING-1.0.10.json), **196.748 bytes**, SHA-256 `bfd013357139a53a42408905470a152e8d82d67aec7c081f946dec1e1d48209b` |
| Fonte pública adjacente | [Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37](https://github.com/Codx-org/AlexsCavesContinued/tree/523308608422ab8e31974befa7111ecdf495dd37), declara **1.1.1**; não é autoridade numérica ou prova de paridade da 1.0.10 |

A nova extração começa por conferir SHA-1, SHA-256 e tamanho do JAR e reproduzir integralmente a antiga sonda de janelas. Seu resultado precisa continuar igual ao manifesto histórico. O novo selo acrescenta corpos nativos completos e seus branches sem reclassificar os escopos antigos. As provas de [Tsunami](EXACT-TSUNAMI-CONTRACT-1.0.10.json), [Second Wave](EXACT-SECOND-WAVE-DISCOVERY-1.0.10.json) e [Sea Swing](EXACT-SEA-SWING-STATIC-1.0.10.json) conservam bytes e limites próprios; compartilhar classes não as promove por associação.

O auditor identifica referências literais diretas a `FLINGING` em classfiles do provider. Esse censo delimita os produtores compilados observados, sem provar ausência de reflexão, transformações de bytecode, datapacks ou consumidores externos.

## Recursos e métodos selados

O selo contém identidade do artefato, hashes SHA-256 e conteúdo JSON do encantamento/tag, recursos associados de Tsunami/Second Wave, tags empacotadas de aquisição, textos de localização, censo de exclusões dos 51 JSONs e hashes das classes escolhidas. O JSON de Flinging declara nível máximo III, peso 10, custos `min=1+8(L−1)` / `max=41+10(L−1)`, bigorna 1 e slot `mainhand`. Seu `exclusive_set` não está declarado; o censo publisher não encontrou exclusão reversa referenciando Flinging. Isso não certifica os dados efetivamente carregados no modpack.

O texto literal `en_us` é “Flinging” / “Ortholance launch moves the player much further”. As chaves próprias não aparecem no `pt_br.json` examinado. A descrição do jogador não define alcance físico em blocos.

Cada método selecionado tem owner, nome, descritor JVM, contagem de instruções, digest do corpo parseado, todas as arestas diretas de branch e tabela de exceções verificados. O método principal `OrtholanceItem.releaseUsing(ItemStack,Level,LivingEntity,int)V` contém **435 instruções**, offsets **0–869**, digest **`00705e7177cb6fe2914531158bd978b64d497ca4c8262f8e7634c1b4ec9ef7ae`**. O novo auditor lê o corpo completo, incluindo os laços normais e Second Wave que não pertenciam às janelas individuais de Tsunami.

O limite do auditor dedicado não altera os limites genéricos do auditor comum: são verificadores distintos. A extração rejeita métodos/seleções vazios, offsets duplicados, destinos de branch ausentes, estruturas não reconhecidas, owners novos do token, divergência de recursos/corpos e promoção indevida dos estados de segurança. Os fingerprints verificam identidade dos corpos; a interpretação dos pivôs e dos fluxos abaixo fecha o escopo semântico do encantamento. Nenhuma dessas verificações executa o jogo.

### Censo dos corpos e recursos

O censo atual sela **55 corpos completos**, **1.662 instruções JVM** e **75 branches diretos**, distribuídos em quatro classes, com **442 pivôs semânticos**. Os corpos escolhidos não declaram tabelas de exceção nem switches. `__class_init__` é a normalização textual do inicializador JVM `static {}`; não é um método adicional da implementação.

| Classe compilada | Métodos selecionados / declarados | Instruções | Branches diretos | SHA-256 do classfile |
|---|---:|---:|---:|---|
| `OrtholanceItem.class` | 13/13 | 587 | 24 | `996b208a60f2c26c275e60e5d0e3a2fd0090cfb0ba1687907cac242de9a17d09` |
| `WaveEntity.class` | 29/29 | 736 | 38 | `93fdaee0239cc4985b351a6c2ac1edd23a51cf0088cb1172f983d0f869d9e42e` |
| `ACCompat.class` | 11/200 | 151 | 13 | `333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b` |
| `ACEnchantmentRegistry.class` | 2/5 | 188 | 0 | `60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32` |

Ortholance e Wave têm todos os métodos declarados selecionados; ACCompat e o registro têm apenas os corpos necessários ao contrato. Isso não certifica toda a classe ACCompat, todos os registros ou chamadas herdadas da engine. Os descritores completos e todas as arestas constam do JSON. Alguns corpos centrais são:

| Owner / método | Instruções / branches | Digest do corpo parseado |
|---|---:|---|
| `OrtholanceItem.getUseDuration` | 2 / 0 | `261037fd2f1d7d62e027c38d2a96af9ccc45a0a01783f1784d1f1b36ce2bbd2f` |
| `OrtholanceItem.releaseUsing` | 435 / 19 | `00705e7177cb6fe2914531158bd978b64d497ca4c8262f8e7634c1b4ec9ef7ae` |
| `OrtholanceItem.use` | 20 / 1 | `3cced1da49821d3f4add491a5351b4ec455d1ea67bdc4d635900e1f3414176a0` |
| `WaveEntity.setOwner` | 12 / 2 | `35f16858fcf932d0f7383155eb72be1083581d9fd415a9019d2652c4e9305852` |
| `WaveEntity.getOwner` | 27 / 4 | `151e62a22a2d16abcd344f2913a9fd2e1461a3d8610c2e8ccb19b30a80a56483` |
| `WaveEntity.readAdditionalSaveData` | 19 / 2 | `bd24ec73f465c5284aa909b1e9b47b9106ddf9e260e051824c655b66be58dc72` |
| `WaveEntity.addAdditionalSaveData` | 14 / 1 | `ddec0df06356e462eaa084f84a2ea90c8944306df5a13e8957ee9a3aa114c4ec` |
| `WaveEntity.tick` | 318 / 21 | `d018fb4b1c90bd6104a52f875e097b9ef3818e36d038045f3668d75c6e120765` |
| `WaveEntity.attackEntities` | 81 / 7 | `f7d6b5c19cec219a1cbfa24ada582b81631528236fd459af40aa8e41196cb6e8` |
| `ACCompat.hurtAndBreakUsedHand` | 8 / 0 | `5349ce0a59e4ce10c8a3b252dd3ea8c200f4da735c1e56fb5a6b316c768c5496` |
| `ACCompat.enchantLevel` | 24 / 3 | `775387837bd0e7dbbd2fd04cd5de0375a6ccd2813de5db375fd152f8b63ad8dc` |
| `ACCompat.attackDamageBonus` | 12 / 0 | `ce63fc4907d1760c5afef512a19375b946fd25f99dca020398cdfc45afeaf2ab` |
| `ACCompat.lambda$attackDamageBonus$2` | 14 / 1 | `7657a3346470dfc64627146970a5cb10a4c0fde324c87450bf922f714e69723e` |

O `invokedynamic` de `ACCompat.attackDamageBonus` é ligado ao callback `lambda$attackDamageBonus$2` pelo bootstrap **#2**, com seção normalizada SHA-256 `bef18232e1739523923d08936a418a6134fdc6407dbfe8ece19bd7a02fd2c295`. A ligação é extraída e verificada, sem presumir que qualquer lambda com nome semelhante seja o callback de execução.

| Recurso publisher | Bytes | SHA-256 |
|---|---:|---|
| `data/alexscaves/enchantment/flinging.json` | 359 | `0680721d1687f85991e11ee33908b67aa8b720339e7b09eeaaaf92cf604356f2` |
| `data/alexscaves/tags/item/enchantable/ortholance.json` | 50 | `1c96a26e08800182b9c4b3b2f5ba4043389fe1bec0dcd5b12f1e5392cc28a5ac` |
| `data/alexscaves/enchantment/tsunami.json` | 358 | `37f1f8c3f8b98084b73b23aa2ec49ba9a925bb9a37089f622cf992234a086242` |
| `data/alexscaves/enchantment/second_wave.json` | 413 | `68d843242cc39b33eb952142b168fa8e72a2695bfa8adea6de3e4bba6febb97c` |
| `data/minecraft/tags/enchantment/in_enchanting_table.json` | 1631 | `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1` |
| `data/minecraft/tags/enchantment/non_treasure.json` | 1631 | `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1` |
| `data/minecraft/tags/enchantment/on_random_loot.json` | 1631 | `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1` |
| `data/minecraft/tags/enchantment/tradeable.json` | 1631 | `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1` |
| `assets/alexscaves/lang/en_us.json` | 121372 | `a2a3fab567b07ec10b3d946d4e4ce3e65417b6f9348bd49478d8a253a4232d1f` |
| `assets/alexscaves/lang/pt_br.json` | 84238 | `080bfaf05b6d710383579dfd0d3c01443f9fa873b0c697f5e6ee0740931018a7` |

Os hashes dos outros JSONs de encantamento e seus campos de exclusão estão no censo publisher de 51 entradas do selo. Eles delimitam os dados empacotados; não representam os datapacks efetivos de uma sessão em jogo.

## Carga, nível e dois vetores de movimento

O argumento inteiro do callback é o tempo **restante**, não a carga. O fluxo integral liga:

| Etapa | Âncoras JVM | Consequência estática |
|---|---|---|
| Duração da sessão | `getUseDuration`: literal 72.000 e retorno | Teto de uso próprio do item; não é cooldown ou carga efetiva de 72.000 |
| Carga C | `releaseUsing@0–15`, `Mth.clamp@12` | `C=clamp(72000−remainingUseTicks,0,60)` |
| Nível F | `FLINGING@18 → ACCompat.enchantLevel@21 → istore6@24` | Capturado da stack recebida no release; o helper não limita ao máximo III |
| Carga não positiva | `ifle@45→869` | Retorna antes de pedir movimento, desgaste ou emissão |
| Escalar P | `@48–61` | `P=0.1F×C+0.1F×F`; aritmética float antes das conversões double |
| Vetor intermediário V | `getDeltaMovement@64`, `getViewVector(1F)@69`, `normalize@72`, `multiply@87`, `add@90`, `astore9@93` | `V=deltaAnterior+normalize(visão).multiply(P,P×0.15F,P)` |
| Parcela vertical final | `onGround@841`, `@844–860`, `Vec3.add@863`, `setDeltaMovement@866` | Pede `V+(0,(onGround?0.2F:0F)+0.1F×F,0)` |

O termo do solo é consultado no final. O vetor V conserva o movimento anterior capturado antes dos callbacks de ondas/dano; não é normalizado novamente nem relido depois deles. O vetor usado para geometria e spawn é V, **anterior** à parcela vertical final. Preservar essa ordem importa para perks de altura, velocidade ou targeting.

Não há clamp local de F ao nível III no reader nem no release. JSON/tag/slot governam aquisição declarativa e são distintos da leitura da stack em execução. Níveis externos, slot forçado, troca de mão e intervenções de outros mods continuam pendentes de QA; esta constatação não é autorização para produzir stacks anômalas.

### Guardas independentes de movimento e servidor

`C<10@99→836` e `level.isClientSide()@106→836` pulam som, desgaste, ondas e ataque direto, mas chegam à solicitação final de movimento. Assim:

| Condição local | Pedido final de movimento | Bloco de ondas/custo/dano direto |
|---|---|---|
| C=0 | Não | Não |
| C=1–9 | Sim, se o callback alcança esse caminho | Não |
| C≥10 no cliente | Sim, se o callback alcança esse caminho | Não |
| C≥10 no servidor | Sim, após o bloco elegível e seus callbacks | Elegível |

A guarda servidor não cobre toda a rotina. Dispatch da engine, reconciliação de movimento, cancelamentos e autorização de um adapter externo não foram testados. `setDeltaMovement` é um pedido nativo de velocidade, não a comprovação de deslocamento, distância final, imunidade a queda ou voo.

## Ondas, contador B e volume do ataque direto

No ramo **C≥10 / servidor**, o custo de liberação é **uma solicitação de desgaste de 1** por `ACCompat.hurtAndBreakUsedHand@135`, anterior à escolha das ondas. O helper usa a mão de uso convertida a slot e delega a `ItemStack.hurtAndBreak`; não há guarda creative própria nesse produtor/helper. Aceitação do desgaste pertence à engine. Não há outro débito próprio de Flinging por onda ou vítima.

`B=C/5` usa divisão inteira em `@138–142`; na faixa elegível, B vai de 2 a 12. O ramo normal executa B iterações com duas tentativas de ondas por iteração. Com `q=i/B`, a origem horizontal é `posição+V×(2q)`, Y é o do usuário e lifespan é `3+trunc((1F−q)×3F)`. Yaws simétricos partem de `−atan2(V.x,V.z)×57.2957763671875D`, acrescidos de `+60−15i` e `−60+15i`. O produtor não copia V como delta de movimento da onda.

No caminho alcançável de Second Wave, nível positivo em `@460–466` adiciona **`2×max(1,B−1)` tentativas**, com espera 8 nas duas ondas de cada par. Tsunami sobrescreve **B=5 em `@149–150`**, tenta uma onda com escala 5, lifespan 20 e espera 2, e executa **`goto@244→705`**. Esse salto pula os laços normais e o reader de Second Wave; não se pode somar suas quantidades nesse caminho. Second Wave declara exclusividade com Tsunami no JSON; stacks forçadas não homologam compatibilidade.

Todos os retornos de `addFreshEntity` no release são descartados. Tentativa de criação não é inserção aceita, sobrevivência, hit aceito ou outro cast deliberado.

### Caixa de dano direto

O trecho `@705–735` constrói:

```text
AABB(usuário.position(), usuário.position()+V.scale((double)B)).inflate(1D)
B=C/5 no caminho normal; B=5 no caminho Tsunami
```

A relação crítica é **`aload9@717 → iload10@719 → i2d@721 → scale(D)@722`**. Não há literal de alcance 3 nesse argumento. A caixa alinhada aos eixos entre os dois pontos é inflada por 1 em cada direção; não é esfera, raio de dano escalar, hitbox de onda ou volume fisicamente varrido pelo usuário. A posição é consultada na fase do ataque, depois das tentativas de emissão; V continua sendo o vetor intermediário pré-lift.

`getEntitiesOfClass(LivingEntity.class,AABB)@758` produz candidatos. O laço exclui aliados por `isAlliedTo@793`, exclui o usuário por `equals@802` e requer `hasLineOfSight@811`. A fonte é **`mobAttack(usuário)@742`**, e o argumento de dano é **`(float)ACCompat.attackDamageBonus(stack)@748`**, calculado uma vez antes da iteração. O helper soma amounts de modificadores `ATTACK_DAMAGE` vistos em MAINHAND; não é aplicação completa de operações de atributos nem soma automática de todo o atributo base do usuário. Flinging não acrescenta coeficiente próprio de dano nessa chamada.

O retorno de **`hurt@824` é descartado por `pop@827`**; em seguida o fluxo pede **`stopRiding@830`** sem condicionar essa desmontagem ao booleano. Dano solicitado, dano aceito, desmontagem, knockback, kill e crédito de Mastery são resultados diferentes. O callback não gera recibo de sucesso ou deduplicação persistente de progressão.

## Consumidor WaveEntity, autoria e persistência

O novo selo liga o produtor aos corpos nativos de WaveEntity, sem recertificar os encantamentos irmãos. O construtor recebe o usuário, `setOwner` grava referência e UUID, e `getOwner` pode resolver UUID em ServerLevel. **`attackEntities` lê o campo owner diretamente**, sem chamar o getter; a existência do resolvedor não comprova reidratação automática antes do dano após reload.

As defaults sincronizadas são `SLAMMING=false`, `LIFESPAN=10`, `WAITING_TICKS=0`, `Y_ROT=0F`, `WAVE_SCALE=1F`. A onda usa sua própria AABB corrente inflada em 0.5D por eixo, diferente da caixa de liberação. `attackEntities(S)` exclui aliados à onda, DeepOneBaseEntity e, se owner estiver resolvido, o owner e seus aliados. Pede `hurt(mobProjectile(onda,campo owner),S+1F)`, descarta o resultado, pede slamming e depois knockback de magnitude `0.1D+0.5D×S`. Não utiliza um recibo de dano aceito ou trava própria persistente por vítima.

No servidor o tick chama `attackEntities` com **`S=2F×getSlamAmount(1F)+1F+getWaveScale()`**. Escala, progresso de slam, espera e contador ativo pertencem à onda; Flinging não entra nessa expressão. Espera positiva retorna cedo em ambos os lados, mas só o servidor a decrementa. Ataque, gravidade, aceleração, movimento, pedido de slam e descarte pertencem ao lifecycle nativo; lifespan não é duração final garantida de dano ou instante exato de remoção.

Os overrides NBT próprios gravam/leem diretamente somente **Owner UUID, quando existe, e Lifespan**. Não serializam ali escala, espera, yaw sincronizado, progresso de slam, contador ativo ou nível Flinging, e não chamam super nesses corpos. Isso delimita o armazenamento próprio, sem provar perda/restauração física de estado herdado, sincronização ou colisão da engine. Não completar essa fronteira com owner paralelo, reembolso, novo spawn ou replay de dano.

**N/A próprios:** Flinging não acrescenta no seu consumidor de movimento cura, efeito de status, conversão elemental, dano de novo tipo, familiar ou mutação de blocos. Não há projétil próprio do encantamento com tamanho/homing separável: as ondas compartilhadas têm contratos nativos de escala, volume, movimento e autoria. Ausência local de chamadas não certifica ausência global de custos/eventos/cooldown.

## Sete eixos, integração e contabilidade

| Eixo da rubrica | Fechamento estático | Limite mantido |
|---|---|---|
| Identidade | JAR SHA-exato, JSON, tag, classe de registro e owners compilados | Fonte 1.1.1 e outros datapacks não substituem a release |
| Comportamento | Reader capturado, carga, movimento, branches de ondas e caixa direta | Nenhum resultado físico presumido |
| Parâmetros | Níveis I–III declarados, duração72.000, clamp60, coeficientes float e B | Sem distância universal ou clamp de nível externo inventado |
| Targeting | Volume derivado de V/B, self/aliança/LOS; onda com volume/filtros próprios | PvP, claims, colisões e callbacks externos não homologados |
| Custos | Desgaste1 no ramo elegível; enchanting separado; ownership/NBT delimitados | Sem débito por onda, reembolso ou recibo de hit inventado |
| Integração | Fronteiras Black Arcana / provider / RPG Skill Tree / Enshrouded | `NOT_VERIFIED`, `NO_MUTATION`; sem adapter executável |
| Validação | Selo reproduzível, hashes/corpos/branches/pivôs, testes de evidência e índices | `NOT_TESTED` para QA física; universo do provider permanece aberto |

O certificado conclui o **contrato técnico estático individual** de Flinging. Acrescenta **+1 contrato certificado**, **+0 fichas novas**, **+0 raízes mágicas**, **+0 hooks homologados** e **+0 providers encerrados**. As oito raízes mágicas e as responsabilidades dos projetos permanecem no escopo documentado; movimento, ataque direto e ondas do mesmo uso não se tornam casts/procs/cobranças independentes.

As contagens vivas são derivadas do ledger e publicadas no [índice do provider](INDEX.md), [índice de encantamentos](enchantments/INDEX.md) e [crosswalk](ENCHANTMENT-PERK-CROSSWALK-1.0.10.md). A regressão documental verifica a igualdade entre certificados, inventário e contadores e deriva o próximo parcial da diferença entre IDs conhecidos e certificados, para impedir que um índice antigo permaneça silenciosamente desatualizado.

## Reprodução e validações

A partir da raiz do repositório, com Python3, Java21 e uma cópia local do JAR oficial:

```bash
python3 docs/qa/alexscaves_1010_flinging_causal_audit.py \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --javap /caminho/jdk-21/bin/javap \
  --output build/alexscaves-1010/flinging-causal.json

python3 docs/qa/alexscaves_1010_flinging_causal_audit_test.py -v
python3 docs/qa/alexscaves_1010_flinging_causal_cards_test.py -v
```

O [auditor dedicado](../../../../docs/qa/alexscaves_1010_flinging_causal_audit.py) verifica o selo inteiro sem mutar o JAR. O [workflow causal](../../../../.github/workflows/alexscaves-1010-flinging-causal.yml) baixa o artefato oficial e executa as verificações read-only. Os [testes semânticos/documentais](../../../../docs/qa/alexscaves_1010_flinging_causal_cards_test.py) mantêm separados os gates de movimento/servidor, o vetor pré-lift, a geometria variável, retornos descartados e as métricas derivadas do ledger. Testes sintéticos de mutação de evidência verificam rejeição; não são casos de combate físico.

**Validação local desta revisão:** a CLI read-only contra o JAR publisher exato passou com 55 corpos / 1.662 instruções / 75 branches / 442 pivôs. Os **34 testes do auditor** e os **13 testes semânticos/documentais** passaram. A regressão aplicável do repositório concluiu **1.512 testes Alex’s Caves + 165 de catálogo = 1.677 aprovados**, sem falhas, erros ou skips. Esses subconjuntos já estão incluídos no total de 1.512; não são testes adicionais somáveis. O verificador confirmou **544 índices**, sem inconsistências, e o gerador em `--check` passou. São verificações estáticas/automatizadas: não representam cliente e servidor reais com o modpack completo, nem validam hooks mutadores.

**QA física pendente:** C0/1/9/10/60, níveis0/I/II/III e externos, mãos/slot e durabilidade/creative; solo/ar/água, velocidade anterior, olhar vertical, colisões/quedas e chunks; spawn recusado, hurt recusado com desmontagem posterior, aliado/self/LOS/Deep One e montarias; ramos normal/Second Wave/Tsunami e stacks forçadas sem redefinir exclusividade; espera/lifespan/slam e vítimas repetidas; save/reload/owner órfão/dimensão; cliente/dedicado/latência, eventos, PvP/claims/datapacks; autoria e crédito único de XP/Mastery somente após resultado autorizado.
