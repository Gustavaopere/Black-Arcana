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
