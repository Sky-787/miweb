# 📘 Scrum + TBD Playbook
**Equipo:** Mi Web / Control de Chanchitos  
**Contexto:** Adaptación de Scrum a Trunk-Based Development (TBD) y Despliegue Continuo (CD)

---

## 1. Principios Acordados (Máximo 5)

1. **`master` siempre verde y desplegable:** La rama principal nunca se rompe; si el CI falla, arreglarlo es la máxima prioridad del equipo.
2. **Batches pequeños y ramas efímeras:** El trabajo se corta en cambios que vivan horas, nunca días ni semanas.
3. **Desacoplar Despliegue de Lanzamiento:** Desplegar código a `master` no obliga a activar la funcionalidad para el usuario final; se usan Feature Flags.
4. **Calidad automatizada antes de mergear:** Ningún código entra a `master` sin linters (Ruff) ni pruebas automatizadas (Pytest) exitosas.
5. **Responsabilidad colectiva:** Todos somos dueños del pipeline, de la salud del repositorio y de la entrega de valor.

---

## 2. Roles Adaptados

* **Product Owner (PO):**
  * Prioriza historias pequeñas (*sliceadas*) y orientadas a valor continuo.
  * Decide y gestiona el ciclo de vida de los **Feature Toggles** (cuándo activar o desactivar una funcionalidad en producción).
  * Participa activamente en el refinamiento técnico para asegurar que las historias se puedan dividir en entregas de pocas horas.

* **Developers:**
  * Responsabilidad directa sobre el código, las pruebas unitarias y el pipeline de CI.
  * Diseñan cambios compatibles hacia atrás (Dark Launching y Feature Flags).
  * **Compromiso individual del equipo:**
    > *"Hago commits y ramas que duran horas, integrando directo a master respaldado por tests automáticos y usando Feature Flags para código que aún no debe verse."*

* **Scrum Master (SM):**
  * Vela por la disciplina de integración continua diaria.
  * Elimina bloqueos que retrasen los merges y cuida el tiempo del equipo para mantener la infraestructura y el pipeline saludables.
  * Fomenta una cultura sin culpa ante incidentes, fortaleciendo la suite de pruebas.

---

## 3. Reglas de Oro de Integración a `master`

1. **Vida útil de la rama < 1 día:** Ninguna rama de trabajo vive más de unas pocas horas.
2. **Branch Protection mandatoria:** Bloquear push directo sin PR y exigir que el job de pruebas de GitHub Actions (`ci.yaml`) esté en verde.
3. **Todo cambio nuevo lleva test:** Nueva función o corrección de bug debe incluir su test unitario correspondiente en `src/test.py`.
4. **Uso de Feature Flags para trabajo en progreso:** Código no listo para el usuario final se sube apagado (Rollout 0% en ConfigCat).
5. **No acumular PRs:** Las revisiones de código se priorizan sobre el inicio de nuevas tareas para no frenar el flujo.

---

## 4. Definition of Ready (DoR) para TBD

Una historia o incremento está **READY** para entrar al sprint si cumple con los siguientes criterios obligatorios:

1. **Tamaño atómico (≤ 1 día):** Está *sliceada* de forma vertical para que su ciclo completo (código + tests + PR + merge) se complete en horas.
2. **Acceptance Criteria verificables en producción/staging:** Tiene criterios claros de aceptación que el PO o QA pueden validar inmediatamente tras el despliegue automático.
3. **Estrategia de Feature Toggle definida:** Se especifica si requiere flag, su identificador único (e.g. `feature_multiplicacion`) y su estado inicial (apagado / rollout 0%).
4. **Cero dependencias bloqueantes externas:** No depende de desarrollos paralelos no integrados. Si requiere servicios externos, se define su contrato o mock previo.
5. **Estrategia de validación acordada:** El equipo entiende qué pruebas unitarias/integración garantizan que `master` no se romperá.

---

## 5. Definition of Done (DoD)

Una tarea o historia se considera **DONE** solo si cumple con:

### Criterios Técnicos:
- [ ] Código implementado con tipado y respetando estándares de estilo (`ruff check .`).
- [ ] Pruebas unitarias escritas y pasando al 100% (`pytest test.py`).
- [ ] Integrado a `master` a través de PR con verificación automática de CI (`ci.yaml`).
- [ ] Imagen Docker construida y publicada en el registro (GHCR) sin errores.
- [ ] Si la funcionalidad aún no debe exponerse al público, queda resguardada por un Feature Flag apagado.

### Criterios de Negocio:
- [ ] Criterios de aceptación de la historia validados en el entorno desplegado.
- [ ] Product Owner informado y con control sobre el toggle de activación (rollout gradual).
- [ ] Monitoreo o logs verificados sin alertas ni regresiones.

---

## 6. Adaptación de Ceremonias y Planificación Orientada a Flujo

| Ceremonia | Adaptación a TBD + CD | Enfoque Clave |
| :--- | :--- | :--- |
| **Sprint Planning** | Se seleccionan solo historias que cumplan el DoR. Se ordenan por valor, riesgo y ventana de integración diaria (Día 1-2, 3-4, 5+). | "¿Cómo cortamos esto para poder mergear a master hoy mismo?" |
| **Daily Scrum** | En lugar del típico "¿Qué hice ayer?", el foco pasa a ser el flujo y la integración continua diaria. | "¿Qué integro hoy a master y qué necesito para que sea seguro?" |
| **Sprint Review** | Se demuestra valor real ya integrado en `master` o producción, alternando toggles en vivo en ConfigCat. | Demostración en vivo sin estrés de merge ni congelamiento de código. |
| **Retrospectiva** | Se analiza la salud del pipeline, tiempo de vida de ramas y deudas técnicas de feature flags. | "¿Cuántos flags viejos debemos retirar y cómo mejoramos el CI?" |

### Reglas de Ordenación del Sprint Backlog:
1. **Regla de oro del Día 1:** El primer ítem del Sprint Backlog debe poder integrarse a `master` durante el Día 1 o Día 2.
2. **Sprint Goal orientado a TBD:** Debe formularse garantizando valor tangible aún si los incrementos tardíos quedan detrás de flags:
   > *Formato:* "Al final del sprint los usuarios podrán [Capacidad A], mientras que [Capacidad B] permanece protegida bajo Feature Toggle en despliegue oscuro."

---

## 7. Acuerdos y Próximos Pasos (Taller 4)

1. **Filtro de Semáforo TBD en Planning:** Toda historia nueva debe evaluarse bajo los 4 criterios (Tamaño, Verticalidad, Feature Toggle, Validación en Producción) antes de subir al sprint.
2. **Desacoplamiento de Desarrollo y Lanzamiento:** La implementación técnica (`feat: código`) y la activación de negocio (`release: rollout 100%`) son tareas separadas.
3. **Gestión activa de deuda de Flags:** Al encender un flag al 100%, se planifica en el siguiente sprint la eliminación del condicional en el código.

