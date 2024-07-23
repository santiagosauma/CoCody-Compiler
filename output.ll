; ModuleID = "S:\Hackatones\Primer Hackaton Código Facilito\CoCody-Compiler\codegen.py"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

define void @"main"()
{
entry:
  store i32 0, i32* @"i"
  br label %"cond"
cond:
  %".4" = load i32, i32* @"i"
  %".5" = icmp sle i32 %".4", 10
  br i1 %".5", label %"loop", label %"afterloop"
loop:
  %".7" = load i32, i32* @"i"
  %".8" = icmp eq i32 %".7", 5
  br i1 %".8", label %"then", label %"ifcont"
afterloop:
  ret void
then:
  br label %"afterloop"
ifcont:
  %".11" = load i32, i32* @"i"
  %".12" = bitcast [4 x i8]* @"fstr0" to i8*
  %".13" = call i32 (i8*, ...) @"printf"(i8* %".12", i32 %".11")
  %".14" = add i32 %".4", 1
  store i32 %".14", i32* @"i"
  br label %"cond"
}

declare i32 @"printf"(i8* %".1", ...)

@"i" = global i32 0
@"fstr0" = internal constant [4 x i8] c"%i\0a\00"