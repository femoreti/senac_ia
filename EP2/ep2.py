from csp import Constraint, CSP
from typing import Dict, List, Optional

class NaoPodeConstraint(Constraint[str, str]):
    def __init__(self, place1: str, place2: str) -> None:
        super().__init__([place1, place2])
        self.place1: str = place1
        self.place2: str = place2
    
    def satisfied(self, assignment: Dict[str, str]) -> bool:
        # If either place is not in the assignment, then it is not
        # yet possible for their colors to be conflicting
        if self.place1 not in assignment or self.place2 not in assignment:
            return True
        # check the color assigned to place1 is not the same as the # color assigned to place2
        return assignment[self.place1] != assignment[self.place2]

class NaoPodeAdjConstraint(Constraint[str, str]):
    def __init__(self, place1: str, place2: str) -> None:
        super().__init__([place1, place2])
        self.place1: str = place1
        self.place2: str = place2
    
    def satisfied(self, assignment: Dict[str, str]) -> bool:
        # If either place is not in the assignment, then it is not
        # yet possible for their colors to be conflicting
        if self.place1 not in assignment or self.place2 not in assignment:
            return True
        return assignment[self.place1] != assignment[self.place2] and (int(assignment[self.place1]) + 1) != int(assignment[self.place2]) and (int(assignment[self.place1]) - 1) != int(assignment[self.place2])

class MesmaJaulaConstraint(Constraint[str, str]):
    def __init__(self, place1: str, place2: str) -> None:
        super().__init__([place1, place2])
        self.place1: str = place1
        self.place2: str = place2
    
    def satisfied(self, assignment: Dict[str, str]) -> bool:
        # If either place is not in the assignment, then it is not
        # yet possible for their colors to be conflicting
        if self.place1 not in assignment or self.place2 not in assignment:
            return True
        # check the color assigned to place1 is not the same as the # color assigned to place2
        return assignment[self.place1] == assignment[self.place2]

class LeaoConstraint(Constraint):
    def __init__(self, animal1: str) -> None:
        super().__init__([animal1])
        self.animal1: str = animal1
    
    def satisfied(self, assignment: Dict[str, str]) -> bool:
        return assignment[self.animal1] == "1"

if __name__ == "__main__":
    variables: List[str] = ["Leao", "Antilope", "Hiena", "Tigre", "Pavao", "Suricate", "Javali"] 
    domains: Dict[str, List[str]] = {}
    for variable in variables:
        domains[variable] = ["1", "2", "3", "4"]
    
    csp: CSP[str, str] = CSP(variables, domains)
    csp.add_constraint(LeaoConstraint("Leao"))
    csp.add_constraint(NaoPodeConstraint("Leao", "Tigre"))
    csp.add_constraint(NaoPodeAdjConstraint("Leao", "Antilope"))
    csp.add_constraint(NaoPodeConstraint("Leao", "Pavao"))
    csp.add_constraint(NaoPodeAdjConstraint("Tigre", "Antilope"))
    csp.add_constraint(NaoPodeConstraint("Tigre", "Suricate"))
    csp.add_constraint(NaoPodeConstraint("Tigre", "Javali"))
    csp.add_constraint(NaoPodeConstraint("Tigre", "Pavao"))
    csp.add_constraint(MesmaJaulaConstraint("Suricate", "Javali"))
    csp.add_constraint(MesmaJaulaConstraint("Hiena", "Tigre"))

solution: Optional[Dict[str, str]] = csp.backtracking_search()
if solution is None:
    print("No solution found!") 
else:
    print(solution)