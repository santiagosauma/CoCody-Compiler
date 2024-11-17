# AST
from llvmlite import ir

from ai import VisualizadorDebug

class Number:
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value

    def eval(self, context, visualizer=None):
        result = ir.Constant(ir.IntType(32), int(self.value))
        if visualizer:
            visualizer.update_variables({"Constant": self.value})
            visualizer.next_step()
        return result

class Identifier:
    def __init__(self, builder, module, name):
        self.builder = builder
        self.module = module
        self.name = name

    def eval(self, context):
        return self.builder.load(context[self.name])

class BinaryOp:
    def __init__(self, builder, module, left, right):
        self.builder = builder
        self.module = module
        self.left = left
        self.right = right

    def eval_operands(self, context):
        left_val = self.left.eval(context)
        right_val = self.right.eval(context)

        if not isinstance(left_val, ir.Value):
            left_val = ir.Constant(ir.IntType(32), left_val)
        if not isinstance(right_val, ir.Value):
            right_val = ir.Constant(ir.IntType(32), right_val)

        return left_val, right_val

class Sum(BinaryOp):
    def eval(self, context, visualizer=None):
        left_val, right_val = self.eval_operands(context)
        result = self.builder.add(left_val, right_val)
        if visualizer:
            visualizer.update_variables({"Sum Result": result})
            visualizer.next_step()
        return result

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
    def __init__(self, builder, module, printf, condition, then_body, else_body=None):
        self.builder = builder
        self.module = module
        self.printf = printf
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body

    def eval(self, context):
        cond = self.condition.eval(context)

        then_block = self.builder.append_basic_block('then')
        merge_block = self.builder.append_basic_block('ifcont')

        if self.else_body:
            else_block = self.builder.append_basic_block('else')
            self.builder.cbranch(cond, then_block, else_block)
        else:
            self.builder.cbranch(cond, then_block, merge_block)

        # Then block
        self.builder.position_at_end(then_block)
        for stmt in self.then_body:
            stmt.eval(context)
        if not self.builder.block.is_terminated:
            self.builder.branch(merge_block)

        # Else block
        if self.else_body:
            self.builder.position_at_end(else_block)
            for stmt in self.else_body:
                stmt.eval(context)
            if not self.builder.block.is_terminated:
                self.builder.branch(merge_block)

        self.builder.position_at_end(merge_block)

class While:
    def __init__(self, builder, module, printf, condition, body):
        self.builder = builder
        self.module = module
        self.printf = printf
        self.condition = condition
        self.body = body

    def eval(self, context):
        condition_block = self.builder.append_basic_block('cond_block')
        loop_block = self.builder.append_basic_block('loop')
        after_loop_block = self.builder.append_basic_block('afterloop')

        self.builder.branch(condition_block)

        self.builder.position_at_end(condition_block)
        cond = self.condition.eval(context)
        self.builder.cbranch(cond, loop_block, after_loop_block)

        self.builder.position_at_end(loop_block)
        for stmt in self.body:
            stmt.eval(context)
        self.builder.branch(condition_block)

        self.builder.position_at_end(after_loop_block)

class List:
    def __init__(self, elements):
        self.elements = elements

    def eval(self, context):
        evaluated_elements = [element.eval(context) for element in self.elements]
        return evaluated_elements

class ListAccess:
    def __init__(self, builder, module, name, index):
        self.builder = builder
        self.module = module
        self.name = name
        self.index = index

    def eval(self, context):
        array = context[self.name]
        index = self.index.eval(context)

        if not isinstance(index, ir.Value):
            index = ir.Constant(ir.IntType(32), int(index.constant))

        value_ptr = self.builder.gep(array, [ir.Constant(ir.IntType(32), 0), index])
        value = self.builder.load(value_ptr)

        return value

class ListAssign:
    def __init__(self, builder, module, name, index, value):
        self.builder = builder
        self.module = module
        self.name = name
        self.index = index
        self.value = value

    def eval(self, context):
        if self.name not in context:
            raise ValueError(f"List '{self.name}' not defined")

        array = context[self.name]
        index = self.index.eval(context)
        value = self.value.eval(context)

        if not isinstance(index, ir.Value):
            index = ir.Constant(ir.IntType(32), int(index))

        element_ptr = self.builder.gep(array, [ir.Constant(ir.IntType(32), 0), index])
        self.builder.store(value, element_ptr)

