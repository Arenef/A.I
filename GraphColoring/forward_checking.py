class variable:
    def __init__(self, name, domains, constraints):
        self.name = name
        self.domains = domains
        self.constraints = constraints

class forward_checking:
    def __init__(self, variables):
        self.variables = variables
        self.assignments = {}

    def is_valid(self, variable, color):        
        for constraint in variable.constraints:
            if constraint in self.assignments and self.assignments[constraint] == color:
                return False
        return True
    
    def remove_domains(self, variable):
        color = self.assignments[variable.name]
        pruned = []
        for i in range(len(self.variables)):
            var = self.variables[i]
            if var.name not in self.assignments and var.name in variable.constraints:
                if color in var.domains:
                    var.domains.remove(color)
                    pruned.append(var)
        return pruned
    
    def add_domains(self, pruned_variables, color):
        for var in pruned_variables:
            if color not in var.domains:
                var.domains.append(color)

    def solve(self, i):
        if i == len(self.variables):
            return self.assignments
        
        current_var = self.variables[i]
        for color in current_var.domains:
            if self.is_valid(current_var, color):
                self.assignments[current_var.name] = color
                pruned = self.remove_domains(current_var)

                any_empty = any(len(var.domains) == 0 for var in self.variables if var.name not in self.assignments)
                
                result = None
                if not any_empty:
                    result = self.solve(i+1)
                if result:
                    return result
                
                self.add_domains(pruned, color)
                del self.assignments[current_var.name]
        return None
        
if __name__ == "__main__":
    adjacency_dict = {
        "Gò Vấp": ["Tân Bình", "Phú Nhuận", "Bình Thạnh"],
        "Bình Thạnh": ["Gò Vấp", "Phú Nhuận", "Quận 1"],
        "Phú Nhuận": ["Gò Vấp", "Bình Thạnh", "Tân Bình", "Quận 3", "Quận 1"],
        "Tân Bình": ["Gò Vấp", "Phú Nhuận", "Quận 3", "Quận 10", "Quận 11"],
        "Quận 1": ["Bình Thạnh", "Phú Nhuận", "Quận 3", "Quận 5", "Quận 4"],
        "Quận 3": ["Phú Nhuận", "Tân Bình", "Quận 1", "Quận 10", "Quận 5"],
        "Quận 10": ["Tân Bình", "Quận 3", "Quận 11", "Quận 5"],
        "Quận 11": ["Tân Bình", "Quận 10", "Quận 6", "Quận 5"],
        "Quận 5": ["Quận 10", "Quận 3", "Quận 1", "Quận 11", "Quận 6", "Quận 4"],
        "Quận 6": ["Quận 11", "Quận 5"],
        "Quận 4": ["Quận 1", "Quận 5"]
    }

    domains = ['Đỏ', 'Xanh lá', 'Vàng', 'Xanh dương']
    variables_list = []
    for name, constraints in adjacency_dict.items():
        variables_list.append(variable(name=name, domains=list(domains), constraints=constraints))

    problem = forward_checking(variables=variables_list)
    solution = problem.solve(0)
    
    print("=== KẾT QUẢ KIỂM THỬ ===")
    if solution:
        for var_name, color in solution.items():
            print(f"Vùng {var_name}: Tô màu {color}")
    else:
        print("Không tìm thấy lời giải hợp lệ.")
