# Galena Gauntlet — movimento e registro da arma magnética (1.0.10)

**DISCOVERY_ONLY / NO_MUTATION.** Publisher exato: SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`, 75.279.314 bytes. Modlist sibling `18144e8318978b8904b584b80b4ddd630f22f8f0`, #019 Alex's Caves Continued, #001 NeoForge 21.1.250. Sem dump físico novo.

A ficha [Galena Gauntlet](equipment/galena-gauntlet.md) já distingue raycast, contato, busca de instâncias, dano, mineração e devolução. A lacuna deste complemento é movimento vetorial, referência da mão, progresso interpolado e factory da entidade; não reexecuta a auditoria de dano.

## Evidência existente relida

[Run 44934418449, job 136937828915](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44934418449/job/136937828915), relatório SHA-256 `c91a48f9892be09c4ab951c8083703b0c5ffbb026fc43e7d808c2033dde8bba9`. Manifesto local `EXACT-GALENA-GAUNTLET-DISCOVERY-1.0.10.json` fixa 24 métodos da entidade. Pivôs observados em directMovementTowards: position @2, subtract @5, length @10, normalize @19, atan2 @31/@50, approachDegrees @94/@110 com argumento 5F, setXRot @97, setYRot @113, getDeltaMovement @118, scale @124, add @127, setDeltaMovement @130. Não deduzir velocidade física a partir desses callsites.

getControllerHandPos: interpola yBodyRotO/yBodyRot @9; teste de identidade da stack da MAIN_HAND @31; fatores ±0,75F, 0,68F e −0,1F; yRot @88, view vector normalizado e scale(0,75D) @104; getPosition @111, add @116/@121. Ordem aritmética e ramos serão projetados individualmente.

## Nova coleta

A sonda `docs/qa/alexscaves_1010_galena_movement_probe.py` fixa hashes dos dois classfiles e os sete instruction digests do manifesto anterior. Examina seis corpos pequenos, janelas delimitadas de calls de movimento dentro de tick, e factory/registro via bootstrap. As janelas não representam todo o tick. Duas execuções idênticas são exigidas; primeiro resultado ainda pendente. Nenhuma execução do jogo, alteração de dados, novo certificado ou raiz semântica.
