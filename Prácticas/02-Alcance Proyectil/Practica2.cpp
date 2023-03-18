#include <iostream>
#include <fstream>
#include <string>
#include <math.h>
#include <iomanip>
using namespace std;

#include <cmatrix> // Necesario instalar esta librería para ejecutar el programa.
using namespace techsoft;

double g = 9.8;

// Transforma grados a radianes
double radianes(double angulo){
    double rad = angulo * M_PI/180.;
    return rad;
}

// Generador de nombres de ficheros
string fname(string roz, string aprox, string angulo){
  string fend = "Pt2_RK4_"+roz+"_"+aprox+"_"+angulo+".txt";
  return fend;
}

// Devuelve la matriz Y' de cada iteración (sin rozamiento)
matrix<double> SistemaYPrimaSinrozamiento(matrix<double> Y){
    // Medimos la matriz de entrada y creamos la que será de salida con el mismo tamaño.
    int row = 0, col = 0;
    row = Y.rowno(); col = Y.colno();
    matrix<double> YPrima(row, col); YPrima.null();

    // Definimos los valores de la matriz YPrima
    YPrima(0,0) = Y(2,0);
    YPrima(1,0) = Y(3,0);
    YPrima(2,0) = 0.0;
    YPrima(3,0) = -g;
    return YPrima;
}

// Devuelve la matriz Y' de cada iteración (con rozamiento)
matrix<double> SistemaYPrimaConrozamiento(matrix<double> Y){
    // Medimos la matriz de entrada y creamos la que será de salida con el mismo tamaño.
    int row = 0, col = 0;
    row = Y.rowno(); col = Y.colno();
    matrix<double> YPrima(row, col); YPrima.null();

    // Definimos los valores de la matriz YPrima
    YPrima(0,0) = Y(2,0);
    YPrima(1,0) = Y(3,0);
    YPrima(2,0) = - ((4e-5*Y(2,0))*(sqrt(pow(Y(2,0),2) + pow(Y(3,0),2))));
    YPrima(3,0) = - g - ((4e-5*Y(2,0))*(sqrt(pow(Y(2,0),2) + pow(Y(3,0),2))));
    return YPrima;
}

// Devuelve la matriz Y' de cada iteración (con rozamiento y aproximación isoterma)
matrix<double> SistemaYPrimaIsotermo(matrix<double> Y){
    // Medimos la matriz de entrada y creamos la que será de salida con el mismo tamaño.
    int row = 0, col = 0;
    row = Y.rowno(); col = Y.colno();
    matrix<double> YPrima(row, col); YPrima.null();

    double y0 = 10e4;
    // Definimos los valores de la matriz YPrima
    YPrima(0,0) = Y(2,0);
    YPrima(1,0) = Y(3,0);
    YPrima(2,0) = - (exp(-Y(1,0)/y0)) * (4e-5*Y(2,0))*(sqrt(pow(Y(2,0),2) + pow(Y(3,0),2)));
    YPrima(3,0) = -g - (exp(-Y(1,0)/y0)) * (4e-5*Y(2,0))*(sqrt(pow(Y(2,0),2) + pow(Y(3,0),2)));
    return YPrima;
}

// Devuelve la matriz Y' de cada iteración (con rozamiento y aproximación adiabática)
matrix<double> SistemaYPrimaAdiabatico(matrix<double> Y){
    // Medimos la matriz de entrada y creamos la que será de salida con el mismo tamaño.
    int row = 0, col = 0;
    row = Y.rowno(); col = Y.colno();
    matrix<double> YPrima(row, col); YPrima.null();

    double a = 6.5e-3, alfa = 2.5, T = 300;
    // Definimos los valores de la matriz YPrima
    YPrima(0,0) = Y(2,0);
    YPrima(1,0) = Y(3,0);
    YPrima(2,0) = - (pow((1-a*Y(1,0)/T),alfa)) * (4e-5*Y(2,0))*(sqrt(pow(Y(2,0),2) + pow(Y(3,0),2)));
    YPrima(3,0) = -g - (pow((1-a*Y(1,0)/T),alfa)) * (4e-5*Y(2,0))*(sqrt(pow(Y(2,0),2) + pow(Y(3,0),2)));
    return YPrima;
}

