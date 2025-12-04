"""
Tests para el sistema de gestión de turnos.
"""

import unittest
from models import Employee, Shift, Schedule
from scheduler import assign_shifts, swap_shifts


class TestShiftScheduler(unittest.TestCase):
    """Tests para la asignación de turnos."""
    
    def setUp(self):
        """Preparación antes de cada test."""
        # Puedes definir empleados y turnos comunes aquí
        pass
    
    def test_basic_assignment(self):
        """
        Test 1: Caso básico - asignación exitosa

        Escenario:
        - 3 empleados con suficiente disponibilidad
        - Varios turnos a asignar
        - Verificar que se asignen correctamente
        """
        # Arrange (preparar datos)
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

        # Act (ejecutar función)
        result = assign_shifts(employees, shifts)

        # Assert (verificar resultados)
        self.assertIsNotNone(result, "assign_shifts debe retornar un resultado")
        self.assertIn('schedule', result, "El resultado debe contener 'schedule'")
        self.assertIn('warnings', result, "El resultado debe contener 'warnings'")
        self.assertIn('employee_hours', result, "El resultado debe contener 'employee_hours'")

        schedule = result['schedule']
        self.assertIsNotNone(schedule, "schedule no puede ser None")

        # Verificar que se realizaron asignaciones
        all_assignments = schedule.get_all_assignments()
        self.assertIsInstance(all_assignments, dict, "get_all_assignments debe retornar un diccionario")

        # Verificar que al menos algunos turnos tienen empleados asignados
        total_assignments = sum(len(emps) for emps in all_assignments.values())
        self.assertGreater(total_assignments, 0, "Debe haber al menos una asignación realizada")

        # Verificar que employee_hours es un diccionario
        self.assertIsInstance(result['employee_hours'], dict, "employee_hours debe ser un diccionario")
    
    def test_max_hours_restriction(self):
        """
        Test 2: Restricción de horas máximas

        Escenario:
        - Empleado con max_hours_per_week = 10
        - Múltiples turnos que suman más de 10 horas
        - Verificar que no se exceda el límite
        """
        # Arrange: Empleado con pocas horas disponibles
        employees = [
            Employee(1, "Ana", max_hours_per_week=10, unavailable_days=set()),
            Employee(2, "Bob", max_hours_per_week=40, unavailable_days=set()),
        ]

        # Múltiples turnos que suman más de 10 horas
        shifts = [
            Shift(1, 'monday', start_hour=8, duration_hours=6, required_employees=1),
            Shift(2, 'tuesday', start_hour=8, duration_hours=6, required_employees=1),
            Shift(3, 'wednesday', start_hour=8, duration_hours=6, required_employees=1),
        ]

        # Act
        result = assign_shifts(employees, shifts)

        # Assert
        self.assertIsNotNone(result)
        employee_hours = result['employee_hours']

        # Ana (employee 1) no debe exceder 10 horas
        if 1 in employee_hours:
            self.assertLessEqual(employee_hours[1], 10,
                               f"Ana no debe exceder 10 horas, pero tiene {employee_hours[1]} asignadas")

        # Verificar que el sistema respeta la restricción
        schedule = result['schedule']
        ana_shifts = schedule.get_shifts_for_employee(1)
        total_hours = sum(s.duration_hours for s_id in ana_shifts
                         for s in shifts if s.id == s_id)
        self.assertLessEqual(total_hours, 10,
                           "Las horas totales de Ana deben ser <= 10")
    
    def test_unavailable_day(self):
        """
        Test 3: Empleado no disponible cierto día

        Escenario:
        - Empleado no disponible los lunes
        - Turno el lunes
        - Verificar que no se le asigne ese turno
        """
        # Arrange: Ana NO está disponible los lunes
        employees = [
            Employee(1, "Ana", max_hours_per_week=40, unavailable_days={'monday'}),
            Employee(2, "Bob", max_hours_per_week=40, unavailable_days=set()),
        ]

        # Turno el lunes
        shifts = [
            Shift(1, 'monday', start_hour=8, duration_hours=8, required_employees=1),
            Shift(2, 'tuesday', start_hour=8, duration_hours=8, required_employees=1),
        ]

        # Act
        result = assign_shifts(employees, shifts)

        # Assert
        self.assertIsNotNone(result)
        schedule = result['schedule']

        # Verificar que Ana NO está asignada al turno del lunes (shift_id=1)
        employees_for_monday_shift = schedule.get_employees_for_shift(1)
        self.assertNotIn(1, employees_for_monday_shift,
                        "Ana no debe estar asignada al turno del lunes porque no está disponible")

        # Verificar que Ana SÍ puede estar asignada al turno del martes
        ana_shifts = schedule.get_shifts_for_employee(1)
        monday_shifts_ana = [s_id for s_id in ana_shifts if s_id == 1]
        self.assertEqual(len(monday_shifts_ana), 0,
                        "Ana no debe tener asignado ningún turno del lunes")
    
    def test_overlapping_shifts(self):
        """
        Test 4: Conflicto de horarios

        Escenario:
        - Dos turnos el mismo día con horarios que se solapan
        - Un empleado no puede estar en ambos
        """
        # Arrange: Un solo empleado disponible
        employees = [
            Employee(1, "Ana", max_hours_per_week=40, unavailable_days=set()),
        ]

        # Dos turnos que se solapan el mismo día
        shifts = [
            Shift(1, 'monday', start_hour=8, duration_hours=8, required_employees=1),   # 8-16
            Shift(2, 'monday', start_hour=14, duration_hours=6, required_employees=1),  # 14-20 (solapa con shift 1)
        ]

        # Act
        result = assign_shifts(employees, shifts)

        # Assert
        self.assertIsNotNone(result)
        schedule = result['schedule']

        # Verificar que Ana no está asignada a ambos turnos simultáneamente
        ana_shifts = schedule.get_shifts_for_employee(1)

        if len(ana_shifts) > 1:
            # Si tiene más de un turno, verificar que no se solapen
            assigned_shift_objects = [s for s in shifts if s.id in ana_shifts]
            for i, shift1 in enumerate(assigned_shift_objects):
                for shift2 in assigned_shift_objects[i+1:]:
                    self.assertFalse(shift1.overlaps_with(shift2),
                                   f"Ana no puede tener dos turnos que se solapan: {shift1} y {shift2}")
    
    def test_successful_swap(self):
        """
        Test 5: Intercambio exitoso de turnos

        Escenario:
        - employee2 tiene un turno asignado
        - employee1 puede tomar ese turno (cumple restricciones)
        - Verificar que el swap funcione
        """
        # Arrange: Crear empleados y turnos
        employees = [
            Employee(1, "Ana", max_hours_per_week=40, unavailable_days=set()),
            Employee(2, "Bob", max_hours_per_week=40, unavailable_days=set()),
        ]

        shifts = [
            Shift(1, 'monday', start_hour=8, duration_hours=8, required_employees=1),
        ]

        # Asignar turno a Bob inicialmente
        schedule = Schedule()
        schedule.assign_employee_to_shift(2, 1)

        # Act: Ana quiere tomar el turno de Bob
        result = swap_shifts(
            schedule=schedule,
            employee1_id=1,  # Ana quiere el turno
            employee2_id=2,  # Bob tiene el turno
            shift_id=1,
            employees=employees,
            shifts=shifts
        )

        # Assert
        self.assertIsNotNone(result)
        self.assertIn('success', result)
        self.assertIn('message', result)

        if result['success']:
            # Si el swap fue exitoso, verificar el estado
            self.assertIsNotNone(result['updated_schedule'])
            updated_schedule = result['updated_schedule']

            # Ana debería tener el turno ahora
            ana_shifts = updated_schedule.get_shifts_for_employee(1)
            self.assertIn(1, ana_shifts, "Ana debería tener el turno después del swap")

            # Bob no debería tener el turno
            bob_shifts = updated_schedule.get_shifts_for_employee(2)
            self.assertNotIn(1, bob_shifts, "Bob no debería tener el turno después del swap")
    
    def test_failed_swap_not_assigned(self):
        """
        Test 6: Intercambio falla porque employee2 no tiene el turno
        """
        # Arrange: Crear empleados y turnos
        employees = [
            Employee(1, "Ana", max_hours_per_week=40, unavailable_days=set()),
            Employee(2, "Bob", max_hours_per_week=40, unavailable_days=set()),
        ]

        shifts = [
            Shift(1, 'monday', start_hour=8, duration_hours=8, required_employees=1),
        ]

        # Crear schedule vacío (Bob NO tiene el turno asignado)
        schedule = Schedule()

        # Act: Ana intenta tomar un turno que Bob no tiene
        result = swap_shifts(
            schedule=schedule,
            employee1_id=1,  # Ana quiere el turno
            employee2_id=2,  # Bob NO tiene el turno
            shift_id=1,
            employees=employees,
            shifts=shifts
        )

        # Assert
        self.assertIsNotNone(result)
        self.assertIn('success', result)
        self.assertIn('message', result)

        # El swap debe fallar
        self.assertFalse(result['success'],
                        "El swap debe fallar porque Bob no tiene el turno asignado")
        self.assertIsNotNone(result['message'],
                           "Debe haber un mensaje explicando por qué falló")

    def test_failed_swap_unavailable_day(self):
        """
        Test 7: Intercambio falla porque employee1 no está disponible ese día
        """
        # Arrange: Ana NO está disponible los lunes
        employees = [
            Employee(1, "Ana", max_hours_per_week=40, unavailable_days={'monday'}),
            Employee(2, "Bob", max_hours_per_week=40, unavailable_days=set()),
        ]

        shifts = [
            Shift(1, 'monday', start_hour=8, duration_hours=8, required_employees=1),
        ]

        # Bob tiene el turno del lunes
        schedule = Schedule()
        schedule.assign_employee_to_shift(2, 1)

        # Act: Ana (no disponible lunes) intenta tomar el turno del lunes de Bob
        result = swap_shifts(
            schedule=schedule,
            employee1_id=1,
            employee2_id=2,
            shift_id=1,
            employees=employees,
            shifts=shifts
        )

        # Assert
        self.assertIsNotNone(result)
        self.assertFalse(result['success'],
                        "El swap debe fallar porque Ana no está disponible los lunes")
        self.assertIsNotNone(result['message'])


