; ModuleID = "S:\Hackatones\Primer Hackaton Código Facilito\CoCody-Compiler\codegen.py"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

define void @"main"()
{
entry:
  store i32 3, i32* @"valor"
  %".3" = load i32, i32* @"valor"
  %".4" = bitcast [5 x i8]* @"fstr0" to i8*
  %".5" = call i32 (i8*, ...) @"printf"(i8* %".4", i32 %".3")
  store i32 10, i32* @"nuevo_valor"
  %".7" = load i32, i32* @"nuevo_valor"
  %".8" = bitcast [5 x i8]* @"fstr1" to i8*
  %".9" = call i32 (i8*, ...) @"printf"(i8* %".8", i32 %".7")
  ret void
}

declare i32 @"printf"(i8* %".1", ...)

@"mi_lista" = internal global [5 x i32] [i32 1, i32 2, i32 3, i32 4, i32 5]
@"valor" = global i32 0
@"fstr0" = internal constant [5 x i8] c"%i \0a\00"
@"nuevo_valor" = global i32 0
@"fstr1" = internal constant [5 x i8] c"%i \0a\00"