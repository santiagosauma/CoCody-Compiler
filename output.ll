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
  %".10" = srem i32 %".9", 2
  %".11" = icmp eq i32 %".10", 0
  br i1 %".11", label %"then", label %"else"
afterloop:
  ret void
then:
  %".13" = bitcast [21 x i8]* @"str0" to i8*
  %".14" = bitcast [5 x i8]* @"fstr1" to i8*
  %".15" = call i32 (i8*, ...) @"printf"(i8* %".14", i8* %".13")
  br label %"endif"
else:
  br label %"endif"
endif:
  %".18" = load i32, i32* @"i"
  %".19" = getelementptr [5 x i32], [5 x i32]* @"mi_lista", i32 0, i32 %".18"
  %".20" = load i32, i32* %".19"
  %".21" = bitcast [5 x i8]* @"fstr2" to i8*
  %".22" = call i32 (i8*, ...) @"printf"(i8* %".21", i32 %".20")
  %".23" = load i32, i32* @"i"
  %".24" = add i32 %".23", 1
  store i32 %".24", i32* @"i"
  br label %"cond_block"
}

declare i32 @"printf"(i8* %".1", ...)

@"mi_lista" = internal global [5 x i32] [i32 5, i32 10, i32 15, i32 20, i32 25]
@"i" = internal global i32 0
@"str0" = internal constant [21 x i8] c"Valor par encontrado\00"
@"fstr1" = internal constant [5 x i8] c"%s \0a\00"
@"fstr2" = internal constant [5 x i8] c"%i \0a\00"