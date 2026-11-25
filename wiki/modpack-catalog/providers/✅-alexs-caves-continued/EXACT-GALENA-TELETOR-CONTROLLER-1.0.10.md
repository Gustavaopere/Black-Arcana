# Galena Gauntlet — distinção de controllers Player e Teletor (publisher 1.0.10)

**DISCOVERY_ONLY / NO_MUTATION.** Modlist sibling identifica #019 Alex's Caves Continued 1.0.10, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, Minecraft 1.21.1/Java 21, NeoForge físico declarado 21.1.250. Publisher SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. Dump instalado e classe transformada não comparados.

## Evidência existente relida

[Run 44934418449, job 136937828915](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44934418449/job/136937828915), relatório 1.780.492 bytes SHA-256 `c91a48f9892be09c4ab951c8083703b0c5ffbb026fc43e7d808c2033dde8bba9`, [manifesto](EXACT-GALENA-GAUNTLET-DISCOVERY-1.0.10.json). Os pivôs de tick distinguem a ramificação Teletor @170/173 da ramificação Player @471/474. O ramo Teletor consulta getTarget @217, solicita setWeaponUUID @203, grava CONTROLLER_ID @195 e TARGET_ID @254; contém getWeaponPosition @295, hurtEntity @382 e directMovementTowards @415 com 0.1F. Constantes 32D @398 e 2.5F @423 aparecem em comparações de comprimento e proximidade, não no raycast do jogador. Não inferir fluxo completo, autoria ou distância de dano a partir de pivôs isolados.

getController consulta UUID no servidor @11 e ServerLevel.getEntity(UUID) @31; a outra rota usa CONTROLLER_ID e Level.getEntity(int) @66. Referência de controller não garante disponibilidade do owner em outro nível/reload. Não aplicar perk de jogador à rota Teletor nem contar tentativa de hurt como Mastery.

## Coleta nova

A [sonda](../../../../docs/qa/alexscaves_1010_galena_teletor_controller_probe.py) exige publisher e classfile MagneticWeaponEntity pinados, Code hash de tick e instruction digests de quatro métodos. Projeta branches, membros tipados, operandos e referências de controller. Examina somente a classe Teletor identificada em callsites do próprio tick, suas declarações diretamente referenciadas e métodos que solicitam métodos da arma ou acessam os campos encontrados nas declarações diretas. Declarações ausentes são registradas, não substituídas por API presumida. Seleção delimitada não demonstra censo integral de IA, reflexão ou hierarquia externa. O workflow exige replay idêntico; primeira execução pendente.

[Contexto player](EXACT-GALENA-GAUNTLET-PLAYER-TARGETING-1.0.10.md) · [ficha](equipment/galena-gauntlet.md). Nenhum novo certificado, cast, hook, mutação, QA física ou mudança de índice. Não promover até inspeção da saída e selo SHA-exato na HEAD final.

## Regressão do auditor e correção delimitada

[Run 45541111082, job 138959564511](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45541111082/job/138959564511), HEAD `3e81029e291404f3c4b55b8059234a85a611bc77`: a coleta falhou em MagneticWeaponEntity.tick porque o decodificador compartilhado rejeita mais de 180 referências tipadas por invocação. Não é falha de gameplay. A correção mantém esse limite, particiona as instruções em blocos de até 120 e exige igualdade da lista de offsets resultante com todos os sites selecionáveis do corpo integral. Para métodos largos sem handlers, o CFG normal é reconstruído sobre o corpo original com validação de todos os destinos; métodos pequenos usam a projeção anterior, verificando igualdade da coleta. O teste sintético isolado de 181 sites reproduziu RED (exit 1, bounded typed member census) e GREEN (exit 0, roster integral, entrada vazia e CP inválido rejeitado). O teste da sonda real e o replay SHA-exato na CI ainda são necessários; não se afirma aprovação da HEAD corrigida. Não há alteração da biblioteca compartilhada nem de seus gates.

## Resultado do replay e selo

