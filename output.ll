; ModuleID = "S:\Hackatones\Primer Hackaton Código Facilito\CoCody-Compiler\codegen.py"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

define void @"main"()
{
entry:
  %".2" = getelementptr i32, i32* @"a", i32 0
  store i32 0, i32* %".2"
  %".4" = getelementptr i32, i32* @"b", i32 0
  store i32 10, i32* %".4"
  %"i" = alloca i32
  store i32 0, i32* %"i"
  br label %"loop"
loop:
  %".8" = load i32, i32* %"i"
  %".9" = icmp slt i32 %".8", 10
  br i1 %".9", label %"loop.if", label %"loop.endif"
afterloop:
  %".22" = load i32, i32* @"a"
  %".23" = bitcast [5 x i8]* @"fstr1" to i8*
  %".24" = call i32 (i8*, ...) @"printf"(i8* %".23", i32 %".22")
  %".25" = load i32, i32* @"a"
  %".26" = icmp eq i32 %".25", 10
  br i1 %".26", label %"then", label %"endif"
loop.if:
  %".11" = load i32, i32* @"a"
  %".12" = bitcast [5 x i8]* @"fstr0" to i8*
  %".13" = call i32 (i8*, ...) @"printf"(i8* %".12", i32 %".11")
  %".14" = getelementptr i32, i32* @"a", i32 0
  %".15" = load i32, i32* @"a"
  %".16" = add i32 %".15", 1
  store i32 %".16", i32* %".14"
  %".18" = add i32 %".8", 1
  store i32 %".18", i32* %"i"
  br label %"loop"
loop.endif:
  br label %"afterloop"
then:
  %".28" = bitcast [20 x i8]* @"str2" to i8*
  %".29" = bitcast [5 x i8]* @"fstr2" to i8*
  %".30" = call i32 (i8*, ...) @"printf"(i8* %".29", i8* %".28")
  br label %"endif"
endif:
  ret void
}

declare i32 @"printf"(i8* %".1", ...)

@"a" = global i32 0
@"b" = global i32 0
@"fstr0" = internal constant [5 x i8] c"%i \0a\00"
@"fstr1" = internal constant [5 x i8] c"%i \0a\00"
@"str2" = internal constant [20 x i8] c"El valor de a es 10\00"
@"fstr2" = internal constant [5 x i8] c"%s \0a\00"