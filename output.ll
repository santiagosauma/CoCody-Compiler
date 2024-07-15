; ModuleID = "S:\Hackatones\Primer Hackaton Código Facilito\CoCody-Compiler\codegen.py"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

define void @"main"()
{
entry:
  store i32 0, i32* @"x"
  store i32 5, i32* @"i"
  br label %"cond"
cond:
  %".5" = load i32, i32* @"i"
  %".6" = icmp sle i32 %".5", 5
  br i1 %".6", label %"loop", label %"afterloop"
loop:
  %".8" = load i32, i32* @"x"
  %".9" = add i32 %".8", 1
  store i32 %".9", i32* @"x"
  %".11" = add i32 %".5", 1
  store i32 %".11", i32* @"i"
  br label %"cond"
afterloop:
  %".14" = load i32, i32* @"x"
  %".15" = bitcast [5 x i8]* @"fstr0" to i8*
  %".16" = call i32 (i8*, ...) @"printf"(i8* %".15", i32 %".14")
  ret void
}

declare i32 @"printf"(i8* %".1", ...)

@"x" = internal global i32 0
@"i" = global i32 0
@"fstr0" = internal constant [5 x i8] c"%i \0a\00"