"""
Ejemplos de uso del sistema de gestión de turnos.

Este archivo contiene datos de ejemplo y demuestra cómo usar el sistema.
NO es necesario modificar este archivo.

Ejecutar: python examples.py
"""

from models import Employee, Shift, Schedule
from scheduler import assign_shifts, swap_shifts


def print_section(title):
    """Helper para imprimir secciones."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def example_data():
    """Retorna datos de ejemplo."""
    
    employees = [
        Employee(1, "Ana", max_hours_per_week=40, unavailable_days={'sunday'}),
        Employee(2, "Bob", max_hours_per_week=30, unavailable_days={'monday', 'friday'}),
        Employee(3, "Carlos", max_hours_per_week=40, unavailable_days=set()),
        Employee(4, "Diana", max_hours_per_week=20, unavailable_days={'saturday', 'sunday'}),
    ]
    
    shifts = [
        Shift(1, 'monday', start_hour=8, duration_hours=8, required_employees=2),
        Shift(2, 'monday', start_hour=16, duration_hours=6, required_employees=1),
        Shift(3, 'tuesday', start_hour=8, duration_hours=8, required_employees=2),
        Shift(4, 'tuesday', start_hour=14, duration_hours=4, required_employees=1),
        Shift(5, 'wednesday', start_hour=8, duration_hours=8, required_employees=2),
        Shift(6, 'thursday', start_hour=8, duration_hours=6, required_employees=1),
        Shift(7, 'friday', start_hour=8, duration_hours=8, required_employees=2),
    ]
    
    return employees, shifts


def main():
    """Función principal con ejemplos."""
    
    print_section("SISTEMA DE GESTIÓN DE TURNOS - EJEMPLOS")
    
    # Obtener datos de ejemplo
    employees, shifts = example_data()
    
    # Mostrar empleados
    print_section("EMPLEADOS DISPONIBLES")
    for emp in employees:
        unavailable = ', '.join(emp.unavailable_days) if emp.unavailable_days else 'ninguno'
        print(f"  {emp.name} (ID: {emp.id})")
        print(f"    - Horas máximas: {emp.max_hours_per_week}h/semana")
        print(f"    - Días no disponibles: {unavailable}")
        print()
    
    # Mostrar turnos
    print_section("TURNOS A ASIGNAR")
    for shift in shifts:
        print(f"  Turno {shift.id}: {shift.day.capitalize()}")
        print(f"    - Horario: {shift.start_hour}:00 - {shift.end_hour()}:00 ({shift.duration_hours}h)")
        print(f"    - Empleados necesarios: {shift.required_employees}")
        print()
    
    # Ejecutar asignación
    print_section("EJECUTANDO ASIGNACIÓN AUTOMÁTICA")
    print("Procesando...")
    
    try:
        result = assign_shifts(employees, shifts)
        
        # Mostrar resultados
        print_section("RESULTADOS DE LA ASIGNACIÓN")
        
        schedule = result['schedule']
        assignments = schedule.get_all_assignments()
        
        if not assignments:
            print("  ⚠️  No se realizaron asignaciones (implementación pendiente)")
        else:
            print("\nAsignaciones por turno:")
            for shift_id, employee_ids in assignments.items():
                shift = next(s for s in shifts if s.id == shift_id)
                print(f"\n  Turno {shift_id} ({shift.day.capitalize()} {shift.start_hour}:00):")
                for emp_id in employee_ids:
                    emp = next(e for e in employees if e.id == emp_id)
                    print(f"    - {emp.name}")
        
        # Mostrar horas por empleado
        print("\n" + "-"*70)
        print("Horas asignadas por empleado:")
        for emp_id, hours in result['employee_hours'].items():
            emp = next(e for e in employees if e.id == emp_id)
            print(f"  {emp.name}: {hours}h / {emp.max_hours_per_week}h")
        
        # Mostrar warnings
        if result['warnings']:
            print_section("⚠️  ADVERTENCIAS")
            for warning in result['warnings']:
                print(f"  • {warning}")
        else:
            print("\n✓ Sin advertencias - todas las asignaciones son válidas")
        
        # Ejemplo de swap (si está implementado)
        print_section("EJEMPLO DE INTERCAMBIO DE TURNOS")
        print("Intentando intercambiar turno 1 entre Ana y Bob...")
        
        swap_result = swap_shifts(
            schedule=result['schedule'],
            employee1_id=2,  # Bob
            employee2_id=1,  # Ana
            shift_id=1,
            employees=employees,
            shifts=shifts
        )
        
        if swap_result['success']:
            print(f"  ✓ {swap_result['message']}")
        else:
            print(f"  ✗ {swap_result['message']}")
            
    except NotImplementedError:
        print("  ⚠️  Funcionalidad aún no implementada")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*70)
    print("  Fin de los ejemplos")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