class TestModels(unittest.TestCase):
    """Tests para los modelos."""

    def test_shift_overlap_same_day(self):
        """Verifica detección de solapamiento de turnos."""
        # Arrange: Dos turnos que se solapan
        shift1 = Shift(1, 'monday', start_hour=8, duration_hours=8, required_employees=1)   # 8-16
        shift2 = Shift(2, 'monday', start_hour=14, duration_hours=6, required_employees=1)  # 14-20

        # Turno que NO se solapa
        shift3 = Shift(3, 'monday', start_hour=16, duration_hours=4, required_employees=1)  # 16-20
        shift4 = Shift(4, 'tuesday', start_hour=8, duration_hours=8, required_employees=1)  # Diferente día

        # Assert
        self.assertTrue(shift1.overlaps_with(shift2),
                       "Shift 1 (8-16) y Shift 2 (14-20) deberían solaparse")
        self.assertTrue(shift2.overlaps_with(shift1),
                       "El solapamiento debe ser simétrico")

        # Verificar que turnos consecutivos sin solapamiento funcionen
        self.assertFalse(shift1.overlaps_with(shift3),
                        "Shift 1 (8-16) y Shift 3 (16-20) NO deberían solaparse si son exactamente consecutivos")

        # Verificar que turnos en diferentes días no se solapen
        self.assertFalse(shift1.overlaps_with(shift4),
                        "Turnos en diferentes días no deberían solaparse")

    def test_employee_availability(self):
        """Verifica validación de disponibilidad de empleado."""
        # Arrange
        employee = Employee(1, "Ana", max_hours_per_week=40, unavailable_days={'monday', 'friday'})

        # Assert
        self.assertFalse(employee.is_available('monday'),
                        "Ana no debería estar disponible los lunes")
        self.assertFalse(employee.is_available('friday'),
                        "Ana no debería estar disponible los viernes")
        self.assertTrue(employee.is_available('tuesday'),
                       "Ana debería estar disponible los martes")
        self.assertTrue(employee.is_available('wednesday'),
                       "Ana debería estar disponible los miércoles")

    def test_shift_end_hour(self):
        """Verifica el cálculo de hora de finalización del turno."""
        # Arrange & Act
        shift1 = Shift(1, 'monday', start_hour=8, duration_hours=8, required_employees=1)
        shift2 = Shift(2, 'monday', start_hour=20, duration_hours=6, required_employees=1)

        # Assert
        self.assertEqual(shift1.end_hour(), 16, "Turno de 8:00 con 8 horas debe terminar a las 16:00")
        self.assertEqual(shift2.end_hour(), 26, "Turno de 20:00 con 6 horas debe terminar a las 26:00 (02:00 del día siguiente)")

    def test_schedule_basic_operations(self):
        """Verifica operaciones básicas del Schedule."""
        # Arrange
        schedule = Schedule()

        # Act & Assert: Asignar empleados a turnos
        schedule.assign_employee_to_shift(1, 101)  # Employee 1 -> Shift 101
        schedule.assign_employee_to_shift(2, 101)  # Employee 2 -> Shift 101
        schedule.assign_employee_to_shift(1, 102)  # Employee 1 -> Shift 102

        # Verificar get_employees_for_shift
        employees_shift_101 = schedule.get_employees_for_shift(101)
        self.assertIn(1, employees_shift_101, "Employee 1 debería estar en shift 101")
        self.assertIn(2, employees_shift_101, "Employee 2 debería estar en shift 101")

        # Verificar get_shifts_for_employee
        shifts_emp_1 = schedule.get_shifts_for_employee(1)
        self.assertIn(101, shifts_emp_1, "Employee 1 debería tener shift 101")
        self.assertIn(102, shifts_emp_1, "Employee 1 debería tener shift 102")

        # Verificar remove_employee_from_shift
        schedule.remove_employee_from_shift(1, 101)
        employees_shift_101_after = schedule.get_employees_for_shift(101)
        self.assertNotIn(1, employees_shift_101_after, "Employee 1 no debería estar en shift 101 después de removerlo")


# ============================================================================
# NO MODIFICAR - Ejecutor de tests
# ============================================================================

if __name__ == '__main__':
    # Configuración para output más legible
    unittest.main(verbosity=2)
