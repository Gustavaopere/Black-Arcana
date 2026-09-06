# Loadout, radial, atalhos e HUD

## Teclas padrão

Todas as teclas são rebindable.

| Ação | padrão atual |
|---|---|
| abrir radial | `R` |
| conjurar selecionado | `V` |
| editar loadout | sem tecla atribuída |
| quick cast 1–8 | sem tecla atribuída |

Os oito quick slots vêm **desvinculados por padrão** para reduzir conflitos em modpacks grandes.

## Radial

O radial é client-only e serve para seleção. Selecionar uma magia no radial não equivale a autorizar/executar o efeito no servidor.

A preferência `radialBehavior` aceita:

- `TOGGLE` — abre e permanece até seleção/fechamento;
- `HOLD` — fecha quando a tecla do radial é solta.

O padrão é `TOGGLE`.

## Loadout

O loadout é persistente e as edições passam por payloads C2S/S2C limitados e validação de servidor. A tela local trabalha sobre um draft, mas o estado aceito é o estado autoritativo retornado/sincronizado pelo servidor.

## HUD contextual

Não existe barra permanente de recurso do Black Arcana no Stage 05. O HUD é contextual e pode exibir seleção e feedback de cast.

Preferências atuais:

| Opção | padrão | faixa/valores |
|---|---:|---|
| `contextualHud` | `true` | liga/desliga HUD contextual |
| `hudScale` | `1.0` | 0.5–2.0 |
| `hudAnchor` | `BOTTOM_CENTER` | anchors de `HudLayout` |
| `selectionDurationTicks` | 60 | 0–400 |
| `feedbackDurationTicks` | 80 | 0–400 |
| `feedbackLevel` | `STANDARD` | MINIMAL / STANDARD / VERBOSE |
| `radialBehavior` | `TOGGLE` | TOGGLE / HOLD |
| `particleDensity` | 1.0 | 0.0–1.0 |
| `reducedMotion` | `false` | boolean |
| `reducedFlashes` | `false` | boolean |

### Densidade de feedback

- `MINIMAL`: prioriza recusas;
- `STANDARD`: inclui seleção;
- `VERBOSE`: inclui também feedback de sucesso.

## Preferências que ainda são reservas de apresentação

`particleDensity`, `reducedMotion` e `reducedFlashes` são client-only e explicitamente não alteram o efeito no servidor. Algumas existem agora para preparar efeitos visuais futuros; a presença da opção não significa que todo tipo de partícula, movimento de câmera ou flash já esteja implementado.

## Reconexão

O client cache é limpo no disconnect. Isso evita que um jogador reconectando com o mesmo UUID veja seleção/loadout/presentation stale da sessão anterior antes da sincronização nova.
