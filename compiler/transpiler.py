class CTranspiler:
    def __init__(self, instructions):
        self.instructions = instructions
        
    def transpile(self):
        c_code = [
            "#include <stdio.h>",
            "#include <stdbool.h>",
            "#include <string.h>",
            "#include <stdint.h>",
            "",
            "// Global Variables & Temporaries"
        ]
        
        variables = set()
        var_types = {}
        
        # Pass 1: Identify all variables and their likely types
        for instr in self.instructions:
            op = instr[0]
            if op == 'ASSIGN':
                val, target = instr[1], instr[2]
                variables.add(target)
                if isinstance(val, str) and val.startswith('"'):
                    var_types[target] = 'char*'
                elif target not in var_types:
                    var_types[target] = 'long long'
            elif op == 'PARAM_POP':
                variables.add(instr[1])
                var_types[instr[1]] = 'long long' # Assuming numeric params for now
            elif len(instr) == 4 and op != 'CALL':
                variables.add(instr[3])
                var_types[instr[3]] = 'long long'
            elif len(instr) == 4 and op == 'CALL':
                variables.add(instr[3])
                var_types[instr[3]] = 'long long'
            elif len(instr) == 3 and op in ('!', '-'):
                variables.add(instr[2])
                var_types[instr[2]] = 'long long'
                
        # Emit variable declarations
        for v in variables:
            v_type = var_types.get(v, 'long long')
            if v_type == 'char*':
                c_code.append(f"char* {v} = NULL;")
            else:
                c_code.append(f"long long {v} = 0;")
            
        c_code.append("")
        
        # Software stack for parameters using intptr_t to hold both ints and pointers safely
        c_code.append("intptr_t param_stack[1000];")
        c_code.append("int param_sp = 0;")
        
        c_code.append("\nint main() {")
        
        for instr in self.instructions:
            op = instr[0]
            if op == 'LABEL':
                c_code.append(f"{instr[1]}:;")
            elif op == 'ASSIGN':
                val, target = instr[1], instr[2]
                v_type = var_types.get(target, 'long long')
                if v_type == 'char*':
                    c_code.append(f"    {target} = {val};")
                else:
                    c_code.append(f"    {target} = (long long){val};")
            elif op == 'PRINT':
                val = instr[1]
                if isinstance(val, str) and val.startswith('"'):
                    c_code.append(f'    printf("%s\\n", {val});')
                else:
                    v_type = var_types.get(val, 'long long')
                    if v_type == 'char*':
                        c_code.append(f'    printf("%s\\n", {val});')
                    else:
                        c_code.append(f'    printf("%lld\\n", (long long){val});')
            elif op in ('+', '-', '*', '/', '<', '>', '<=', '>=', '==', '!=', '&&', '||'):
                left, right, target = instr[1], instr[2], instr[3]
                c_code.append(f"    {target} = {left} {op} {right};")
            elif op in ('!', '-'):
                val, target = instr[1], instr[2]
                c_code.append(f"    {target} = {op}{val};")
            elif op == 'IF_FALSE_GOTO':
                cond, label = instr[1], instr[2]
                c_code.append(f"    if (!{cond}) goto {label};")
            elif op == 'GOTO':
                label = instr[1]
                c_code.append(f"    goto {label};")
            elif op == 'PARAM_PUSH':
                val = instr[1]
                c_code.append(f"    param_stack[param_sp++] = (intptr_t){val};")
            elif op == 'PARAM_POP':
                var_name = instr[1]
                c_code.append(f"    {var_name} = (long long)param_stack[--param_sp];")
            elif op == 'CALL':
                func_name, args_count, target = instr[1], instr[2], instr[3]
                c_code.append(f"    // CALL {func_name} - Simulated by flat IR jumps")
            elif op == 'RETURN':
                c_code.append(f"    // RETURN {instr[1]}")
            elif op == 'RETURN_VOID':
                c_code.append(f"    // RETURN_VOID")
                
        c_code.append("    return 0;")
        c_code.append("}")
        
        return '\n'.join(c_code)
