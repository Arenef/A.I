class variable:
    def __init__(self, name, domains, constraints):
        self.name = name
        self.domains = domains
        self.constraints = constraints


class ac3:
    def __init__(self, variables):
        self.variables = variables
        self.assignments = {}

    def rm_inconsistent_values(self, Xi, Xj):
        removed = False
        to_remove = []
        
        for x in Xi.domains:
            has_support = False
            for y in Xj.domains:
                if x != y:
                    has_support = True
                    break
            
            if not has_support:
                to_remove.append(x)
                removed = True
                
        for x in to_remove:
            Xi.domains.remove(x)
                
        return removed

    def ac3(self, queue=None):
        var_map = {var.name: var for var in self.variables}
        
        if queue is None:
            queue = []
            for var in self.variables:
                for neighbor in var.constraints:
                    queue.append((var.name, neighbor))
                    
        from collections import deque
        q = deque(queue)
        
        while q:
            xi_name, xj_name = q.popleft()
            if xi_name in var_map and xj_name in var_map:
                Xi = var_map[xi_name]
                Xj = var_map[xj_name]
                
                if self.rm_inconsistent_values(Xi, Xj):
                    if len(Xi.domains) == 0:
                        return False
                    
                    for xk_name in Xi.constraints:
                        if xk_name != xj_name:
                            q.append((xk_name, xi_name))
        return True

    def is_valid(self, variable, color):
        for constraint in variable.constraints:
            if constraint in self.assignments and self.assignments[constraint] == color:
                return False
        return True

    def solve(self, i):
        if i == len(self.variables):
            return self.assignments

        current_var = self.variables[i]
        
        for color in list(current_var.domains):
            if self.is_valid(current_var, color):
                self.assignments[current_var.name] = color
                
                domain_backup = {var.name: list(var.domains) for var in self.variables}
                
                current_var.domains = [color]
                
                queue = []
                for neighbor_name in current_var.constraints:
                    if neighbor_name not in self.assignments:
                        queue.append((neighbor_name, current_var.name))
                
                consistent = self.ac3(queue)
                
                result = None
                if consistent:
                    result = self.solve(i + 1)
                    
                if result is not None:
                    return result
                
                for var in self.variables:
                    var.domains = list(domain_backup[var.name])
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

    problem = ac3(variables=variables_list)
    solution = problem.solve(0)
    
    print("=== KẾT QUẢ KIỂM THỬ AC-3 (MAC) ===")
    if solution:
        for var_name, color in solution.items():
            print(f"Vùng {var_name}: Tô màu {color}")
    else:
        print("Không tìm thấy lời giải hợp lệ.")
