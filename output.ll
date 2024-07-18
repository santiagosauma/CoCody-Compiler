; ModuleID = "S:\Hackatones\Primer Hackaton Código Facilito\CoCody-Compiler\codegen.py"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

define void @"main"()
{
entry:
  store i32 0, i32* @"i"
  %".3" = load i32, i32* @"i"
  %".4" = bitcast [5 x i8]* @"fstr0" to i8*
  %".5" = call i32 (i8*, ...) @"printf"(i8* %".4", i32 %".3")
  br label %"cond_block"
cond_block:
  %".7" = load i32, i32* @"i"
  %".8" = sub i32 5, 1
  %".9" = icmp slt i32 %".7", %".8"
  br i1 %".9", label %"loop", label %"afterloop"
loop:
  %".11" = load i32, i32* @"i"
  %".12" = bitcast [5 x i8]* @"fstr1" to i8*
  %".13" = call i32 (i8*, ...) @"printf"(i8* %".12", i32 %".11")
  %".14" = load i32, i32* @"i"
  %".15" = add i32 %".14", 1
  store i32 %".15", i32* @"i"
  br label %"cond_block"
afterloop:
  %".18" = sub i32 5, 1
  store i32 1, i32* @"j"
  br label %"cond"
cond:
  %".21" = load i32, i32* @"j"
  %".22" = icmp sle i32 %".21", %".18"
  br i1 %".22", label %"loop.1", label %"afterloop.1"
loop.1:
  %".24" = load i32, i32* @"j"
  %".25" = bitcast [5 x i8]* @"fstr2" to i8*
  %".26" = call i32 (i8*, ...) @"printf"(i8* %".25", i32 %".24")
  %".27" = add i32 %".21", 1
  store i32 %".27", i32* @"j"
  br label %"cond"
afterloop.1:
  ret void
}

declare i32 @"printf"(i8* %".1", ...)

@"i" = internal global i32 0
@"fstr0" = internal constant [5 x i8] c"%i \0a\00"
@"fstr1" = internal constant [5 x i8] c"%i \0a\00"
@"j" = global i32 0
@"fstr2" = internal constant [5 x i8] c"%i \0a\00"