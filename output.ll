; ModuleID = "S:\Hackatones\Primer Hackaton Código Facilito\CoCody-Compiler\codegen.py"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

define void @"main"()
{
entry:
  store i32 5, i32* @"n"
  %".3" = load i32, i32* @"n"
  %".4" = sub i32 %".3", 1
  store i32 1, i32* @"i"
  br label %"cond"
cond:
  %".7" = load i32, i32* @"i"
  %".8" = icmp sle i32 %".7", %".4"
  br i1 %".8", label %"loop", label %"afterloop"
loop:
  %".10" = load i32, i32* @"i"
  %".11" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".10"
  %".12" = load i32, i32* %".11"
  store i32 %".12", i32* @"clave"
  %".14" = load i32, i32* @"i"
  %".15" = sub i32 %".14", 1
  store i32 %".15", i32* @"j"
  br label %"cond_block"
afterloop:
  %".46" = load i32, i32* @"n"
  %".47" = sub i32 %".46", 1
  store i32 0, i32* @"k"
  br label %"cond.1"
cond_block:
  %".18" = load i32, i32* @"j"
  %".19" = icmp sge i32 %".18", 0
  %".20" = load i32, i32* @"j"
  %".21" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".20"
  %".22" = load i32, i32* %".21"
  %".23" = load i32, i32* @"clave"
  %".24" = icmp sgt i32 %".22", %".23"
  %".25" = and i1 %".19", %".24"
  br i1 %".25", label %"loop.1", label %"afterloop.1"
loop.1:
  %".27" = load i32, i32* @"j"
  %".28" = add i32 %".27", 1
  %".29" = load i32, i32* @"j"
  %".30" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".29"
  %".31" = load i32, i32* %".30"
  %".32" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".28"
  store i32 %".31", i32* %".32"
  %".34" = load i32, i32* @"j"
  %".35" = sub i32 %".34", 1
  store i32 %".35", i32* @"j"
  br label %"cond_block"
afterloop.1:
  %".38" = load i32, i32* @"j"
  %".39" = add i32 %".38", 1
  %".40" = load i32, i32* @"clave"
  %".41" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".39"
  store i32 %".40", i32* %".41"
  %".43" = add i32 %".7", 1
  store i32 %".43", i32* @"i"
  br label %"cond"
cond.1:
  %".50" = load i32, i32* @"k"
  %".51" = icmp sle i32 %".50", %".47"
  br i1 %".51", label %"loop.2", label %"afterloop.2"
loop.2:
  %".53" = load i32, i32* @"k"
  %".54" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".53"
  %".55" = load i32, i32* %".54"
  %".56" = bitcast [4 x i8]* @"fstr0" to i8*
  %".57" = call i32 (i8*, ...) @"printf"(i8* %".56", i32 %".55")
  %".58" = add i32 %".50", 1
  store i32 %".58", i32* @"k"
  br label %"cond.1"
afterloop.2:
  ret void
}

declare i32 @"printf"(i8* %".1", ...)

@"lista" = internal global [5 x i32] [i32 5, i32 3, i32 8, i32 4, i32 2]
@"n" = internal global i32 0
@"i" = global i32 0
@"clave" = internal global i32 0
@"j" = internal global i32 0
@"k" = global i32 0
@"fstr0" = internal constant [4 x i8] c"%i\0a\00"