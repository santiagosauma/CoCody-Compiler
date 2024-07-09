from llvmlite import ir
import numpy as np

class Number:
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value

    def eval(self, context):
        return ir.Constant(ir.IntType(32), int(self.value))

class Identifier:
    def __init__(self, builder, module, name):
        self.builder = builder
        self.module = module
        self.name = name

    def eval(self, context):
        return self.builder.load(self.module.globals[self.name])

class BinaryOp:
    def __init__(self, builder, module, left, right):
        self.builder = builder
        self.module = module
        self.left = left
        self.right = right

    def eval_operands(self, context):
        left_val = self.left.eval(context)
        right_val = self.right.eval(context)
        
        # Ensure both operands are LLVM IR values
        if not isinstance(left_val, ir.Value):
            left_val = ir.Constant(ir.IntType(32), left_val)
        if not isinstance(right_val, ir.Value):
            right_val = ir.Constant(ir.IntType(32), right_val)

        return left_val, right_val

class Sum(BinaryOp):
    def eval(self, context):
        left_val, right_val = self.eval_operands(context)
        return self.builder.add(left_val, right_val)

class Sub(BinaryOp):
    def eval(self, context):
        left_val, right_val = self.eval_operands(context)
        return self.builder.sub(left_val, right_val)

class Mul(BinaryOp):
    def eval(self, context):
        left_val, right_val = self.eval_operands(context)
        return self.builder.mul(left_val, right_val)

class Div(BinaryOp):
    def eval(self, context):
        left_val, right_val = self.eval_operands(context)
        return self.builder.sdiv(left_val, right_val)

class Mod(BinaryOp):
    def eval(self, context):
        left_val, right_val = self.eval_operands(context)
        return self.builder.srem(left_val, right_val)

class Pow(BinaryOp):
    def eval(self, context):
        left_val, right_val = self.eval_operands(context)
        left_float = self.builder.uitofp(left_val, ir.DoubleType())
        right_float = self.builder.uitofp(right_val, ir.DoubleType())
        pow_func = self.module.declare_intrinsic('llvm.pow', [ir.DoubleType()])
        result = self.builder.call(pow_func, [left_float, right_float])
        return self.builder.fptoui(result, ir.IntType(32))

class If:
    def __init__(self, builder, module, printf, condition, body):
        self.builder = builder
        self.module = module
        self.printf = printf
        self.condition = condition
        self.body = body

    def eval(self, context):
        cond = self.condition.eval(context)
        then_block = self.builder.append_basic_block('then')
        endif_block = self.builder.append_basic_block('endif')
        
        self.builder.cbranch(cond, then_block, endif_block)
        
        self.builder.position_at_end(then_block)
        for stmt in self.body:
            stmt.eval(context)
        self.builder.branch(endif_block)
        
        self.builder.position_at_end(endif_block)

class While:
    def __init__(self, builder, module, printf, condition, body):
        self.builder = builder
        self.module = module
        self.printf = printf
        self.condition = condition
        self.body = body

    def eval(self, context):
        loop_block = self.builder.append_basic_block('loop')
        after_loop_block = self.builder.append_basic_block('afterloop')
        
        self.builder.branch(loop_block)
        self.builder.position_at_end(loop_block)
        
        cond = self.condition.eval(context)
        with self.builder.if_then(cond):
            for stmt in self.body:
                stmt.eval(context)
            self.builder.branch(loop_block)
        
        self.builder.branch(after_loop_block)
        self.builder.position_at_end(after_loop_block)

class List:
    def __init__(self, elements):
        self.elements = elements

    def eval(self, context):
        evaluated_elements = []
        for element in self.elements:
            eval_element = element.eval(context)
            if isinstance(eval_element, ir.Constant):
                evaluated_elements.append(int(eval_element.constant))
            else:
                evaluated_elements.append(eval_element)
        return np.array(evaluated_elements, dtype=np.int32)

class ListAccess:
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def eval(self, context):
        array = context[self.name]
        index = self.index.eval(context)
        return array[index]

class ListAssign:
    def __init__(self, name, index, value):
        self.name = name
        self.index = index
        self.value = value

    def eval(self, context):
        array = context[self.name]
        index = self.index.eval(context)
        value = self.value.eval(context)
        array[index] = value

