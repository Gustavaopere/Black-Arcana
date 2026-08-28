# Custos, cooldowns, charge e channel

## Custos

`ArcanaCost` suporta duas unidades atuais:

- `FLAT` — quantidade absoluta;
- `PERCENT_OF_MAX` — fração do máximo do recurso, limitada a `1.0`.

O resource id é textual e provider-neutral. Isso permite que uma magia use mana de um host, espíritos de outro ou outro recurso sem codificar todos os sistemas dentro da engine central.

Custos inválidos (NaN, infinito, negativo ou percentual maior que 100%) são rejeitados pela própria estrutura de dados.

## Reserva transacional

A checagem de custo acontece antes da reserva. A reserva só é `commit()` depois que o efeito foi aplicado com sucesso. Caso contrário, `refund()` é executado.

Esse detalhe é importante em integrações: consumir mana/espíritos não é o primeiro passo da conjuração.

## Cooldowns

`ArcanaCooldownSpec` associa:

- `groupId`;
- duração em ticks;
- flag `persistent`.

O limite absoluto aceito pela estrutura atual é 30 dias de ticks (`20 * 60 * 60 * 24 * 30`). É um teto de segurança, não um cooldown usado por uma magia canônica atual.

Há implementações distintas para cooldown persistente e para pools de charges, além de `CompositeCooldownService` e migrações de grupos de runtime.

## Grupos compartilhados

Como cooldown usa `groupId`, conteúdos diferentes podem ser configurados para compartilhar o mesmo grupo. Isso permite que duas ações se bloqueiem mutuamente sem precisarem ser a mesma spell id.

## Charge pools

`ChargePoolCooldownService` implementa o modelo de múltiplas cargas/recargas separado do cooldown simples persistente. A existência dessa infraestrutura não implica que todos os candidatos atuais usem charges; ela é a primitiva disponível para conteúdos futuros/registrados.

## Channel

O core possui `ArcanaChannelSpec`, `ArcanaChannelManager` e `ArcanaChannelCastCoordinator`. Channel é tratado como estado server-side próprio, e não como uma animação local que automaticamente garante o cast.

A mesma regra de autoridade permanece: manter a tecla/tela ativa no cliente não substitui validação de servidor.
