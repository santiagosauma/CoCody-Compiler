; ModuleID = "S:\Hackatones\Primer Hackaton Código Facilito\CoCody-Compiler\codegen.py"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

define void @"main"()
{
entry:
  store i32 5, i32* @"n"
  %".3" = load i32, i32* @"n"
  %".4" = sub i32 %".3", 1
  store i32 0, i32* @"i"
  br label %"cond"
cond:
  %".7" = load i32, i32* @"i"
  %".8" = icmp sle i32 %".7", %".4"
  br i1 %".8", label %"loop", label %"afterloop"
loop:
  %".10" = load i32, i32* @"n"
  %".11" = load i32, i32* @"i"
  %".12" = sub i32 %".10", %".11"
  %".13" = sub i32 %".12", 2
  store i32 0, i32* @"j"
  br label %"cond.1"
afterloop:
  %".51" = load i32, i32* @"n"
  %".52" = sub i32 %".51", 1
  store i32 0, i32* @"k"
  br label %"cond.2"
cond.1:
  %".16" = load i32, i32* @"j"
  %".17" = icmp sle i32 %".16", %".13"
  br i1 %".17", label %"loop.1", label %"afterloop.1"
loop.1:
  %".19" = load i32, i32* @"j"
  %".20" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".19"
  %".21" = load i32, i32* %".20"
  %".22" = load i32, i32* @"j"
  %".23" = add i32 %".22", 1
  %".24" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".23"
  %".25" = load i32, i32* %".24"
  %".26" = icmp sgt i32 %".21", %".25"
  br i1 %".26", label %"then", label %"ifcont"
afterloop.1:
  %".48" = add i32 %".7", 1
  store i32 %".48", i32* @"i"
  br label %"cond"
then:
  %".28" = load i32, i32* @"j"
  %".29" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".28"
  %".30" = load i32, i32* %".29"
  store i32 %".30", i32* @"temp"
  %".32" = load i32, i32* @"j"
  %".33" = load i32, i32* @"j"
  %".34" = add i32 %".33", 1
  %".35" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".34"
  %".36" = load i32, i32* %".35"
  %".37" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".32"
  store i32 %".36", i32* %".37"
  %".39" = load i32, i32* @"j"
  %".40" = add i32 %".39", 1
  %".41" = load i32, i32* @"temp"
  %".42" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".40"
  store i32 %".41", i32* %".42"
  br label %"ifcont"
ifcont:
  %".45" = add i32 %".16", 1
  store i32 %".45", i32* @"j"
  br label %"cond.1"
cond.2:
  %".55" = load i32, i32* @"k"
  %".56" = icmp sle i32 %".55", %".52"
  br i1 %".56", label %"loop.2", label %"afterloop.2"
loop.2:
  %".58" = load i32, i32* @"k"
  %".59" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".58"
  %".60" = load i32, i32* %".59"
  %".61" = bitcast [4 x i8]* @"fstr0" to i8*
  %".62" = call i32 (i8*, ...) @"printf"(i8* %".61", i32 %".60")
  %".63" = add i32 %".55", 1
  store i32 %".63", i32* @"k"
  br label %"cond.2"
afterloop.2:
  ret void
}

declare i32 @"printf"(i8* %".1", ...)

@"lista" = internal global [5 x i32] [i32 5, i32 0, i32 2, i32 15, i32 1]
@"n" = internal global i32 0
@"i" = global i32 0
@"j" = global i32 0
@"temp" = internal global i32 0
@"k" = global i32 0
@"fstr0" = internal constant [4 x i8] c"%i\0a\00"