#include <stdio.h>
#include <math.h>

double target_f(double x)
{
    return -2 * pow(x, 3) + 15 * pow(x, 2) -24 * x -3;
}

double simpson(double (*f)(double), double a, double b)
{
    double result = 0;
    double n = 100;
    double h = (b - a) / n;
	double x = 0;
    int i = 0;
    
    for(; i <= n; i++)
    {
		x = a + i * h;
        
        if(i == 0 || i == n)
        {
            result += f(x);
			continue;
        }else if(i % 2 != 0)
		{
			result += 4 * f(x);
		}else{
			result += 2 * f(x);
		}
    }

    result = (h * result) / 3;
    
    return result;
}

double simpson_error(double (*f)(double), double a, double b)
{
	double result = 0;
    double n = 100;
	double h = (b - a) / n;
    
	result = - (pow(h, 4) * (b - a) * pow(f(0.00001), 4)) / 180;
    
	return result;
}

int main(void)
{
	double a = 0;
	double b = 4;
    
	printf("積分[%lf → %lf]:%lf\n", a, b, simpson(target_f, a, b));
	printf("最大誤差(参考):%lf\n", simpson_error(target_f, a, b));
    
    return 0;
}