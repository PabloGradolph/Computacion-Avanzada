#include <iostream>
#include <math.h>
#include <iomanip>
#include <stdlib.h>
#include <time.h>
using namespace std;

#include <chrono>
using namespace chrono;

double CirculoMontecarlo(int N, double r){
    double x, y;
    // Método de Montecarlo
    int exitos = 0;
    for (int i=0; i++; i<=N){
        x = rand() % 101;
        x = x/100.;
        y = rand() % 101;
        y = y/100.;

        if (y<=sqrt(1-(x*x))){
            exitos++;
        }
    }

    double area;
    area = 4 * ((exitos/N) * (r*r));
    return area;
}

int main(){
    time_point<system_clock> start, end;
    duration<double> elapsed_seconds;
    start = system_clock::now();

    int N = 100;
    double area = CirculoMontecarlo(N,1);
    cout<<"Area del circulo con "<<N<<" intentos = "<<area<<". Error cometido = "<<fabs(area-M_PI)<<endl;

    N = 1000;
    area = CirculoMontecarlo(N,1);
    cout<<"Area del circulo con "<<N<<" intentos = "<<area<<". Error cometido = "<<fabs(area-M_PI)<<endl;

    N = 10000;
    area = CirculoMontecarlo(N,1);
    cout<<"Area del circulo con "<<N<<" intentos = "<<area<<". Error cometido = "<<fabs(area-M_PI)<<endl;

    N = 100000;
    area = CirculoMontecarlo(N,1);
    cout<<"Area del circulo con "<<N<<" intentos = "<<area<<". Error cometido = "<<fabs(area-M_PI)<<endl;

    N = 1000000;
    area = CirculoMontecarlo(N,1);
    cout<<"Area del circulo con "<<N<<" intentos = "<<area<<". Error cometido = "<<fabs(area-M_PI)<<endl;

    N = 10000000;
    area = CirculoMontecarlo(N,1);
    cout<<"Area del circulo con "<<N<<" intentos = "<<area<<". Error cometido = "<<fabs(area-M_PI)<<endl;

    end = system_clock::now();
    elapsed_seconds = end - start;
    cout<<"* Tiempo de ejecucion del programa (s) = "<<elapsed_seconds.count()<<endl;

    return 0;
}