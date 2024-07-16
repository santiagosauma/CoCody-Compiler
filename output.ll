; ModuleID = "D:\Code Cursos en Local\hack-cody\CoCody-Compiler\codegen.py"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

define void @"main"()
{
entry:
  ret void
}

declare i32 @"printf"(i8* %".1", ...)
  store i32 0, i32* @"i"
  br label %"cond_block"
cond_block:
  %".4" = load i32, i32* @"i"
  %".5" = icmp slt i32 %".4", 5
  br i1 %".5", label %"loop", label %"afterloop"
loop:
  %".7" = load i32, i32* @"i"
  %".8" = bitcast [5 x i8]* @"fstr0" to i8*
  %".9" = call i32 (i8*, ...) @"printf"(i8* %".8", i32 %".7")
  %".10" = load i32, i32* @"i"
  %".11" = add i32 %".10", 1
  store i32 %".11", i32* @"i"
  br label %"cond_block"
afterloop:
  ret void
}

declare i32 @"printf"(i8* %".1", ...)

@"i" = internal global i32 0
<<<<<<< HEAD
@"fstr0" = internal constant [5 x i8] c"%i \0a\00"
=======
@"str0" = internal constant [21 x i8] c"Valor par encontrado\00"
@"fstr1" = internal constant [5 x i8] c"%s \0a\00"
@"fstr2" = internal constant [5 x i8] c"%i \0a\00"
>>>>>>> origin/feature/add-translate-from-cody-to-language