class Assign:
    def __init__(self, builder, module, name, value):
        self.builder = builder
        self.module = module
        self.name = name
        self.value = value

    def eval(self, context):
        value = self.value.eval(context)
        if isinstance(value, list):
            if len(value) == 0:
                array_type = ir.ArrayType(ir.IntType(32), 10)
                global_array = ir.GlobalVariable(self.module, array_type, name=self.name)
                global_array.linkage = 'internal'
                global_array.initializer = ir.Constant(array_type, [ir.Constant(ir.IntType(32), 0)] * 10)
            else:
                array_type = ir.ArrayType(ir.IntType(32), len(value))
                global_array = ir.GlobalVariable(self.module, array_type, name=self.name)
                global_array.linkage = 'internal'
                global_array.initializer = ir.Constant(array_type, value)
            context[self.name] = global_array
        else:
            if not isinstance(value, ir.Value):
                value = ir.Constant(ir.IntType(32), value)
            if self.name not in context:
                var = ir.GlobalVariable(self.module, value.type, name=self.name)
                var.initializer = ir.Constant(value.type, None)
                var.linkage = 'internal'
                var.global_constant = False
                context[self.name] = var
            self.builder.store(value, context[self.name])

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

        if not isinstance(left_val, ir.Value):
            left_val = ir.Constant(ir.IntType(32), left_val)
        if not isinstance(right_val, ir.Value):
            right_val = ir.Constant(ir.IntType(32), right_val)

        if self.operator == 'EQ':
            result = self.builder.icmp_signed('==', left_val, right_val)
        elif self.operator == 'NEQ':
            result = self.builder.icmp_signed('!=', left_val, right_val)
        elif self.operator == 'GT':
            result = self.builder.icmp_signed('>', left_val, right_val)
        elif self.operator == 'LT':
            result = self.builder.icmp_signed('<', left_val, right_val)
        elif self.operator == 'GTE':
            result = self.builder.icmp_signed('>=', left_val, right_val)
        elif self.operator == 'LTE':
            result = self.builder.icmp_signed('<=', left_val, right_val)
        elif self.operator == 'AND':
            result = self.builder.and_(left_val, right_val)
        else:
            raise ValueError(f"Unsupported operator: {self.operator}")

        print(f"Condition evaluated to: {result}")
        return result

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

global_string_counter = 0

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

        if isinstance(value.type, ir.PointerType) and value.type.pointee == ir.IntType(8):
            fmt = "%s\n\0"
        elif isinstance(value.type, ir.PointerType) and isinstance(value.type.pointee, ir.ArrayType):
            array_ptr = value
            array_type = value.type.pointee
            
            if array_type.count == 0:
                self.print_empty_list()
                return

            self.print_list_elements(array_ptr, array_type)
            return
        elif isinstance(value.type, ir.ArrayType):
            if value.type.count == 0:
                self.print_empty_list()
                return
            
            self.print_global_array_elements(value)
            return
        elif isinstance(value.type, ir.IntType) or isinstance(value, ir.Constant):
            fmt = "%i\n\0"
        else:
            raise TypeError(f"Unsupported value type for Print: {value.type}")

        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)), bytearray(fmt.encode("utf8")))
        global_fmt_name = f"fstr{global_string_counter}"
        global_string_counter += 1

        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name=global_fmt_name)
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        fmt_arg = self.builder.bitcast(global_fmt, voidptr_ty)
        self.builder.call(self.printf, [fmt_arg, value])

    def print_empty_list(self):
        global global_string_counter
        empty_msg = "Empty list\n\0"
        c_empty_msg = ir.Constant(ir.ArrayType(ir.IntType(8), len(empty_msg)), bytearray(empty_msg.encode("utf8")))
        global_empty_msg_name = f"fstr{global_string_counter}"
        global_string_counter += 1

        global_empty_msg = ir.GlobalVariable(self.module, c_empty_msg.type, name=global_empty_msg_name)
        global_empty_msg.linkage = 'internal'
        global_empty_msg.global_constant = True
        global_empty_msg.initializer = c_empty_msg
        empty_msg_arg = self.builder.bitcast(global_empty_msg, ir.IntType(8).as_pointer())
        self.builder.call(self.printf, [empty_msg_arg])

    def print_list_elements(self, array_ptr, array_type):
        global global_string_counter
        fmt = "%i "
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)), bytearray(fmt.encode("utf8")))
        global_fmt_name = f"fstr{global_string_counter}"
        global_string_counter += 1

        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name=global_fmt_name)
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        fmt_arg = self.builder.bitcast(global_fmt, ir.IntType(8).as_pointer())

        for i in range(array_type.count):
            element_ptr = self.builder.gep(array_ptr, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), i)])
            element = self.builder.load(element_ptr)
            self.builder.call(self.printf, [fmt_arg, element])
        
        self.print_newline()

    def print_global_array_elements(self, global_array):
        global global_string_counter
        fmt = "%i "
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)), bytearray(fmt.encode("utf8")))
        global_fmt_name = f"fstr{global_string_counter}"
        global_string_counter += 1

        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name=global_fmt_name)
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        fmt_arg = self.builder.bitcast(global_fmt, ir.IntType(8).as_pointer())

        array_type = global_array.type.pointee
        for i in range(array_type.count):
            element_ptr = self.builder.gep(global_array, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), i)])
            element = self.builder.load(element_ptr)
            self.builder.call(self.printf, [fmt_arg, element])
        
        self.print_newline()

    def print_newline(self):
        global global_string_counter
        newline_fmt = "\n\0"
        c_newline_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(newline_fmt)), bytearray(newline_fmt.encode("utf8")))
        global_newline_fmt_name = f"fstr{global_string_counter}"
        global_string_counter += 1

        global_newline_fmt = ir.GlobalVariable(self.module, c_newline_fmt.type, name=global_newline_fmt_name)
        global_newline_fmt.linkage = 'internal'
        global_newline_fmt.global_constant = True
        global_newline_fmt.initializer = c_newline_fmt
        newline_fmt_arg = self.builder.bitcast(global_newline_fmt, ir.IntType(8).as_pointer())
        self.builder.call(self.printf, [newline_fmt_arg])

