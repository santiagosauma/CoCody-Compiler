; ModuleID = "S:\Hackatones\Primer Hackaton Código Facilito\CoCody-Compiler\codegen.py"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

define void @"main"()
{
entry:
  %".2" = getelementptr i32, i32* @"x", i32 0
  store i32 0, i32* %".2"
  br label %"loop"
loop:
  %".5" = load i32, i32* @"x"
  %".6" = icmp slt i32 %".5", 10
  br i1 %".6", label %"loop.if", label %"loop.endif"
afterloop:
  %".22" = bitcast [14 x i8]* @"str1" to i8*
  %".23" = bitcast [5 x i8]* @"fstr1" to i8*
  %".24" = call i32 (i8*, ...) @"printf"(i8* %".23", i8* %".22")
  ret void
loop.if:
  %".8" = getelementptr i32, i32* @"x", i32 0
  %".9" = load i32, i32* @"x"
  %".10" = add i32 %".9", 1
  store i32 %".10", i32* %".8"
  %".12" = load i32, i32* @"x"
  %".13" = srem i32 %".12", 2
  %".14" = icmp ne i32 %".13", 0
  br i1 %".14", label %"then", label %"endif"
loop.endif:
  br label %"afterloop"
then:
  %".16" = load i32, i32* @"x"
  %".17" = bitcast [5 x i8]* @"fstr0" to i8*
  %".18" = call i32 (i8*, ...) @"printf"(i8* %".17", i32 %".16")
  br label %"endif"
endif:
  br label %"loop"
}

declare i32 @"printf"(i8* %".1", ...)

@"x" = global i32 0
@"fstr0" = internal constant [5 x i8] c"%i \0a\00"
@"str1" = internal constant [14 x i8] c"Fin del ciclo\00"
@"fstr1" = internal constant [5 x i8] c"%s \0a\00"