#include <iostream>
#include <fstream>
#include <string>

std::ofstream fout("output.txt", std::ios::app);

int n, m, p, k, x, y;
int m1[101][101], m2[101][101];

const int dirx[8] = {-1, -1, -1, 0, 1, 1, 1, 0};
const int diry[8] = {-1, 0, 1, 1, 1, 0, -1, -1};

void resetMatrix()
{
    for (int i = 1; i <= m; i++)
        for (int j = 1; j <= n; j++)
        {
            m1[i][j] = 0;
            m2[i][j] = 0;
        }
}

void copiere()
{
    for (int i = 1; i <= m; i++)
        for (int j = 1; j <= n; j++)
            m1[i][j] = m2[i][j];
}

void afisare()
{
    for (int i = 1; i <= m; i++, fout << '\n')
        for (int j = 1; j <= n; j++)
            fout << m1[i][j] << " ";

    fout << '\n';
}

int main(int argc, char *argv[])
{
    if (argc < 2)
        return 1;

    for (int fileIndex = 1; fileIndex <= 50 && fileIndex < argc; ++fileIndex)
    {
        std::ifstream infile(argv[fileIndex]);
        if (!infile.is_open())
            return 1;

        infile >> m >> n >> p;
        for (int i = 1; i <= p; i++)
        {
            infile >> x >> y;
            m1[x + 1][y + 1] = 1;
        }
        infile >> k;

        for (int l = 1; l <= k; l++)
        {
            for (int i = 1; i <= m; i++)
                for (int j = 1; j <= n; j++)
                {
                    int vec = 0;
                    for (int d = 0; d < 8; d++)
                        if (m1[i + dirx[d]][j + diry[d]])
                            vec++;

                    if (m1[i][j])
                    {
                        if (vec == 2 || vec == 3)
                            m2[i][j] = 1;
                        else
                            m2[i][j] = 0;
                    }
                    else
                    {
                        if (vec == 3)
                            m2[i][j] = 1;
                        else
                            m2[i][j] = 0;
                    }
                }

            copiere();
        }

        afisare();

        resetMatrix();

        infile.close();
    }

    return 0;
}
