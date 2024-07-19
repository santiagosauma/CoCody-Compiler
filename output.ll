; ModuleID = "S:\Hackatones\Primer Hackaton Código Facilito\CoCody-Compiler\codegen.py"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

define void @"main"()
{
entry:
  store i32 5, i32* @"n"
  store i32 4, i32* @"clave"
  store i32 0, i32* @"encontrado"
  %".5" = load i32, i32* @"n"
  store i32 %".5", i32* @"indice"
  %".7" = load i32, i32* @"n"
  %".8" = sub i32 %".7", 1
  store i32 0, i32* @"i"
  br label %"cond"
cond:
  %".11" = load i32, i32* @"i"
  %".12" = icmp sle i32 %".11", %".8"
  br i1 %".12", label %"loop", label %"afterloop"
loop:
  %".14" = load i32, i32* @"encontrado"
  %".15" = icmp eq i32 %".14", 0
  br i1 %".15", label %"then", label %"endif"
afterloop:
  %".31" = load i32, i32* @"encontrado"
  %".32" = icmp eq i32 %".31", 1
  br i1 %".32", label %"then.2", label %"endif.2"
then:
  %".17" = load i32, i32* @"i"
  %".18" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".17"
  %".19" = load i32, i32* %".18"
  %".20" = load i32, i32* @"clave"
  %".21" = icmp eq i32 %".19", %".20"
  br i1 %".21", label %"then.1", label %"endif.1"
endif:
  %".28" = add i32 %".11", 1
  store i32 %".28", i32* @"i"
  br label %"cond"
then.1:
  store i32 1, i32* @"encontrado"
  %".24" = load i32, i32* @"i"
  store i32 %".24", i32* @"indice"
  br label %"endif.1"
endif.1:
  br label %"endif"
then.2:
  %".34" = bitcast [30 x i8]* @"str0" to i8*
  %".35" = bitcast [5 x i8]* @"fstr1" to i8*
  %".36" = call i32 (i8*, ...) @"printf"(i8* %".35", i8* %".34")
  %".37" = load i32, i32* @"indice"
  %".38" = bitcast [5 x i8]* @"fstr2" to i8*
  %".39" = call i32 (i8*, ...) @"printf"(i8* %".38", i32 %".37")
  br label %"endif.2"
endif.2:
  ret void
}

declare i32 @"printf"(i8* %".1", ...)

@"lista" = internal global [5 x i32] [i32 5, i32 3, i32 8, i32 4, i32 2]
@"n" = internal global i32 0
@"clave" = internal global i32 0
@"encontrado" = internal global i32 0
@"indice" = internal global i32 0
@"i" = global i32 0
@"str0" = internal constant [30 x i8] c"Elemento encontrado en indice\00"
@"fstr1" = internal constant [5 x i8] c"%s \0a\00"
@"fstr2" = internal constant [5 x i8] c"%i \0a\00"