class Assign:
    def __init__(self, builder, module, name, value):
        self.builder = builder
        self.module = module
        self.name = name
        self.value = value

    def eval(self, context):
        value = self.value.eval(context)
        if isinstance(value, np.ndarray):
            # Handle numpy arrays separately
            array_type = ir.ArrayType(ir.IntType(32), len(value))
            array_constant = ir.Constant(array_type, [ir.Constant(ir.IntType(32), int(v)) for v in value])
            if self.name not in self.module.globals:
                var = ir.GlobalVariable(self.module, array_type, self.name)
                var.linkage = 'internal'
                var.global_constant = False
                var.initializer = array_constant
                context[self.name] = value
            else:
                var = self.module.globals[self.name]
                self.builder.store(array_constant, var)
                context[self.name] = value
        else:
            # Handle scalar values
            if not isinstance(value, ir.Value):
                value = ir.Constant(ir.IntType(32), value)

            if self.name not in self.module.globals:
                var = ir.GlobalVariable(self.module, value.type, self.name)
                var.initializer = ir.Constant(value.type, None)
                var.linkage = 'internal'
                var.global_constant = False
                context[self.name] = value
            else:
                var = self.module.globals[self.name]

            self.builder.store(value, var)
            context[self.name] = value

class Condition:
    def __init__(self, builder, module, left, right, operator):
        self.builder = builder
        self.module = module
        self.left = left
        self.right = right
        self.operator = operator

    def eval(self, context):
        left_val = self.left.eval(context)
        right_val = self.right.eval(context)

        # Ensure both operands are LLVM IR values
        if not isinstance(left_val, ir.Value):
            left_val = ir.Constant(ir.IntType(32), left_val)
        if not isinstance(right_val, ir.Value):
            right_val = ir.Constant(ir.IntType(32), right_val)

        if self.operator == 'EQ':
            return self.builder.icmp_signed('==', left_val, right_val)
        elif self.operator == 'NEQ':
            return self.builder.icmp_signed('!=', left_val, right_val)
        elif self.operator == 'GT':
            return self.builder.icmp_signed('>', left_val, right_val)
        elif self.operator == 'LT':
            return self.builder.icmp_signed('<', left_val, right_val)
        elif self.operator == 'GTE':
            return self.builder.icmp_signed('>=', left_val, right_val)
        elif self.operator == 'LTE':
            return self.builder.icmp_signed('<=', left_val, right_val)

class String:
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value.strip('"')

    def eval(self, context):
        global global_string_counter
        string_ty = ir.ArrayType(ir.IntType(8), len(self.value) + 1)
        string_constant = ir.Constant(string_ty, bytearray(self.value.encode("utf8") + b"\00"))
        global_string = ir.GlobalVariable(self.module, string_ty, name=f"str{global_string_counter}")
        global_string.linkage = 'internal'
        global_string.global_constant = True
        global_string.initializer = string_constant
        global_string_counter += 1
        return self.builder.bitcast(global_string, ir.IntType(8).as_pointer())

global_string_counter = 0  # Contador global para generar nombres únicos

class Print:
    def __init__(self, builder, module, printf, value):
        self.builder = builder
        self.module = module
        self.printf = printf
        self.value = value

    def eval(self, context):
        global global_string_counter
        value = self.value.eval(context)
        voidptr_ty = ir.IntType(8).as_pointer()

        if isinstance(self.value, String):
            fmt = "%s \n\0"
            value = self.builder.bitcast(value, voidptr_ty)  # Ensure value is a pointer for strings
        else:
            fmt = "%i \n\0"

        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)), bytearray(fmt.encode("utf8")))
        global_fmt_name = f"fstr{global_string_counter}"  # Usar un nombre único
        global_string_counter += 1

        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name=global_fmt_name)
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        fmt_arg = self.builder.bitcast(global_fmt, voidptr_ty)
        self.builder.call(self.printf, [fmt_arg, value])

