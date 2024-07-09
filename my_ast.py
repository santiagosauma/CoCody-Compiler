from llvmlite import ir
import numpy as np

class Number:
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value

    def eval(self, context):
        return int(self.value)

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

class Sum(BinaryOp):
    def eval(self, context):
        return self.builder.add(self.left.eval(context), self.right.eval(context))

class Sub(BinaryOp):
    def eval(self, context):
        return self.builder.sub(self.left.eval(context), self.right.eval(context))

class Mul(BinaryOp):
    def eval(self, context):
        return self.builder.mul(self.left.eval(context), self.right.eval(context))

class Div(BinaryOp):
    def eval(self, context):
        return self.builder.sdiv(self.left.eval(context), self.right.eval(context))

class Mod(BinaryOp):
    def eval(self, context):
        return self.builder.srem(self.left.eval(context), self.right.eval(context))

class Pow(BinaryOp):
    def eval(self, context):
        left_val = self.left.eval(context)
        right_val = self.right.eval(context)
        left_float = self.builder.uitofp(left_val, ir.DoubleType())
        right_float = self.builder.uitofp(right_val, ir.DoubleType())
        pow_func = self.module.declare_intrinsic('llvm.pow', [ir.DoubleType()])
        result = self.builder.call(pow_func, [left_float, right_float])
        return self.builder.fptoui(result, ir.IntType(32))

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

        if isinstance(value, String):
            fmt = "%s \n\0"
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
            if isinstance(value, ir.Constant):
                value_type = value.type
            else:
                value = ir.Constant(ir.IntType(32), value)
                value_type = value.type

            if self.name not in self.module.globals:
                var = ir.GlobalVariable(self.module, value_type, self.name)
                var.initializer = ir.Constant(value_type, None)
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
        if self.operator == 'EQ':
            return self.builder.icmp_signed('==', self.left.eval(context), self.right.eval(context))
        elif self.operator == 'NEQ':
            return self.builder.icmp_signed('!=', self.left.eval(context), self.right.eval(context))
        elif self.operator == 'GT':
            return self.builder.icmp_signed('>', self.left.eval(context), self.right.eval(context))
        elif self.operator == 'LT':
            return self.builder.icmp_signed('<', self.left.eval(context), self.right.eval(context))
        elif self.operator == 'GTE':
            return self.builder.icmp_signed('>=', self.left.eval(context), self.right.eval(context))
        elif self.operator == 'LTE':
            return self.builder.icmp_signed('<=', self.left.eval(context), self.right.eval(context))

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
