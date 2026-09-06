# Integração mágica com Immersive Portals

## Estado

`DESIGN / PROVIDER PRESENTE — integração ampliada ainda não implementada pelo Black Arcana`

## Providers instalados relevantes

O pack já possui Immersive Portals através do stack Immersive Aeronautics/Immersive Portals, True Immersion e o addon `Immersive Portal - Iron's Spells 'n Spellbooks Addon`. O addon existente já converte o Portal Spell do Iron's em portal contínuo do Immersive Portals e deve ser reutilizado antes de qualquer implementação paralela.

## Regra principal

Immersive Portals é o backend preferencial de **apresentação e travessia contínua** para spells de portal compatíveis. Ele não substitui:

- custo e casting do provider;
- ownership do cast;
- proteção/claims;
- safe destination;
- world border;
- loaded-chunk policy;
- cooldown;
- anti-abuso;
- lifecycle do spell.

## Pipeline pretendido

`Iron's/Black Arcana cast request`
→ validar custo/gates/authority
→ resolver dois endpoints
→ aplicar Stage 04 protection + 07.04 Safe Destination quando pertinente
→ confirmar chunks/dimensões permitidos
→ criar sessão de portal bounded
→ pedir ao adapter Immersive Portals a superfície/travessia visual
→ manter lifecycle server-authoritative
→ destruir os endpoints ao expirar/invalidar.

Nenhum spell pode usar o renderer de portal como prova de que uma travessia é autorizada.

## Uso por escola

### Ordem

Portais estáveis, geométricos, precisos e previsíveis. Círculos/mandalas podem formar o frame antes da abertura. Ideal para paired gates, retorno, transposição e contenção espacial.

### Caos

Rasgos irregulares e instáveis podem usar a mesma autoridade espacial, mas com apresentação assimétrica. Instabilidade visual não autoriza destino aleatório inseguro.

### Divina

Portais/limiares luminosos devem ser raros e ligados a sanctums, marcas consagradas ou locais previamente autorizados, não teleporte global gratuito.

### Infernal

Fendas infernais podem conectar locais válidos, mas o design do combustível infernal não permite transportar a própria Lava Infernal para fora do Nether. Um portal não é loophole para fluid transport ou cross-dimensional source draining.

## Segurança

- nunca force-load de chunk para satisfazer portal mágico;
- revalidar destino antes de travessia quando o provider permitir estado mutável;
- não criar portal dentro de bloco/fluido/claim proibido;
- respeitar dimensão e world border;
- limitar quantidade de portais por caster/servidor e duração;
- limpar sessões em logout, unload, shutdown ou invalidação;
- impedir loops infinitos e recursão de portais quando possível pela API;
- falhar fechado se a bridge/API requerida não estiver disponível.

## Visual

O portal deve mostrar o destino real quando o backend suportar isso. Frames mágicos, partículas e shaders são camada adicional. O objetivo é evitar o efeito vanilla de 'tela + teleporte' quando uma travessia contínua segura puder ser usada.

## Validação necessária antes de implementação ampliada

- API/hook exato da versão instalada do addon/Immersive Portals;
- criação/remoção segura de portal por servidor;
- suporte a dimensões e orientação;
- lifecycle após chunk unload/restart;
- compat com Sable/Aeronautics;
- compat com Epic Fight/casting;
- impacto de performance e recursion depth;
- dedicated server e multiplayer.
