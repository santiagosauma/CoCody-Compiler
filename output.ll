; ModuleID = "S:\Hackatones\Primer Hackaton C�digo Facilito\CoCody-Compiler\codegen.py"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

define void @"main"()
{
entry:
  store i32 0, i32* @"i"
  br label %"cond_block"
cond_block:
  %".4" = load i32, i32* @"i"
  %".5" = icmp slt i32 %".4", 5
  br i1 %".5", label %"loop", label %"afterloop"
loop:
  %".7" = load i32, i32* @"i"
  %".8" = bitcast [5 x i8]* @"fstr0" to i8*
  %".9" = call i32 (i8*, ...) @"printf"(i8* %".8", i32 1)
  %".10" = load i32, i32* @"i"
  %".11" = add i32 %".10", 1
  store i32 %".11", i32* @"i"
  br label %"cond_block"
afterloop:
  ret void
}

declare i32 @"printf"(i8* %".1", ...)

@"mi_lista" = internal global [5 x i32] [i32 1, i32 2, i32 3, i32 4, i32 5]
@"i" = internal global i32 0
@"fstr0" = internal constant [5 x i8] c"%i \0a\00"