class Assign:
    def __init__(self, builder, module, name, value):
        self.builder = builder
        self.module = module
        self.name = name
        self.value = value

    def eval(self, context):
        value = self.value.eval(context)
        if isinstance(value, np.ndarray):
            # Handle numpy arrays separately
            array_type = ir.ArrayType(ir.IntType(32), len(value))
            array_constant = ir.Constant(array_type, [ir.Constant(ir.IntType(32), int(v)) for v in value])
            if self.name not in self.module.globals:
                var = ir.GlobalVariable(self.module, array_type, self.name)
                var.linkage = 'internal'
                var.global_constant = False
                var.initializer = array_constant
                context[self.name] = value
            else:
                var = self.module.globals[self.name]
                self.builder.store(array_constant, var)
                context[self.name] = value
        else:
            # Handle scalar values
            if not isinstance(value, ir.Value):
                value = ir.Constant(ir.IntType(32), value)

            if self.name not in self.module.globals:
                var = ir.GlobalVariable(self.module, value.type, self.name)
                var.initializer = ir.Constant(value.type, None)
                var.linkage = 'internal'
                var.global_constant = False
                context[self.name] = value
            else:
                var = self.module.globals[self.name]

            self.builder.store(value, var)
            context[self.name] = value

class Condition:
    def __init__(self, builder, module, left, right, operator):
        self.builder = builder
        self.module = module
        self.left = left
        self.right = right
        self.operator = operator

    def eval(self, context):
        left_val = self.left.eval(context)
        right_val = self.right.eval(context)

        # Ensure both operands are LLVM IR values
        if not isinstance(left_val, ir.Value):
            left_val = ir.Constant(ir.IntType(32), left_val)
        if not isinstance(right_val, ir.Value):
            right_val = ir.Constant(ir.IntType(32), right_val)

        if self.operator == 'EQ':
            return self.builder.icmp_signed('==', left_val, right_val)
        elif self.operator == 'NEQ':
            return self.builder.icmp_signed('!=', left_val, right_val)
        elif self.operator == 'GT':
            return self.builder.icmp_signed('>', left_val, right_val)
        elif self.operator == 'LT':
            return self.builder.icmp_signed('<', left_val, right_val)
        elif self.operator == 'GTE':
            return self.builder.icmp_signed('>=', left_val, right_val)
        elif self.operator == 'LTE':
            return self.builder.icmp_signed('<=', left_val, right_val)

class If:
    def __init__(self, builder, module, printf, condition, body):
        self.builder = builder
        self.module = module
        self.printf = printf
        self.condition = condition
        self.body = body

    def eval(self, context):
        cond = self.condition.eval(context)
        then_block = self.builder.append_basic_block('then')
        endif_block = self.builder.append_basic_block('endif')
        
        self.builder.cbranch(cond, then_block, endif_block)
        
        self.builder.position_at_end(then_block)
        for stmt in self.body:
            stmt.eval(context)
        self.builder.branch(endif_block)
        
        self.builder.position_at_end(endif_block)

class While:
    def __init__(self, builder, module, printf, condition, body):
        self.builder = builder
        self.module = module
        self.printf = printf
        self.condition = condition
        self.body = body

    def eval(self, context):
        loop_block = self.builder.append_basic_block('loop')
        after_loop_block = self.builder.append_basic_block('afterloop')
        
        self.builder.branch(loop_block)
        self.builder.position_at_end(loop_block)
        
        cond = self.condition.eval(context)
        with self.builder.if_then(cond):
            for stmt in self.body:
                stmt.eval(context)
            self.builder.branch(loop_block)
        
        self.builder.branch(after_loop_block)
        self.builder.position_at_end(after_loop_block)

class List:
    def __init__(self, elements):
        self.elements = elements

    def eval(self, context):
        evaluated_elements = []
        for element in self.elements:
            eval_element = element.eval(context)
            if isinstance(eval_element, ir.Constant):
                evaluated_elements.append(int(eval_element.constant))
            else:
                evaluated_elements.append(eval_element)
        return np.array(evaluated_elements, dtype=np.int32)

class ListAccess:
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def eval(self, context):
        array = context[self.name]
        index = self.index.eval(context)
        return array[index]

class ListAssign:
    def __init__(self, name, index, value):
        self.name = name
        self.index = index
        self.value = value

    def eval(self, context):
        array = context[self.name]
        index = self.index.eval(context)
        value = self.value.eval(context)
        array[index] = value
