; ModuleID = "S:\Hackatones\Primer Hackaton Código Facilito\CoCody-Compiler\codegen.py"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

define void @"main"()
{
entry:
  store i32 10, i32* @"n"
  store i32 0, i32* @"a"
  store i32 1, i32* @"b"
  %".5" = load i32, i32* @"a"
  %".6" = bitcast [5 x i8]* @"fstr0" to i8*
  %".7" = call i32 (i8*, ...) @"printf"(i8* %".6", i32 %".5")
  %".8" = load i32, i32* @"b"
  %".9" = bitcast [5 x i8]* @"fstr1" to i8*
  %".10" = call i32 (i8*, ...) @"printf"(i8* %".9", i32 %".8")
  store i32 2, i32* @"contador"
  br label %"cond_block"
cond_block:
  %".13" = load i32, i32* @"contador"
  %".14" = load i32, i32* @"n"
  %".15" = icmp slt i32 %".13", %".14"
  br i1 %".15", label %"loop", label %"afterloop"
loop:
  %".17" = load i32, i32* @"a"
  %".18" = load i32, i32* @"b"
  %".19" = add i32 %".17", %".18"
  store i32 %".19", i32* @"aux"
  %".21" = load i32, i32* @"aux"
  %".22" = bitcast [5 x i8]* @"fstr2" to i8*
  %".23" = call i32 (i8*, ...) @"printf"(i8* %".22", i32 %".21")
  %".24" = load i32, i32* @"b"
  store i32 %".24", i32* @"a"
  %".26" = load i32, i32* @"aux"
  store i32 %".26", i32* @"b"
  %".28" = load i32, i32* @"contador"
  %".29" = add i32 %".28", 1
  store i32 %".29", i32* @"contador"
  br label %"cond_block"
afterloop:
  ret void
}

declare i32 @"printf"(i8* %".1", ...)

@"n" = internal global i32 0
@"a" = internal global i32 0
@"b" = internal global i32 0
@"fstr0" = internal constant [5 x i8] c"%i \0a\00"
@"fstr1" = internal constant [5 x i8] c"%i \0a\00"
@"contador" = internal global i32 0
@"aux" = internal global i32 0
@"fstr2" = internal constant [5 x i8] c"%i \0a\00"