[Run 45544346069, job 138970221560](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45544346069/job/138970221560), HEAD `d843f1e611860ef5c362a4a438312833087a3db2`: sete self-checks, dois relatórios byte a byte iguais, 233.786 bytes, SHA-256 `a882a1870a5dce6a190005f83281d3876db815025fd5ce0c96c568fda446874e`. O workflow consolidado fixa tamanho e hash; sua nova execução é gate distinto. A sonda registra 4 métodos de MagneticWeaponEntity e 9 de TeletorEntity. Tick da arma: 744 instruções, 234 referências tipadas, 82 branches e zero handlers próprios. TeletorEntity SHA-256 `fa8c02bb83b9f3e267d194bd83d0690e5668e3d414499bb357575ab2f88127f1`, superclasse Monster; getId/getTarget não são declarações locais dessa classe.

### Separação causal dos controllers

- O tick consulta controller e target antes da atualização de TARGET_ID. No servidor a arma solicita noPhysics quando comingBack ou quando controller Teletor e target ausente/morto; a remoção é solicitada para stack vazia ou controller ausente após tickCount >20. Se hadPlayerController, chama plopItem e limpa a flag antes da remoção. O progresso de strike decai por max(0, progress - 0.1F) sob gates de target ausente, retorno ou cooldown positivo, se progress >0.
- Ramo Teletor: grava CONTROLLER_ID @195 e solicita setWeaponUUID @203. No servidor consulta Teletor.getTarget @217 e sincroniza ID de alvo vivo ou -1 @254. A referência local de target veio da leitura anterior; não confundir escrita do ID com confirmação de novo alvo no mesmo tick. Destino é eyePosition do target anterior quando vivo e não retornando, senão Teletor.getWeaponPosition @295. O vetor q é destino menos posição da arma @306.
- Quando target não nulo e não retornando, IDLING=false; se |q| < largura do target +1, strikeProgress <1 solicita max(0,progress+0.35F), senão chama hurtEntity @382 e marca comingBack @387. Fora do contato, |q|>32 @398/402 marca retorno. directMovementTowards @415 recebe 0.1F. Se distância ao controller <2.5 @426 e Y da arma acima do controller @438, marca IDLING e limpa comingBack. O ramo salta para @1554, não percorre o targeting Player @471. 32 e 2.5 não são alcance de magia do jogador, AOE ou distância garantida de dano.

### Criação, vínculo e drop do Teletor

| Método local | Evidência causal delimitada |
|---|---|
| finalizeSpawn | Code SHA `4d765f57cd3a45bc1a567345bfcd3180a3c730bd4cedea3ad9d97d5ec58412fb`; createItemStack(random) @31; chance declarada randomFloat < 0.25F*(specialMultiplier+0.5F); nível solicitado a enchantRandomly @104 é int(5F+specialMultiplier*nextInt(18)); stack @113, posição @122, UUID controller @131, UUID arma @140, addFreshEntity @149. Não garante spawn aceito. |
| getWeaponPosition | Code SHA `f0b1b5a2e2a18cfdcc33279e1bcfe00adefa7127d3e1776ac9ecc00e63462c5b`; eyePos + (0, 1.399999976158142 - sin(double(float(tickCount)*0.1F))*0.20000000298023224, 0). É destino oscilante, não hitbox. |
| dropEquipment | Code SHA `2410cb1da01b27dd84eca95c782d32ffc677a648595c8d538ae731e3d028208d`; após super, exige tipo de arma; para stack não vazia, sem vanishing e randomFloat < equipmentDropChance(mainhand), ajusta damageable de maxDamage M a M - nextInt(1+nextInt(max(M-3,1))), solicita spawnAtLocation @112. Remoção KILLED @120 não depende da chance de drop. Sem recibo de entrega. |
| getWeapon | Code SHA `ac26f255a6654ecae05b8d2843af0e6d9d28d6c6190a6e5b7ba87fd3c17219c0`; server lookup UUID no ServerLevel; client WEAPON_ID, -1 retorna null. getController da arma usa ControllerUUID/CONTROLLER_ID. |
| tick | Code SHA `e25f15bf958c4da3aa130f595f0412f75c3c0eef4a0a7a2304c6c630e80995ae`; sincroniza ID/UUID sob instanceof, controlProgress +1 com alvo vivo e <5, -1 sem alvo vivo e >0. Não assumir clamp de estado prévio adulterado. |

Esses são parâmetros e chamadas do produtor Teletor, não perks/atributos de Player. Não transferir chance de enchant, drop, alcance ou autoria. Sem execução física, mutação, certificado individual novo ou mudança de numerador.
