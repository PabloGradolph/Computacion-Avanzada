#include <iostream>
#include <math.h>
#include <iomanip>
using namespace std;

#include <chrono>
using namespace chrono;

double constanteMadelung(double L){
    // Del enunciado sacamos la fórmula para M que procedemos a programar.
    // Primero inicializamos en cero la constante.
    double M = 0;

    // Tres bucles para las 3 coordenadas.
    for (int i=-L; i<=L; i++){
        for (int j=-L; j<=L; j++){
            for (int k=-L; k<=L; k++){
                if ((i==0) && (j==0) && (k==0)){
                    continue;
                } else {
                    if ((i+j+k)%2==0){
                        M = M + (1/sqrt(i*i + j*j + k*k));
                    } else {
                        M = M - (1/sqrt(i*i + j*j + k*k));
                    }
                }
            }
        }
    }

    return M;
}

void errores(double exacto, double obtenido, double &Ea, double &Er){
    // Cálculo de los errores absoluto y relativo
    Ea = fabs(exacto - obtenido);
    Er = fabs(Ea/exacto)*100;
}

int main(){
    cout<<setprecision(10);

    // Medimos el tiempo de ejecución
    time_point<system_clock> start, end;
    duration<double> elapsed_seconds;
    start = system_clock::now();

    double Mexacta = -1.74756, Mobtenida = 0., Ea = 0., Er = 0., tol = 10e-5;
    int L = 100;

    // Para L = 20
    do {
        Mobtenida = constanteMadelung(L);
        errores(Mexacta, Mobtenida, Ea, Er);
        cout<<"Para L = "<<L<<" --> M = "<<Mobtenida<<"; Error absoluto = "<<Ea<<"; Error relativo = "<<Er<<"%"<<endl;
        L = L + 100;
    } while (fabs(Ea)>tol);

    cout<<"Tolerancia alcanzada para un L = "<<L-100<<endl<<endl;

    // Terminamos de medir el tiempo de ejecución.
    end = system_clock::now();
    elapsed_seconds = end - start;
    cout<<"* Tiempo de ejecucion del programa (s) = "<<elapsed_seconds.count()<<endl;

    return 0;
}