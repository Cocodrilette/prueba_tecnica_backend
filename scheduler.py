"""
Lógica de asignación y gestión de turnos.

TODO: Implementa las funciones principales del sistema.
"""

from models import Employee, Shift, Schedule


def assign_shifts(employees: list[Employee], shifts: list[Shift]) -> dict:
    """
    Asigna turnos a empleados de forma automática.
    
    Estrategia:
    1. Ordenar turnos por día y hora (lunes primero, etc.)
    2. Para cada turno, buscar empleados disponibles que:
       - Estén disponibles ese día
       - No excedan sus horas semanales
       - No tengan conflicto de horario con otros turnos asignados
    3. Priorizar empleados con menos horas acumuladas (para balancear)
    4. Asignar hasta alcanzar required_employees o hasta que no haya más disponibles
    
    Args:
        employees: Lista de empleados disponibles
        shifts: Lista de turnos a asignar
        
    Returns:
        dict con estructura:
        {
            'schedule': Schedule object con las asignaciones,
            'warnings': [lista de strings con problemas encontrados],
            'employee_hours': {employee_id: total_hours_asignadas}
        }
        
    Ejemplo de warning:
        "Shift 3 (tuesday 8:00) tiene solo 1 empleado asignado, necesita 2"
    """
    # TODO: Implementar
    
    schedule = Schedule()
    warnings = []
    employee_hours = {emp.id: 0 for emp in employees}
    
    # Tu código aquí
    
    return {
        'schedule': schedule,
        'warnings': warnings,
        'employee_hours': employee_hours
    }


def swap_shifts(
    schedule: Schedule,
    employee1_id: int,
    employee2_id: int,
    shift_id: int,
    employees: list[Employee],
    shifts: list[Shift]
) -> dict:
    """
    Intenta intercambiar asignaciones: employee1 toma el turno de employee2.
    
    Proceso:
    1. Verificar que employee2 esté asignado al turno
    2. Verificar que employee1 cumpla todas las restricciones para ese turno:
       - Esté disponible ese día
       - No exceda horas máximas semanales
       - No tenga conflicto de horario
    3. Si todo es válido, hacer el intercambio
    4. Si no es válido, retornar la razón del fallo
    
    Args:
        schedule: Horario actual
        employee1_id: ID del empleado que quiere tomar el turno
        employee2_id: ID del empleado que tiene el turno actualmente
        shift_id: ID del turno a intercambiar
        employees: Lista de todos los empleados (para validar restricciones)
        shifts: Lista de todos los turnos (para validar horarios)
        
    Returns:
        dict con estructura:
        {
            'success': bool,
            'message': str (explicación del resultado),
            'updated_schedule': Schedule (solo si success=True, None si no)
        }
        
    Ejemplos de mensajes:
        - Success: "Intercambio realizado exitosamente"
        - Failure: "Employee 2 no está asignado al turno 5"
        - Failure: "Employee 1 no está disponible el monday"
        - Failure: "Employee 1 excedería sus horas máximas (40h)"
    """
    # TODO: Implementar
    
    # Pistas:
    # - Necesitas buscar el objeto Employee por su id
    # - Necesitas buscar el objeto Shift por su id
    # - Necesitas calcular las horas actuales del employee1
    # - Necesitas verificar solapamientos con otros turnos de employee1
    
    return {
        'success': False,
        'message': 'No implementado',
        'updated_schedule': None
    }


# ============================================================================
# FUNCIONES AUXILIARES (OPCIONALES)
# ============================================================================
# Puedes agregar funciones auxiliares aquí para hacer tu código más limpio

def _get_employee_by_id(employees: list[Employee], employee_id: int) -> Employee:
    """Helper: Busca un empleado por ID."""
    # TODO: Implementar si lo necesitas
    pass


def _get_shift_by_id(shifts: list[Shift], shift_id: int) -> Shift:
    """Helper: Busca un turno por ID."""
    # TODO: Implementar si lo necesitas
    pass


def _calculate_total_hours(schedule: Schedule, employee_id: int, shifts: list[Shift]) -> int:
    """Helper: Calcula horas totales asignadas a un empleado."""
    # TODO: Implementar si lo necesitas
    pass


def _has_schedule_conflict(schedule: Schedule, employee_id: int, new_shift: Shift, shifts: list[Shift]) -> bool:
    """Helper: Verifica si un nuevo turno genera conflicto de horario."""
    # TODO: Implementar si lo necesitas
    pass


def _day_order() -> dict:
    """Helper: Retorna orden de días para ordenamiento."""
    return {
        'monday': 1,
        'tuesday': 2,
        'wednesday': 3,
        'thursday': 4,
        'friday': 5,
        'saturday': 6,
        'sunday': 7
    }
