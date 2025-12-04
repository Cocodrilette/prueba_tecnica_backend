# Sistema de Gestión de Turnos - Prueba Técnica

## Contexto
Necesitas implementar un sistema que asigne turnos de trabajo a empleados considerando sus disponibilidades y restricciones laborales.

## Tiempo límite
**2 horas**

## Estructura del proyecto
```
shift_scheduler/
├── README.md          (este archivo)
├── models.py          (clases base - COMPLETAR)
├── scheduler.py       (lógica de asignación - IMPLEMENTAR)
├── test_scheduler.py  (tests - NO MODIFICAR)
└── examples.py        (datos de ejemplo - NO MODIFICAR)
```

## Tareas a realizar

### Parte 1: Clases Básicas (30 minutos)
Completa las clases en `models.py`:

- **Employee**: Representa un empleado con sus restricciones
- **Shift**: Representa un turno de trabajo
- **Schedule**: Mantiene las asignaciones de turnos

### Parte 2: Algoritmo de Asignación (50 minutos)
Implementa en `scheduler.py`:

```python
def assign_shifts(employees, shifts) -> dict
```

Debe retornar un diccionario con:
- `schedule`: asignaciones realizadas
- `warnings`: lista de problemas encontrados
- `employee_hours`: horas totales por empleado

**Reglas de negocio:**
1. Un empleado NO puede trabajar en días marcados como no disponibles
2. Un empleado NO puede exceder sus horas máximas semanales
3. Un empleado NO puede tener turnos que se solapen en horario
4. Cada turno debe intentar tener el número requerido de empleados

**Estrategia sugerida:**
- Ordenar turnos por día y hora
- Para cada turno, asignar empleados disponibles
- Priorizar empleados con menos horas acumuladas (balance)

### Parte 3: Función de Intercambio (30 minutos)
Implementa en `scheduler.py`:

```python
def swap_shifts(schedule, employee1_id, employee2_id, shift_id) -> dict
```

Permite que employee1 tome el turno de employee2.

Debe validar:
- employee2 está asignado a ese turno
- employee1 cumple restricciones para ese turno
- El intercambio no viola ninguna regla

## Cómo ejecutar

```bash
# Ejecutar tests
python test_scheduler.py
```

## Criterios de evaluación

- **Lógica (40%)**: Algoritmo funciona correctamente, maneja casos básicos
- **Código (35%)**: Legibilidad, estructura, buenas prácticas
- **Validaciones (25%)**: Verifica restricciones, manejo de errores

## Notas importantes

- Puedes usar solo la biblioteca estándar de Python
- Comenta decisiones de diseño importantes
- Si algo no está claro, haz suposiciones razonables y documéntalas
- La claridad del código es tan importante como que funcione

## Preguntas frecuentes

**¿Puedo agregar métodos adicionales a las clases?**
Sí, siéntete libre de agregar lo que necesites.

**¿Qué hago si no hay suficientes empleados para un turno?**
Asigna los que puedas y agrega un warning.

**¿Cómo manejo los horarios que se solapan?**
Dos turnos se solapan si están el mismo día y sus horas se cruzan.

**¿Qué pasa si termino antes?**
Agrega más tests, mejora el algoritmo, o implementa funcionalidad extra.

¡Buena suerte!
