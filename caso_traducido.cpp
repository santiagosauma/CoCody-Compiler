#include <iostream>

int main() {
  double n = 10;
  double a = 0;
  double b = 1;

  std::cout << a << std::endl;
  std::cout << b << std::endl;

  double contador = 2;
  while (contador < n) {
    double aux = a + b;
    std::cout << aux << std::endl;
    a = b;
    b = aux;
    contador += 1;
  }
  return 0;
}