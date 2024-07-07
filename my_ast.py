from llvmlite import ir

class Number():
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value

    def eval(self):
        return ir.Constant(ir.IntType(32), int(self.value))

class Identifier():
    def __init__(self, builder, module, name):
        self.builder = builder
        self.module = module
        self.name = name

    def eval(self):
        return self.builder.load(self.module.globals[self.name])

class BinaryOp():
    def __init__(self, builder, module, left, right):
        self.builder = builder
        self.module = module
        self.left = left
        self.right = right

class Sum(BinaryOp):
    def eval(self):
        return self.builder.add(self.left.eval(), self.right.eval())

class Sub(BinaryOp):
    def eval(self):
        return self.builder.sub(self.left.eval(), self.right.eval())

class Mul(BinaryOp):
    def eval(self):
        return self.builder.mul(self.left.eval(), self.right.eval())

class Div(BinaryOp):
    def eval(self):
        return self.builder.sdiv(self.left.eval(), self.right.eval())

class Mod(BinaryOp):
    def eval(self):
        return self.builder.srem(self.left.eval(), self.right.eval())

class String():
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value.strip('"')

    def eval(self):
        string_ty = ir.ArrayType(ir.IntType(8), len(self.value) + 1)
        string_constant = ir.Constant(string_ty, bytearray(self.value.encode("utf8") + b"\00"))
        global_string = ir.GlobalVariable(self.module, string_ty, name=f"str{global_string_counter}")
        global_string.linkage = 'internal'
        global_string.global_constant = True
        global_string.initializer = string_constant
        return self.builder.bitcast(global_string, ir.IntType(8).as_pointer())

global_string_counter = 0  # Contador global para generar nombres únicos

class Print():
    def __init__(self, builder, module, printf, value):
        self.builder = builder
        self.module = module
        self.printf = printf
        self.value = value

    def eval(self):
        global global_string_counter
        value = self.value.eval()
        voidptr_ty = ir.IntType(8).as_pointer()

        if isinstance(self.value, String):
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

class Assign():
    def __init__(self, builder, module, name, value):
        self.builder = builder
        self.module = module
        self.name = name
        self.value = value

    def eval(self):
        if self.name not in self.module.globals:
            var = ir.GlobalVariable(self.module, ir.IntType(32), self.name)
            var.initializer = ir.Constant(ir.IntType(32), 0)
        var_ptr = self.builder.gep(self.module.globals[self.name], [ir.Constant(ir.IntType(32), 0)])
        self.builder.store(self.value.eval(), var_ptr)

class Condition():
    def __init__(self, builder, module, left, right, operator):
        self.builder = builder
        self.module = module
        self.left = left
        self.right = right
        self.operator = operator

    def eval(self):
        if self.operator == 'EQ':
            return self.builder.icmp_signed('==', self.left.eval(), self.right.eval())
        elif self.operator == 'NEQ':
            return self.builder.icmp_signed('!=', self.left.eval(), self.right.eval())
        elif self.operator == 'GT':
            return self.builder.icmp_signed('>', self.left.eval(), self.right.eval())
        elif self.operator == 'LT':
            return self.builder.icmp_signed('<', self.left.eval(), self.right.eval())
        elif self.operator == 'GTE':
            return self.builder.icmp_signed('>=', self.left.eval(), self.right.eval())
        elif self.operator == 'LTE':
            return self.builder.icmp_signed('<=', self.left.eval(), self.right.eval())

class If():
    def __init__(self, builder, module, printf, condition, body):
        self.builder = builder
        self.module = module
        self.printf = printf
        self.condition = condition
        self.body = body

    def eval(self):
        cond = self.condition.eval()
        then_block = self.builder.append_basic_block('then')
        endif_block = self.builder.append_basic_block('endif')
        
        self.builder.cbranch(cond, then_block, endif_block)
        
        self.builder.position_at_end(then_block)
        for stmt in self.body:
            stmt.eval()
        self.builder.branch(endif_block)
        
        self.builder.position_at_end(endif_block)

class While():
    def __init__(self, builder, module, printf, condition, body):
        self.builder = builder
        self.module = module
        self.printf = printf
        self.condition = condition
        self.body = body

    def eval(self):
        loop_block = self.builder.append_basic_block('loop')
        after_loop_block = self.builder.append_basic_block('afterloop')
        
        self.builder.branch(loop_block)
        self.builder.position_at_end(loop_block)
        
        cond = self.condition.eval()
        with self.builder.if_then(cond):
            for stmt in self.body:
                stmt.eval()
            self.builder.branch(loop_block)
        
        self.builder.branch(after_loop_block)
        self.builder.position_at_end(after_loop_block)
