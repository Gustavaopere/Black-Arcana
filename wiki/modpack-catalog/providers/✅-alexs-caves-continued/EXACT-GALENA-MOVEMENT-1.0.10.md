# Galena Gauntlet — movimento e registro da arma magnética (1.0.10)

**DISCOVERY_ONLY / NO_MUTATION.** Publisher exato: SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`, 75.279.314 bytes. Modlist sibling `18144e8318978b8904b584b80b4ddd630f22f8f0`, #019 Alex's Caves Continued, #001 NeoForge 21.1.250. Sem dump físico novo.

A ficha [Galena Gauntlet](equipment/galena-gauntlet.md) já distingue raycast, contato, busca de instâncias, dano, mineração e devolução. A lacuna deste complemento é movimento vetorial, referência da mão, progresso interpolado e factory da entidade; não reexecuta a auditoria de dano.

## Evidência existente relida

[Run 44934418449, job 136937828915](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44934418449/job/136937828915), relatório SHA-256 `c91a48f9892be09c4ab951c8083703b0c5ffbb026fc43e7d808c2033dde8bba9`. Manifesto local `EXACT-GALENA-GAUNTLET-DISCOVERY-1.0.10.json` fixa 24 métodos da entidade. Pivôs observados em directMovementTowards: position @2, subtract @5, length @10, normalize @19, atan2 @31/@50, approachDegrees @94/@110 com argumento 5F, setXRot @97, setYRot @113, getDeltaMovement @118, scale @124, add @127, setDeltaMovement @130. Não deduzir velocidade física a partir desses callsites.

getControllerHandPos: interpola yBodyRotO/yBodyRot @9; teste de identidade da stack da MAIN_HAND @31; fatores ±0,75F, 0,68F e −0,1F; yRot @88, view vector normalizado e scale(0,75D) @104; getPosition @111, add @116/@121. Ordem aritmética e ramos serão projetados individualmente.

## Nova coleta

A sonda `docs/qa/alexscaves_1010_galena_movement_probe.py` fixa hashes dos dois classfiles e os sete instruction digests do manifesto anterior. Examina seis corpos pequenos, janelas delimitadas de calls de movimento dentro de tick, e factory/registro via bootstrap. As janelas não representam todo o tick. Duas execuções idênticas são exigidas; primeiro resultado observado abaixo. Nenhuma execução do jogo, alteração de dados, novo certificado ou raiz semântica.

## Resultado observado e reprodução

[Run 45525982648, job 138909294764](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45525982648/job/138909294764), HEAD `9eb628fd0c269f14417f2ef5a82bf60b811381d8`: quatro checks de janela/escopo, sete métodos, dois classfiles pinados e factory ligada ao registry. Relatório 94.727 bytes SHA-256 `1cc3b211a9ae87de6ef4cd58e179bb72b8edc4f0cb3e54adb300eda3046e34a7`; replay idêntico. O workflow fixa agora o selo; exige CI final.

### Fórmula vetorial e apresentação

- directMovementTowards (Code `63155115b01f4db70031477d88fe31b4fb6f4cd07f32d9b4b0fd7d1e2789b821`): seja q = destino − position. Se |q|>1, normaliza; caso contrário conserva o vetor. Solicita v'=v+q*s após essa condição, s é o argumento float promovido a double. Não é velocidade constante nem distância percorrida. Pitch desejado = −atan2(q.y, horizontalDistance(q)) × 57.2957763671875; yaw = −atan2(q.x,q.z) × mesmo fator. Em idling substitui pitch desejado pelo atual e yaw desejado pelo atual+5. Em ambos aplica approachDegrees com passo 5F. Nenhuma autoridade de dano deriva dessas rotações.
- getControllerHandPos (Code `55666893b3cfbc1cd5a13bb0e99ac05572fc706732a0cbbcba31cf0492140e99`): interpola yaw corporal anterior/atual com partialTick; m = identidade Gauntlet na MAIN_HAND. Vetor local (width×(m?−0,75F:0,75F), height×0,68F, width×−0,1F), yRot de −yaw em radianos; soma posição interpolada do player e 0,75D×viewVector(partialTick).normalize(). Não é raycast e não consulta handedness nesse corpo.
- getReturnProgress e getStrikeProgress calculam prev + (current−prev)×partialTick, sem clamp local (Code `b6eec4318cbe2ee6027a05c7c9bc841a35c001b6a244fafd158542b5fe37d8a1` e `591c8a28bd83fd9baaceac675ae4fd3b66085cc9f939c10a0e553dd53910c6cc`). isIdling lê accessor IDLING.
- tick: quatro sites de movimento nas janelas: directMovementTowards @415 com s=0,1F, no ramo Teletor; @1551 usa variável local de destino e velocidade, condicionado a destino não nulo; move(MoverType.SELF,getDeltaMovement()) @1579; depois escala delta por 0,8999999761581421D @1587–1593. Constantes corroboradas pelo log anterior 136937828915. As janelas não fecham todos os ramos que definem a variável de velocidade @1551. A colisão, transformação e deslocamento efetivo não foram observados.

### Factory e registry

ACEntityRegistry.lambda$static$4 Code `abdc9c05851540ce3ce06ca508ac287c4c3d52d51ca9b3802f15ee2c4f854138`: MISC, sized(0,5F,0,5F) @17, setUpdateInterval(1) @21, setShouldReceiveVelocityUpdates(true) @25, clientTrackingRange(20) @30, id/build @36/39. <clinit> literal magnetic_weapon @95, bootstrap @98, register @103, MAGNETIC_WEAPON @106. Reuso da ligação distribuída de EntityType/Builder no [dossiê defaults](EXACT-ITEM-ENTITY-DEFAULTS-21.1.250.md): tracking supplier padrão lê campo bruto, clientTrackingRange(I) escreve o campo; lambdas de atualização e velocidade retornam os valores capturados. Valores nominais 20/1/true. Não equiparar tracking 20, dimensão 0,5, raio da busca de instâncias 64 e alcance do raycast.

Sem novo certificado, hook ou QA. `NO_MUTATION`.
