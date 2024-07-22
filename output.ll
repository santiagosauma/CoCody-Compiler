; ModuleID = "S:\Hackatones\Primer Hackaton Código Facilito\CoCody-Compiler\codegen.py"
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
  %".8" = getelementptr [5 x i32], [5 x i32]* @"mi_lista", i32 0, i32 %".7"
  %".9" = load i32, i32* %".8"
  %".10" = icmp slt i32 %".9", 30
  br i1 %".10", label %"then", label %"ifcont"
afterloop:
  ret void
then:
  %".12" = load i32, i32* @"i"
  %".13" = load i32, i32* @"i"
  %".14" = getelementptr [5 x i32], [5 x i32]* @"mi_lista", i32 0, i32 %".13"
  %".15" = load i32, i32* %".14"
  %".16" = add i32 %".15", 5
  %".17" = getelementptr [5 x i32], [5 x i32]* @"mi_lista", i32 0, i32 %".12"
  store i32 %".16", i32* %".17"
  br label %"ifcont"
ifcont:
  %".20" = load i32, i32* @"i"
  %".21" = getelementptr [5 x i32], [5 x i32]* @"mi_lista", i32 0, i32 %".20"
  %".22" = load i32, i32* %".21"
  store i32 %".22", i32* @"valor"
  %".24" = load i32, i32* @"valor"
  %".25" = bitcast [5 x i8]* @"fstr0" to i8*
  %".26" = call i32 (i8*, ...) @"printf"(i8* %".25", i32 %".24")
  %".27" = load i32, i32* @"i"
  %".28" = add i32 %".27", 1
  store i32 %".28", i32* @"i"
  br label %"cond_block"
}

declare i32 @"printf"(i8* %".1", ...)

@"mi_lista" = internal global [5 x i32] [i32 10, i32 20, i32 30, i32 40, i32 50]
@"i" = internal global i32 0
@"valor" = internal global i32 0
@"fstr0" = internal constant [5 x i8] c"%i \0a\00"