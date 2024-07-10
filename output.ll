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
  %".5" = icmp slt i32 %".4", 10
  br i1 %".5", label %"loop", label %"afterloop"
loop:
  %".7" = load i32, i32* @"i"
  %".8" = srem i32 %".7", 2
  %".9" = icmp eq i32 %".8", 0
  br i1 %".9", label %"then", label %"endif"
afterloop:
  ret void
then:
  %".11" = load i32, i32* @"i"
  %".12" = bitcast [5 x i8]* @"fstr0" to i8*
  %".13" = call i32 (i8*, ...) @"printf"(i8* %".12", i32 %".11")
  br label %"endif"
endif:
  %".15" = load i32, i32* @"i"
  %".16" = add i32 %".15", 1
  store i32 %".16", i32* @"i"
  br label %"cond_block"
}

declare i32 @"printf"(i8* %".1", ...)

@"i" = internal global i32 0
@"fstr0" = internal constant [5 x i8] c"%i \0a\00"