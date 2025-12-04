"""
Modelos para el sistema de gestión de turnos.

TODO: Completa la implementación de las clases.
"""

class Employee:
    """
    Representa un empleado con sus restricciones.
    
    Atributos:
        id (int): Identificador único
        name (str): Nombre del empleado
        max_hours_per_week (int): Máximo de horas que puede trabajar por semana
        unavailable_days (set): Conjunto de días en los que NO puede trabajar
                                Valores válidos: 'monday', 'tuesday', 'wednesday', 
                                'thursday', 'friday', 'saturday', 'sunday'
    """
    
    def __init__(self, id: int, name: str, max_hours_per_week: int, unavailable_days: set):
        # TODO: Implementar inicialización
        pass
    
    def is_available(self, day: str) -> bool:
        """
        Verifica si el empleado está disponible en un día específico.
        
        Args:
            day: Día de la semana (ej: 'monday')
            
        Returns:
            bool: True si está disponible, False si no
        """
        # TODO: Implementar
        pass
    
    def __repr__(self):
        return f"Employee({self.id}, {self.name})"


class Shift:
    """
    Representa un turno de trabajo.
    
    Atributos:
        id (int): Identificador único
        day (str): Día de la semana
        start_hour (int): Hora de inicio (0-23)
        duration_hours (int): Duración en horas
        required_employees (int): Cantidad de empleados necesarios
    """
    
    def __init__(self, id: int, day: str, start_hour: int, duration_hours: int, required_employees: int):
        # TODO: Implementar inicialización
        # Considera agregar validaciones básicas
        pass
    
    def end_hour(self) -> int:
        """
        Calcula la hora de finalización del turno.
        
        Returns:
            int: Hora de finalización (puede ser >= 24 si cruza medianoche)
        """
        # TODO: Implementar
        pass
    
    def overlaps_with(self, other_shift) -> bool:
        """
        Verifica si este turno se solapa con otro turno.
        Dos turnos se solapan si son el mismo día y sus horarios se cruzan.
        
        Args:
            other_shift (Shift): Otro turno para comparar
            
        Returns:
            bool: True si hay solapamiento, False si no
        """
        # TODO: Implementar
        # Pista: primero verifica si son el mismo día
        pass
    
    def __repr__(self):
        return f"Shift({self.id}, {self.day}, {self.start_hour}:00-{self.end_hour()}:00)"


class Schedule:
    """
    Representa un horario de turnos asignados.
    
    Mantiene el registro de qué empleados están asignados a qué turnos.
    """
    
    def __init__(self):
        """
        Inicializa un horario vacío.
        
        Sugerencia de estructura de datos:
        - Un diccionario {shift_id: [employee_ids]}
        - O la estructura que prefieras
        """
        # TODO: Implementar inicialización
        pass
    
    def assign_employee_to_shift(self, employee_id: int, shift_id: int):
        """
        Asigna un empleado a un turno.
        
        Args:
            employee_id: ID del empleado
            shift_id: ID del turno
        """
        # TODO: Implementar
        pass
    
    def get_employees_for_shift(self, shift_id: int) -> list:
        """
        Obtiene la lista de empleados asignados a un turno.
        
        Args:
            shift_id: ID del turno
            
        Returns:
            list: Lista de IDs de empleados asignados
        """
        # TODO: Implementar
        pass
    
    def get_shifts_for_employee(self, employee_id: int) -> list:
        """
        Obtiene la lista de turnos asignados a un empleado.
        
        Args:
            employee_id: ID del empleado
            
        Returns:
            list: Lista de IDs de turnos asignados
        """
        # TODO: Implementar
        pass
    
    def remove_employee_from_shift(self, employee_id: int, shift_id: int):
        """
        Remueve un empleado de un turno.
        
        Args:
            employee_id: ID del empleado
            shift_id: ID del turno
        """
        # TODO: Implementar
        pass
    
    def get_all_assignments(self) -> dict:
        """
        Retorna todas las asignaciones.
        
        Returns:
            dict: {shift_id: [employee_ids]}
        """
        # TODO: Implementar
        pass
    
    def __repr__(self):
        return f"Schedule(assignments={self.get_all_assignments()})"