// Resolución de sistemas de ecuaciones diferenciales por el método de Ronge-Kutta(cuarto orden).
void RK4Sistemas(double dt, double tmin, bool roz, int aproximacion, matrix<double> Y0, string angulo){
    double t = tmin;

    // Medimos el tamaño de la matriz de entrada
    int row = 0, col = 0;
    row = Y0.rowno(); col = Y0.colno();

    // Inicializamos la matriz Y.
    matrix<double> Y(row,col); Y.null();
    Y = Y0;

    // Definimos las matrices k.
    matrix<double> k1(row,col); k1.null();
    matrix<double> k2(row,col); k2.null();
    matrix<double> k3(row,col); k3.null();
    matrix<double> k4(row,col); k4.null();

    if (roz==false){
        k1 = SistemaYPrimaSinrozamiento(Y);
        k2 = SistemaYPrimaSinrozamiento(Y + 0.5*dt*k1);
        k3 = SistemaYPrimaSinrozamiento(Y + 0.5*dt*k2);
        k4 = SistemaYPrimaSinrozamiento(Y + dt*k3);
        string file = fname("sinrozamiento", "", angulo);
        ofstream ff(file);
        if (ff.is_open()){
            ff << "#DATOS PARA dt = " << dt << endl;
            ff << "Alcance\tAltura" << endl;
            ff << Y(0,0) << "\t" << Y(1,0) << endl;
            while (true) {
                Y = Y + 1/6. * (k1 + 2.*k2 + 2.*k3 + k4) * dt;
                t = t + dt;
                k1 = SistemaYPrimaSinrozamiento(Y);
                k2 = SistemaYPrimaSinrozamiento(Y + 0.5*dt*k1);
                k3 = SistemaYPrimaSinrozamiento(Y + 0.5*dt*k2);
                k4 = SistemaYPrimaSinrozamiento(Y + dt*k3);
                ff << Y(0,0) << "\t" << Y(1,0) << endl;
                if (Y(1,0)<0){
                    break;
                }
            }
        }
    } else {
        if (aproximacion == 0){
            k1 = SistemaYPrimaConrozamiento(Y);
            k2 = SistemaYPrimaConrozamiento(Y + 0.5*dt*k1);
            k3 = SistemaYPrimaConrozamiento(Y + 0.5*dt*k2);
            k4 = SistemaYPrimaConrozamiento(Y + dt*k3);
            string file = fname("conrozamiento", "", angulo);
            ofstream ff(file);
            if (ff.is_open()){
                ff << "#DATOS PARA dt = " << dt << endl;
                ff << "Alcance\tAltura" << endl;
                ff << Y(0,0) << "\t" << Y(1,0) << endl;
                while (true) {
                    Y = Y + 1/6. * (k1 + 2.*k2 + 2.*k3 + k4) * dt;
                    t = t + dt;
                    k1 = SistemaYPrimaSinrozamiento(Y);
                    k2 = SistemaYPrimaSinrozamiento(Y + 0.5*dt*k1);
                    k3 = SistemaYPrimaSinrozamiento(Y + 0.5*dt*k2);
                    k4 = SistemaYPrimaSinrozamiento(Y + dt*k3);
                    ff << Y(0,0) << "\t" << Y(1,0) << endl;
                    if (Y(1,0)<0){
                        break;
                    }
                }
            }
        } else if (aproximacion == 1){
            k1 = SistemaYPrimaIsotermo(Y);
            k2 = SistemaYPrimaIsotermo(Y + 0.5*dt*k1);
            k3 = SistemaYPrimaIsotermo(Y + 0.5*dt*k2);
            k4 = SistemaYPrimaIsotermo(Y + dt*k3);
            string file = fname("conrozamiento", "isoterma", angulo);
            ofstream ff(file);
            if (ff.is_open()){
                ff << "#DATOS PARA dt = " << dt << endl;
                ff << "Alcance\tAltura" << endl;
                ff << Y(0,0) << "\t" << Y(1,0) << endl;
                while (true) {
                    Y = Y + 1/6. * (k1 + 2.*k2 + 2.*k3 + k4) * dt;
                    t = t + dt;
                    k1 = SistemaYPrimaIsotermo(Y);
                    k2 = SistemaYPrimaIsotermo(Y + 0.5*dt*k1);
                    k3 = SistemaYPrimaIsotermo(Y + 0.5*dt*k2);
                    k4 = SistemaYPrimaIsotermo(Y + dt*k3);
                    ff << Y(0,0) << "\t" << Y(1,0) << endl;
                    if (Y(1,0)<0){
                        break;
                    }
                }
            }
        } else if (aproximacion == 2){
            k1 = SistemaYPrimaAdiabatico(Y);
            k2 = SistemaYPrimaAdiabatico(Y + 0.5*dt*k1);
            k3 = SistemaYPrimaAdiabatico(Y + 0.5*dt*k2);
            k4 = SistemaYPrimaAdiabatico(Y + dt*k3);
            string file = fname("conrozamiento", "adiabatica", angulo);
            ofstream ff(file);
            if (ff.is_open()){
                ff << "#DATOS PARA dt = " << dt << endl;
                ff << "Alcance\tAltura" << endl;
                ff << Y(0,0) << "\t" << Y(1,0) << endl;
                while (true) {
                    Y = Y + 1/6. * (k1 + 2.*k2 + 2.*k3 + k4) * dt;
                    t = t + dt;
                    k1 = SistemaYPrimaAdiabatico(Y);
                    k2 = SistemaYPrimaAdiabatico(Y + 0.5*dt*k1);
                    k3 = SistemaYPrimaAdiabatico(Y + 0.5*dt*k2);
                    k4 = SistemaYPrimaAdiabatico(Y + dt*k3);
                    ff << Y(0,0) << "\t" << Y(1,0) << endl;
                    if (Y(1,0)<0){
                        break;
                    }
                }
            }
        } else {
            cout<<"Error en la entrada del método escogido."<<endl;
        }
    }
}

int main(){
    // Datos iniciales.
    double dt = 0.1, tmin = 0.0;

    for (int angulo=30; angulo<=55; angulo=angulo+5){
        // Definimos la matriz inicial
        matrix<double> y0(4, 1); y0.null();
        y0(0,0) = 0.0;
        y0(1,0) = 0.0;
        y0(2,0) = 700*cos(radianes(angulo));
        y0(3,0) = 700*sin(radianes(angulo));

        // Sin rozamiento.
        bool rozamiento = false;
        int aproximacion = 0;
        RK4Sistemas(dt, tmin, rozamiento, aproximacion, y0, to_string(angulo));

        // Con rozamiento.
        rozamiento = true;
        aproximacion = 0;
        RK4Sistemas(dt, tmin, rozamiento, aproximacion, y0, to_string(angulo));

        // Con rozamiento y aproximación isoterma.
        rozamiento = true;
        aproximacion = 1;
        RK4Sistemas(dt, tmin, rozamiento, aproximacion, y0, to_string(angulo));

        // Con rozamiento y aproximación adiabática.
        rozamiento = true;
        aproximacion = 2;
        RK4Sistemas(dt, tmin, rozamiento, aproximacion, y0, to_string(angulo));

    }

    return 0;
}

