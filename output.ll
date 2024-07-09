; ModuleID = "S:\Hackatones\Primer Hackaton Código Facilito\CoCody-Compiler\codegen.py"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

define void @"main"()
{
entry:
  store i32 5, i32* @"a"
  store i32 3, i32* @"b"
  %".4" = load i32, i32* @"a"
  %".5" = load i32, i32* @"b"
  %".6" = add i32 %".4", %".5"
  store i32 %".6", i32* @"suma"
  %".8" = load i32, i32* @"suma"
  %".9" = bitcast [5 x i8]* @"fstr0" to i8*
  %".10" = call i32 (i8*, ...) @"printf"(i8* %".9", i32 %".8")
  %".11" = load i32, i32* @"a"
  %".12" = load i32, i32* @"b"
  %".13" = sub i32 %".11", %".12"
  store i32 %".13", i32* @"resta"
  %".15" = load i32, i32* @"resta"
  %".16" = bitcast [5 x i8]* @"fstr1" to i8*
  %".17" = call i32 (i8*, ...) @"printf"(i8* %".16", i32 %".15")
  %".18" = load i32, i32* @"a"
  %".19" = load i32, i32* @"b"
  %".20" = mul i32 %".18", %".19"
  store i32 %".20", i32* @"multiplicacion"
  %".22" = load i32, i32* @"multiplicacion"
  %".23" = bitcast [5 x i8]* @"fstr2" to i8*
  %".24" = call i32 (i8*, ...) @"printf"(i8* %".23", i32 %".22")
  %".25" = load i32, i32* @"a"
  %".26" = load i32, i32* @"b"
  %".27" = sdiv i32 %".25", %".26"
  store i32 %".27", i32* @"division"
  %".29" = load i32, i32* @"division"
  %".30" = bitcast [5 x i8]* @"fstr3" to i8*
  %".31" = call i32 (i8*, ...) @"printf"(i8* %".30", i32 %".29")
  %".32" = load i32, i32* @"a"
  %".33" = load i32, i32* @"b"
  %".34" = srem i32 %".32", %".33"
  store i32 %".34", i32* @"modulo"
  %".36" = load i32, i32* @"modulo"
  %".37" = bitcast [5 x i8]* @"fstr4" to i8*
  %".38" = call i32 (i8*, ...) @"printf"(i8* %".37", i32 %".36")
  %".39" = load i32, i32* @"a"
  %".40" = load i32, i32* @"b"
  %".41" = uitofp i32 %".39" to double
  %".42" = uitofp i32 %".40" to double
  %".43" = call double @"llvm.pow.f64"(double %".41", double %".42")
  %".44" = fptoui double %".43" to i32
  store i32 %".44", i32* @"potencia"
  %".46" = load i32, i32* @"potencia"
  %".47" = bitcast [5 x i8]* @"fstr5" to i8*
  %".48" = call i32 (i8*, ...) @"printf"(i8* %".47", i32 %".46")
  ret void
}

declare i32 @"printf"(i8* %".1", ...)

@"a" = internal global i32 0
@"b" = internal global i32 0
@"suma" = internal global i32 0
@"fstr0" = internal constant [5 x i8] c"%i \0a\00"
@"resta" = internal global i32 0
@"fstr1" = internal constant [5 x i8] c"%i \0a\00"
@"multiplicacion" = internal global i32 0
@"fstr2" = internal constant [5 x i8] c"%i \0a\00"
@"division" = internal global i32 0
@"fstr3" = internal constant [5 x i8] c"%i \0a\00"
@"modulo" = internal global i32 0
@"fstr4" = internal constant [5 x i8] c"%i \0a\00"
declare double @"llvm.pow.f64"(double %".1", double %".2")

@"potencia" = internal global i32 0
@"fstr5" = internal constant [5 x i8] c"%i \0a\00"