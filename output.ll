; ModuleID = "S:\Hackatones\Primer Hackaton Código Facilito\CoCody-Compiler\codegen.py"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

define void @"main"()
{
entry:
  %".2" = getelementptr i32, i32* @"x", i32 0
  store i32 2, i32* %".2"
  %".4" = getelementptr i32, i32* @"y", i32 0
  store i32 3, i32* %".4"
  %".6" = getelementptr i32, i32* @"resultado", i32 0
  %".7" = load i32, i32* @"x"
  %".8" = load i32, i32* @"y"
  %".9" = uitofp i32 %".7" to double
  %".10" = uitofp i32 %".8" to double
  %".11" = call double @"llvm.pow.f64"(double %".9", double %".10")
  %".12" = fptoui double %".11" to i32
  store i32 %".12", i32* %".6"
  %".14" = load i32, i32* @"resultado"
  %".15" = bitcast [5 x i8]* @"fstr0" to i8*
  %".16" = call i32 (i8*, ...) @"printf"(i8* %".15", i32 %".14")
  ret void
}

declare i32 @"printf"(i8* %".1", ...)

@"x" = global i32 0
@"y" = global i32 0
@"resultado" = global i32 0
declare double @"llvm.pow.f64"(double %".1", double %".2")

@"fstr0" = internal constant [5 x i8] c"%i \0a\00"