class ForLoop:
    def __init__(self, builder, module, printf, variable, start_expr, end_expr, body):
        self.builder = builder
        self.module = module
        self.printf = printf
        self.variable = variable
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.body = body
        self.break_block = None

    def eval(self, context):
        start_val = self.start_expr.eval(context)
        end_val = self.end_expr.eval(context)

        if self.variable not in context:
            loop_var = ir.GlobalVariable(self.module, ir.IntType(32), self.variable)
            loop_var.initializer = ir.Constant(ir.IntType(32), 0)
            context[self.variable] = loop_var
        else:
            loop_var = context[self.variable]

        self.builder.store(start_val, loop_var)

        cond_block = self.builder.append_basic_block('cond')
        loop_block = self.builder.append_basic_block('loop')
        after_loop_block = self.builder.append_basic_block('afterloop')
        self.break_block = after_loop_block

        self.builder.branch(cond_block)
        self.builder.position_at_end(cond_block)

        loop_val = self.builder.load(loop_var)
        cond = self.builder.icmp_signed('<=', loop_val, end_val)
        self.builder.cbranch(cond, loop_block, after_loop_block)

        self.builder.position_at_end(loop_block)

        new_context = context.copy()
        new_context[self.variable] = loop_var
        new_context['loop_context'] = self

        for stmt in self.body:
            stmt.eval(new_context)

        if not self.builder.block.is_terminated:
            incremented_val = self.builder.add(loop_val, ir.Constant(ir.IntType(32), 1))
            self.builder.store(incremented_val, loop_var)
            self.builder.branch(cond_block)

        self.builder.position_at_end(after_loop_block)

class LengthFunc:
    def __init__(self, builder, module, name):
        self.builder = builder
        self.module = module
        self.name = name

    def eval(self, context):
        array = context[self.name]
        array_type = array.type.pointee
        length = array_type.count
        return ir.Constant(ir.IntType(32), length)
    
class FunctionCall:
    def __init__(self, builder, module, name, args):
        self.builder = builder
        self.module = module
        self.name = name
        self.args = args

    def eval(self, context):
        if self.name == 'length':
            array_name = self.args[0]
            array = context[array_name]
            array_type = array.type.pointee
            length = array_type.count
            return ir.Constant(ir.IntType(32), length)
        else:
            raise NotImplementedError(f"Function '{self.name}' is not implemented")

class Expression:
    def __init__(self, builder, module, left, operator, right):
        self.builder = builder
        self.module = module
        self.left = left
        self.operator = operator
        self.right = right

    def eval(self, context):
        left_val = self.left.eval(context)
        right_val = self.right.eval(context)

        if not isinstance(left_val, ir.Value):
            left_val = ir.Constant(ir.IntType(32), left_val)
        if not isinstance(right_val, ir.Value):
            right_val = ir.Constant(ir.IntType(32), right_val)

        if self.operator == 'SUM':
            return self.builder.add(left_val, right_val)
        elif self.operator == 'SUB':
            return self.builder.sub(left_val, right_val)
        elif self.operator == 'MUL':
            return self.builder.mul(left_val, right_val)
        elif self.operator == 'DIV':
            return self.builder.sdiv(left_val, right_val)
        elif self.operator == 'MOD':
            return self.builder.srem(left_val, right_val)
        elif self.operator == 'POW':
            left_float = self.builder.uitofp(left_val, ir.DoubleType())
            right_float = self.builder.uitofp(right_val, ir.DoubleType())
            pow_func = self.module.declare_intrinsic('llvm.pow', [ir.DoubleType()])
            result = self.builder.call(pow_func, [left_float, right_float])
            return self.builder.fptoui(result, ir.IntType(32))

class Break:
    def __init__(self, builder):
        self.builder = builder

    def eval(self, context):
        loop_context = context.get('loop_context')
        if loop_context is not None and hasattr(loop_context, 'break_block'):
            if not self.builder.block.is_terminated:
                self.builder.branch(loop_context.break_block)
        else:
            raise ValueError("Break statement outside of loop")
        
class Visualiza:
    def __init__(self, source):
        self.source = source

    def eval(self, context):
        with open(self.source.strip('"'), 'r') as f:
            code = f.read()
        visualizer = VisualizadorDebug(code)
        visualizer.run()