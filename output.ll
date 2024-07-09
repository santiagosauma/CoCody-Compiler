; ModuleID = "S:\Hackatones\Primer Hackaton Código Facilito\CoCody-Compiler\codegen.py"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

define void @"main"()
{
entry:
  store i32 0, i32* @"i"
  br label %"loop"
loop:
  %".4" = load i32, i32* @"i"
  %".5" = icmp slt i32 %".4", 5
  br i1 %".5", label %"loop.if", label %"loop.endif"
afterloop:
  ret void
loop.if:
  %".7" = load i32, i32* @"i"
  %".8" = bitcast [5 x i8]* @"fstr0" to i8*
  %".9" = call i32 (i8*, ...) @"printf"(i8* %".8", i32 %".7")
  %".10" = load i32, i32* @"i"
  %".11" = add i32 %".10", 1
  store i32 %".11", i32* @"i"
  br label %"loop"
loop.endif:
  br label %"afterloop"
}

declare i32 @"printf"(i8* %".1", ...)

@"i" = internal global i32 0
@"fstr0" = internal constant [5 x i8] c"%i \0a\00"